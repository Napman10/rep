from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import login, logout, authenticate
from .services import set_psswrd, auth, reg, profileDict, savepost, fullBag, deleteimage, deleteself, editUserDict, edituser, renderableDict, savestatus, for_note_edit_dict, saveimage, edit_note
from .models import Article
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "BlogApp/index.html", fullBag(request))

def log_in(request):
    if request.method == "POST":
        user = auth(request)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "BlogApp/login.html", {"err":True})
    else:
        return render(request, "BlogApp/login.html", {"err":False})

@login_required
def log_out(request):
    logout(request)
    return redirect("index")

def user_fill(request, r=True):
    if request.method == "POST":
        if r:
            reg(request)
        else:
            edituser(request)
        return redirect("index")     
    else:      
        return render(request, "BlogApp/userform.html", editUserDict(request, r))

def editme(request):
    return user_fill(request, False)

@login_required
def profile(request):
    return render(request, "BlogApp/profile.html", profileDict(request))

@login_required
def writenote(request):
    if request.method == "POST":
        savepost(request)
        return redirect('index')
    else:
        return render(request, "BlogApp/writepost.html", renderableDict(request))

@login_required
def editstatus(request):
    if request.method == "POST":
        savestatus(request)
        return redirect("index")
    else:
        return render(request, "BlogApp/editstatus.html", renderableDict(request))

@login_required
def editnote(request):
    if request.method == "POST":
        edit_note(request)
        return redirect('index')
    else:
        return render(request, "BlogApp/writepost.html", for_note_edit_dict(request))

@login_required
def deletenote(request):
    noteId = request.GET.get("noteId", "")
    note = Article.manager.get(id=noteId)
    if request.user == note.user:
        note.delete()
    return redirect('index')


@login_required
def editimage(request):
    if request.method == "POST":
        saveimage(request)
        return redirect("index")
    else:
        return render(request, "BlogApp/changeimage.html", renderableDict(request))

@login_required
def delimage(request):
    deleteimage(request)
    return redirect("index")

@login_required
def delself(request):
    deleteself(request)
    return redirect("index")

@login_required
def setpassword(request):
    if request.method == "POST":
        return set_psswrd(request)
    else:
        return render(request, "BlogApp/setpassword.html", renderableDict(request))
# Create your views here.
