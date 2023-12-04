from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import User
import uuid


class wallpost(models.Model):
    
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    creator = models.ForeignKey("account.usercore", on_delete=models.CASCADE, verbose_name='yazar', related_name='created_posts')
    picture = models.ImageField(upload_to='uploads/wallpics', verbose_name="post görseli", blank=True, null=True)
    text = models.CharField(max_length=300, verbose_name="içerik", blank=True, null=True)

    hashtag_croom = models.ForeignKey("activities.classic_room", on_delete=models.CASCADE, verbose_name='varsa croom', blank=True, null=True)
    hashtag_nroom = models.ForeignKey("activities.non_classic_activity_room", on_delete=models.CASCADE, verbose_name='varsa nroom', blank=True, null=True)
    hashtag_proom = models.ForeignKey("activities.placer_room", on_delete=models.CASCADE, verbose_name='varsa proom', blank=True, null=True)

    area = models.ForeignKey("activities.places", on_delete=models.CASCADE, verbose_name='konum')

    likes = models.ManyToManyField("account.usercore", verbose_name='liker', blank=True)
