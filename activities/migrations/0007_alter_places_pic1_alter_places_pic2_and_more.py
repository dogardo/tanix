# Generated by Django 4.1.2 on 2022-12-07 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_places_pic1_places_pic2_places_pic3_places_pic4_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='pic1',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/places/', verbose_name='pic1'),
        ),
        migrations.AlterField(
            model_name='places',
            name='pic2',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/places/', verbose_name='pic2'),
        ),
        migrations.AlterField(
            model_name='places',
            name='pic3',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/places/', verbose_name='pic3'),
        ),
        migrations.AlterField(
            model_name='places',
            name='pic4',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/places/', verbose_name='pic4'),
        ),
        migrations.AlterField(
            model_name='places',
            name='pic5',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/places/', verbose_name='pic5'),
        ),
    ]
