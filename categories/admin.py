from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'on_navbar')
    list_editable = ('on_navbar', )


admin.site.register(Category, CategoryAdmin)
