# Generated by Django 3.2.9 on 2022-04-08 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bfc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firstteamstaff',
            name='bio',
            field=models.TextField(default='N/A'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='playerBio',
            field=models.TextField(blank=True, default='N/A', null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staffBio',
            field=models.TextField(blank=True, default='N/A', null=True),
        ),
    ]
