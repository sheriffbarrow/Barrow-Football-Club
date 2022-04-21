"""Barrow_Football_Club URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from bfc.sitemaps import PostSitemap
from django.views.generic.base import TemplateView 

sitemaps = {
    'posts': PostSitemap
}

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('', include('django.contrib.auth.urls')),
    path('only_admin/', admin.site.urls),
    path('', include('bfc.urls')),
    path('account/', include('account.urls')),
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps},
    name = 'django.contrib.sitemaps.views.sitemap'),
    path("robots.txt",TemplateView.as_view(template_name="bfc/robots.txt", content_type="text/plain")),
    path('summernote/', include('django_summernote.urls')),
]

handler500 = 'bfc.views.error_500'
handler404 = 'bfc.views.error_404'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
