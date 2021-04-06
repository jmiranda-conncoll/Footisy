# Generated by Django 3.1.6 on 2021-04-06 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signUps', '0010_game_temp'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='isFull',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='lat',
            field=models.DecimalField(decimal_places=18, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='lng',
            field=models.DecimalField(decimal_places=18, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateField(null=True),
        ),
    ]