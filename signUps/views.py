from django.shortcuts import render
from signUps.forms import UserForm, UserProfileInfoForm, CreateGameInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from signUps.models import Accounts, Game, GamePlayers
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
            #initialize the account record on registration
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
    if (profile_objs.profile_pic == ""):
        profile_objs.profile_pic = "images/pro_pic.jpg"
    context = {
        "profile": profile_objs,
    }
    return render(request, "profile.html", context)

@login_required
def editProfile(request):
    if request.method == 'POST':
        user_profile_form = UserProfileInfoForm(data=request.POST,files = request.FILES)
        if user_profile_form.is_valid():
            bio = request.POST["bio"]
            pro_pic = request.FILES["profile_pic"]
            sports = request.POST["sports"]
            user = request.user
            a = Accounts.objects.get(user_id = user.id)

            #add if statements here to check if each field was changed
            #make sure none of the fields are required

            a.bio = bio
            a.profile_pic = pro_pic
            a.sports = sports
            a.save()
        else:
            print(user_profile_form.errors)
    else:
        user_profile_form = UserProfileInfoForm()
    return render(request,'editProfile.html',
                          {'user_profile_form':user_profile_form,})

@login_required
def createGame(request):
    created = True
    if request.method == 'POST':
        game_form = CreateGameInfoForm(data=request.POST)
        if game_form.is_valid():
            game = game_form.save()
            game.current_players = 1
            game.host = request.user
            game.save()
            created = False
        else:
            print(game_form.errors)
    else:
        game_form = CreateGameInfoForm()
    return render(request,'createGame.html',
                          {'game_form':game_form,
                          'not_created':created})

@login_required
def displayMyGames(request):
    user = request.user
    game_objs = Game.objects.filter(host_id = user.id)

    #add here games they are attending 

    #add them to same list and sort by date

    context = {
        "games_list": game_objs,
    }
    return render(request, "myGames.html", context)

@login_required
def gamebyId(request, game_id):
    game_obj = Game.objects.get(id = game_id)
    #add here to check if the host
    if (game_obj.host == request.user):
        is_host = True
    else:
        is_host = False
    
    #get the attending users
    attending_objs = GamePlayers.objects.filter(game_id = game_id)
    #add here to check if they are attending
    is_attending = False
    for obj in attending_objs:
        temp_user = obj.player
        if (request.user == temp_user):
            is_attending = True
            break

    context = {
        "game": game_obj,
        "players_list": attending_objs,
        "host": is_host,
        "attending": is_attending,
    }
    return render(request, "gamebyID.html", context)

@login_required
def profilebyID(request, profile_id):
    profile_obj = Accounts.objects.get(user_id = profile_id)

    #check if teammates

    context = {
        "profile": profile_obj,
    }
    return render(request, "profilebyID.html", context)

@login_required
def displayAllGames(request):
    game_objs = Game.objects.filter()

    #get rid of games that user is the host of


    attending_objs = GamePlayers.objects.filter(player_id = request.user.id)
    for g in attending_objs:
        for game in game_objs:
            if game.id == g.game.id:
                game.temp = True
                break
    context = {
        "games_list": game_objs,
    }
    return render(request, "allGames.html", context)

@login_required
def attendGame(request, game_id):
    game_obj = Game.objects.get(id = game_id)
    temp = game_obj.current_players

    #check here if game is full before creating the record, create 2 paths here with if statement

    temp = temp + 1
    game_obj.current_players = temp
    game_obj.save()
    gp = GamePlayers()
    gp.game = game_obj
    gp.player = request.user
    gp.save()
    #add here to check if the host
    is_host = False
    #add here to say they are attending
    is_attending = True
    #get the attending users
    attending_objs = GamePlayers.objects.filter(game_id = game_obj.id)
    context = {
        "game": game_obj,
        "players_list": attending_objs,
        "host": is_host,
        "attending": is_attending,
    }
    return render(request, "gamebyID.html", context)