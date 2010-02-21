from django.contrib.syndication.feeds import Feed
from mysite.polls.models import Poll

class LatestEntries(Feed):
    title = "Erunama.com Polls"
    link = "/polls/"
    description = "Polls hosted at Erunama.com"

    def items(self):
        return Poll.objects.order_by('-pub_date')[:5]
        
    def item_link(self):
        return 'http://localhost/'
