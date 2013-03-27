from decimal import Decimal
import random
import hashlib

from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, m2m_changed

from waffle.models import Flag, Sample, Switch


VERSION = (0, 9, 0)
__version__ = '.'.join(map(str, VERSION))


CACHE_PREFIX = getattr(settings, 'WAFFLE_CACHE_PREFIX', u'waffle:')
FLAGS = getattr(settings, 'WAFFLE_FLAGS', {})
FLAGS_FORCE = getattr(settings, 'WAFFLE_FLAGS_FORCE', {})
FLAG_CACHE_KEY = u'flag:%s'
FLAG_USERS_CACHE_KEY = u'flag:%s:users'
FLAG_GROUPS_CACHE_KEY = u'flag:%s:groups'
SAMPLES = getattr(settings, 'WAFFLE_SAMPLES', {})
SAMPLES_FORCE = getattr(settings, 'WAFFLE_SAMPLES_FORCE', {})
SAMPLE_CACHE_KEY = u'sample:%s'
SWITCHES = getattr(settings, 'WAFFLE_SWITCHES', {})
SWITCHES_FORCE = getattr(settings, 'WAFFLE_SWITCHES_FORCE', {})
SWITCH_CACHE_KEY = u'switch:%s'
SWITCHES_ALL_CACHE_KEY = u'switches:all'
COOKIE_NAME = getattr(settings, 'WAFFLE_COOKIE', 'dwf_%s')
ALLOW_OVERRIDE = getattr(settings, 'WAFFLE_OVERRIDE', False)
TEST_COOKIE_NAME = getattr(settings, 'WAFFLE_TESTING_COOKIE', 'dwft_%s')


def keyfmt(k, v=None):
    if v is None:
        return CACHE_PREFIX + k
    return CACHE_PREFIX + hashlib.md5(k % v).hexdigest()


def all_flags(request):
    return {f: flag_is_active(request, f) for f in FLAGS}


def all_switches():
    switches = cache.get(SWITCHES_ALL_CACHE_KEY)
    if switches is None:
        switches = {s: switch_is_active(s) for s in SWITCHES}
        cache.set(SWITCHES_ALL_CACHE_KEY, switches)
    return switches


def all_samples():
    return {s: sample_is_active(s) for s in SAMPLES}


def set_flag(request, flag_name, active=True, session_only=False):
    """Set a flag value on a request object."""
    request.waffles[flag_name] = [active, session_only]


def flag_is_requested(request, flag_name):
    requested = request.GET.get(flag_name)
    value = None

    if requested is not None:
        if requested != '':
            value = requested == '1'

        # Save the value in request.waffle_tests so that WaffleMiddleware
        # will save in TEST_COOKIE_NAME
        request.waffle_tests[flag_name] = value

    elif flag_name in request.waffle_tests:
        # This probably means ?waffle_reset, see
        # WaffleMiddleware.process_request
        value = request.waffle_tests[flag_name]

    else:
        tc = TEST_COOKIE_NAME % flag_name
        if tc in request.COOKIES:
            value = request.COOKIES[tc] == 'True'

    return value


def flag_is_active(request, flag_name):
    if settings.DEBUG:
        assert flag_name in FLAGS
    elif flag_name not in FLAGS:
        return False

    if ALLOW_OVERRIDE:
        value = flag_is_requested(request, flag_name)
        if value is not None:
            return value

    if flag_name in FLAGS_FORCE:
        return FLAGS_FORCE[flag_name]

    flag = cache.get(keyfmt(FLAG_CACHE_KEY, flag_name))
    if flag is None:
        flag, created = Flag.objects.get_or_create(name=flag_name)
        cache_flag(instance=flag)

    if flag.testing:  # Testing mode is on.
        value = flag_is_requested(request, flag_name)
        if value is not None:
            return value

    if flag.everyone:
        return True
    elif flag.everyone is False:
        return False

    user = request.user

    if flag.authenticated and user.is_authenticated():
        return True

    if flag.staff and user.is_staff:
        return True

    if flag.superusers and user.is_superuser:
        return True

    if flag.languages:
        languages = flag.languages.split(',')
        if (hasattr(request, 'LANGUAGE_CODE') and
                request.LANGUAGE_CODE in languages):
            return True

    flag_users = cache.get(keyfmt(FLAG_USERS_CACHE_KEY, flag.name))
    if flag_users is None:
        flag_users = flag.users.all()
        cache_flag(instance=flag)
    if user in flag_users:
        return True

    flag_groups = cache.get(keyfmt(FLAG_GROUPS_CACHE_KEY, flag.name))
    if flag_groups is None:
        flag_groups = flag.groups.all()
        cache_flag(instance=flag)
    user_groups = user.groups.all()
    for group in flag_groups:
        if group in user_groups:
            return True

    if flag.percent > 0:
        if not hasattr(request, 'waffles'):
            request.waffles = {}
        elif flag_name in request.waffles:
            return request.waffles[flag_name][0]

        cookie = COOKIE_NAME % flag_name
        if cookie in request.COOKIES:
            flag_active = (request.COOKIES[cookie] == 'True')
            set_flag(request, flag_name, flag_active, flag.rollout)
            return flag_active

        if Decimal(str(random.uniform(0, 100))) <= flag.percent:
            set_flag(request, flag_name, True, flag.rollout)
            return True
        set_flag(request, flag_name, False, flag.rollout)

    return FLAGS[flag_name]


