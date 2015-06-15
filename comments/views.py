from django import forms
from .forms import EmailUserCreationForm as UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from comments.models import News, Comment, Vote, EmailUser
from comments.models import EmailUser as User
from django.core.urlresolvers import resolve
from django.contrib import auth
from django.contrib.auth import login
from social.apps.django_app.utils import psa
from django.contrib.auth.decorators import login_required
from provider import scope
from provider.oauth2.views import AccessTokenView
from provider.oauth2.models import Client
from social.apps.django_app.default.models import UserSocialAuth
import json # for sending user data as json
import requests # for GETing https://graph.facebook.com/me?access_token=...
import uuid

def home(request):
    return render(request, 'home.html', {'news': News.objects.all()})

def news(request, url_arg):
    c = Comment.objects.all().filter(news__news_id=url_arg, isDeleted=False)
    n = News.objects.all().get(news_id=url_arg)
    dict = {'news': n.text, 'cts': c, 'news_id': n.news_id}
    return render(request, 'news.html', dict)

def register_by_access_token(request, backend):
    token = request.GET.get('access_token')
    fb_response = requests.get('https://graph.facebook.com/me?access_token=' + token)
    if fb_response.status_code != 200:
        return HttpResponse("Invalid access token")
    data_json = fb_response.content
    data_dict = json.loads(data_json)
    user = EmailUser.objects.filter(email=data_dict['email'])
    if user.exists():
        user = user[0]
    else:
        user = EmailUser(username=data_dict['name'], name=data_dict['name'], email=data_dict['email'], facebook_id = data_dict['id'], source = 'facebook')
        user.save()
    cl = Client(user = user, name = 'opinion', client_type=1, url = 'http://opinion.elasticbeanstalk.com')
    cl.save()
    at = AccessTokenView().get_access_token(request, user, scope.to_int('read', 'write'), cl)
    user_data = {'token': at.token}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['email'] = user.email
    print "facebook_id = ", user.facebook_id
    user_data['image_url'] = 'https://graph.facebook.com/v2.3/' + user.facebook_id + '/picture?type=large'
    if user:
        return HttpResponse(json.dumps(user_data), content_type="application/json")
    else:
        return HttpResponse('ERROR')

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
    Comment.objects.filter(uuid=comment_id).update(isDeleted=True)
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
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")

def loaderio(request):
    return HttpResponse(open('/Users/kamal/code/django/nis_comments/loaderio-60e1acefed2821f0dd26089f4126ca85.txt').read(), content_type='text/plain')

@login_required
def loggedin(request):
    return HttpResponse("You have successfully signed in! <a href='/'>Home</a>.")

def logout(request):
    auth.logout(request)
    return HttpResponse('You have successfully logged out. <a href="/">Home</a>')