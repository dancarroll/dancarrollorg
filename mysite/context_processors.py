from django.contrib.sites.models import Site

def CurrentSite(request):
    return { 'current_site': Site.objects.get_current() }
