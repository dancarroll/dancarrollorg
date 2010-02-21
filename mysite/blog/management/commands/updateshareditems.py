from django.core.management.base import NoArgsCommand
from django.core.management.color import no_style
from django.core.mail import mail_admins
from optparse import make_option

import os
import sys
import time
import socket
import datetime
import feedparser

try:
    set
except NameError:
    from sets import Set as set   # Python 2.3 fallback

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--verbosity', action='store', dest='verbosity', default='1',
            type='choice', choices=['0', '1', '2'],
            help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
    )
    help = "Update shared items by depositing them into the blog database."

    def handle_noargs(self, **options):
        from blog.models import SharedItem
        
        self.style = no_style()
        
        added_item_list = []
        try:
            # Google Reader
            parsed_feed = feedparser.parse("http://www.google.com/reader/public/atom/user%2F10780706687522073033%2Fstate%2Fcom.google%2Fbroadcast")
            for entry in parsed_feed.entries:
                if entry.has_key('content'):
                    if len(entry.content) == 2:
                        title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
                        guid = entry.get("id", entry.link).encode(parsed_feed.encoding, "xmlcharrefreplace")
                        link = entry.link.encode(parsed_feed.encoding, "xmlcharrefreplace")
                        source = 1 # Google Reader is source choice 1
                        
                        if not guid:
                            guid = link
                        
                        comments = entry.content[1].value.encode(parsed_feed.encoding, "xmlcharrefreplace")
                        shared_by = u"Dan Carroll"
                        
                        try:
                            if entry.has_key('published_parsed'):
                                date_published = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
                            elif entry.has_key('updated_parsed'):
                                date_published = datetime.datetime.fromtimestamp(time.mktime(entry.updated_parsed))
                            elif entry.has_key('modified_parsed'):
                                date_published = datetime.datetime.fromtimestamp(time.mktime(entry.modified_parsed))
                            else:
                                date_published = datetime.datetime.now()
                        except TypeError:
                            date_published = datetime.datetime.now()
                            
                        try:
                            SharedItem.objects.get(guid=guid)
                        except SharedItem.DoesNotExist:
                            print "Created item: %s (%s)" % (title, link)
                            added_item_list.append("Created item: %s (%s)\n" % (title, link))
                            added_item_list.append("  With comment: %s\n\n" % comments)
                            try:
                                SharedItem.objects.create(title=title, link=link, source=source, comments=comments, shared_by=shared_by, pub_date=date_published, guid=guid)
                            except:
                                print "Unexpected error in Google Reader:", sys.exc_info()[0]
                                added_item_list.append("Unexpected error in Google Reader: %s\n\n" % sys.exc_info()[0])
        except:
            print "Unexpected error:", sys.exc_info()[0]
            added_item_list.append("Unexpected error: %s\n\n" % sys.exc_info()[0])
        finally:
            if len(added_item_list) > 0:
                mail_admins('Update Shared Items command completed', ''.join(added_item_list), fail_silently=False)
                print 'Mail sent to admins'
