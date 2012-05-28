from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from blog.models import Article, Collection, Template
from django.contrib.contenttypes.models import ContentType
from django.db import models
from blog.widgets import EpicEditor
from settings import STATIC_URL
from django.utils.translation import ugettext_lazy as _
from rockycode.blog.models import Profile

BODY_HELP = _("""
<style>
  #id_body { display: none; }
  #epiceditor {
    min-width: 400px;
    max-width: 620px;
    height: 400px;
    margin: -7px 0 0 105px;
  }
</style>
<div id='epiceditor'></div>
<script>
django.jQuery(function () {
  var editor = new EpicEditor(django.jQuery('#epiceditor')[0]);
  editor.options({
    basePath: '%s/epiceditor'
  });
  editor.load();
  editor.get('editor').value = django.jQuery('#id_body').val();

  django.jQuery('.submit-row input[type=submit]').click(function () {
    django.jQuery('#id_body').val(editor.get('editor').value);
    editor.remove('epiceditor');
  });

});
</script>

""")

class ArticleForm(forms.ModelForm):
  body = forms.CharField(widget=EpicEditor(), help_text=(BODY_HELP % STATIC_URL))

  class Meta:
    model = Article

class ArticleAdmin(admin.ModelAdmin):
  form = ArticleForm
  list_display = ['title', 'id', 'date_published', 'active', 'tags']
  prepopulated_fields = {'title_slug': ('title',)}
  search_fields = ['title','summary','body']
  date_hierarchy = 'date_published'
  list_editable = ('tags',)
  fieldsets = (
    (None, {
        'classes': ('',),
        'fields': ('title', 'title_slug', 'summary', 'body')
    }),
    ('', {
        'classes': ('',),
        'fields': ('markup', 'collection', 'user', 'tags' ,'date_published')
    }),
    ('Other', {
        'classes': ('',),
  #        'fields': ('demo', 'source', 'source_path', 'image_path', 'active')
        'fields': ('demo', 'source', 'source_path', 'image_path', 'active')
    }),

  )

  def save_model(self, request, obj, form, change):
    """Set the article's author based on the logged in user and make sure at least one site is selected"""
    try:
      user = obj.user
    except User.DoesNotExist:
      obj.user = request.user
    obj.save()

  def queryset(self, request):
    """Limit the list of articles to article posted by this user unless they're a superuser"""
    if request.user.is_superuser:
      return self.model._default_manager.all()
    else:
      return self.model._default_manager.filter(user=request.user)


class CollectionAdmin(admin.ModelAdmin):
	list_display = ['title', 'id', 'date_created', 'date_updated', 'active']
	prepopulated_fields = {'title_slug': ('title',)}

class TemplateAdmin(admin.ModelAdmin):
	list_display = ['title', 'id', 'date_created', 'date_updated', 'active']
	prepopulated_fields = {'title_slug': ('title',)}

class ContentTypeAdmin(admin.ModelAdmin):
  list_display = ['name', 'app_label']
  fieldsets = (
    ('', {
      'classes': ('',),
      'fields': ('name', 'app_label')
    }),
  )

class ProfileAdmin(admin.ModelAdmin):
  pass



admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Profile, ProfileAdmin)