from rockycode import settings
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.urlresolvers import reverse
from rockycode.blog.models import Article
from tagging.models import Tag, TaggedItem
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

SITE = Site.objects.get_current()
FEED_TIMEOUT = getattr(settings, 'FEED_TIMEOUT', 86400) # 24 hrs

class TechFeed(Feed):
    def get_object(self, request, tag):
        return Tag.objects.get(name__iexact=tag)

    def title(self, obj):
        return "%s: %s articles" % (SITE.name, obj.name)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('article_list_tech', args=[obj.name])

    def description(self, obj):
        return "Articles related to %s" % obj.name

    def items(self, obj):
        return self.item_set(obj)

    def item_set(self, obj):
        key = 'articles_tech_%s' % obj.name
        articles = cache.get(key)

        if articles is None:
            articles = list(TaggedItem.objects.get_by_model(Article, obj).order_by("-date_published"))
            cache.set(key, articles, FEED_TIMEOUT)

        return articles

    def item_author_name(self, item):
        return item.user.username

    def item_author_link(self, item):
        return reverse('author_list_un', args=[item.user.username])

    def item_pubdate(self, item):
        return item.date_published

class AuthorFeed(Feed):
    def get_object(self, request, username):
        return get_object_or_404(User, username=username)

    def title(self, obj):
        return "%s: %s's articles" % (SITE.name, obj.username)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('article_list_author', args=[obj.username  ])

    def description(self, obj):
        return "Articles written by %s %s" % (obj.first_name, obj.last_name)

    def items(self, obj):
        return self.item_set(obj)

    def item_set(self, obj):
        key = 'articles_author_%s' % obj.username
        articles = cache.get(key)

        if articles is None:
            articles = list(Article.objects.filter(user__username = obj).order_by("-date_published"))
            cache.set(key, articles, FEED_TIMEOUT)

        return articles

    def item_author_name(self, item):
        return item.user.username

    def item_author_link(self, item):
        return reverse('author_list_un', args=[item.user.username])

    def item_pubdate(self, item):
        return item.date_published

class AllArticlesFeed(Feed):

  def title(self):
    return "%s: all articles" % SITE.name

  def link(self):
    return reverse('article_list', args=[])

  def description(self):
    return "All rockycode.com articles"
    
  def items(self):
    return Article.objects.filter(active=True).order_by("-date_published")

  def item_title(self, item):
    return item.title

  def item_description(self, item):
    return item.summary

  def item_pubdate(self, item):
    return item.date_published
