from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at',
                    'post', 'is_published')

    list_editable = ('is_published', )


admin.site.register(Comment, CommentAdmin)
