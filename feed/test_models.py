from django.contrib.auth.models import User
from django.test import TestCase
from feed.models import Post


def create_user(username, password):
    return User.objects.create_user(username=username, password=password)

# Create your tests here.
class PostTests(TestCase):
    #     '''
    #     A string representation of a post should only return the first 100
    #     characters in admin.
    #     '''
    def setUp(self):
        self.post = Post.objects.create(
            text="a test post with more than 100 characters!a test post with more than 100 characters!a test post with more than 100 characters!",
            author=create_user(username="Fred", password="fred123")
        )

    def test_post_string(self):
        self.assertEqual(str(self.post), self.post.text[0:100])
 