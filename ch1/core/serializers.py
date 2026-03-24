from rest_framework import serializers
from core.models import Keyword,ContentItem,Flag

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model=Keyword
        fields=['id','name']

class FlagSerializer(serializers.ModelSerializer):
    keyword_name=serializers.CharField(source='keyword.name',read_only=True)
    content_title=serializers.CharField(source='content_item.title',read_only=True)
    class Meta:
        model=Flag
        fields=['id','keyword','keyword_name','content_item', 'content_title','score','status','created_at']
        read_only_fields=['keyword','content_item','score','created_at']