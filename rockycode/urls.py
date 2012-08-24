from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rockycode.blog.models import ArticleSitemap
from rockycode import settings

from django.contrib import admin
admin.autodiscover()

sitemaps = {
  'articles': ArticleSitemap,
}

urlpatterns = patterns('',
    (r'^', include('rockycode.blog.urls')),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '%simages/favicon.ico' % settings.STATIC_URL}),
    (r'^tagging_autocomplete/', include('rockycode.tagging_autocomplete.urls')),
    (r'^profile/', include('profiles.urls'), {'success_url': '/profile/edit/'}),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name="sitemap"),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG is False:
  urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
  )