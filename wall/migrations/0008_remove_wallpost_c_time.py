# Generated by Django 4.1.2 on 2023-08-13 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0007_wallpost_c_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallpost',
            name='c_time',
        ),
    ]