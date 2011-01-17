from django.db.models import Manager
import datetime

class ActivityManager(Manager):
    def get_query_set(self):
        return super(ActivityManager, self).get_query_set().select_related('provider')
   
    def published(self):
        """Returns published posts that are not in the future."""
        return self.get_query_set().filter(published=True, pub_date__lte=datetime.datetime.now())

