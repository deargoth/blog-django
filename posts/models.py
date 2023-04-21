from django.db import models
from django.utils.text import slugify
from django.conf import settings
from PIL import Image

from accounts.models import User
from categories.models import Category


class Post(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(blank=True, null=True)
    description = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    image = models.ImageField(
        upload_to='blog_imgs/%Y/%m', blank=True, null=True)

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = settings.MEDIA_ROOT / image.name
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            self.slug = slug

        super().save(*args, **kwargs)

        if self.image:
            self.resize_image(self.image, 800)

    def __str__(self):
        return self.title
