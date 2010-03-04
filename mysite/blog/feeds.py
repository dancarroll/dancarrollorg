from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from mysite.blog.models import Entry
from tagging.models import Tag, TaggedItem

class LatestEntriesFeed(Feed):
    title = "Dan Carroll | Blog"
    link = "/"
    
    def items(self):
        return Entry.objects.published()[:5]
    
    def description(self):
        return "Latest blog entries for %s" % Site.objects.get_current().domain
        
class LatestEntriesByTagFeed(Feed):
    def get_object(self, request, tag_name):
        return get_object_or_404(Tag, name=tag_name)
        
    def title(self, obj):
        return "Dan Carroll | Blog | %s" % obj.name
        
    def link(self, obj):
        return reverse('blog_tag_detail', args=[obj.name])
        
    def description(self, obj):
        return "Latest blog entries tagged with '%s'" % obj.name
        
    def items(self, obj):
        return TaggedItem.objects.get_by_model(Entry.objects.published(), obj)[:5]