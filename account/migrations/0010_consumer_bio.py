# Generated by Django 4.1.2 on 2022-12-09 10:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_usercore_chats'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumer',
            name='bio',
            field=models.CharField(default=django.utils.timezone.now, max_length=1000, verbose_name='bio'),
            preserve_default=False,
        ),
    ]
