from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm, CommentForm, EmailPostForm
from django.contrib.auth.decorators import login_required
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from .models import Post, Comment
from django.contrib.auth.models import User
from rest_framework import viewsets


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'story/post_list.html',
                  context={'posts': posts})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'story/post_detail.html',
                  context={'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form}
    )


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('story:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'story/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'story/post_edit.html', {'form': form})


def post_share(request, pk):
    post = get_object_or_404(Post, pk=pk)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data  # атрибут представляет собой словарь полей форм и их значений Если данные формы не
            # валидные, cleaned_data будет содержать только валидные поля
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) рекомендует Вам прочесть "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Читайте "{}" на {}\n\n{}\'s прокомментировал: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'mrmikhail88@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'story/share.html', {'post': post, 'form': form, 'sent': sent})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('published_date')
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('post')
    serializer_class = CommentSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

