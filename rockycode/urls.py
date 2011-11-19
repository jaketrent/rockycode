from django.conf.urls.defaults import patterns, include, url
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('blog.urls')),
    (r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    (r'^profile/', include('profiles.urls'), {'success_url': '/authors/'}),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    # Examples:
    # url(r'^$', 'rockycode.views.home', name='home'),
    # url(r'^rockycode/', include('rockycode.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

#urlpatterns += staticfiles_urlpatterns()