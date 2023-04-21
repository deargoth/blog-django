from django.test import TestCase
from .models import Comment
from posts.tests.post_model_base import BasePostModel


class TestCommentModel(BasePostModel):
    def setUp(self, *args, **kwargs):
        self.post = self.make_post()

        self.comment = self.make_comment(
            author=self.post.author, post=self.post)

        return super().setUp(*args, **kwargs)

    def test_comment_is_published_is_false_by_default(self):
        field = self.comment.is_published

        self.assertEqual(field, False)

    def test_comment_string_representation(self):
        self.assertEqual(str(self.comment), 'Comment')
