from django.shortcuts import render
from signUps.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from signUps.models import Accounts
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request,'index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            name = user.first_name + " " + user.last_name
            a = Accounts()
            a.email = user.email
            a.username = user.username
            a.name = name
            a.user = user
            a.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})

@login_required
def profile(request):
    user = request.user
    profile_objs = Accounts.objects.get(user_id = user.id)
    context = {
        "profile": profile_objs,
    }
    return render(request, "profile.html", context)

@login_required
def editProfile(request):
    if request.method == 'POST':
        user_profile_form = UserProfileInfoForm(data=request.POST,files = request.FILES)
        if user_profile_form.is_valid():
            user = request.user
            a = Accounts.objects.get(user_id = user.id)
            user_profile_form.instance.user = user
            #user_profile_form.save()
            a = user_profile_form.save()
            #a.profile_pic = user_profile_form.profile_pic
            a.save()
        else:
            print(user_profile_form.errors)
    else:
        user_profile_form = UserProfileInfoForm()
    return render(request,'editProfile.html',
                          {'user_profile_form':user_profile_form,})

