from django.db import models
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.template.defaultfilters import slugify

from mysite.blog.managers import PublishedManager
from tagging.fields import TagField
from tagging.models import Tag

import datetime
import tagging

class Entry(models.Model):
    title = models.CharField('title', max_length=200)
    snip = models.CharField('snip', max_length=500)
    slug = models.SlugField('slug', unique_for_date='pub_date')
    
    pub_date = models.DateTimeField('Date published',
                                    default=datetime.datetime.now)
    mod_date = models.DateTimeField('Date modified',
                                    default=datetime.datetime.now,
                                    auto_now=True)
    
    tags = TagField()
    body = models.TextField()
    published = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    objects = PublishedManager()
    
    class Meta:
        verbose_name = 'entry'
        verbose_name_plural = 'entries'
        db_table = 'blog_entries'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
    
    
    def __unicode__(self):
        return u'%s' % self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('blog_entry_detail', None, {
                'year': self.pub_date.year,
                'month': self.pub_date.strftime("%m"),
                'slug': self.slug
            })
    
    def get_previous_entry(self):
        return self.get_previous_by_pub_date(published=True)
    
    def get_next_entry(self):
        return self.get_next_by_pub_date(published=True)

    def as_metaweblog_struct(self):
        """Convert an Entry to a MetaWeblog API struct."""
        #tags = [tag.name for tag in Tag.objects.get_for_object(self)]

        struct = {
            'title': self.title,
            'link': "http://%s%s" % (
                #Site.objects.get_current().domain, self.get_absolute_url()),
                "127.0.0.1:8000", self.get_absolute_url()),
            'description': self.body,
            'author': 'Dan Carroll',
            'comments': "http://%s%s" % (
                Site.objects.get_current().domain, self.get_absolute_url()),
            'guid': "http://%s%s" % (
                Site.objects.get_current().domain, self.get_absolute_url()),
            'pubDate': self.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
            'categories': self.tags,
            'postid': self.id,
            'wp_slug': self.slug,
            'mt_excerpt': self.snip,
        }

        return struct

    def populate_from_metaweblog_struct(self, struct, user):
        """Populate a post from a metaweblog struct.

        :param struct: The struct to use for population.
        :param user: The user doing the work.
        """
        self.title = struct.get('title')
        self.body = struct.get('description')
        if self.pub_date is None:
            self.pub_date = datetime.datetime.now()
        #self.author = user
        self.mod_date = datetime.datetime.now()

        # We only alter the slug if it's not None
        wp_slug = struct.get('wp_slug')
        if not self.slug:
            if wp_slug:
                self.slug = wp_slug
            else:
                self.slug = slugify(self.title)[0:49]

        mt_excerpt = struct.get('mt_excerpt')
        if mt_excerpt:
            self.snip = mt_excerpt
        else:
            if not self.snip:
                self.snip = ""

        tag_list = struct.get('categories', [])
        self.tags = ','.join(tag_list)

        try:
            self.save()
        except Warning:
            pass # Usually a truncation warning


class Activity(models.Model):
    """Activity from social network (Twitter, Flickr, etc)."""
    SOURCE_CHOICES = (
        ('T', 'twitter'),
        ('DG', 'digg'),
        ('DL', 'delicious'),
        ('FB', 'facebook'),
        ('HU', 'hulu'),
        ('RD', 'reddit'),
        ('GR', 'googlereader'),
    )
    
    title = models.CharField('title', max_length=200)
    link = models.URLField(max_length=500)
    source = models.CharField(max_length=2, choices=SOURCE_CHOICES)
    username = models.CharField(max_length=20, blank=True)
    author = models.CharField(max_length=20, blank=True)
    comments = models.TextField(blank=True)
    pub_date = models.DateTimeField('Date published')
    published = models.BooleanField(default=True)
    guid = models.CharField(max_length=255, unique=True, db_index=True)
    objects = PublishedManager()
    
    class Meta:
        verbose_name = 'activity'
        verbose_name_plural = 'activities'
        db_table = 'blog_activities'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
    
    def __unicode__(self):
        return u'%s' % self.title

    def get_activity_prefix(self):
        if self.source == 'DG':
            return u'Dugg '
        elif self.source == 'DL':
            return u'Bookmarked '
        elif self.source == 'HU':
            return u'Watched '
        elif self.source == 'RD':
            return u'Liked '
        elif self.source == 'GR':
            return u'Shared '
        else:
            return u''
    
    def get_network_link(self):
        if self.source == 'T':
            return u"http://twitter.com/erunama"
        elif self.source == 'DG':
            return u"http://digg.com/users/erunama"
        elif self.source == 'DL':
            return u"http://delicious.com/erunama"
        elif self.source == 'FB':
            return u"http://www.facebook.com/people/Dan-Carroll/401024"
        elif self.source == 'HU':
            return u"http://www.hulu.com/profiles/erunama/"
        elif self.source == 'RD':
            return u"http://www.reddit.com/user/erunama/"
        elif self.source == 'GR':
            return u"http://www.google.com/reader/shared/dancarroll"
            