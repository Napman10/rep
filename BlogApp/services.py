from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Article, UserStatus, UserImage
from BlogServ import settings
import os

def auth(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    return user

def cmpr_password(request):
    p1 = request.POST['password']
    p2 = request.POST['confirm_password']
    return p1 == p2

def reg(request):
    user_form = UserRegistrationForm(request.POST)
    if user_form.is_valid() and cmpr_password(request):
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
    return redirect("index")

def renderableDict(request):
    me = request.user
    photodict = dict()
    status = ''
    try:
        status = UserStatus.manager.get(user=me).status
    except:
        pass
    try:
        photodict.update({"myphoto":UserImage.manager.filter(user=me)[0].photo.url})
    except:
        pass
    dict1 = {"id":me.id,"username":me.username, "name":me.first_name, "surname":me.last_name,
    "status":status, "auth":True, "haveph": "myphoto" in photodict}
    dict1.update(photodict)
    return dict1

def profileDict(request):
    dict1 = renderableDict(request)
    profile = request.user
    searchId = request.GET.get("id", "")
    if len(searchId)!=0:
        profile = User.objects.get(id=int(searchId))
    photodict = dict()
    try:
        photodict.update({"photo":UserImage.manager.filter(user=profile)[0].photo.url})
    except:
        pass
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
    "pstatus":pstatus, "hasph": "photo" in photodict}
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

def deleteself(request):
    id = request.user.id
    deleteimage(request)
    logout(request)
    user = User.objects.get(id=id)
    user.delete()

def set_psswrd(request):
    user = request.user
    if user.check_password(request.POST["current_password"]) and cmpr_password(request):
        user.set_password(request.POST["password"])
        user.save()
        login(request, user)
        return redirect('index')
    else:
        dict1 = renderableDict(request)
        dict1.update({"err":True})
        return render(request, "BlogApp/setpassword.html", dict1)
