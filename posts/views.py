from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, View
from django.http import Http404
from django.contrib import messages
from django.db.models import Q, Case, When, Count

from .models import Post
from comments import forms, models
from utils import site_messages


class Index(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True).order_by('-id')
        qs = qs.annotate(
            num_comments=Count(
                Case(
                    When(
                        comment__is_published=True, then=1
                    )
                )
            )
        )

        return qs


class Details(View):
    template_name = 'posts/details.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.messages = site_messages

        slug = self.kwargs.get('slug')

        try:
            self.current_post = Post.objects.get(slug=slug)
        except:
            raise Http404()

        if self.request.user.is_authenticated:
            comment_form = forms.CommentFormUser(self.request.POST or None)
        else:
            comment_form = forms.CommentFormVisitor(self.request.POST or None)

        comments = models.Comment.objects.filter(
            post=self.current_post, is_published=True)

        self.context = {
            'post': self.current_post,
            'comment_form': comment_form,
            'comments': comments,
        }
        self.comment_form = self.context['comment_form']

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render

    def post(self, *args, **kwargs):
        if not self.comment_form.is_valid():
            messages.error(self.request,
                           self.messages.errors['comment_form_invalid'])
            return render(self.request, self.template_name, self.context)

        form = self.comment_form.save(commit=False)
        form.post = self.current_post

        if self.request.user.is_authenticated:
            form.author = self.request.user
            form.name = self.request.user.first_name
            form.email = self.request.user.email

        form.save()

        messages.success(self.request,
                         self.messages.success['comment_posted_to_avaliate'])

        return redirect(reverse('posts:details', kwargs={'slug': f'{self.current_post.slug}'}))


class Category(Index):
    template_name = 'posts/category.html'

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.kwargs.get('category')

        qs = qs.filter(category__name__exact=category)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = f'"{self.kwargs.get("category")}"'

        return context
