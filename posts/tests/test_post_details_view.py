from .post_model_base import BasePostModel
from django.urls import reverse, resolve

from posts import views
from accounts.models import User
from comments import forms


class TestDetailsView(BasePostModel):
    def setUp(self, *args, **kwargs):
        self.post = self.make_post()
        self.comment = self.make_comment(
            post=self.post, author=self.post.author)

        self.comment2 = self.make_comment(
            post=self.post, author=self.post.author)

        self.comment.is_published = True
        self.comment2.is_published = True
        self.comment.save()
        self.comment2.save()

        return super().setUp(*args, **kwargs)

    def test_details_view_is_rendering_the_correct_template(self):
        url = reverse('posts:details', kwargs={'slug': 'post-default-title'})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'posts/details.html')

    def test_details_view_is_loading_the_correct_view(self):
        url = reverse('posts:details', kwargs={'slug': 'post-default-title'})
        response = resolve(url)

        self.assertIs(response.func.view_class, views.Details)

    def test_details_view_returns_400_error_if_no_post_founded(self):
        url = reverse('posts:details', kwargs={
                      'slug': 'lorem-ipsum-dolor-error-404-return'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_details_view_returns_200_OK_if_post_founded(self):
        url = reverse('posts:details', kwargs={'slug': 'post-default-title'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_details_view_is_rendering_comments_if_is_published(self):
        url = reverse('posts:details', kwargs={'slug': 'post-default-title'})
        response = self.client.get(url)
        response_context = response.context['comments']

        self.assertEqual(len(response_context), 2)

    def test_details_view_is_not_rendering_comments_if_is_not_published(self):
        self.comment2.is_published = False
        self.comment2.save()

        url = reverse('posts:details', kwargs={'slug': 'post-default-title'})
        response = self.client.get(url)
        response_context = response.context['comments']

        self.assertEqual(len(response_context), 1)

    def test_details_view_rendering_the_correct_form_for_authenticated_users(self):
        user = User.objects.create_user('test@email.com')
        user.set_password('123456')
        user.save()

        self.client.login(email='test@email.com', password='123456')

        url = reverse('posts:details', kwargs={'slug': 'post-default-title'})
        response = self.client.get(url)

        response_context = response.context['comment_form']

        self.assertIs(response_context.__class__,
                      forms.CommentFormUser)

    def test_details_view_rendering_the_correct_form_for_unauthenticated_users(self):
        url = reverse('posts:details', kwargs={'slug': 'post-default-title'})
        response = self.client.get(url)

        response_context = response.context['comment_form']

        self.assertIs(response_context.__class__,
                      forms.CommentFormVisitor)
