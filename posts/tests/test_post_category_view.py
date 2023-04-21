from .post_model_base import BasePostModel
from django.urls import reverse, resolve

from posts.views import Category


class TestCategoryView(BasePostModel):
    def setUp(self, *args, **kwargs):
        self.post1 = self.make_post(title='Post One', author={
                                    'email': 'post1@email.com'}, category={'name': 'Python'})
        self.post2 = self.make_post(title='Post Two', author={
                                    'email': 'post2@email.com'}, category={'name': 'Python'})
        self.post3 = self.make_post(title='Post Three', author={
                                    'email': 'post3@email.com'}, category={'name': 'JavaScript'})

        self.post1.is_published = True
        self.post2.is_published = True
        self.post3.is_published = True

        self.post1.save()
        self.post2.save()
        self.post3.save()

        return super().setUp(*args, **kwargs)

    def test_category_view_is_loading_correct_template(self):
        url = reverse('posts:category', kwargs={'category': 'Python'})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'posts/category.html')

    def test_category_view_is_loading_correct_view_class(self):
        url = reverse('posts:category', kwargs={'category': 'Python'})
        response = resolve(url)

        self.assertIs(response.func.view_class, Category)

    def test_category_view_is_returning_just_posts_from_the_current_category(self):
        url = reverse('posts:category', kwargs={'category': 'Python'})
        response = self.client.get(url)

        response_context = response.context['posts']

        '''
        We created three posts, but two of them are from the category
        "Python" (wich is the one that we're looking for), 
        and the other is from "JavaScript", so it must have just 2 posts on the context.
        '''
        self.assertEqual(len(response_context), 2)

    def test_category_view_is_rendering_only_published_posts(self):
        self.post2.is_published = False
        self.post2.save()

        url = reverse('posts:category', kwargs={'category': 'Python'})
        response = self.client.get(url)

        response_context = response.context['posts']

        '''
        We have only two posts in "Python" category, and we setted one as not published,
        so it must be just ONE in the context of the response.
        '''
        self.assertEqual(len(response_context), 1)
