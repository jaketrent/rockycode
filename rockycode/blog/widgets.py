from django.forms.widgets import Textarea
from settings import STATIC_URL

class EpicEditor(Textarea):
  class Media:
    js = (
      'scripts/epiceditor.js',
      )
    css = {
      'screen': (
        '%sepiceditor/themes/editor/epic-light.css' % STATIC_URL,
        '%sepiceditor/themes/preview/github.css' % STATIC_URL,
        '%sepiceditor/themes/preview/preview-dark.css' % STATIC_URL,
      )
    }

