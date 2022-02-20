from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'image', 'published_date')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'text')
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ['published_date']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

