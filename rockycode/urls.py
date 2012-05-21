from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blog.models import ArticleSitemap
from settings import STATIC_URL

from django.contrib import admin
admin.autodiscover()

sitemaps = {
  'articles': ArticleSitemap,
}

urlpatterns = patterns('',
    (r'^', include('blog.urls')),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '%simages/favicon.ico' % STATIC_URL}),
    (r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    (r'^profile/', include('profiles.urls'), {'success_url': '/profile/edit/'}),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    # Examples:
    # url(r'^$', 'rockycode.views.home', name='home'),
    # url(r'^rockycode/', include('rockycode.foo.urls')),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name="sitemap"),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()