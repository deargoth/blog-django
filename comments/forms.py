from django import forms
from .models import Comment


class CommentFormVisitor(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment')


class CommentFormUser(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', )
