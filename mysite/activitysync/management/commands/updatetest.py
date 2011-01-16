from django.conf import settings
from django.core import exceptions
from django.core.management.base import NoArgsCommand
from django.core.management.color import no_style
from django.core.mail import mail_admins
from optparse import make_option
from activitysync.models import Activity
from activitysync.providers import ActivityProvider, ActivityInfo

import os
import sys
import time
import socket
import datetime
import feedparser
import twitter

class Command(NoArgsCommand):
    help = "Update activities by depositing them into the blog database."

    def handle_noargs(self, **options): 
        self.style = no_style()
        
        email_status_info = []
        items_added = False
        try:
            # Go through provider list
            provider_list = getattr(settings, 'ACTIVITYSYNC_PROVIDERS', [])
            for provider_path in provider_list:
                try:
                    dot = provider_path.rindex('.')
                except ValueError:
                    raise exceptions.ImproperlyConfigured('%s is not an activity provider' % provider_path)
                provider_module, provider_classname = provider_path[:dot], provider_path[dot+1:]
                try:
                    mod = __import__(provider_module, {}, {}, [''])
                except ImportError, e:
                    raise exceptions.ImproperlyConfigured('Error importing provider %s: %s' % (provider_module, e))
                try:
                    provider_class = getattr(mod, provider_classname)
                except AttributeError:
                    raise exceptions.ImproperlyConfigured('Provider module "%s" does not define a "%s" class' % (provider_module, provider_classname))

                provider_instance = provider_class()
                email_status_info.append('\n\n%s\n\n' % provider_instance.name())
                for activity_item in provider_instance.get_activity():
                    try:
                        Activity.objects.get(guid=activity_item.guid)
                    except Activity.DoesNotExist:
                        print "Created item: %s (%s)" % (activity_item.title, activity_item.link)
                        email_status_info.append("Created item: %s (%s)\n" % (activity_item.title, activity_item.link))
                        items_added = True

                        #Activity.objects.create(title=activity_item.title, link=activity_item.link, source=provider_instance.sourceid(), username=activity_item.username, author=activity_item.author, comments=activity_item.comments, pub_date=activity_item.pub_date, published=activity_item.published, guid=activity_item.guid)

        except:
            ### DEBUGGING CODE
            raise
            ### END DEBUGGING
            items_added = True
            print "Unexpected error:", sys.exc_info()[0]
            email_status_info.append("Unexpected error: %s\n\n" % sys.exc_info()[0])    
        finally:
            if items_added:
                mailBody = u""
                for itemString in email_status_info:
                    try:
                        mailBody = mailBody.encode('utf-8') + itemString.encode('utf-8')
                    except UnicodeDecodeError:
                        mailBody = mailBody + "\n\nFAILED TO PARSE ACTIVITY\n\n"
                ### DISABLED TEMPORARILY FOR DEBUGGING
                #mail_admins('Update Activities command completed', mailBody, fail_silently=False)
                #print 'Mail sent to admins'
                ### END DISABLE
