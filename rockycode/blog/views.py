
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404

from blog.models import Article, Collection
from django.contrib.auth.models import User
from django.db.models import Count, Max
from tagging.models import Tag, TaggedItem
import settings
from blog import util
from django.views.generic.simple import direct_to_template
import datetime
from dateutil.relativedelta import relativedelta

def home(request):
  articles = Article.objects.filter(active=True).order_by('-date_published')[:5]
  authors = User.objects.annotate(article_count=Count('article__id'), has_active=Count('article__active')).filter(has_active__gt=0, article_count__gt=0).order_by("-article_count","id")
  techs = Tag.objects.annotate(article_count=Count('items__id')).order_by("-article_count")
  return render_to_response("home.html", locals(),
                            context_instance=RequestContext(request))

def article_list(request):
  articles = util.paginate(request, Article.objects.filter(active=True).order_by("-date_published"), 20)
  authors = User.objects.annotate(article_count=Count('article__id'), has_active=Count('article__active')).filter(has_active__gt=0, article_count__gt=0).order_by("-article_count")
  return render_to_response("blog/article_list.html", locals(),
                            context_instance=RequestContext(request))

def article_list_author(request, author_username):
  user = User.objects.filter(username=author_username)
  rawArticles = Article.objects.filter(active=True, user=user).order_by("-date_published")
  articles = util.paginate(request, rawArticles, 20)
  site_start_date = getattr(settings, 'SITE_START_DATE')
  months = util.get_monthly_activity(rawArticles)
  authors = User.objects.annotate(article_count=Count('article__id'), has_active=Count('article__active')).filter(has_active__gt=0, article_count__gt=0).order_by("-article_count")
  filter_type = "author"
  filter_item = "%s %s" % (user[0].first_name, user[0].last_name)
  return render_to_response("blog/article_list.html", locals(),
                            context_instance=RequestContext(request))

def article_list_tech(request, filter_item):
  tag = get_object_or_404(Tag, name = filter_item)
  rawArticles = TaggedItem.objects.get_by_model(Article.objects.filter(active=True), tag).order_by("-date_published")
  articles = util.paginate(request, rawArticles)
  months = util.get_monthly_activity(rawArticles)
  authors = User.objects.annotate(article_count=Count('article__id'), has_active=Count('article__active')).filter(has_active__gt=0, article_count__gt=0).order_by("-article_count")
  filter_type = "technology"
  return render_to_response("blog/article_list.html", locals(),
                            context_instance=RequestContext(request))

def article_detail(request, slug):
  article = get_object_or_404(Article, title_slug = slug)
  disqus_forum = getattr(settings, 'DISQUS_FORUM', 'rockycode')
  disqus_dev = getattr(settings, 'DISQUS_DEV', '0')
  return render_to_response("blog/article_detail.html", locals(),
                            context_instance=RequestContext(request))

def author_list(request):
  authors = User.objects.annotate(article_count=Count('article__id'), has_active=Count('article__active')).filter(has_active__gt=0, article_count__gt=0).order_by("-article_count","id")
  return render_to_response("blog/author_list.html", locals(),
                            context_instance=RequestContext(request))

def tech_list(request):
  top_techs = Tag.objects.annotate(article_count=Count('items__id')).order_by("-article_count")[:10]
  return render_to_response("blog/tech_list.html", locals(),
                            context_instance=RequestContext(request))

def author_detail(request, username):
  try:
    author = User.objects.annotate(article_count=Count('article__active')).get(username=username)
    articles = Article.objects.filter(active=True, user=author).order_by("-date_published")
    article_count = len(articles)
    current_date = datetime.date.today()
  except User.DoesNotExist:
      raise Http404
  return render_to_response("blog/author_detail.html", locals(),
                            context_instance=RequestContext(request))

def guide_list(request):
  guides = Collection.objects.filter(title_slug="xquery-unit-testing-guide", active=True)
  return render_to_response("blog/guide_list.html", locals(),
                            context_instance=RequestContext(request))

def guide_detail(request, slug):
  guide = get_object_or_404(Collection, title_slug=slug, active=True)
  articles = Article.objects.filter(collection=guide, active=True).order_by("-date_published")
  return render_to_response("blog/guide_detail.html", locals(),
                            context_instance=RequestContext(request))

def guide_article_detail(request, guide_slug, article_slug):
  article = get_object_or_404(Article, collection__title_slug=guide_slug, title_slug=article_slug, active=True)
  disqus_forum = getattr(settings, 'DISQUS_FORUM', 'rockycode')
  disqus_dev = getattr(settings, 'DISQUS_DEV', '0')
  return render_to_response("blog/guide_article_detail.html", locals(),
                            context_instance=RequestContext(request))
