from .post_model_base import BasePostModel
from django.urls import reverse, resolve

from posts import views


class PostIndexViewTests(BasePostModel):
    def setUp(self, *args, **kwargs):
        self.post = self.make_post()
        self.category = self.make_category('PHP Category')

        self.category.on_navbar = True
        self.category.save()

        return super().setUp(*args, **kwargs)

    def test_post_nav_bar_just_show_a_category_if_on_navbar_is_true(self):
        url = reverse('posts:index')
        response = self.client.get(url)

        response_content = response.content.decode('utf-8')
        self.assertIn('PHP Category', response_content)

    def test_post_nav_bar_dont_show_a_category_if_on_navbar_is_false(self):
        self.category.on_navbar = False
        self.category.save()

        url = reverse('posts:index')
        response = self.client.get(url)

        response_content = response.content.decode('utf-8')
        self.assertNotIn('PHP Category', response_content)

    def test_post_index_view_is_loading_correct_template(self):
        url = reverse('posts:index')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'posts/index.html')

    def test_post_index_is_returning_view_code_200_OK(self):
        url = reverse('posts:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_post_index_is_loading_correct_view(self):
        url = reverse('posts:index')
        response = resolve(url)

        self.assertIs(response.func.view_class, views.Index)

    def test_post_index_load_a_post(self):
        self.post.is_published = True
        self.post.save()

        url = reverse('posts:index')
        response = self.client.get(url)

        response_content = response.content.decode('utf-8')

        self.assertIn('Post Default Title', response_content)
        self.assertIn('Category Default Name', response_content)

    def test_post_index_do_not_show_post_when_is_published_is_false(self):
        post = self.make_post(
            title='Another post to test is_published',
            author={'email': 'testfield@email.com'},
        )
        post.is_published = True
        post.save()

        url = reverse('posts:index')
        response = self.client.get(url)

        response_context = response.context['posts']

        '''
        We already have a post created on setUp, but it's setted as false, 
        so it must be just one post, since we created another just for the test
        '''
        self.assertEqual(len(response_context), 1)

    def test_post_index_returns_no_posts_found_when_there_is_not_published_posts(self):
        url = reverse('posts:index')
        response = self.client.get(url)

        response_content = response.content.decode('utf-8')
        self.assertIn("We didn\'t encounter any post here, i\'m sorry! Come here later",
                      response_content)
