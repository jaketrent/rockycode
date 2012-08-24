from django.conf.urls.defaults import *

urlpatterns = patterns('rockycode.tagging_autocomplete.views',
    url(r'^json$', 'list_tags', name='tagging_autocomplete-list'),
)
