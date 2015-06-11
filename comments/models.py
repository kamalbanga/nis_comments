from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
import uuid

class EmailUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        is_active = extra_fields.pop("is_active", True)
        user = self.model(email=email, is_staff=is_staff, is_active=is_active, 
            is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(email, password, is_staff, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', max_length=255, unique=True, db_index=True)
    is_staff = models.BooleanField('staff status', default=False, help_text=
        'Designates whether the use can log into this admin site.')
    is_active = models.BooleanField('active', default=True, help_text='Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = EmailUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = True

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

class EmailUser(AbstractEmailUser):

    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'

class News(models.Model):
    news_id = models.CharField(max_length=1000,null=True)
    author = models.CharField(max_length=100, null=True)
    text = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return self.news_id

class Comment(models.Model):
    uuid = models.CharField(max_length=40, default=uuid.uuid4)
    news = models.ForeignKey(News)
    user = models.ForeignKey(EmailUser)
    text = models.CharField(max_length=300, null=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    isDeleted = models.BooleanField(default=False)
    votes = models.ManyToManyField(EmailUser, through='Vote', related_name='votes_table', blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_edit = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __unicode__(self):
        return self.text

    class Meta:
        unique_together = ('news', 'user')

class Edit(models.Model):
    # editid = models.CharField(max_length=40,default='random')
    # edit_type = models.CharField(max_length=40,null=False)
    # edit_subtype = models.CharField(max_length=40,null=False)
    cmt = models.ForeignKey(Comment)
    # gen_id = models.CharField(max_length=40,null=False)
    old_text = models.CharField(max_length=1000,null=False)
    new_text = models.CharField(max_length=1000,null=False)
    edit_ts = models.DateTimeField(auto_now_add=True, blank=True, null=True)
 #todo:   edit_time = timestamp field
    # userid = models.ForeignKey(User)

class Vote(models.Model):
    comment = models.ForeignKey(Comment, null=True, blank=True, default=None)
    user = models.ForeignKey(EmailUser, null=True, blank=True, default=None)
    vote_type = models.SmallIntegerField(default=0) # vote_type is +1 for upvote & -1 for downvote
    ts = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __unicode__(self):
        if self.vote_type == 1:
            vote_type_str = '+1'
        else:
            vote_type_str = '-1'
        return vote_type_str + " by " + self.user.email + " on " + self.Comment.text

class Follow(models.Model):
    follower = models.ForeignKey(EmailUser, related_name='follower', null=True, blank=True)
    followed = models.ForeignKey(EmailUser, related_name='followed', null=True, blank=True)

    def __unicode__(self):
        return self.follower.email + "->" + self.followed.email