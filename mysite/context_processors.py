from django.conf import settings
from django.contrib.sites.models import Site

def CurrentSite(request):
    try:
        google_analytics_code = settings.GOOGLE_ANALYTICS_CODE
    except AttributeError:
        google_analytics_code = ''

    return {
        'current_site': Site.objects.get_current(),
        'UA_code': google_analytics_code,
    }
