from django.forms.widgets import Input
from django.conf import settings
from django.utils.safestring import mark_safe

class EpicEditor(Input):
  input_type = 'input'

  def render(self, name, value, attrs=None):
    html = super(EpicEditor, self).render(name, value, attrs)
    js = u"<script type='text/javascript'>var element = document.getElementById(%s);var editor = new EpicEditor(element).load();</script>" % (attrs['id'])
    return mark_safe("\n".join([html, js]))

  class Media:
    js_base_url = getattr(settings, 'EPIC_EDITOR_JS_BASE_URL','%s/epiceditor' % settings.MEDIA_URL)
    css = {
      'all': ('%s/jquery.autocomplete.css' % js_base_url,)
    }
    js = (
      '%s/epiceditor.js' % js_base_url,
      )

