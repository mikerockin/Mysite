from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm, CommentForm, EmailPostForm, SearchForm
from django.contrib.auth.decorators import login_required
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from .models import Post, Comment
from django.contrib.auth.models import User
from rest_framework import viewsets
from taggit.models import Tag
from django.db.models import Count #позволяет получать агрегированные показатели
from django.contrib.postgres.search import SearchVector

def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'story/post_list.html', context={'page':page, 'posts': posts, 'tag': tag})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True) #извлекаем список идентификаторов(id) тегов текущей записи. Набор запросов values_list() возвращает кортежи со значениями для заданных полей
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id) # получим все записи, которые содержат любые из этих тегов, исключая текущую запись.
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-published_date')[:4] # Для создания вычисляемого same_tags, содержащего число тегов, общих со всеми запрошенными тегами, используется статистическая функция Count.
    return render(request, 'story/post_detail.html',
                  context={'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'similar_posts': similar_posts})


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
            return redirect('story:post_detail', pk=post.pk)
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

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'text'),
            ).filter(search=query)
    return render(request,
                  'story/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('published_date')
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('post')
    serializer_class = CommentSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

