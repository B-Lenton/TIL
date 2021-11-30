from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls.base import reverse


class ProfileViewTests(TestCase):
    '''
    Setup copied from feed/test_views.py & slightly modified.
    TODO: not yet working as expected.
    '''
    def setUp(self):
        follower = User.objects.create_user(
            username="follower",
            password="followerpwd"
        )
        followed = User.objects.create_user(
            username="followed",
            password="followedpwd"
        )
        self.client = Client()
        self.client.force_login(user=follower)
        self.client.force_login(user=followed)

    def test_profile_view(self):
        '''
        TODO: Modify this copied code to check whether the profile correctly
        displays followers, total posts etc (may need to be separate tests):
        '''
        response = self.client.get(reverse("profiles:details"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "a post for testing!")
        self.assertTemplateUsed(response, "feed/homepage.html")
