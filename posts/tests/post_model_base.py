from django.test import TestCase

from posts.models import Post
from accounts.models import User
from categories.models import Category
from comments.models import Comment


class BasePostModel(TestCase):
    def setUp(self, *args, **kwargs):
        return super().setUp()

    def make_post(
        self,
        title='Post Default Title',
        slug=None,
        description='Post Default Description',
        content='Post Default Content',
        author=None,
        category=None,
    ):
        if author is None:
            author = {}

        if category is None:
            category = {}

        return Post.objects.create(
            title=title,
            slug=slug,
            description=description,
            content=content,
            author=self.make_author(**author),
            category=self.make_category(**category),
        )

    def make_author(
        self,
        email='admindemo@email.com',
        first_name='demo',
        last_name='admin',
        password='demodemo',
    ):
        return User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

    def make_category(
        self,
        name='Category Default Name'
    ):
        return Category.objects.create(
            name=name,
        )

    def make_comment(
        self,
        author=None,
        post=None,
        name='Comment',
        email='comment@email.com',
        comment='Just a generic comment here.',
    ):

        return Comment.objects.create(
            author=author,
            post=post,
            name=name,
            email=email,
            comment=comment,
        )
