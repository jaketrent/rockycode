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

@register.inclusion_tag('admin/submit_line_publish.html', takes_context=True)
def submit_row_publish(context):
  """
  Displays the row of buttons for delete and save.
  """
  opts = context['opts']
  change = context['change']
  is_popup = context['is_popup']
  save_as = context['save_as']
  original = None
  try:
    original = context['original']
  except KeyError:
    original = None
  return {
    'onclick_attrib': (opts.get_ordered_objects() and change
                       and 'onclick="submitOrderForm();"' or ''),
    'show_delete_link': (not is_popup and context['has_delete_permission']
                         and (change or context['show_delete'])),
    'show_save_as_new': not is_popup and change and save_as,
    'show_save_and_add_another': context['has_add_permission'] and
                                 not is_popup and (not save_as or context['add']),
    'show_save_and_continue': not is_popup and context['has_change_permission'],
    'is_popup': is_popup,
    'show_save': True,
    'original': original,
    'show_publish': (original and original.collection and original.collection.title_slug == "blog")
  }