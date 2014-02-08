from django.contrib import admin

from snl.models import Article
from snl.models import Author
from snl.models import Image

class ImageInline(admin.StackedInline):
    model = Image

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at', 'changed_at')
    inlines = (ImageInline,)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Image)
