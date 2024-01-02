from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase
from .models import Post


class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="user1")
        # published Post
        cls.obj1 = Post.objects.create(title="new post", text="this a text", author=cls.user,
                                       status=Post.STATUS_CHOICES[0][0])
        # draft Post
        cls.obj2 = Post.objects.create(title="new post 1", text="this a text 1", author=cls.user,
                                       status=Post.STATUS_CHOICES[1][0])

    # def setUp(self):
    #     self.user = User.objects.create(username="user1")
    #     # published Post
    #     self.obj1 = Post.objects.create(title="new post", text="this a text", author=self.user,
    #                                     status=Post.STATUS_CHOICES[0][0])
    #     # draft Post
    #     self.obj2 = Post.objects.create(title="new post 1", text="this a text 1", author=self.user,
    #                                     status=Post.STATUS_CHOICES[1][0])

    def test_post_representation(self):
        self.assertEqual(str(self.obj1), self.obj1.title)

    def test_post_list_url(self):
        response = self.client.get('/blogs/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_title(self):
        response = self.client.get(reverse('post_list'))
        # print(self.obj)
        self.assertContains(response, self.obj1.title)
        self.assertNotContains(response, "post 12")

    def test_detail_url(self):
        response = self.client.get(f'/blog/{self.obj1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_detail_url_by_name(self):
        response = self.client.get(reverse('post_detail', args=(self.obj1.id,)))
        self.assertEqual(response.status_code, 200)

    def test_post_detail(self):
        response = self.client.get(f'/blog/{self.obj1.id}/')
        self.assertContains(response, self.obj1.title)
        self.assertContains(response, self.obj1.text)
        self.assertContains(response, self.obj1.author)

    def test_status_404_if_id_not_exist(self):
        response = self.client.get(reverse('post_detail', args=(12,)))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show(self):
        response = self.client.get(reverse('post_list'))
        self.assertNotContains(response, self.obj2)

    def test_post_create_view(self):
        response = self.client.post(reverse("post_create"), {
            "title": "title 1",
            "text": "text 1",
            "status": "pub",
            "author": self.user.id,
        })
        # 302: object created
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "title 1")
        self.assertEqual(Post.objects.last().text, "text 1")

    def test_post_update_view(self):
        response = self.client.post(reverse("post_update", args=(self.obj1.id,)), {
            "title": "updated title",
            "text": "updated text",
            "status": "pub",
            "author": self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.first().title, "updated title")
        self.assertEqual(Post.objects.first().text, "updated text")

    def test_post_delete_view(self):
        response = self.client.post(reverse("post_delete", args=(self.obj1.id,)))
        self.assertEqual(response.status_code, 302)
