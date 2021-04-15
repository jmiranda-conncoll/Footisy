from django import forms
from signUps.models import Accounts, Game
from django.contrib.auth.models import User
import datetime


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','first_name','last_name','password','email')

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password')
        help_texts = {
            'username': None,
        }

class UserProfileInfoForm(forms.ModelForm):
    bio = forms.CharField(label='Enter bio:', required=False)
    sports = forms.CharField(label='Enter your favorite 3 sports:', required=False)
    profile_pic = forms.ImageField(label='Upload a profile picture here:', required=False)
    class Meta():
        model = Accounts
        fields = ('bio','sports','profile_pic')

SPORT_CHOICES = [
    ('basketball', 'Basketball'),
    ('football', 'Football'),
    ('soccer', 'Soccer'),
    ('tennis', 'Tennis'),
    ('spikeball', 'Spikeball'),
    ]
LEVEL_CHOICES = [
    ('Level 1: Beginner', 'Level 1: Beginner'),
    ('Level 2: Just For Fun', 'Level 2: Just For Fun'),
    ('Level 3: Break a sweat', 'Level 3: Break a sweat'),
    ('Level 4: High Competition', 'Level 4: High Competition'),
    ('Level 5: Intense Training', 'Level 5: Intense Training'),
    ]

class CreateGameInfoForm(forms.ModelForm):
    sport = forms.CharField(label='Select Sport:', widget=forms.Select(choices= SPORT_CHOICES))
    level = forms.CharField(label='Select Level:', widget=forms.Select(choices= LEVEL_CHOICES))
    date = forms.DateTimeField(label='Set Date:', widget=forms.SelectDateWidget(years=range(datetime.date.today().year, datetime.date.today().year+1)))
    class Meta():
        model = Game
        fields = ('name', 'sport', 'level', 'max_players', 'date', 'time', 'description')
        help_texts = {
            'time': "Input time as military time format, ex: 16:00  (=4PM)",
        }

SPORT_CHOICES2 = [
    ('', 'All'),
    ('basketball', 'Basketball'),
    ('football', 'Football'),
    ('soccer', 'Soccer'),
    ('tennis', 'Tennis'),
    ('spikeball', 'Spikeball'),
    ]
LEVEL_CHOICES2 = [
    ('', 'All'),
    ('Level 1: Beginner', 'Level 1: Beginner'),
    ('Level 2: Just For Fun', 'Level 2: Just For Fun'),
    ('Level 3: Break a sweat', 'Level 3: Break a sweat'),
    ('Level 4: High Competition', 'Level 4: High Competition'),
    ('Level 5: Intense Training', 'Level 5: Intense Training'),
    ]

class Gamefilters(forms.ModelForm):
    sport = forms.CharField(label='Select Sport:', widget=forms.Select(choices= SPORT_CHOICES2), required=False)
    level = forms.CharField(label='Select Level:', widget=forms.Select(choices= LEVEL_CHOICES2), required=False)
    class Meta():
        model = Game
        fields = ('sport', 'level')