from django.shortcuts import render
from comments.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from comments.models import News, User, Comment
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
    print "in views.news; cookies = ", request.COOKIES
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
    c = Comment(uuid=uuid.uuid4(),news=n, user=request.user, text=comment_text)
    print "c.uuid = ", c.uuid, " c.text = ", c.text
    c.save()
    return HttpResponse("Thanks for your opinion! <a href='/%s'>Back</a>." % url_arg)

@login_required
def like_category(request):
    print "got a like"
    context = RequestContext(request)
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        id = request.GET['id']
        c = Comment.objects.get(uuid=id)
        print 'id in like = ', id, " & comment text = ", c.text, " upvotes = ", c.upvotes
        Comment.objects.filter(uuid=id).update(upvotes=c.upvotes+1)
        # Comment.objects.get(uuid=id).upvote_table.add(User.objects.)
        print "upvotes = ", c.upvotes

    likes = 0
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        if category:
            likes = category.likes + 1
            category.likes = likes
            category.save()

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