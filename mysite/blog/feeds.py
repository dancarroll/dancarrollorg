from django.contrib.syndication.feeds import Feed
from mysite.blog.models import Entry

class LatestEntries(Feed):
    title = "erunama.com"
    link = "/blog/"
    description = "Test RSS feed"
    
    def items(self):
        return Entry.objects.published()