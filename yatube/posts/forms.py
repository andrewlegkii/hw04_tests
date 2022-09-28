# posts/forms.py
from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group',)
        help_texts = {
            'text': 'Тут пишите текст поста',
            'group': 'Тут выбираете группу, к которой принадлежит пост',
        }
        labels = {
            'text': 'Текст',
            'group': 'Группа',
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
