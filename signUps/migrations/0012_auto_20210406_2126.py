# Generated by Django 3.1.6 on 2021-04-06 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signUps', '0011_auto_20210406_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='lat',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='lng',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
