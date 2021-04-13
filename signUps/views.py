from django.shortcuts import render
from signUps.forms import UserForm, UserProfileInfoForm, CreateGameInfoForm, Gamefilters, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from signUps.models import Accounts, Game, GamePlayers, Teammates
from django.contrib.auth.models import User
from decimal import Decimal
import requests
import json
from urllib.parse import urlencode, urlparse, parse_qsl
from datetime import date, timedelta

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
        # da = date.today()
        # if (Game.objects.filter(date < da).exists()):
        #     games = Game.objects.filter(date <= da)
        #     for g in games:
        #         deleteGamebyId(g.id)
        username = request.POST['username']
        password = request.POST['password']
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
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})

@login_required
def profile(request):
    user = request.user
    profile_objs = Accounts.objects.get(user_id = user.id)
    if (profile_objs.profile_pic == ""):
        profile_objs.profile_pic = "images/pro_pic.jpg"

    user_list = []
    if (Teammates.objects.filter(user1_id = user.id).exists()):
        team_list = Teammates.objects.filter(user1_id = user.id)
        for u in team_list:
            temp_user = u.user2
            user_list.append(temp_user)

    context = {
        "profile": profile_objs,
        "team": user_list,
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
            if (bio != ""):
                a.bio = bio

            if (sports != ""):
                a.sports = sports

            if (pro_pic != ""):
                a.profile_pic = pro_pic

            #make sure none of the fields are required

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
            game.lat = request.POST["game_lat"]
            game.lng = request.POST["game_long"]
            _lat = request.POST["game_lat"]
            _lng = request.POST["game_long"]
            #add code here to create address
            locat = getAddress(_lat, _lng)
            game.location = locat
            game.current_players = 1
            game.host = request.user
            game.isFull = False
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
    attending_list = []
    user = request.user
    game_objs = Game.objects.filter(host_id = user.id).order_by('date')

    #add here games they are attending
    if (GamePlayers.objects.filter(player = user).exists()):
        gp_objs = GamePlayers.objects.filter(player = user)
        for gp in gp_objs:
            game = Game.objects.get(id = gp.game.id)
            game.temp = True
            attending_list.append(game)

    #sort attending list by date?

    context = {
        "games_list": game_objs,
        "attending_list": attending_list
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
    user_list = []
    #add here to check if they are attending
    is_attending = False
    for obj in attending_objs:
        temp_user = obj.player
        user_list.append(temp_user)
        if (request.user == temp_user):
            is_attending = True

    context = {
        "game": game_obj,
        "players_list": user_list,
        "host": is_host,
        "attending": is_attending,
    }
    return render(request, "gamebyID.html", context)

@login_required
def profilebyID(request, profile_id):
    if (profile_id == request.user.id):
        return profile(request)
    else:
        profile_obj = Accounts.objects.get(user_id = profile_id)

        attending_list = []
        if (Game.objects.filter(host_id = profile_id).exists()):
            g_objs = Game.objects.filter(host_id = profile_id)
            for gp in g_objs:
                attending_list.append(gp)
        #add here games they are attending
        if (GamePlayers.objects.filter(player_id = profile_id).exists()):
            gp_objs = GamePlayers.objects.filter(player_id = profile_id)
            for gp in gp_objs:
                game = Game.objects.get(id = gp.game.id)
                attending_list.append(game)

        isTeammate = False
        #check if teammates
        if (Teammates.objects.filter(user1_id = request.user.id, user2_id = profile_id).exists()):
            isTeammate = True

        user_list = []
        if (Teammates.objects.filter(user1_id = profile_id).exists()):
            team_list = Teammates.objects.filter(user1_id = profile_id)
            for u in team_list:
                temp_user = u.user2
                user_list.append(temp_user)

        if (profile_obj.profile_pic == "" or profile_obj.profile_pic == None):
            profile_obj.profile_pic = "images/pro_pic.jpg"

        context = {
            "profile": profile_obj,
            "isTeammate": isTeammate,
            "team": user_list,
            "attending": attending_list,
        }
        return render(request, "profilebyID.html", context)

@login_required
def displayAllGames(request):
    if request.method == 'POST':
        filter_form = Gamefilters(data=request.POST)
        if filter_form.is_valid():
            sp = request.POST['sport']
            le = request.POST['level']
            if (sp != ""):
                sport = sp
                if (le != ""):
                    level = le
                    game_objs = Game.objects.filter(sport = sport, level = level).exclude(host_id = request.user.id, isFull = True)[:50]
                else:
                    game_objs = Game.objects.filter(sport = sport).exclude(host_id = request.user.id, isFull = True)[:50]
            else:
                if (le != ""):
                    level = le
                    game_objs = Game.objects.filter(level = level).exclude(host_id = request.user.id, isFull = True)[:50]
                else:
                    #displays all games but filters out the ones they created
                    game_objs = Game.objects.filter().exclude(host_id = request.user.id, isFull = True)[:50]

            #filter out games that are full
            attending_objs = GamePlayers.objects.filter(player_id = request.user.id)
            for g in attending_objs:
                for game in game_objs:
                    if game.id == g.game.id:
                        game.temp = True
                        break
            
            context = {
                "games_list": game_objs,
                "filter_form": Gamefilters(),
            }
        else:
            print(filter_form.errors)
    else:
        filter_form = Gamefilters()
        #displays all games but filters out the ones they created
        game_objs = Game.objects.filter().exclude(host_id = request.user.id, isFull = True)[:50]
        #filter out games that are full
        attending_objs = GamePlayers.objects.filter(player_id = request.user.id)
        for g in attending_objs:
            for game in game_objs:
                if game.id == g.game.id:
                    game.temp = True
                    break
        context = {
            "games_list": game_objs,
            "filter_form": filter_form,
        }

    return render(request, "allGames.html", context)

@login_required
def attendGame(request):
    game_id = request.GET.get('id', None)
    game_obj = Game.objects.get(id = game_id)
    temp = game_obj.current_players
    boolis = True

    #check here if game is full before creating the record, create 2 paths here with if statement
    if (temp == game_obj.max_players):
        data = {
            'yes': boolis,
        }
        if (data['yes']):
            data['error_message'] = 'hey im full'

        return JsonResponse(data)
    
    else:
        #check if they are already attending
        if (GamePlayers.objects.filter(game = game_obj).filter(player = request.user).exists()):
            data = {
                'yes': boolis,
            }
            if (data['yes']):
                data['error_message'] = 'hey i exist'

            return JsonResponse(data)
        else:

            temp = temp + 1
            game_obj.current_players = temp
            if (temp == game_obj.max_players):
                game_obj.isFull = True
            game_obj.save()
            gp = GamePlayers()
            gp.game = game_obj
            gp.player = request.user
            gp.save()
            _max = game_obj.max_players

            boolis = False
            data = {
                'yes': boolis,
                'attend': temp,
                'max': _max,
            }
            data['error_message'] = 'hey i am attending'
            return JsonResponse(data)

@login_required
def leaveGame(request):
    game_id = request.GET.get('id', None)
    player = request.user
    gamePlayer = GamePlayers.objects.filter(game_id = game_id).get(player = player).delete()
    game_obj = Game.objects.get(id = game_id)
    temp = game_obj.current_players

    temp = temp - 1
    game_obj.current_players = temp
    game_obj.save()

    boolis = False
    data = {
        'yes': boolis,
        'attend': temp,
        'max': game_obj.max_players,
    }
    if (data['yes']):
        data['error_message'] = 'hi there'

    return JsonResponse(data)

@login_required
def deleteGame(request):
    game_id = request.GET.get('id', None)
    #check here if user is host of game first
    game = Game.objects.get(id = game_id)
    if (game.host == request.user):
        #first delete all game players from the table
        if (GamePlayers.objects.filter(game_id = game_id).exists()):
            GamePlayers.objects.filter(game_id = game_id).delete()
        #then delete game from Game table
        Game.objects.get(id = game_id).delete()

    data = {
        'id': game_id,
    }

    return JsonResponse(data)

@login_required
def centerMap(request):
    address = request.GET.get('add', None)
    #address = "59 Woodside Rd, Winchester, MA"
    api_key = "AIzaSyBiRulAGF1hJPBF0Wh7qnw5dNZvL2lFP5c"
    data_type = 'json'
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": address, "key": api_key}
    url_params = urlencode(params)

    url = f"{endpoint}?{url_params}"

    r = requests.get(url)
    if (r.status_code not in range(200, 299)):
        return {}
    latlng = {}
    try: 
        latlng = r.json()['results'][0]['geometry']['location']
    except:
        pass

    data = {
        'lat': latlng.get("lat"),
        'lng': latlng.get("lng"),
    }

    return JsonResponse(data)

def deleteGamebyId(id):
    #first delete all game players from the table 
    GamePlayers.objects.filter(game_id = id).delete()
    #then delete game from Game table
    Game.objects.get(id = id).delete()

@login_required
def addTeammate(request):
    user2_id = request.GET.get('id', None)
    tm = Teammates()
    tm.user1 = request.user
    tm.user2_id = user2_id
    tm.save()
    data = {
        'user_id': request.user.id
    }

    return JsonResponse(data)

@login_required
def removeTeammate(request):
    user2_id = request.GET.get('id', None)
    Teammates.objects.get(user2_id = user2_id, user1 = request.user).delete()
    data = {
        'user_id': request.user.id
    }
    return JsonResponse(data)

def getAddress(lat,lng):
    api_key = "AIzaSyBiRulAGF1hJPBF0Wh7qnw5dNZvL2lFP5c"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}"

    r = requests.get(url)
    if (r.status_code not in range(200, 299)):
        return ""
    address = ""
    try: 
        address = r.json()['results'][0]['formatted_address']
    except:
        pass

    return address


