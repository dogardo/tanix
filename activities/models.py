from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import User
import uuid

###---------------------------------

class places(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    place = models.CharField(max_length=30,verbose_name="place")
    existence_of_places = models.ManyToManyField("account.placer", verbose_name='placers exists',null=True,blank=True)
    pic1 = models.ImageField(upload_to = 'uploads/places/',verbose_name="pic1",blank=True, null=True)
    pic2 = models.ImageField(upload_to = 'uploads/places/',verbose_name="pic2",blank=True, null=True)
    pic3 = models.ImageField(upload_to = 'uploads/places/',verbose_name="pic3",blank=True, null=True)
    pic4 = models.ImageField(upload_to = 'uploads/places/',verbose_name="pic4",blank=True, null=True)
    pic5 = models.ImageField(upload_to = 'uploads/places/',verbose_name="pic5",blank=True, null=True)
    
    def __str__(self):
        return self.place

###---------------------------------

class universities(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    university_n = models.CharField(max_length=30,verbose_name="place")

    def __str__(self):
        return self.university_n

###---------------------------------

class classic_activities(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    activity_creator = models.ForeignKey("account.usercore",on_delete = models.CASCADE, verbose_name='creator Admin')
    activity_name = models.CharField(max_length=70,verbose_name="activity name")
    activity_capacity = models.IntegerField(verbose_name="activity capacity")
    activity_picture = models.ImageField(upload_to = 'uploads/activities/',verbose_name="activity picture",blank=True, null=True)
    activity_htp = models.CharField(max_length=1000,verbose_name="how to play")
    activity_cd = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.activity_name

###---------------------------------

class classic_room(models.Model):

    #,limit_choices_to={'max_table_normal': True}

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50,verbose_name="title")
    description = models.CharField(max_length=1000,verbose_name="description")
    place = models.ForeignKey("account.placer",on_delete = models.CASCADE, verbose_name='area',blank=True, null=True)
    m_time = models.DateTimeField(auto_now_add=False)
    c_time = models.DateTimeField(auto_now_add=True) 
    closing_time = models.DateTimeField(auto_now_add=False) 
    ppl_existence = models.ManyToManyField("account.consumer", verbose_name='in loby',blank=True, null=True,)
    max_ppl_existence = models.IntegerField(verbose_name="activity capacity",blank=True)
    offers= models.ManyToManyField("account.consumer", verbose_name='wants to be in loby' ,related_name="wants to be in loby1+")
    if_its_anywhere = models.ForeignKey("activities.places",on_delete = models.CASCADE, verbose_name='spesific activity place',blank=True, null=True,)
    creator = models.ForeignKey("account.usercore",on_delete = models.CASCADE, verbose_name='creator')
    game_type = models.ForeignKey("activities.classic_activities",on_delete = models.CASCADE, verbose_name='activity')
    chat = models.ManyToManyField("activities.c_message", verbose_name='normal game existence',blank=True, null=True,related_name="chatroom+")
    entrance = models.BooleanField(verbose_name="can anyone enter",default=1)
    ok_avab_1 = models.BooleanField(verbose_name="is time passed",default=1)
    ok_avab_2 = models.BooleanField(verbose_name="is capacity ok",default=1)

    def __str__(self):
        return self.name

###---------------------------------

class non_classic_activity_room(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50,verbose_name="title")
    description = models.CharField(max_length=1000,verbose_name="description")
    place = models.ForeignKey("account.placer",on_delete = models.CASCADE, verbose_name='area',blank=True, null=True, limit_choices_to={'max_table_not_normal': True},)
    m_time = models.DateTimeField(auto_now_add=False)
    c_time = models.DateTimeField(auto_now_add=True) 
    closing_time = models.DateTimeField(auto_now_add=False) 
    ppl_existence = models.ManyToManyField("account.consumer", verbose_name='in loby')
    max_ppl_existence = models.IntegerField(verbose_name="activity capacity")
    offers= models.ManyToManyField("account.consumer", verbose_name='wants to be in loby',related_name="wants to be in loby2+")
    if_its_anywhere = models.ForeignKey("activities.places",on_delete = models.CASCADE, verbose_name='spesific activity place',blank=True, null=True)
    creator = models.ForeignKey("account.usercore",on_delete = models.CASCADE, verbose_name='creator')
    game_type = models.CharField(max_length=50,verbose_name='activity')
    chat = models.ManyToManyField("activities.n_message", verbose_name='normal game existence',blank=True, null=True,related_name="chatroom1+")
    entrance = models.BooleanField(verbose_name="is time passed",default=1)
    ok_avab_1 = models.BooleanField(verbose_name="is time passed",default=1)
    ok_avab_2 = models.BooleanField(verbose_name="is time passed",default=1)
 
    def __str__(self):
        return self.name

###---------------------------------

class c_message(models.Model) :

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    message_itself = models.CharField(max_length=200, verbose_name='name',blank=True, null=True,default=None)
    creator =models.ForeignKey("account.consumer",on_delete = models.CASCADE, verbose_name='area',blank=True, null=True)
    c_time = models.DateTimeField(auto_now_add=False) 
    room = models.ForeignKey("activities.classic_room",on_delete = models.CASCADE, verbose_name='area',blank=True, null=True)

###---------------------------------

class n_message(models.Model) :

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    message_itself = models.CharField(max_length=200, verbose_name='name',blank=True, null=True,default=None)
    creator = models.ForeignKey("account.consumer",on_delete = models.CASCADE, verbose_name='area',blank=True, null=True)
    c_time = models.DateTimeField(auto_now_add=False) 
    room = models.ForeignKey("activities.non_classic_activity_room",on_delete = models.CASCADE, verbose_name='area',blank=True, null=True)

###---------------------------------

class placer_room(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50,verbose_name="title")
    description = models.CharField(max_length=1000,verbose_name="description")
    game_type = models.CharField(max_length=50,verbose_name='activity')
    if_its_anywhere = models.ForeignKey("activities.places",on_delete = models.CASCADE, verbose_name='spesific activity place',blank=True, null=True)
    m_time = models.DateTimeField(auto_now_add=False)
    c_time = models.DateTimeField(auto_now_add=True) 
    closing_time = models.DateTimeField(auto_now_add=False) 
    creator = models.ForeignKey("account.usercore",on_delete = models.CASCADE, verbose_name='creator')
    contact = models.CharField(max_length=50,verbose_name='contact',blank=True,null=True)
    ppl_existence = models.ManyToManyField("account.consumer", verbose_name='in loby',blank=True, null=True,)
    max_ppl_existence = models.IntegerField(verbose_name="activity capacity",blank=True)
    offers= models.ManyToManyField("account.consumer", verbose_name='wants to be in loby' ,related_name="wants to be in loby1+")
    entry_price = models.IntegerField(verbose_name="entry price")
    fee = models.IntegerField(verbose_name="entry price", null=True, blank=True)
    pay = models.IntegerField(verbose_name="entry price", null=True, blank=True)
    offerprice = models.IntegerField(verbose_name="entry price", null=True, blank=True)


    def __str__(self):
        return self.name

class placer_room_query(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50,verbose_name="title")
    description = models.CharField(max_length=1000,verbose_name="description")
    game_type = models.CharField(max_length=50,verbose_name='activity')
    if_its_anywhere = models.ForeignKey("account.placer",on_delete = models.CASCADE, verbose_name='spesific activity place',blank=True, null=True)
    m_time = models.DateTimeField(auto_now_add=False)
    c_time = models.DateTimeField(auto_now_add=True) 
    closing_time = models.DateTimeField(auto_now_add=False) 
    creator = models.ForeignKey("account.usercore",on_delete = models.CASCADE, verbose_name='creator')
    ppl_existence = models.ManyToManyField("account.consumer", verbose_name='in loby',blank=True, null=True,)
    max_ppl_existence = models.IntegerField(verbose_name="activity capacity",blank=True)
    offers= models.ManyToManyField("account.consumer", verbose_name='wants to be in loby' ,related_name="wants to be in loby1+")
    entry_price = models.IntegerField(verbose_name="entry price")
    room_node = models.CharField(max_length=500,verbose_name="title")
    fee = models.IntegerField(verbose_name="entry price", null=True, blank=True)
    pay = models.IntegerField(verbose_name="entry price", null=True, blank=True)
    offerprice = models.IntegerField(verbose_name="entry price", null=True, blank=True)

    def __str__(self):
        return self.name
