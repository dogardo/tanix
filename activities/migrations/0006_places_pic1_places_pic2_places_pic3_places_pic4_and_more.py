# Generated by Django 4.1.2 on 2022-12-06 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_placer_room_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='pic1',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/user/', verbose_name='pic1'),
        ),
        migrations.AddField(
            model_name='places',
            name='pic2',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/user/', verbose_name='pic2'),
        ),
        migrations.AddField(
            model_name='places',
            name='pic3',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/user/', verbose_name='pic3'),
        ),
        migrations.AddField(
            model_name='places',
            name='pic4',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/user/', verbose_name='pic4'),
        ),
        migrations.AddField(
            model_name='places',
            name='pic5',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/user/', verbose_name='pic5'),
        ),
    ]
