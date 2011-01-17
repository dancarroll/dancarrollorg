from django.conf import settings
from activitysync.providers import ActivityProvider, ActivityInfo

import time
import datetime
import feedparser

class GoogleReaderProvider(ActivityProvider):
    """
    Provider for accessing shared Google Reader items for one user.
    """
#class ActivityInfo(object):
#    def __init__(self, title=None, link=None, username=None, author=None, comments=None, pub_data=None, published=True, guid=None)

    def get_activity(self):
        item_list = []

        print 'Attempting to parse Google Reader feed'
        parsed_feed = feedparser.parse(settings.GOOGLEREADER_SHARED_RSS)
    
        for entry in parsed_feed.entries:
            title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
            guid = entry.get("id", entry.link).encode(parsed_feed.encoding, "xmlcharrefreplace")
            link = entry.link.encode(parsed_feed.encoding, "xmlcharrefreplace")

            shared_by = u"Dan Carroll"
            comments =u""
                
            if not guid:
                guid = link
                    
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
                        
            if entry.has_key('content'):        
                if len(entry.content) == 2:
                    comments = entry.content[1].value.encode(parsed_feed.encoding, "xmlcharrefreplace")
            
            activity_info = ActivityInfo(title=title, link=link, pub_date=date_published, guid=guid, username=shared_by, author=shared_by, comments=comments)
            item_list.append(activity_info)

        return item_list


    def name(self):
        return 'Google Reader'

    def prefix(self):
        return 'Shared'

    def link(self):
        return settings.GOOGLEREADER_PUBLIC_URL

    def sourceid(self):
        return 'googlereader'

