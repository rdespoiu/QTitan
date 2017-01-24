# Django Imports
from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth import (authenticate, get_user_model, login, logout,)
from .forms import UserLoginForm
from django.shortcuts import redirect

# Views
def index(request):
    return HttpResponse("Index placeholder")
    #return TemplateResponse(request,'index.html',{})

def login_view (request):
    title = "Login"
    print(request.user.is_authenticated())
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password= password)
        login(request, user)
        print(request.user.is_authenticated())
        #return redirect('index') #sends user to index page
        return HttpResponse("Welcome "+username)
        
    return render(request, 'index.html',{"form":form,"title":title})

def logout_view (request):
    return render(request, 'form.html',{})
