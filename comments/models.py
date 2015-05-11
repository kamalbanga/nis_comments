from django.db import models
from django.forms import ModelForm
import uuid

class User(models.Model):
    name = models.CharField(max_length=100,null=True)
    user_id = models.CharField(max_length=100,null=True)

    def __unicode__(self):
        return self.user_id

class News(models.Model):
    news_id = models.CharField(max_length=1000,null=True)
    author = models.CharField(max_length=100, null=True)
    text = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return self.news_id

class Comment(models.Model):
    uuid = models.CharField(max_length=40, default='random')
    news = models.ForeignKey('News')
    user = models.OneToOneField('User', primary_key=True) # ForeignKey('User')
    text = models.CharField(max_length=300, null=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    upvote_table = models.ManyToManyField(User, related_name = 'upvote',)
    downvote_table = models.ManyToManyField(User, related_name = 'downvote',)

    def __unicode__(self):
        return self.text

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'text']
