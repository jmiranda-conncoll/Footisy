from django import forms
from signUps.models import Accounts, Game
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','first_name','last_name','password','email')

class UserProfileInfoForm(forms.ModelForm):
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
    ('level 1: beginner', 'Level 1: Beginner'),
    ('level 2: fun', 'Level 2: Just For Fun'),
    ('level 3: sweat', 'Level 3: Break a sweat'),
    ('level 4: skilled', 'Level 4: High Competition'),
    ('level 5: intense', 'Level 5: Intense Training'),
    ]

class CreateGameInfoForm(forms.ModelForm):
    sport = forms.CharField(label='Select Sport:', widget=forms.Select(choices= SPORT_CHOICES))
    level = forms.CharField(label='Select Level:', widget=forms.Select(choices= LEVEL_CHOICES))
    class Meta():
        model = Game
        fields = ('name', 'sport', 'level', 'location', 'max_players', 'description', 'date')