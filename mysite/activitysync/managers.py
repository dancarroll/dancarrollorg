from django.db.models import Manager
import datetime

class PublishedManager(Manager):
    """Returns published posts that are not in the future."""
   
    def published(self):
        return self.get_query_set().filter(published=True, pub_date__lte=datetime.datetime.now())

