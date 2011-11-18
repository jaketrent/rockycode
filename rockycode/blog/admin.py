from django.contrib import admin
from django.contrib.auth.models import User
from blog.models import Article, Collection, Template

class ArticleAdmin(admin.ModelAdmin):
  list_display = ['title', 'id', 'date_published', 'date_created', 'date_updated', 'active', 'tags']
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

admin.site.register(Article, ArticleAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Template, TemplateAdmin)