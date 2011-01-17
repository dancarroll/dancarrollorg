from django.conf import settings
from django.contrib.sites.models import Site

def CurrentSite(request):
    google_analytics_code = getattr(settings, 'GOOGLE_ANALYTICS_CODE', None)

    return {
        'current_site': Site.objects.get_current(),
        'UA_code': google_analytics_code,
    }
