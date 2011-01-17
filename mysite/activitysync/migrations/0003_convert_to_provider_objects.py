# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for activity in orm.Activity.objects.all():
            print "Activity: %s" % activity.title
            provider = self.get_or_create_provider(orm, activity)
            print "   - Has provider: %s" % provider.name
            activity.provider = provider
            activity.save()

    def backwards(self, orm):
        for activity in orm.Activity.objects.all():
            provider = activity.provider
            print 'Activity: %s' % activity.title
            print '   - Has source: %s' % self.sourceid_to_sourcechoice(provider)
            activity.source = self.sourceid_to_sourcechoice(provider)
            activity.save()   

    def get_or_create_provider(self, orm, activity):
        sourceid = self.get_provider_sourceid(activity)

        try:
            provider = orm.Provider.objects.get(sourceid=sourceid)
            return provider
        except orm.Provider.DoesNotExist:
            name = self.get_provider_name(activity)
            prefix = self.get_activity_prefix(activity)
            link = self.get_network_link(activity)

            provider = orm.Provider.objects.create(name=name, prefix=prefix, link=link, sourceid=sourceid)
            return provider

    def get_provider_sourceid(self, activity):
        if activity.source == 'T':
            return u"twitter"
        elif activity.source == 'DL':
            return u"delicious"
        elif activity.source == 'FB':
            return u"facebook"
        elif activity.source == 'HU':
            return u"hulu"
        elif activity.source == 'RD':
            return u"reddit"
        elif activity.source == 'GR':
            return u"googlereader"

    def get_provider_name(self, activity):
        if activity.source == 'T':
            return u"Twitter"
        elif activity.source == 'DL':
            return u"Delicious"
        elif activity.source == 'FB':
            return u"Facebook"
        elif activity.source == 'HU':
            return u"Hulu"
        elif activity.source == 'RD':
            return u"Reddit"
        elif activity.source == 'GR':
            return u"Google Reader"
 
    def get_activity_prefix(self, activity):
        if activity.source == 'DL':
            return u'Bookmarked '
        elif activity.source == 'HU':
            return u'Watched '
        elif activity.source == 'RD':
            return u'Liked '
        elif activity.source == 'GR':
            return u'Shared '
        else:
            return u''
    
    def get_network_link(self, activity):
        if activity.source == 'T':
            return u"http://twitter.com/erunama"
        elif activity.source == 'DL':
            return u"http://delicious.com/erunama"
        elif activity.source == 'FB':
            return u"http://www.facebook.com/people/Dan-Carroll/401024"
        elif activity.source == 'HU':
            return u"http://www.hulu.com/profiles/erunama/"
        elif activity.source == 'RD':
            return u"http://www.reddit.com/user/erunama/"
        elif activity.source == 'GR':
            return u"http://www.google.com/reader/shared/dancarroll"

# HELPER METHODS FOR BACKWARDS MIGRATION
    def sourceid_to_sourcechoice(self, provider):
        if provider.sourceid == 'twitter':
            return u"T"
        elif provider.sourceid == 'delicious':
            return u"DL"
        elif provider.sourceid == 'facebook':
            return u"FB"
        elif provider.sourceid == 'hulu':
            return u"HU"
        elif provider.sourceid == 'reddit':
            return u"RD"
        elif provider.sourceid == 'googlereader':
            return u"GR"


    models = {
        'activitysync.activity': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Activity'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activitysync.Provider']", 'null': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'activitysync.provider': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Provider'},
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sourceid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['activitysync']
