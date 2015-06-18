from django import forms
from .forms import EmailUserCreationForm as UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from comments.models import News, Comment, Vote, AllApproved
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
# from django.contrib.auth.models import User as SU
import json # for sending user data as json
import requests # for GETing https://graph.facebook.com/me?access_token=...
import uuid

def home(request):
    return render(request, 'home.html', {'news': News.objects.all()})

# def news(request, url_arg):
#     c = Comment.objects.all().filter(news__news_id=url_arg, is_deleted=False)
#     n = News.objects.all().get(news_id=url_arg)
#     dict = {'news': n.text, 'cts': c, 'news_id': n.news_id}
#     return render(request, 'news.html', dict)

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

def admin_panel(request):
    # print "in admin_panel: user = ", request.user
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
    # Comment.objects.filter(news_id=news_id).update(all_approved=flag)

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

def loaderio(request):
    return HttpResponse(open('/Users/kamal/code/django/nis_comments/loaderio-60e1acefed2821f0dd26089f4126ca85.txt').read(), content_type='text/plain')

@login_required
def loggedin(request):
    return HttpResponse("You have successfully signed in! <a href='/'>Home</a>.")

def logout(request):
    auth.logout(request)
    return HttpResponse('You have successfully logged out. <a href="/">Home</a>')