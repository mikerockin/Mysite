from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'image')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label='Имя')
    email = forms.EmailField()
    to = forms.EmailField(label='Кому')
    comments = forms.CharField(label='Комментарий', required=False, widget=forms.Textarea)

class SearchForm(forms.Form):
    query = forms.CharField(label='Что ищем?')