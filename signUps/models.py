from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Accounts(models.Model):

    email = models.EmailField()

    name = models.CharField(max_length=80)

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    username = models.CharField(max_length=80)

    password = models.CharField(max_length=80)

    bio = models.CharField(max_length=300)

    sports = models.CharField(max_length=150)

    profile_pic = models.ImageField(upload_to='images/')


class Game(models.Model):

    name = models.CharField(max_length=80)

    sport = models.CharField(max_length=40)

    level = models.CharField(max_length=80)

    location = models.CharField(max_length=300)

    max_players = models.IntegerField()

    current_players = models.IntegerField(null=True)

    host = models.ForeignKey(User,on_delete=models.CASCADE, null=True)

    description = models.CharField(max_length=600)

    #date
    date = models.DateTimeField()
    #time

class GamePlayers(models.Model):

    game = models.ForeignKey(Game,on_delete=models.CASCADE, null=True)

    player = models.ForeignKey(User,on_delete=models.CASCADE, null=True)


""" class Teammates(models.Model):

    user1 = models.ForeignKey(User,on_delete=models.CASCADE, null=True)

    user2 = models.ManyToManyField(User,on_delete=models.CASCADE, null=True) """