from django.test import TestCase

class MyTests(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)

    def test_blog(self):
        response = self.client.get('/blog/')
        self.failUnlessEqual(response.status_code, 200)

    def test_activity(self):
        response = self.client.get('/activity/')
        self.failUnlessEqual(response.status_code, 200)

    def test_feed(self):
        response = self.client.get('/feeds/latest/')
        self.failUnlessEqual(response.status_code, 200)