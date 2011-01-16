from django.conf import settings
from activitysync.providers import ActivityProvider, ActivityInfo

import time
import datetime
import feedparser

class RedditProvider(ActivityProvider):
    """
    Provider for accessing liked Reddit items for one user.
    """
    
    def get_activity(self):
        item_list = []

        print 'Attempting to parse Reddit feed'
        username = settings.REDDIT_USERNAME
        parsed_feed = feedparser.parse("http://www.reddit.com/user/%s/liked/.rss" % username)

        for entry in parsed_feed.entries:
            title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
            guid = entry.get("id", entry.link).encode(parsed_feed.encoding, "xmlcharrefreplace")
            link = entry.link.encode(parsed_feed.encoding, "xmlcharrefreplace")

            if not guid:
                guid = link

            if entry.has_key('author'):
                author = entry.author.encode(parsed_feed.encoding, "xmlcharrefreplace")
            else:
                author = u''

            try:
                if entry.has_key('published_parsed'):
                    date_published = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed) - time.timezone)
                elif entry.has_key('updated_parsed'):
                    date_published = datetime.datetime.fromtimestamp(time.mktime(entry.updated_parsed) - time.timezone)
                elif entry.has_key('modified_parsed'):
                    date_published = datetime.datetime.fromtimestamp(time.mktime(entry.modified_parsed) - time.timezone)
                else:
                    date_published = datetime.datetime.now()
            except TypeError:
                date_published = datetime.datetime.now()
                    
            activity_info = ActivityInfo(title=title, link=link, pub_date=date_published, guid=guid, username=username, author=author)
            item_list.append(activity_info)

        return item_list


    def name(self):
        return 'Reddit'

    def prefix(self):
        return 'Liked'

    def link(self):
        return 'http://www.reddit.com/user/%s/' % settings.REDDIT_USERNAME

    def sourceid(self):
        return 'reddit'

