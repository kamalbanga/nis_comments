from django.db import models
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

def unique_id():
    return str(uuid.uuid4())

class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', max_length=255, null=True)
    username = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    image_url = models.URLField(null=True)
    source = models.CharField(max_length=20, null=True) # facebook, google, nis ...
    id = models.CharField(max_length=40, primary_key=True, default=unique_id)
    facebook_id = models.CharField(max_length=40, null=True)
    google_id = models.CharField(max_length=40, null=True)
    is_staff = models.BooleanField('staff status', default=False, help_text=
        'Designates whether the use can log into this admin site.')
    is_active = models.BooleanField('active', default=True, help_text='Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    follow_count = models.PositiveIntegerField(default=0) # no. of people this creep is stalking
    followed_count = models.PositiveIntegerField(default=0) # no. of people following this stud

    objects = EmailUserManager()
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = True

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

class EmailUser(AbstractEmailUser):

    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'

class AllApproved(models.Model):
    news_id = models.CharField(unique=True, max_length=200, null=True)
    all_approved = models.BooleanField()

    def __unicode__(self):
        if self.all_approved == True:
            string = 'Approved'
        else:
            string = 'Rejected'
        return 'All ' + string + ' on ' + self.news_id

class Comment(models.Model):
    uuid = models.CharField(max_length=40, default=uuid.uuid4)
    news_id = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(EmailUser)
    text = models.CharField(max_length=300, null=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    votes = models.ManyToManyField(EmailUser, through='Vote', related_name='votes_table', blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_edit = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_approved = models.NullBooleanField()

    def __unicode__(self):
        return self.text

    class Meta:
        unique_together = ('news_id', 'user')

class Edit(models.Model):
    cmt = models.ForeignKey(Comment)
    old_text = models.CharField(max_length=1000,null=False)
    new_text = models.CharField(max_length=1000,null=False)
    edit_ts = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # userid = models.ForeignKey(User) # person who edited the opinion

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

    class Meta:
        unique_together = ('comment', 'user')

class Follow(models.Model):
    follower = models.ForeignKey(EmailUser, related_name='follower', null=True, blank=True)
    followed = models.ForeignKey(EmailUser, related_name='followed', null=True, blank=True)

    def __unicode__(self):
        return self.follower.email + "->" + self.followed.email