def switch_is_active(switch_name):
    if settings.DEBUG:
        assert switch_name in SWITCHES
    elif switch_name not in SWITCHES:
        return False

    if switch_name in SWITCHES_FORCE:
        switch = Switch(name=switch_name, active=SWITCHES_FORCE[switch_name])
    else:
        switch = cache.get(keyfmt(SWITCH_CACHE_KEY, switch_name))
        if switch is None:
            try:
                switch = Switch.objects.get(name=switch_name)
            except Switch.DoesNotExist:
                switch = Switch(name=switch_name, active=SWITCHES[switch_name])
            cache_switch(instance=switch)

    return switch.active


def sample_is_active(sample_name):
    if settings.DEBUG:
        assert sample_name in SAMPLES
    elif sample_name not in SAMPLES:
        return False

    value_percent = lambda v: (100 if v is True else 0 if v is False else v)

    if sample_name in SAMPLES_FORCE:
        sample = Sample(name=sample_name, percent=value_percent(SAMPLES_FORCE[sample_name]))
    else:
        sample = cache.get(keyfmt(SAMPLE_CACHE_KEY, sample_name))
        if sample is None:
            try:
                sample = Sample.objects.get(name=sample_name)
            except Sample.DoesNotExist:
                sample = Sample(name=sample_name, percent=value_percent(SAMPLES[sample_name]))
            cache_sample(instance=sample)

    return (False if sample.percent == 0 else
            Decimal(str(random.uniform(0, 100))) <= sample.percent)


def cache_flag(**kwargs):
    action = kwargs.get('action', None)
    # action is included for m2m_changed signal. Only cache on the post_*.
    if not action or action in ['post_add', 'post_remove', 'post_clear']:
        f = kwargs['instance']
        cache.set_many({
            keyfmt(FLAG_CACHE_KEY, f.name): f,
            keyfmt(FLAG_USERS_CACHE_KEY, f.name): f.users.all(),
            keyfmt(FLAG_GROUPS_CACHE_KEY, f.name): f.groups.all(),
            })


def uncache_flag(**kwargs):
    flag = kwargs['instance']
    cache.delete_many([
        keyfmt(FLAG_CACHE_KEY, flag.name),
        keyfmt(FLAG_USERS_CACHE_KEY, flag.name),
        keyfmt(FLAG_GROUPS_CACHE_KEY, flag.name),
        ])

post_save.connect(uncache_flag, sender=Flag, dispatch_uid='save_flag')
post_delete.connect(uncache_flag, sender=Flag, dispatch_uid='delete_flag')
m2m_changed.connect(uncache_flag, sender=Flag.users.through,
                    dispatch_uid='m2m_flag_users')
m2m_changed.connect(uncache_flag, sender=Flag.groups.through,
                    dispatch_uid='m2m_flag_groups')


def cache_sample(**kwargs):
    sample = kwargs['instance']
    cache.set(keyfmt(SAMPLE_CACHE_KEY, sample.name), sample)


def uncache_sample(**kwargs):
    sample = kwargs['instance']
    cache.delete(keyfmt(SAMPLE_CACHE_KEY, sample.name))

post_save.connect(uncache_sample, sender=Sample, dispatch_uid='save_sample')
post_delete.connect(uncache_sample, sender=Sample,
                    dispatch_uid='delete_sample')


def cache_switch(**kwargs):
    switch = kwargs['instance']
    cache.set(keyfmt(SWITCH_CACHE_KEY, switch.name), switch)


def uncache_switch(**kwargs):
    switch = kwargs['instance']
    cache.delete_many([
        keyfmt(SWITCH_CACHE_KEY, switch.name),
        keyfmt(SWITCHES_ALL_CACHE_KEY),
        ])

post_delete.connect(uncache_switch, sender=Switch,
                    dispatch_uid='delete_switch')
post_save.connect(uncache_switch, sender=Switch, dispatch_uid='save_switch')
