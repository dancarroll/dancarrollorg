from django import template
from mysite.blog.models import Entry
from tagging.models import Tag

register = template.Library()

@register.inclusion_tag('blog/month_links_tag.html')
def render_month_links():
    return {
        'dates': Entry.objects.dates('pub_date', 'month', order='DESC'),
    }

@register.inclusion_tag('blog/tag_cloud_tag.html')
def render_tag_cloud():
    return {
        'tag_cloud': Tag.objects.cloud_for_model(Entry, steps=3, filters=dict(published=True)),
    }