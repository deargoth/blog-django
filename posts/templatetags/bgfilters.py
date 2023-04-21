from django.template import Library
from django.template.loader import render_to_string

from categories.models import Category

register = Library()


@register.filter()
def format_comments_string(num_comments):
    if num_comments == 1:
        return f'{num_comments} comentário'

    if num_comments > 1:
        return f'{num_comments} comentários'

    return 'Nenhum comentário'


@register.simple_tag
def categories_on_navbar():
    category = Category.objects.filter(on_navbar=True)
    return render_to_string('posts/_categories.html', {'categories': category})
