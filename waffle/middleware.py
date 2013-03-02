from django.conf import settings
from django.utils.encoding import smart_str

from waffle import FLAGS, COOKIE_NAME, TEST_COOKIE_NAME


class WaffleMiddleware(object):
    def process_request(self, request):
        request.waffles = {}
        request.waffle_tests = {}

        if 'waffle_reset' in request.GET:
            # This will reset the cookies in process_response()
            request.waffle_tests.update({name: None for name in FLAGS})

    def process_response(self, request, response):
        secure = getattr(settings, 'WAFFLE_SECURE', False)
        max_age = getattr(settings, 'WAFFLE_MAX_AGE', 2592000)  # 1 month

        if hasattr(request, 'waffles'):
            for k in request.waffles:
                name = smart_str(COOKIE_NAME % k)
                active, rollout = request.waffles[k]
                if rollout and not active:
                    # "Inactive" is a session cookie during rollout mode.
                    age = None
                else:
                    age = max_age
                response.set_cookie(name, value=active, max_age=age,
                                    secure=secure)

        if hasattr(request, 'waffle_tests'):
            for k in request.waffle_tests:
                name = smart_str(TEST_COOKIE_NAME % k)
                value = request.waffle_tests[k]
                if value is not None:
                    response.set_cookie(name, value=value)
                elif name in request.COOKIES:
                    response.delete_cookie(name)

        return response
