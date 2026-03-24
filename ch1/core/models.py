from django.db import models

class Keyword(models.Model):
    name=models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name

class ContentItem(models.Model):
    title=models.CharField(max_length=500)
    source=models.CharField(max_length=500)
    body=models.TextField()
    last_updated=models.DateTimeField()

    def __str__(self):
        return self.title
    
class Flag(models.Model):
    STATUS_CHOICES =[
        ('pending','Pending'),
        ('relevant','Relevant'),
        ('irrelevant','Irrelevant'),
    ]

    keyword= models.ForeignKey(Keyword,on_delete=models.CASCADE,related_name='flag')
    content_item = models.ForeignKey(ContentItem,on_delete=models.CASCADE,related_name='flag')
    score=models.IntegerField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"[{self.status.upper()}] {self.keyword.name} -> {self.content_item.title}"

# Create your models here.
