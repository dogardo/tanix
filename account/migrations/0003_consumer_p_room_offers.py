# Generated by Django 4.1.2 on 2022-11-27 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumer',
            name='p_room_offers',
            field=models.ManyToManyField(blank=True, null=True, related_name='proom_query+', to='activities.placer_room', verbose_name='game querys placer'),
        ),
    ]
