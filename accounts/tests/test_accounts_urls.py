from django.test import TestCase
from django.urls import reverse


class TestAccountsUrls(TestCase):
    def test_if_the_login_url_is_redirecting_to_correct_url(self):
        url = reverse('accounts:login')
        self.assertEqual(url, '/accounts/login/')

    def test_if_the_register_url_is_redirecting_to_correct_url(self):
        url = reverse('accounts:register')
        self.assertEqual(url, '/accounts/register/')
