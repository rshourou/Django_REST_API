from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse ("users:login"))
    return  render (request, "users/user.html")

def login_view(request):
    username=request.POST["username"]
    password=request.POST["password"]
    user=authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("users:index"))
    else:
        return render (request, "users/login.html", {"message": "Invalid credentials."})


def logout_view(request):
   logout(request)
   return render (reqeust, "users/login.html", {"message": "Logged out."})
