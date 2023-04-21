from django.test import TestCase
from django.urls import reverse, resolve

from accounts.models import User
from accounts import views
from accounts import forms


class TestAccountsLoginViews(TestCase):
    def test_login_view_is_rendering_code_200_OK(self):
        url = reverse('accounts:login')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_login_view_is_rendering_correct_view_class(self):
        url = reverse('accounts:login')
        response = resolve((url))

        self.assertIs(response.func.view_class, views.Login)

    def test_login_view_is_rendering_correct_template_view(self):
        url = reverse('accounts:login')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_is_rendering_correct_form(self):
        url = reverse('accounts:login')
        response = self.client.get(url)

        response_context = response.context['login_form']

        self.assertIs(response_context.__class__, forms.UserLoginForm)

    def test_login_page_redirect_to_index_when_user_already_logged(self):
        user = User.objects.create_user(
            email="testlogin@email.com",
        )
        user.set_password('123456')
        user.save()

        self.client.login(email="testlogin@email.com",
                          password='123456')

        url = reverse('accounts:login')
        response = self.client.get(url)
        redirect_url = reverse('posts:index')

        self.assertRedirects(response, redirect_url)
