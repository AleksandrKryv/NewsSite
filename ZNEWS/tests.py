from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from .models import *
from .views import *
from .urls import *


class UrlsTest(TestCase):

    def setUp(self):
        Category.objects.create(category_name="heh")
        self.client = Client()

    def test_main_page_returns_200(self):
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)

    def test_category_returns_200(self):
        response = self.client.get(reverse('category', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

class TestModels(TestCase):

    def test_post_creation(self):
        post = NewsPost.objects.create(
            post_header='heh',
            post_content='hoh',
        )
        self.assertIsNotNone(post)
