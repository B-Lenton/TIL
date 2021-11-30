from django.test import SimpleTestCase
from django.urls import reverse, resolve
from feed.views import HomePage, PostDetailView, CreateNewPost


class TestUrls(SimpleTestCase):
    '''
    Three simple tests to check that the feed/urls resolve to
    the correct View in feed/views.py - tests created for practice.
    '''
    def test_home_url_is_resolved(self):
        url = reverse('feed:index')
        self.assertEquals(resolve(url).func.view_class, HomePage)

    def test_post_detail_url_is_resolved(self):
        url = reverse('feed:detail', args=['1'])
        self.assertEquals(resolve(url).func.view_class, PostDetailView)
    
    def test_new_post_url_is_resolved(self):
        url = reverse('feed:new_post')
        self.assertEquals(resolve(url).func.view_class, CreateNewPost)

