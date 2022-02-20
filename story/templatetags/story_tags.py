from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

from ..models import Post
from django.db.models import Count


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.simple_tag
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('story/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-published_date')[:count]
    return {'latest_posts': latest_posts}
