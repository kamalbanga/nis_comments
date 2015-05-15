from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from comments.models import News, Comment, Vote
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import uuid

def home(request):
    return render(request, 'home.html', {'news': News.objects.all()})

def news(request, url_arg):
    c = Comment.objects.all().filter(news__news_id=url_arg)
    n = News.objects.all().get(news_id=url_arg)
    dict = {'news': n.text, 'cts': c, 'news_id': n.news_id}
    return render(request, 'news.html', dict)

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

def loggedin(request):
    print "Is user authenticated?, bool = ", request.user.is_authenticated()
    return HttpResponse("You have successfully signed in! <a href='/'>Home</a>.")

def logout(request):
    auth.logout(request)
    return HttpResponse('You have successfully logged out. <a href="/">Home</a>')