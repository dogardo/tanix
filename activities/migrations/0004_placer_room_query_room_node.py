# Generated by Django 4.1.2 on 2022-11-28 21:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_alter_placer_room_query_if_its_anywhere'),
    ]

    operations = [
        migrations.AddField(
            model_name='placer_room_query',
            name='room_node',
            field=models.CharField(default=django.utils.timezone.now, max_length=500, verbose_name='title'),
            preserve_default=False,
        ),
    ]