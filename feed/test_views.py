from datetime import datetime
from django.test import Client, TestCase
from unittest.mock import patch
import pytz
from freezegun import freeze_time
from django.urls import reverse
from feed.models import Post

from django.contrib.auth.models import User

from profiles.views import FollowView


class PostsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="specialpwd"
        )
        self.client = Client()
        self.client.force_login(user=self.user)
        self.post = Post.objects.create(
            text="a post for testing!",
            author=self.user
        )

    def test_post_content(self):
        self.assertEqual(f"{self.post.author}", "testuser")
        self.assertEqual(f"{self.post.text}", "a post for testing!")

    def test_post_list_view(self):
        response = self.client.get(reverse("feed:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "a post for testing!")
        self.assertTemplateUsed(response, "feed/homepage.html")

    @freeze_time("1997-05-20 16:17:03", tz_offset=0)
    def test_post_create_view(self):
        post_objects_before = Post.objects.count()
        response = self.client.post(reverse("feed:new_post"), {
            "text": "new post",
        })
        self.assertTrue(Post.objects.count(), post_objects_before + 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"new post", response.content)
        post = Post.objects.filter(author=self.user).last()
        self.assertEqual(post.text, "new post")
        self.assertEqual(post.date, datetime(1997, 5, 20, 16, 17, 3).replace(tzinfo=pytz.utc))
        self.assertEqual(post.author, self.user)


class MockResponse:
    def __init__(self) -> None:
        self.status_code = 200

    def json(self):
        return {
            "action": "follow",
            "username": "followed",
            "success": "true",
            "wording": "Unfollow"
        }


class TestFeedDisplay(TestCase):
    '''
    TODO: Mock response isn't working as it should:
    AttributeError: 'dict' object has no attribute 'POST'
    '''
    @patch("requests.post", return_value=MockResponse())
    def test_call(self, mocked):
        self.assertEqual(
            FollowView().post(request={"action": "follow", "user": "followed"}),
            {
            'success': True,
            "wording": "Unfollow"
            },
        )


    # def test_feed_display(self):
    #     '''
    #     TODO: Too much setup, so may need to put into new test class.
    #     See profiles/views.py FollowView for idea of how to structure the follow request.
    #     ERROR: Returning 400 rather than 200; not the right data passed to the post request.
    #     '''
    #     follower = self.user
    #     followed = User.objects.create_user(
    #         username="followed",
    #         password="securepwd"
    #     )
    #     not_followed = User.objects.create_user(
    #         username="not-followed",
    #         password="safepwd"
    #     )
    #     response1 = self.client.post(reverse("feed:new_post"), {
    #         "text": "seen post",
    #         "author": followed
    #     })
    #     response2 = self.client.post(reverse("feed:new_post"), {
    #         "text": "unseen post",
    #         "author": not_followed
    #     })
    #     self.assertEqual(response1.status_code, 200)
    #     self.assertEqual(response2.status_code, 200)
    #     follow = self.client.post(reverse("profiles:follow", args=[followed]), {
    #         "follower": follower,
    #         "other_user": followed,
    #     }, follow=True)
    #     self.assertEqual(follow.status_code, 200)
    
    # def test_not_follow_feed(self):
    #     pass

    # def test_posts_displayed(self):
        '''
        If following other profiles, users should only see the posts of those
        profiles; If following no one, the default most recent 30 posts should
        be shown.
        '''
        # follower = create_user(username="testuser1", password="12345")
        # followed = create_user(username="testuser2", password="abcde")
        # not_followed = create_user(username="testuser3", password="1b3d5")
        # Follower.objects.create(followed_by=follower, following=followed)
        # create_post(text="test post for follower to see", author=followed)
        # create_post(text="test post not to be seen", author=not_followed)
        # following = list(Follower.objects.filter(followed_by=follower).values_list("following", flat=True))
        # follower_homepage = Post.objects.filter(author__in=following).order_by("-id")[0:60]
        # default_homepage = Post.objects.all().order_by("-id")[0:30] 
        # self.assertNotEqual(follower_homepage, default_homepage)
        

    # def test_no_posts(self):
    #     '''
    #     If no posts exist, an appropriate message is displayed.
    #     '''
    #     response = self.client.get(reverse('feed:index'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "No posts are available.")

    # def test_new_post(self):
    #     '''
    #     Asserts that new user posts are successfully created.
    #     TODO: Passes but isn't acknowledged by "coverage".
    #     '''
    #     self.user = create_user(username='test user', password='12345')
    #     post = create_post(text="new post!", author=self.user)
    #     response = self.client.get(reverse('feed:index'))
    #     self.assertQuerysetEqual(
    #         response.context["posts"], 
    #         [post],
    #     )
