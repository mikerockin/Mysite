from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager

class Post(models.Model):
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, verbose_name="Название")
    text = models.TextField(verbose_name="История на снимке")
    image = models.ImageField(upload_to='images/%Y-%m-%d/', default='images/noimage.jpg', verbose_name="Фото",null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('story:post_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=25)
    email = models.EmailField(null=True)
    body = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  # булево значение, которое будет использоваться для отключения неприемлемых комментариев вручную

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Комментировано {} в {}'.format(self.name, self.post)
