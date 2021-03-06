from django.urls import path, include, re_path
from django.conf.urls.static import static
from rest_framework import routers
from django.conf import settings
from . import views


router = routers.DefaultRouter()
router.register(r'Posts', views.PostViewSet)
router.register(r'Comments', views.CommentViewSet)
router.register(r'Users', views.UserViewSet)


app_name = 'story'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/share/', views.post_share, name='post_share'),
    path('search/', views.post_search, name='post_search'),
    path('', views.post_list, name='post_list'),
    re_path(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)