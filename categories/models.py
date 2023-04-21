from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)
    on_navbar = models.BooleanField(default=False)

    def __str__(self):
        return self.name
