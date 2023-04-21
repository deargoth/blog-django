from django.db import models
from accounts.models import User
from posts.models import Post
from django.utils import timezone


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name
