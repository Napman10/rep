from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import login, logout, authenticate
from .services import auth, reg, profileDict, savepost, fullBag, deleteimage, editUserDict, edituser, renderableDict, savestatus, for_note_edit_dict, saveimage, edit_note
from django.template.response import TemplateResponse
from .models import Article

def index(request):
    return render(request, "BlogApp/index.html", fullBag(request))

def log_in(request):
    if request.method == "POST":
        user = auth(request)
        if user is not None:
            login(request, user)
            return HttpResponsePermanentRedirect("index")
        else:
            return render(request, "BlogApp/login.html", {"err":True})
    else:
        return render(request, "BlogApp/login.html", {"err":False})

def log_out(request):
    logout(request)
    return redirect("index")

def user_fill(request, r=True):
    if request.method == "POST":
        if r:
            return reg(request)
        else:
            edituser(request)
            return redirect("index")     
    else:      
        return render(request, "BlogApp/userform.html", editUserDict(request, r))

def editme(request):
    return user_fill(request, False)

def profile(request):
    if request.user.is_authenticated:
        return render(request, "BlogApp/profile.html", profileDict(request))
    else:
        return redirect("login")

def writenote(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            savepost(request)
            return redirect('index')
        else:
            return render(request, "BlogApp/writepost.html", renderableDict(request))
    else:
        return redirect("login")

def editstatus(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            savestatus(request)
            return redirect("index")
        else:
            return render(request, "BlogApp/editstatus.html", renderableDict(request))
    else:
        return redirect("login")

def editnote(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            edit_note(request)
            return redirect('index')
        else:
            return render(request, "BlogApp/writepost.html", for_note_edit_dict(request))
    else:
        return redirect("login")

def deletenote(request):
    noteId = request.GET.get("noteId", "")
    note = Article.manager.get(id=noteId)
    if request.user == note.user:
        note.delete()
        return redirect('index')
    else:
        return HttpResponse("err")

def editimage(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            saveimage(request)
            return redirect("index")
        else:
            return render(request, "BlogApp/changeimage.html", renderableDict(request))
    else:
        return redirect("login")

def delimage(request):
    if request.user.is_authenticated:
        deleteimage(request)
        return redirect("index")
    else:
        return redirect("login")

# Create your views here.
