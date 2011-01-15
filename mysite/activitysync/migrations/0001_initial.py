# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Activity'
        db.create_table('activitysync_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal('activitysync', ['Activity'])


    def backwards(self, orm):
        
        # Deleting model 'Activity'
        db.delete_table('activitysync_activity')


    models = {
        'activitysync.activity': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Activity'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['activitysync']
