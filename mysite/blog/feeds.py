from django.contrib.syndication.feeds import Feed
from mysite.blog.models import Entry

class LatestEntries(Feed):
    title = "Dan Carroll"
    link = "/"
    description = "RSS feed for Dan Carroll's blog (erunama.com)"
    
    def items(self):
        return Entry.objects.published()