# Generated by Django 3.1.6 on 2021-02-17 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signUps', '0003_accounts_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='profile_pic',
            field=models.ImageField(default='pro_pic.jpg', upload_to=''),
            preserve_default=False,
        ),
    ]
