from django.contrib import admin
from core.models import Keyword,ContentItem,Flag
# Register your models here.

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display=('id','name')

@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display=('id','title','source','last_updated')
    search_fields=('title','source')

@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display=('id','keyword','content_item','score','status','created_at')
    list_filter=('status','keyword')