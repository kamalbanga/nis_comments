# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import uuid
import comments.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, null=True, verbose_name=b'email address')),
                ('username', models.CharField(max_length=100, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('image_url', models.URLField(null=True)),
                ('source', models.CharField(max_length=20, null=True)),
                ('id', models.CharField(default=comments.models.unique_id, max_length=40, serialize=False, primary_key=True)),
                ('facebook_id', models.CharField(max_length=40, null=True)),
                ('google_id', models.CharField(max_length=40, null=True)),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the use can log into this admin site.', verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date joined')),
                ('follow_count', models.PositiveIntegerField(default=0)),
                ('followed_count', models.PositiveIntegerField(default=0)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AllApproved',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('news_id', models.CharField(max_length=200, unique=True, null=True)),
                ('all_approved', models.BooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=40)),
                ('news_id', models.CharField(max_length=100, null=True)),
                ('text', models.CharField(max_length=300, null=True)),
                ('upvotes', models.PositiveIntegerField(default=0)),
                ('downvotes', models.PositiveIntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_edit', models.DateTimeField(auto_now=True, null=True)),
                ('is_approved', models.NullBooleanField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Edit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('old_text', models.CharField(max_length=1000)),
                ('new_text', models.CharField(max_length=1000)),
                ('edit_ts', models.DateTimeField(auto_now_add=True, null=True)),
                ('cmt', models.ForeignKey(to='comments.Comment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('followed', models.ForeignKey(related_name=b'followed', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('follower', models.ForeignKey(related_name=b'follower', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote_type', models.SmallIntegerField(default=0)),
                ('ts', models.DateTimeField(auto_now_add=True, null=True)),
                ('comment', models.ForeignKey(default=None, blank=True, to='comments.Comment', null=True)),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('comment', 'user')]),
        ),
        migrations.AddField(
            model_name='comment',
            name='votes',
            field=models.ManyToManyField(default=None, related_name=b'votes_table', through='comments.Vote', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('news_id', 'user')]),
        ),
    ]
