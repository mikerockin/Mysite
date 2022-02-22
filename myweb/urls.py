from django.contrib import admin
from django.contrib.auth import logout
from rest_framework import permissions
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from myweb import settings
from story.sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = { 'posts': PostSitemap,}

schema_view = get_schema_view(
   openapi.Info(
      title="History of instant API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL},
         name='logout'),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', include('story.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/docs/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/docs/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]

