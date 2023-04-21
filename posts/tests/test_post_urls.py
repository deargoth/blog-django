from django.test import TestCase
from django.urls import reverse


class PostUrlsTests(TestCase):
    def test_if_index_url_is_redirecting_to_correct_url(self):
        url = reverse('posts:index')
        self.assertEqual(url, '/')

    def test_if_details_url_is_redirecting_to_correct_url(self):
        url = reverse('posts:details', kwargs={'slug': 'lorem-ipsum-dolor'})
        self.assertEqual(url, '/details/lorem-ipsum-dolor')

    def test_if_category_url_is_redirecting_to_correct_url(self):
        url = reverse('posts:category', kwargs={
                      'category': 'Python'})
        self.assertEqual(url, '/category/Python')
