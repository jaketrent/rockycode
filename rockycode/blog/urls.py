from django.conf.urls.defaults import *

import settings
from django.contrib.syndication.views import feed
from blog.views import *
from blog.feeds import TechFeed, AuthorFeed, AllArticlesFeed
from profiles import views as pv
from django.core.urlresolvers import reverse
from blog.models import ArticleSitemap

feeds = {
  'tech': TechFeed,
  'author': AuthorFeed,
  'blog': AllArticlesFeed
}

sitemaps = {
  'articles': ArticleSitemap,
}

urlpatterns = patterns('',
  url(r'^$', home, name='home'),
  url(r'^blog/$', article_list, name='article_list'),
  url(r'^blog/author/(?P<author_username>[\-\d\w]+)/$', article_list_author, name='article_list_author'),
  url(r'^blog/tech/(?P<filter_item>[^/]+)/$', article_list_tech, name='article_list_tech'),
  url(r'^blog/(?P<slug>[\-\d\w]+)/$', article_detail, name='article_detail'),

  url(r'^guides/$', guide_list, name='guide_list'),
  url(r'^guides/(?P<slug>[\-\d\w]+)/$', guide_detail, name='guide_detail'),
  url(r'^guides/(?P<slug>[\-\d\w]+)/$', guide_detail, name='guide_detail'),
  url(r'^guides/(?P<guide_slug>[\-\d\w]+)/(?P<article_slug>[\-\d\w]+)/$', guide_article_detail, name='guide_article_detail'),


  url(r'^authors/$', author_list, name='author_list'),
  url(r'^authors/#(?P<username>[\-\d\w]+)$', author_list, name='author_list_un'),
  url(r'^authors/(?P<username>[\-\d\w]+)$', author_detail, name='author_detail'),
  url(r'^techs/$', tech_list, name="tech_list"),

  url(r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': feeds}, name="feeds"),
  url(r'^feeds/(?P<url>.*)\.rss$', feed, {'feed_dict': feeds}, name='dyn-feeds'),
  
  url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name="sitemap"),

  url(r'^blog/upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.UPLOAD_PATH}, name="upload_path"),
  url(r'^media/files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.UPLOAD_PATH}, name="upload_path")
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^techs/$', 'direct_to_template', {'template': 'blog/tech_list.html'}, name="tech_list"),
    url(r'^about/$', 'direct_to_template', {'template': 'blog/about.html'}, name="about"),
)
