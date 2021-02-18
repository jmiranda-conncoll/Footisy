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

    level = models.IntegerField()

    location = models.CharField(max_length=300)

    max_players = models.IntegerField()

    current_players = models.IntegerField()

    host = models.ForeignKey(User,on_delete=models.CASCADE)

    description = models.CharField(max_length=600)
