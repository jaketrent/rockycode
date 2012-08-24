from datetime import datetime
from tagging.fields import TagField
import os, tagging
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
#from rockycode.tagging_autocomplete.models import TagAutocompleteField
from rockycode import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.markup.templatetags import markup
from django.utils.html import linebreaks
from rockycode.blog.code import rendercode
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.contrib.admin.widgets import AdminTextareaWidget

MARKUP_HTML = 'h'
MARKUP_REST = 'r'
MARKUP_MARKDOWN = 'm'
#MARKUP_TEXTILE = 't'
MARKUP_OPTIONS = getattr(settings, 'ARTICLE_MARKUP_OPTIONS', (
        (MARKUP_HTML, _('HTML/Plain Text')),
        (MARKUP_REST, _('ReStructured Text')),
        (MARKUP_MARKDOWN, _('Markdown')),
#        (MARKUP_TEXTILE, _('Textile'))
    ))
MARKUP_DEFAULT = getattr(settings, 'ARTICLE_MARKUP_DEFAULT', MARKUP_MARKDOWN)
MARKUP_HELP = _("""Select the type of markup you are using in this article.
<ul>
<li><a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target="_blank">ReStructured Text Guide</a></li>
<li><a href="http://daringfireball.net/projects/markdown/basics" target="_blank">Markdown Guide</a></li>
<li><a href="http://www.freewisdom.org/projects/python-markdown/CodeHilite">Markdown Codeblocks Help</a></li>
</ul>""")
BODY_HELP = "query, <span id='epiceditor'>asdf</span>"
#<li><a href="http://daringfireball.net/projects/markdown/basics" target="_blank">Markdown Guide</a></li>
#<li><a href="http://thresholdstate.com/articles/4312/the-textile-reference-manual" target="_blank">Textile Guide</a></li>

class Template(models.Model):
	title = models.CharField(max_length=250)
	title_slug = models.SlugField(unique=True)
	list_path = models.FilePathField(path=os.path.join(settings.PROJ_PATH, "templates/collections/"), match=".*\.html$", recursive=True)
	detail_path = models.FilePathField(path=os.path.join(settings.PROJ_PATH, "templates/collections/"), match=".*\.html$", recursive=True)
	date_created = models.DateTimeField(editable=False, auto_now_add=True)
	date_updated = models.DateTimeField(editable=False, auto_now=True)
	active = models.BooleanField(default=True)
	class Meta:
		ordering = ["title"]
	def __unicode__(self):
		return u'%s' % (self.title)

class Collection(models.Model):
	title = models.CharField(max_length=250)
	title_slug = models.SlugField(unique=True)
	description = models.TextField(max_length=10000, blank=True, null=True)
	template = models.ForeignKey(Template)
	date_created = models.DateTimeField(editable=False, auto_now_add=True)
	date_updated = models.DateTimeField(editable=False, auto_now=True)
	active = models.BooleanField(default=True)
	fake_sort = models.IntegerField(blank=True, null=True, default=100)
	class Meta:
		ordering = ["title"]
	def __unicode__(self):
		return u'%s' % (self.title)

class Article(models.Model):
  title = models.CharField(max_length=250)
  title_slug = models.SlugField(unique=True)
  summary = models.TextField(max_length=1000, blank=True, null=True)
  body = models.TextField(blank=True, null=True)
  rendered_body = models.TextField(blank=True, null=True)
  markup = models.CharField(max_length=1, choices=MARKUP_OPTIONS, default=MARKUP_DEFAULT, help_text=MARKUP_HELP)
  collection = models.ForeignKey(Collection)
  image_path = models.CharField(max_length=500, blank=True, null=True)
  demo = models.CharField(max_length=500, null=True, blank=True)
  source = models.FileField(upload_to='uploads/blog/source/', null=True, blank=True)
  source_path = models.CharField(max_length=500, null=True, blank=True)
  user = models.ForeignKey(User, help_text='This should be you.')
  tags = TagField(help_text='Separate tags with spaces, put quotes around multiple-word tags.', blank=True, null=True)
  date_published = models.DateTimeField(default=datetime.now)
  date_created = models.DateTimeField(editable=False, auto_now_add=True)
  date_updated = models.DateTimeField(editable=False, auto_now=True)
  active = models.BooleanField(default=False)

  class Meta:
    ordering = ["title"]

  def __unicode__(self):
    return u'%s' % (self.title)

  def get_absolute_url(self):
    return reverse('article_detail', args=[self.title_slug])

  def get_url(self):
    protocol = getattr(settings, "PROTOCOL", "http")
    domain = Site.objects.get_current().domain
    port = getattr(settings, "PORT", "")
    path = self.get_absolute_url()
    if port:
      assert port.startswith(":"), "The PORT setting must have a preceeding ':'."
    return "%s://%s%s%s" % (protocol, domain, port, path)
    get_url.dont_recurse = True

  def save(self, *args, **kwargs):
    """
    Renders the article using the appropriate markup language.
    """
    if self.markup == MARKUP_REST:
      self.rendered_body = markup.restructuredtext(self.body)
    elif self.markup == MARKUP_MARKDOWN:
      self.rendered_body = markup.markdown(self.body, "codehilite")
#    elif self.markup == MARKUP_TEXTILE:
#      self.rendered_body = markup.textile(self.body)
    else:
      self.rendered_body = self.body

    super(Article, self).save(*args, **kwargs)

  def get_rendered_body(self):
    if self.markup != MARKUP_HTML:
      return self.rendered_body
    else:
      return rendercode(self.rendered_body)


class Profile(models.Model):
  #essential 
  user = models.ForeignKey(User, unique=True)
  image_path = models.CharField(max_length=500, null=True, blank=True)
  bio = models.TextField(max_length=1000)

  #meta
  location = models.CharField(max_length=150, blank=True, null=True)

  #social
  website = models.CharField(max_length=250, blank=True, null=True)
  linkedin = models.CharField(max_length=250, blank=True, null=True)
  twitter = models.CharField(max_length=250, blank=True, null=True)
  google_chatback = models.CharField(max_length=1000, blank=True, null=True)

  def __unicode__(self):
    return u'%s' % (self.user)

  def get_absolute_url(self):
    return ('profiles_profile_detail', (), { 'username': self.user.username })
  get_absolute_url = models.permalink(get_absolute_url)


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Article.objects.filter(active=True).order_by("-date_published")

    def lastmod(self, obj):
        return obj.date_updated
