from django import forms
from .forms import EmailUserCreationForm as UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from comments.models import Comment, Vote, AllApproved
from comments.models import EmailUser as User
from comments.models import EmailUser
from django.core.urlresolvers import resolve
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models, IntegrityError
from provider import scope
from provider.oauth2.views import AccessTokenView
from provider.oauth2.models import Client
import json # for sending user data as json
import requests # for GETing https://graph.facebook.com/me?access_token=...
import uuid
from django.core.cache import cache
from silk.profiling.dynamic import *

def home(request):
    return render(request, 'home.html', {'news': News.objects.all()})

def loaderio(request):
    content = 'loaderio-5b4540e24d0a6151b10967817c468dc1'
    return HttpResponse(content, content_type='text/plain')

@silk_profile()
def get_opinions(request):
    cached_opinions = cache.get('opinions')
    if cached_opinions is not None:
        return HttpResponse(cached_opinions, content_type='application/json')
    print "in get_opinions; didn't get opinions in cache"
    opinions = Comment.objects.all()
    cache.set('opinions', opinions, 100)
    return HttpResponse(opinions, content_type='text/plain')

@silk_profile()
def get_opinions_without_cache(request):
    return HttpResponse(Comment.objects.all(), content_type='text/plain')

def register_by_access_token(request, backend):
    if backend != 'facebook' and backend != 'google':
        return HttpResponse(status=400, reason='Backend ' + backend + ' not supported')
    token = request.GET.get('access_token')
    print 'token = ', token
    if backend == 'facebook':
        response = requests.get('https://graph.facebook.com/me?access_token=' + token)
    elif backend == 'google':
        response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + token)
    data_json = response.content
    data_dict = json.loads(data_json)
    print 'data_dict = ', data_dict
    if response.status_code != 200:
        # if data_dict['error']['code'] == 190 and data_dict['error']['error_subcode'] == 463:
        #     return HttpResponse(status=400, reason='Facebook token expired')
        # else:
        return HttpResponse("Invalid access token")
    # try:
    #     e = data_dict['email']
    # except KeyError:
    #     return HttpResponse(status=400, reason="Facebook access token doesn't have email permissions")
    if backend == 'facebook':
        user = EmailUser.objects.filter(source=backend, facebook_id=data_dict['id'])
    elif backend == 'google':
        user = EmailUser.objects.filter(source=backend, google_id=data_dict['id'])
    if user.exists():
        user = user[0]
    else:
        if 'email' in data_dict:
            email = data_dict['email']
        else:
            email = None
        user = EmailUser(name=data_dict['name'],
            email=email, source = backend)
        if backend == 'facebook':
            user.image_url = 'https://graph.facebook.com/v2.3/' + data_dict['id'] + '/picture'
            user.facebook_id = data_dict['id']
        elif backend == 'google':
            user.image_url = data_dict['picture']
            user.google_id = data_dict['id']
        user.save()
    cl = Client(user = user, name = 'opinion', client_type=1, url = 'http://opinion.elasticbeanstalk.com')
    cl.save()
    print 'user = ', user.email, ' ', user.name, ' ', user.facebook_id, ' ', user.google_id, ' ', user.image_url
    at = AccessTokenView().get_access_token(request, user, scope.to_int('read', 'write'), cl)
    user_data = {'token': at.token}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['email'] = user.email
    print "facebook_id = ", user.facebook_id
    user_data['image_url'] = user.image_url
    print "Serialize Issue: user_data = ", user_data
    if user:
        return HttpResponse(json.dumps(user_data), content_type="application/json")
    else:
        return HttpResponse('ERROR')

def admin_panel(request):
    opinions = Comment.objects.filter(is_approved=None).order_by('-created')
    dict = {'opinions': opinions}
    return render(request, 'admin_panel.html', dict)

@login_required
def admin_panel2(request):
    return render(request, 'opinionsPerNews.html', {})

def approve(request):
    opinion_id = request.GET['id']
    flag = request.GET['flag']
    print "in approve, opinion_id = ", "flag = ", flag
    c = Comment.objects.get(id=opinion_id)
    if flag == '1':
        c.is_approved = True
    else:
        c.is_approved = False
    c.save()
    return HttpResponse('Approved')

def allApprove(request):
    news_id = request.GET['news-id']
    flag = request.GET['flag']
    if flag == '1':
        flag = True
    else:
        flag = False
    try:
        AllApproved(news_id=news_id, all_approved=flag).save()
    except IntegrityError:
        return HttpResponse(status=409,reason='Duplicate entry for news_id: ' + news_id)
    return HttpResponse(status=201)
    # Comment.objects.filter(news_id=news_id).update(all_approved=flag) # this won't work

def loadAllNews(request):
    news = requests.post('http://crud.newsinshorts.com/app/loadAllNews')
    json = news.text[9:]
    return HttpResponse(json, content_type='application/json')

@login_required
def submit(request, url_arg):
    comment_text = request.POST.get('comment')
    n = News.objects.all().get(news_id=url_arg)
    c = Comment(uuid=uuid.uuid4(),news=n, user=request.user, text=comment_text)
    c.save()
    return HttpResponse("Thanks for your opinion! <a href='/%s'>Back</a>." % url_arg)

@login_required
def vote(request):
    context = RequestContext(request)
    if request.method == 'GET':
        id = request.GET['id']
        vote_type = request.GET['vote']
        cmt = Comment.objects.get(uuid=id)
        if cmt.votes.filter(username=request.user.username).exists():
            print "This user had already voted"
        else:
            if vote_type == '1':
                Comment.objects.filter(uuid=id).update(upvotes=cmt.upvotes+1)
            else:
                Comment.objects.filter(uuid=id).update(downvotes=cmt.downvotes+1)
            Vote.objects.create(cmt=cmt, user=request.user, vote_type=vote_type)
    return HttpResponse(str)

@login_required
def delete_comment(request):
    comment_id = request.GET['uuid']
    Comment.objects.filter(uuid=comment_id).update(is_deleted=True)
    return HttpResponse("Your comment is successfully deleted")

def edit_comment(request):
    comment_id = request.GET['id']
    content = request.GET['content']
    Comment.objects.filter(uuid=comment_id).update(text=content)
    return render(request,'home.html',{})
    return HttpResponse("Your comment is edited successfully")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponse("New user created! <a href='/'>Home</a>.")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

def login(request):
    return render(request, 'login.html', {})

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    u = User.objects.filter(source='ORP', username=username)
    if not u.exists():
        response = requests.post('http://editorpanel.newsinshorts.com/isAdmin?username=' + username + '&password=' + password)
        if response.text == 'YES':
            user = User(username=username)
            user.set_password(password)
            user.source = 'ORP'
            user.save()
        else:
            return HttpResponse("Oops. No such user. Contact Ramlal")
    user = User.objects.get(source='ORP', username=username)
    if user.check_password(password):
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)
        return HttpResponseRedirect("/loggedin/")
    else:
        return HttpResponse('Oops. Wrong password')

# def loaderio(request):
#     return HttpResponse(open('/Users/kamal/code/django/nis_comments/loaderio-60e1acefed2821f0dd26089f4126ca85.txt').read(), content_type='text/plain')

@login_required
def loggedin(request):
    return HttpResponse("You have successfully signed in! <a href='/'>Home</a>.")

def logout(request):
    auth.logout(request)
    return HttpResponse('You have successfully logged out. <a href="/">Home</a>')