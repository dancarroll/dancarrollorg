from django.core.management.base import NoArgsCommand
from django.core.management.color import no_style
from django.core.mail import mail_admins
from optparse import make_option
from blog.models import Activity, SharedItem

import os
import sys
import time
import socket
import datetime
import feedparser

#try:
#    set
#except NameError:
#    from sets import Set as set   # Python 2.3 fallback

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        #make_option('--verbosity', action='store', dest='verbosity', default='1',
        #    type='choice', choices=['0', '1', '2'],
        #    help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
    )
    help = "Update activities by depositing them into the blog database."

    def handle_noargs(self, **options): 
        self.style = no_style()
        
        added_item_list = []
        items_added = False
        try:
            added_item_list.append("GOOGLE READER\n\n")
            for readerItem in self.add_googlereader_items():
                items_added = True
                added_item_list.append(readerItem)
                
            added_item_list.append("\nTWITTER\n\n")
            # for twitterItem in self.add_twitter_items():
                # added_item_list.append(twitterItem)
            for twitterItem in self.add_network_items(u'T', u'erunama', "erunama: ", "http://twitter.com/statuses/user_timeline/erunama.atom"):
                items_added = True
                added_item_list.append(twitterItem)
                
            added_item_list.append("\nDIGG\n\n")
            # for diggItem in self.add_digg_items():
                # added_item_list.append(diggItem)
            for diggItem in self.add_network_items(u'DG', u'erunama', None, "http://digg.com/users/erunama/history/diggs.rss"):
                items_added = True
                added_item_list.append(diggItem)
                
            added_item_list.append("\nDELICIOUS\n\n")
            # for deliciousItem in self.add_delicious_items():
                # added_item_list.append(deliciousItem)
            for deliciousItem in self.add_network_items(u'DL', u'erunama', None, "http://feeds.delicious.com/v2/rss/erunama?count=5"):
                items_added = True
                added_item_list.append(deliciousItem)

            # FACEBOOK
            # http://www.facebook.com/feeds/status.php?id=401024&viewer=401024&key=c1ba152f09&format=rss20
            added_item_list.append("\nFACEBOOK\n\n")
            for facebookItem in self.add_network_items(u'FB', u'Dan Carroll', None, "http://www.facebook.com/feeds/status.php?id=401024&viewer=401024&key=c1ba152f09&format=rss20"):
                items_added = True
                added_item_list.append(facebookItem)

            # REDDIT
            # http://www.reddit.com/user/erunama/liked/.rss
            added_item_list.append("\nREDDIT\n\n")
            for redditItem in self.add_network_items(u'RD', u'erunama', None, "http://www.reddit.com/user/erunama/liked/.rss"):
                items_added = True
                added_item_list.append(redditItem)
            
            # HULU
            # http://www.hulu.com/feed/history/erunama
            #added_item_list.append("\nHULU\n\n")
            #for facebookItem in self.add_network_items(u'HU', u'erunama', None, "http://www.hulu.com/feed/history/erunama"):
            #    items_added = True
            #    added_item_list.append(facebookItem)
            
            
        except:
            items_added = True
            print "Unexpected error:", sys.exc_info()[0]
            added_item_list.append("Unexpected error: %s\n\n" % sys.exc_info()[0])    
        finally:
            if items_added:
                mailBody = u""
                for itemString in added_item_list:
                    try:
                        mailBody = mailBody.encode('utf-8') + itemString.encode('utf-8')
                    except UnicodeDecodeError:
                        mailBody = mailBody + "\n\nFAILED TO PARSE ACTIVITY\n\n"
                #mailBody = ''.encode('utf-8').join(added_item_list)
                mail_admins('Update Activities command completed', mailBody, fail_silently=False)
                print 'Mail sent to admins'
    
    def add_googlereader_items(self):
        added_item_list = []
        # Google Reader
        try:
            print 'Attempting to parse Google Reader feed'
            parsed_feed = feedparser.parse("http://www.google.com/reader/public/atom/user%2F10780706687522073033%2Fstate%2Fcom.google%2Fbroadcast")
            for entry in parsed_feed.entries:
                title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
                guid = entry.get("id", entry.link).encode(parsed_feed.encoding, "xmlcharrefreplace")
                link = entry.link.encode(parsed_feed.encoding, "xmlcharrefreplace")
                source = u'GR' #1 # Google Reader is source choice 1
                public = True
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
                        
      
                try:
                    #SharedItem.objects.get(guid=guid)
                    Activity.objects.get(guid=guid)
                #except SharedItem.DoesNotExist:
                except Activity.DoesNotExist:
                    print "Created item: %s (%s)" % (title, link)
                    added_item_list.append("Created item: %s (%s)\n" % (title, link))
                    if comments:
                        added_item_list.append("  With comment: %s\n\n" % comments)
                    try:
                        #SharedItem.objects.create(title=title, link=link, source=source, comments=comments, shared_by=shared_by, pub_date=date_published, guid=guid)
                        Activity.objects.create(title=title, link=link, source=source, username=shared_by, author=shared_by, comments=comments, pub_date=date_published, published=public, guid=guid)
                    except:
                        print "Unexpected error in Google Reader:", sys.exc_info()[0]
                        added_item_list.append("Unexpected error in Google Reader: %s\n\n" % sys.exc_info()[0])
        except:
            print "Unexpected error:", sys.exc_info()[0]
            added_item_list.append("Unexpected error: %s\n\n" % sys.exc_info()[0])             
        finally:
            return added_item_list
            
    def add_network_items(self, sourceId, username, stripInitialString, feedUrl):
        added_item_list = []
        try:
            print 'Attempting to parse feed ' + feedUrl
            parsed_feed = feedparser.parse(feedUrl)
            for entry in parsed_feed.entries:
                title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
                guid = entry.get("id", entry.link).encode(parsed_feed.encoding, "xmlcharrefreplace")
                link = entry.link.encode(parsed_feed.encoding, "xmlcharrefreplace")
                source = sourceId
                public = True
                
                if not guid:
                    guid = link
                
                if entry.has_key('author'):
                    author = entry.author.encode(parsed_feed.encoding, "xmlcharrefreplace")
                else:
                    author = u''
                    
                title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
                if stripInitialString:
                    if title.find(stripInitialString) == 0:
                        title = title.lstrip(stripInitialString)
                
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
                    
                try:
                    Activity.objects.get(guid=guid)
                except Activity.DoesNotExist:
                    print "Created item: %s (%s)" % (title, link)
                    added_item_list.append("Created item: %s (%s)\n" % (title, link))
                    try:
                        Activity.objects.create(title=title, link=link, source=source, username=username, author=author, pub_date=date_published, published=public, guid=guid)
                    except:
                        print "Unexpected error with feed:", sys.exc_info()[0]
                        added_item_list.append("Unexpected error with feed: %s\n\n" % sys.exc_info()[0])
        except:
            print "Unexpected error:", sys.exc_info()[0]
            added_item_list.append("Unexpected error: %s\n\n" % sys.exc_info()[0])             
        finally:
            return added_item_list    

# Authenticated feeds
#>>> import urllib2
#>>> auth = urllib2.HTTPBasicAuthHandler()
#>>> auth.add_password('Twitter API', 'twitter.com', 'erunama', password)
#d = feedparser.parse('http://feedparser.org/docs/examples/basic_auth.xml', \
#                     handlers=[auth])