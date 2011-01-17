"""Base ActivityProvider class"""

class ActivityProvider(object):
    """
    Base class for activity providers (networks that provide social activity)
    """

    def get_activity(self):
        """Returns a list of ActivityInfo objects representing the provider's activity"""
        raise NotImplementedError

    def name(self):
        """Name of the network the provider connects to"""
        raise NotImplementedError

    def prefix(self):
        """Prefix to put before activity item representing the action of the activity (i.e. "shared", "liked", etc)"""
        raise NotImplementedError

    def link(self):
        """Link to the network or user profile page on the network"""
        raise NotImplementedError

    def sourceid(self):
        """String representing the name or identification for the network. Used to associate items with the provider."""
        raise NotImplementedError

class ActivityInfo(object):
    def __init__(self, title, link, pub_date, guid, username=None, author=None, comments='', published=True):
        self.title = title
        self.link = link
        self.username = username
        self.author = author
        self.comments = comments
        self.pub_date = pub_date
        self.published = published
        self.guid = guid

