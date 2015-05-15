from django.db import models
from django.contrib.auth.models import User
import uuid

class News(models.Model):
    news_id = models.CharField(max_length=1000,null=True)
    author = models.CharField(max_length=100, null=True)
    text = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return self.news_id

class Comment(models.Model):
    uuid = models.CharField(max_length=40, default='random')
    news = models.ForeignKey(News)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=300, null=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    votes = models.ManyToManyField(User, through='Vote', related_name='votes_table', default=None)

    def __unicode__(self):
        return self.text

class Vote(models.Model):
    cmt = models.ForeignKey(Comment)
    user = models.ForeignKey(User)
    vote_type = models.SmallIntegerField(default=0) # vote_type is +1 for upvote & -1 for downvote