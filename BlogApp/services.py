from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, UserManager
from .models import Article, UserStatus, UserImage
from BlogServ import settings
import os

def auth(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    return user

def reg(request):
    user_form = UserRegistrationForm(request.POST)
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        userstatus = UserStatus(user=new_user, status="Hi there! It's my new Sandox page!")
        userstatus.save()
        login(request, new_user)
        return redirect("index")
    else:
        return render(request, "BlogApp/userform.html", {"err":True, "reg":True})    

def edituser(request):
    u = User.objects.get(username=request.user.username)
    u.first_name = request.POST['first_name']
    u.last_name = request.POST['last_name']
    u.save()

def renderableDict(request):
    me = request.user
    photolist = list()
    photodict = dict()
    status = ''
    try:
        status = UserStatus.manager.get(user=me).status
    except:
        pass
    try:
        photolist = UserImage.manager.filter(user=me)
        photodict.update({"myphoto":photolist[0].photo.url})
    except:
        pass
    dict1 = {"id":me.id,"username":me.username, "name":me.first_name, "surname":me.last_name,
    "status":status, "auth":True, "haveph": len(photolist)!=0}
    dict1.update(photodict)
    return dict1

def profileDict(request):
    dict1 = renderableDict(request)
    profile = request.user
    searchId = request.GET.get("id", "")
    if len(searchId)!=0:
        profile = User.objects.get(id=int(searchId))
    photolist = UserImage.manager.filter(user=profile)
    photodict = dict()
    if len(photolist)!=0:
        photodict.update({"photo":photolist[0].photo.url})
    me = request.user.id
    pstatus = ''
    try:
        pstatus = UserStatus.manager.get(user=profile).status
    except:
        pass
    bag = list(Article.manager.filter(user=profile))
    bag.reverse()
    dict2 = {"pid":profile.id, "isMy":profile.id==me, "bag":bag,
    "pusername":profile.username, "pname":profile.first_name, "psurname":profile.last_name,
    "pstatus":pstatus, "hasph": len(photolist)!=0}
    dict1.update(dict2)
    dict1.update(photodict)
    return dict1

def saveimage(request):
    if request.FILES["photo"] is None:
        return
    else:
        deleteimage(request)
        img = UserImage(user = request.user, photo = request.FILES["photo"])
        img.save()

def savepost(request):
    article = Article()
    article.user = request.user
    article.title = request.POST["title"]
    article.text = request.POST["text"]
    article.author_name = request.user.username
    article.save()

def savestatus(request):
    me = request.user
    status = UserStatus.manager.get(user=me)
    status.status = request.POST["status"]
    status.save()

def fullBag(request):
    dict1 = dict()
    if request.user.is_authenticated:
        dict1.update(profileDict(request))
        del dict1["bag"]
    bag = list(Article.manager.all())
    bag.reverse()
    dict1.update({"bag": bag})
    return dict1

def editUserDict(request, r):
    dict1 = {"reg":r}
    if not r:
        u = request.user
        dict1.update({"username":u.username, "name":u.first_name, "surname":u.last_name, "email":u.email})
    return dict1

def for_note_edit_dict(request):
    dict1 = renderableDict(request)
    searchId = request.GET.get("noteId", "")
    note = Article.manager.get(id=searchId)
    dict1.update({"title":note.title, "text":note.text})
    return dict1

def edit_note(request):
    searchId = request.GET.get("noteId", "")
    note = Article.manager.get(id=searchId)
    note.title = request.POST["title"]
    note.text = request.POST["text"]
    note.save()

def deleteimage(request):
    photolist = UserImage.manager.filter(user=request.user)
    if len(photolist)!=0:
        os.remove(photolist[0].photo.path)
        photolist[0].delete()