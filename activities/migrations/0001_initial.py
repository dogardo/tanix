# Generated by Django 4.1.2 on 2022-11-27 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='c_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_itself', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='name')),
                ('c_time', models.DateTimeField()),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.consumer', verbose_name='area')),
            ],
        ),
        migrations.CreateModel(
            name='classic_activities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name', models.CharField(max_length=70, verbose_name='activity name')),
                ('activity_capacity', models.IntegerField(verbose_name='activity capacity')),
                ('activity_picture', models.ImageField(blank=True, null=True, upload_to='uploads/activities/', verbose_name='activity picture')),
                ('activity_htp', models.CharField(max_length=1000, verbose_name='how to play')),
                ('activity_cd', models.DateTimeField(auto_now_add=True)),
                ('activity_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='creator Admin')),
            ],
        ),
        migrations.CreateModel(
            name='n_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_itself', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='name')),
                ('c_time', models.DateTimeField()),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.consumer', verbose_name='area')),
            ],
        ),
        migrations.CreateModel(
            name='universities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university_n', models.CharField(max_length=30, verbose_name='place')),
            ],
        ),
        migrations.CreateModel(
            name='places',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=30, verbose_name='place')),
                ('existence_of_places', models.ManyToManyField(blank=True, null=True, to='account.placer', verbose_name='placers exists')),
            ],
        ),
        migrations.CreateModel(
            name='placer_room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='title')),
                ('description', models.CharField(max_length=1000, verbose_name='description')),
                ('game_type', models.CharField(max_length=50, verbose_name='activity')),
                ('m_time', models.DateTimeField()),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('closing_time', models.DateTimeField()),
                ('max_ppl_existence', models.IntegerField(blank=True, verbose_name='activity capacity')),
                ('entry_price', models.IntegerField(verbose_name='entry price')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('if_its_anywhere', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activities.places', verbose_name='spesific activity place')),
                ('offers', models.ManyToManyField(related_name='wants to be in loby1+', to='account.consumer', verbose_name='wants to be in loby')),
                ('ppl_existence', models.ManyToManyField(blank=True, null=True, to='account.consumer', verbose_name='in loby')),
            ],
        ),
        migrations.CreateModel(
            name='non_classic_activity_room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='title')),
                ('description', models.CharField(max_length=1000, verbose_name='description')),
                ('m_time', models.DateTimeField()),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('closing_time', models.DateTimeField()),
                ('max_ppl_existence', models.IntegerField(verbose_name='activity capacity')),
                ('game_type', models.CharField(max_length=50, verbose_name='activity')),
                ('entrance', models.BooleanField(default=1, verbose_name='is time passed')),
                ('ok_avab_1', models.BooleanField(default=1, verbose_name='is time passed')),
                ('ok_avab_2', models.BooleanField(default=1, verbose_name='is time passed')),
                ('chat', models.ManyToManyField(blank=True, null=True, related_name='chatroom1+', to='activities.n_message', verbose_name='normal game existence')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('if_its_anywhere', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activities.places', verbose_name='spesific activity place')),
                ('offers', models.ManyToManyField(related_name='wants to be in loby2+', to='account.consumer', verbose_name='wants to be in loby')),
                ('place', models.ForeignKey(blank=True, limit_choices_to={'max_table_not_normal': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.placer', verbose_name='area')),
                ('ppl_existence', models.ManyToManyField(to='account.consumer', verbose_name='in loby')),
            ],
        ),
        migrations.AddField(
            model_name='n_message',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activities.non_classic_activity_room', verbose_name='area'),
        ),
        migrations.CreateModel(
            name='classic_room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='title')),
                ('description', models.CharField(max_length=1000, verbose_name='description')),
                ('m_time', models.DateTimeField()),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('closing_time', models.DateTimeField()),
                ('max_ppl_existence', models.IntegerField(blank=True, verbose_name='activity capacity')),
                ('entrance', models.BooleanField(default=1, verbose_name='can anyone enter')),
                ('ok_avab_1', models.BooleanField(default=1, verbose_name='is time passed')),
                ('ok_avab_2', models.BooleanField(default=1, verbose_name='is capacity ok')),
                ('chat', models.ManyToManyField(blank=True, null=True, related_name='chatroom+', to='activities.c_message', verbose_name='normal game existence')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('game_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.classic_activities', verbose_name='activity')),
                ('if_its_anywhere', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activities.places', verbose_name='spesific activity place')),
                ('offers', models.ManyToManyField(related_name='wants to be in loby1+', to='account.consumer', verbose_name='wants to be in loby')),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.placer', verbose_name='area')),
                ('ppl_existence', models.ManyToManyField(blank=True, null=True, to='account.consumer', verbose_name='in loby')),
            ],
        ),
        migrations.AddField(
            model_name='c_message',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activities.classic_room', verbose_name='area'),
        ),
    ]