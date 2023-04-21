from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from .models import Post


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = 'content'
    list_display = ('id', 'title', 'slug', 'author', 'created_at',
                    'updated_at', 'category', 'is_published')
    list_editable = ('is_published', )
    list_display_links = ('id', 'title', 'slug')


admin.site.register(Post, PostAdmin)
