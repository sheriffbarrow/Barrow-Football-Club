# Generated by Django 3.2.9 on 2022-04-08 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bfc', '0003_post_approve'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='approve',
            new_name='approve_to_post',
        ),
    ]