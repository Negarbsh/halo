from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm, HackerCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetCompleteView
from hacker.models import hacker
from organizer.models import organizer
from .helper import add_group, decide_redirect
from .emailer import *


def landing(request):

    context = {}
    return render(request, 'defaults/landing.html', context)


def register_hacker(request):
    if request.method == 'POST':
        user = CustomUserCreationForm(request.POST)
        hacker = HackerCreationForm(request.POST)

        # print("in thingy")
        
        if hacker.is_valid() and user.is_valid():
            pword = user.cleaned_data['password1']
            user = user.save()

            hacker = hacker.save(commit=False)
            hacker.hacker = user
            hacker.save()
            add_group(user, 'hacker')

            user = authenticate(request, username=user.email, password=pword)
            if user is not None:
                login(request, user)
                return redirect('hacker-dash')
        else:
            print('fail')
    else:
        user = CustomUserCreationForm()
        hacker = HackerCreationForm()
        print(hacker)
    context = {'hacker': hacker, 'user': user}
    return render(request, 'defaults/register.html', context)


def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pword = request.POST.get('password')

        user = authenticate(request, email=email, password=pword)

        if user is not None:
            print(user)
            login(request, user)

            return redirect(decide_redirect(user))
        else:
            HttpResponse("Username or Password Incorrect")

    context = {}
    return render(request, 'defaults/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('landing')
