from django.test import TestCase
from django.urls import reverse, resolve

from accounts import views
from accounts.models import User
from accounts import forms


class TestAccountsRegisterViews(TestCase):
    def test_register_view_is_rendering_code_200_OK(self):
        url = reverse('accounts:register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_register_view_is_rendering_correct_view_class(self):
        url = reverse('accounts:register')
        response = resolve((url))

        self.assertIs(response.func.view_class, views.Register)

    def test_register_view_is_rendering_correct_template_view(self):
        url = reverse('accounts:register')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_view_redirect_to_index_when_already_authenticated(self):
        user = User.objects.create_user(
            email='testdemo@email.com',
        )
        user.set_password('password')
        user.save()

        user = self.client.login(email='testdemo@email.com',
                                 password='password')

        url = reverse('accounts:register')
        response = self.client.get(url)

        redirect_url = reverse('posts:index')

        self.assertRedirects(response, redirect_url)

    def test_register_view_is_rendering_the_correct_form(self):
        url = reverse('accounts:register')
        response = self.client.get(url)

        response_context = response.context['register_form']

        self.assertIs(response_context.__class__, forms.UserRegisterForm)
