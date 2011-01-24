from django import template
from django.conf import settings
from activitysync.models import Activity

register = template.Library()

@register.inclusion_tag('activitysync/activities_tag.html')
def render_activities(activities):
    return {
        'activities': activities,
        'use_date_headers': False,
        'MEDIA_URL': settings.MEDIA_URL,
    }

@register.inclusion_tag('activitysync/activities_tag.html')
def render_activities_with_date_headers(activities):
    return {
        'activities': activities,
        'use_date_headers': True,
        'MEDIA_URL': settings.MEDIA_URL,
    }

