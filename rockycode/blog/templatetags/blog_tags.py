from django import template
from django.template.defaultfilters import stringfilter
from django.template import loader
register = template.Library()
from blog.models import Article
from django.template.defaultfilters import stringfilter

@register.simple_tag
def list_template(article):
	return loader.render_to_string(article.collection.template.list_path, {'object': article})

@register.simple_tag
def detail_template(article):
	return loader.render_to_string(article.collection.template.detail_path, {'object': article})
