from django.core.cache import cache
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache

from waffle import all_flags, all_switches, all_samples


@never_cache
def wafflejs(request):
    return render_to_response('waffle/waffle.js', {'flags': all_flags(request).items(),
                                                   'switches': all_switches().items(),
                                                   'samples': all_samples().items()},
                              mimetype='application/x-javascript')
