from django.test import TestCase
from .post_model_base import BasePostModel
from django.core.exceptions import ValidationError
from parameterized import parameterized


class PostModelTests(BasePostModel):
    def setUp(self):
        self.post = self.make_post()
        return super().setUp()

    @parameterized.expand([
        ('title', 64),
        ('description', 255),
    ])
    def test_post_model_max_length(self, field, max_length):
        setattr(self.post, field, 'A' * (max_length + 1))

        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_post_model_is_published_field_is_false_by_default(self):
        self.assertIs(self.post.is_published, False)

    def test_post_model_string_representation_is_correct(self):
        self.post.title = 'String Representation Test'
        self.post.full_clean()
        self.post.save()

        self.assertEqual(str(self.post), 'String Representation Test')
