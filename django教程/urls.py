"""django教程 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include,re_path
from  polls.models import Question

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'polls': GenericSitemap({'queryset': Question.objects.all(), 'question_text': 'pub_date'}, priority=0.6),
    # 如果还要加其它的可以模仿上面的
}
urlpatterns = [
    re_path(r'^admin/doc/',include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
]
