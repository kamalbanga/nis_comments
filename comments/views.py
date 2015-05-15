from django.shortcuts import render
from comments.models import User
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
    # n = News.objects.all()
    # c = Context({'news': n})
    # t = loader.get_template('home.html')
    # return HttpResponse(t.render(RequestContext(request, c)))

def news(request, url_arg):
    c = Comment.objects.all().filter(news__news_id=url_arg)
    n = News.objects.all().get(news_id=url_arg)
    dict = {'news': n.text, 'cts': c, 'news_id': n.news_id}
    return render(request, 'news.html', dict)
    # rc = RequestContext(request, cont)
    # t = loader.get_template('news.html')
    # return HttpResponse(t.render(rc))
    # return render(request, 'news.html', context_dict, context_instance=RequestContext(request))

@login_required
def submit(request, url_arg):
    user_id = request.POST.get('user_id')
    comment_text = request.POST.get('comment')
    print "news_id =", url_arg, "user_id = ", user_id, "comment_text = ", comment_text
    n = News.objects.all().get(news_id=url_arg)
    # u = User(name='random',user_id=user_id)
    # u.save()
    id = 'cb77109d-31a5-48ad-84cc-e378237636f4'
    # print "test4 = ", Comment.objects.get(uuid=id)
    c = Comment(uuid=uuid.uuid4(),news=n, user=request.user, text=comment_text)
    # print "test4 = ", Comment.objects.get(uuid=id)
    # print "c.uuid = ", c.uuid, " c.text = ", c.text, "c.upvotes = ", c.upvotes, " c.votes.exists() = ", c.votes.get(username=request.user.username)
    c.save()
    # print "test4 = ", Comment.objects.get(uuid=id)
    return HttpResponse("Thanks for your opinion! <a href='/%s'>Back</a>." % url_arg)

@login_required
def vote(request):
    print "got a vote. Yay!"
    context = RequestContext(request)
    if request.method == 'GET':
        id = request.GET['id']
        vote_type = request.GET['vote']
        cmt = Comment.objects.get(uuid=id)
        print "vote_type = ", vote_type, " & vote_type == 1 = ", vote_type == 1, " & vote_type == '1' = ", vote_type == '1'
        print "cmt = ", cmt.text, " cmt.upvotes = ", cmt.upvotes
        print "exists? = ", cmt.votes.filter(username=request.user.username).exists()
        # ci = cmt.votes.filter(username=request.user.username)[0]
        # print "ci.text = ", ci.text, " upvotes = ", ci.upvotes
        if cmt.votes.filter(username=request.user.username).exists():
            print "This user has already voted"
        else:
            print "In first else stmt"
            if vote_type == '1':
                print "in within if & vote_type == 1 is ", vote_type == '1'
                Comment.objects.filter(uuid=id).update(upvotes=cmt.upvotes+1)
            else:
                print "in else, vote_type == 1", vote_type == 1
                Comment.objects.filter(uuid=id).update(downvotes=cmt.downvotes+1)
            Vote.objects.create(cmt=cmt, user=request.user, vote_type=vote_type)
    return HttpResponse(likes)

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