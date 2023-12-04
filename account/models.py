from locale import normalize
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import uuid

from django.forms import NullBooleanField

class usercoremanager(BaseUserManager):

    def create_user(self,username,email,phone,password):
        if not username:
            raise ValueError("username is required")
        if not email:
            raise ValueError("email is required")
        if not phone:
            raise ValueError("phone number needs to be valid")

        user=self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            max_table_normal=0,
            max_table_not_normal=0
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,phone,password):
        if not username:
            raise ValueError("username is required")
        if not email:
            raise ValueError("email is required")
        if not phone:
            raise ValueError("phone number needs to be valid")

        user=self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            is_admin=True,
            is_staff=True,
            is_superuser=True,
            user_type=1,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class usercore(AbstractBaseUser):

    username = models.CharField(max_length=200, verbose_name='username',unique=True)
    email = models.EmailField(unique=True,max_length=50,verbose_name='place mail adress')
    name = models.CharField(max_length=200, verbose_name='name',blank=True, null=True,default=None)
    surname = models.CharField(max_length=200, verbose_name='surname',blank=True, null=True,default=None)
    place_name = models.CharField(max_length=200,verbose_name='place name',blank=True, null=True,default=None)
    pic1 = models.ImageField(upload_to = 'uploads/user/',verbose_name="pic1",blank=True, null=True)
    pic2 = models.ImageField(upload_to = 'uploads/user/',verbose_name="pic2",blank=True, null=True)
    pic3 = models.ImageField(upload_to = 'uploads/user/',verbose_name="pic3",blank=True, null=True)
    pic4 = models.ImageField(upload_to = 'uploads/user/',verbose_name="pic4",blank=True, null=True)
    pic5 = models.ImageField(upload_to = 'uploads/user/',verbose_name="pic5",blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Kadın','Kadın'),('Erkek','Erkek'),('Diğer','Diğer')]
   ,blank=True, null=True,default=None)
    
    university = models.ForeignKey("activities.universities",on_delete = models.CASCADE, verbose_name='university',blank=True, null=True,default=None)
    phone = models.IntegerField(unique=True,verbose_name='phone')
    ranking = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+5)],verbose_name="ranking",blank=True, null=True)
    money = models.IntegerField(verbose_name="money",blank=True, null=True)
    in_classics_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='in which normal games',blank=True, null=True)
    in_non_classics_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='in which spesific games',blank=True, null=True)
    verify = models.BooleanField(verbose_name="can avaliable",default=True)
    can_enter_game = models.BooleanField(verbose_name="can avaliable",default=True)
    verify_pic = models.ImageField(upload_to = 'uploads/user/',verbose_name="vpic",blank=True, null=True)
    max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="classic game existence",blank=True, null=True,default=None)
    max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="spesific game existence",blank=True, null=True,default=None)
    place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",blank=True, null=True)
    place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",blank=True, null=True)
    area = models.ForeignKey("activities.places",on_delete = models.CASCADE, verbose_name='place area',blank=True, null=True,default=None)
    acc_can_open_normal_game = models.BooleanField(verbose_name="can open normal loby",default=True)
    acc_can_open_not_normal_game = models.BooleanField(verbose_name="can open spesific game",default=True)
    user_type= models.IntegerField(validators=[MinValueValidator(+1), MaxValueValidator(+4)],verbose_name="user type",blank=True, null=True,default=None)
  
    date_joined = models.DateTimeField(auto_now=True,verbose_name="date joined")
    last_login = models.DateTimeField(auto_now=True,verbose_name="last login")

    is_admin= models.BooleanField(default=False,verbose_name="is admin")
    is_superuser=models.BooleanField(default=False,verbose_name="is superuser")
    is_staff=models.BooleanField(default=False,verbose_name="is staff")

    chats = models.ManyToManyField("account.message_manager_2", verbose_name='messages',blank=True, null=True, related_name="chats+" )
    
    USERNAME_FIELD="username"

    REQUIRED_FIELDS=["email","phone"]

    objects=usercoremanager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True       
    
class consumer(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(usercore, on_delete=models.CASCADE,max_length=15,verbose_name='username',unique=True)
    email = models.EmailField(unique=True,max_length=50,verbose_name='place mail adress')
    name = models.CharField(max_length=200, verbose_name='name')
    surname = models.CharField(max_length=200, verbose_name='surname')
    pic1 = models.ImageField(upload_to = 'uploads/consumer',verbose_name="pic1",blank=True, null=True)
    pic2 = models.ImageField(upload_to = 'uploads/consumer',verbose_name="pic2",blank=True, null=True)
    pic3 = models.ImageField(upload_to = 'uploads/consumer',verbose_name="pic3",blank=True, null=True)
    pic4 = models.ImageField(upload_to = 'uploads/consumer',verbose_name="pic4",blank=True, null=True)
    pic5 = models.ImageField(upload_to = 'uploads/consumer',verbose_name="pic5",blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Kadın','Kadın'),('Erkek','Erkek'),('Diğer','Diğer')]
    )
    university = models.ForeignKey("activities.universities",on_delete = models.CASCADE, verbose_name='university')
    phone = models.IntegerField(unique=True,verbose_name='phone')
    ranking = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+5)],verbose_name="ranking",blank=True, null=True)
    money = models.IntegerField(verbose_name="money",blank=True, null=True, default=0)
    in_classics = models.ManyToManyField("activities.classic_room", verbose_name='which type of game exists',blank=True, null=True)
    in_non_classics = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='in which spesific games',blank=True, null=True)
    in_placer_rooms = models.ManyToManyField("activities.placer_room", verbose_name='which type of placer game exists',blank=True, null=True)
    verify = models.BooleanField(verbose_name="can avaliable",default=True)
    can_enter_game = models.BooleanField(verbose_name="can avaliable",default=True)
    verify_pic = models.ImageField(upload_to = 'uploads/consumers/',verbose_name="vpic",blank=True, null=True)
    friends = models.ManyToManyField("account.consumer", verbose_name='friendsquery',blank=True, null=True, related_name="friendsquery+" )
    friendsquery = models.ManyToManyField("account.consumer", verbose_name='friends',blank=True, null=True, related_name="friends+" )
    ibanned = models.ManyToManyField("account.consumer", verbose_name='ibanned',blank=True, null=True, related_name="banned+" )
    imbanned = models.ManyToManyField("account.consumer", verbose_name='imbanned',blank=True, null=True, related_name="imbanned+" )
    date_joined = models.DateTimeField(auto_now=True,verbose_name="date joined")
    last_login = models.DateTimeField(auto_now=True,verbose_name="last login")
    chats = models.ManyToManyField("account.message_manager", verbose_name='messages',blank=True, null=True, related_name="chats+" )
    c_room_offers = models.ManyToManyField("activities.classic_room", verbose_name='game querys normal',blank=True, null=True, related_name="croom_query+")
    n_room_offers = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='game querys not normal',blank=True, null=True, related_name="nroom_query+")
    p_room_offers = models.ManyToManyField("activities.placer_room", verbose_name='game querys placer',blank=True, null=True, related_name="proom_query+")
    bio = models.CharField(max_length=1000, verbose_name='bio')

    def __str__ (self):
        return str(self.username)

class placer(models.Model):

    username = models.ForeignKey(usercore, on_delete=models.CASCADE,max_length=15,verbose_name='username',unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True,max_length=50,verbose_name='place mail adress')
    place_name = models.CharField(max_length=200,verbose_name='place name')

    min_price = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+200)],verbose_name="value",blank=True, null=True, default=0)

    area = models.ForeignKey("activities.places",on_delete = models.CASCADE, verbose_name='place area')
    pic1 = models.ImageField(upload_to = 'uploads/placer',verbose_name="pic1",blank=True, null=True)
    pic2 = models.ImageField(upload_to = 'uploads/placer',verbose_name="pic2",blank=True, null=True)
    pic3 = models.ImageField(upload_to = 'uploads/placer',verbose_name="pic3",blank=True, null=True)
    pic4 = models.ImageField(upload_to = 'uploads/placer',verbose_name="pic4",blank=True, null=True)
    pic5 = models.ImageField(upload_to = 'uploads/placer',verbose_name="pic5",blank=True, null=True)

    existence_of_classic_activities = models.ManyToManyField("activities.classic_activities", verbose_name='classic_activites',blank=True, null=True)
    
    ###----------------------------0 

    max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="classic game existence")
    max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="spesific game existence")
    place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)
    existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True)
    existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True)


    acc_can_open_normal_game = models.BooleanField(verbose_name="can open normal loby",default=True)
    acc_can_open_not_normal_game = models.BooleanField(verbose_name="can open spesific game",default=True)

    ###----------------------------d1/h1 

    a11_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d1/h1 classic game existence",default=0)
    a11_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d1/h1 spesific game existence",default=0)
    
    a11_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a11_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a11_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d1/h1 normals+")
    a11_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d1/h1 spesifics+")
    

    ###----------------------------d1/h2 

    a12_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d1/h2 classic game existence",default=0)
    a12_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d1/h2 spesific game existence",default=0)
    
    a12_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a12_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a12_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d1/h2 normals+")
    a12_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d1/h2 spesifics+")
    
    ###----------------------------d1/h3 

    a13_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d1/h3 classic game existence",default=0)
    a13_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d1/h3 spesific game existence",default=0)
    a13_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a13_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a13_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d1/h3 normals+")
    a13_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d1/h3 spesifics+")

    ###----------------------------d1/h4

    a14_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d1/h4 classic game existence",default=0)
    a14_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d1/h4 spesific game existence",default=0)
    a14_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a14_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a14_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d1/h4 normals+")
    a14_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d1/h4 spesifics+")
    
    ###----------------------------d1/h5

    a15_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d1/h5 classic game existence",default=0)
    a15_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d1/h5 spesific game existence",default=0)
    a15_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a15_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a15_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d1/h5 normals+")
    a15_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d1/h5 spesifics+")
    
    ###----------------------------d2/h1 

    a21_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h1 classic game existence",default=0)
    a21_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h1 spesific game existence",default=0)
    a21_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a21_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a21_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d2/h1 normals+")
    a21_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d2/h1 spesifics+")

    ###----------------------------d2/h2 

    a22_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h2 classic game existence",default=0)
    a22_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h2 spesific game existence",default=0)
    a22_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a22_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a22_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d2/h2 normals+")
    a22_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d2/h2 spesifics+")
    
    ###----------------------------d2/h3 

    a23_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h3 classic game existence",default=0)
    a23_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h3 spesific game existence",default=0)
    a23_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a23_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a23_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d2/h3 normals+")
    a23_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d2/h3 spesifics+")
    
    ###----------------------------d2/h4

    a24_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h4 classic game existence",default=0)
    a24_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h4 spesific game existence",default=0)
    a24_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a24_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a24_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d2/h4 normals+")
    a24_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d2/h4 spesifics+")
    
    ###----------------------------d2/h5

    a25_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h5 classic game existence",default=0)
    a25_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h5 spesific game existence",default=0)
    a25_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a25_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a25_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d2/h5 normals+")
    a25_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d2/h5 spesifics+")

    ###----------------------------d3/h1

    a31_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d3/h1 classic game existence",default=0)
    a31_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d3/h1 spesific game existence",default=0)
    a31_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a31_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a31_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d3/h1 normals+")
    a31_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d3/h1 spesifics+")

    ###----------------------------d3/h2

    a32_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d3/h2 classic game existence",default=0)
    a32_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d3/h2 spesific game existence",default=0)
    a32_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a32_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a32_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d3/h2 normals+")
    a32_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d3/h2 spesifics+")

    ###----------------------------d3/h3

    a33_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d3/h3 classic game existence",default=0)
    a33_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d3/h3 spesific game existence",default=0)
    a33_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a33_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a33_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d3/h3 normals+")
    a33_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d3/h3 spesifics+")

    ###----------------------------d3/h4

    a34_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d3/h4 classic game existence",default=0)
    a34_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d3/h4 spesific game existence",default=0)
    a34_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a34_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a34_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d3/h4 normals+")
    a34_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d3/h4 spesifics+")

    ###----------------------------d3/h5

    a35_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d3/h5 classic game existence",default=0)
    a35_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d3/h5 spesific game existence",default=0)
    a35_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a35_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a35_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d3/h5 normals+")
    a35_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d3/h5 spesifics+")

    ###----------------------------d4/h1

    a41_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d4/h1 classic game existence",default=0)
    a41_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d4/h1 spesific game existence",default=0)
    a41_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a41_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a41_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d4/h1 normals+")
    a41_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d4/h1 spesifics+")

    ###----------------------------d4/h2

    a42_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d4/h2 classic game existence",default=0)
    a42_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d4/h2 spesific game existence",default=0)
    a42_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a42_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a42_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d4/h2 normals+")
    a42_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d4/h2 spesifics+")

    ###----------------------------d4/h3

    a43_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d4/h3 classic game existence",default=0)
    a43_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d4/h3 spesific game existence",default=0)
    a43_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a43_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a43_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d4/h3 normals+")
    a43_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d4/h3 spesifics+")

    ###----------------------------d4/h4

    a44_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d4/h4 classic game existence",default=0)
    a44_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d4/h4 spesific game existence",default=0)
    a44_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a44_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a44_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d4/h4 normals+")
    a44_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d4/h4 spesifics+")

    ###----------------------------d4/h5

    a45_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d4/h5 classic game existence",default=0)
    a45_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d4/h5 spesific game existence",default=0)
    a45_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a45_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a45_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d4/h5 normals+")
    a45_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d4/h5 spesifics+")

    ###----------------------------d5/h1

    a51_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d5/h1 classic game existence",default=0)
    a51_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d5/h1 spesific game existence",default=0)
    a51_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a51_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a51_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d5/h1 normals+")
    a51_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d5/h1 spesifics+")

    ###----------------------------d5/h2

    a52_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d5/h2 classic game existence",default=0)
    a52_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d5/h2 spesific game existence",default=0)
    a52_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a52_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a52_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d5/h2 normals+")
    a52_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d5/h2 spesifics+")

    ###----------------------------d5/h3

    a53_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d5/h3 classic game existence",default=0)
    a53_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d5/h3 spesific game existence",default=0)
    a53_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a53_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a53_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d5/h3 normals+")
    a53_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d5/h3 spesifics+")

    ###----------------------------d5/h4

    a54_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d5/h4 classic game existence",default=0)
    a54_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d5/h4 spesific game existence",default=0)
    a54_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a54_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a54_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d5/h4 normals+")
    a54_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d5/h4 spesifics+")

    ###----------------------------d5/h5

    a55_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d5/h5 classic game existence",default=0)
    a55_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d5/h5 spesific game existence",default=0)
    a55_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a55_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a55_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d5/h5 normals+")
    a55_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d5/h5 spesifics+")

    ###----------------------------d6/h1

    a61_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d6/h1 classic game existence",default=0)
    a61_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d6/h1 spesific game existence",default=0)
    a61_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a61_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a61_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d6/h1 normals+")
    a61_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d6/h1 spesifics+")

    ###----------------------------d6/h2

    a62_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d6/h2 classic game existence",default=0)
    a62_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d6/h2 spesific game existence",default=0)
    a62_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a62_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a62_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d6/h2 normals+")
    a62_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d6/h2 spesifics+")

    ###----------------------------d6/h3

    a63_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d6/h3 classic game existence",default=0)
    a63_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d6/h3 spesific game existence",default=0)
    a63_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a63_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a63_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d6/h3 normals+")
    a63_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d6/h3 spesifics+")

    ###----------------------------d6/h4

    a64_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d6/h4 classic game existence",default=0)
    a64_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d6/h4 spesific game existence",default=0)
    a64_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a64_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a64_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d6/h4 normals+")
    a64_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d6/h4 spesifics+")

    ###----------------------------d6/h5

    a65_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d6/h5 classic game existence",default=0)
    a65_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d6/h5 spesific game existence",default=0)
    a65_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a65_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a65_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d6/h5 normals+")
    a65_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d6/h5 spesifics+")

    ###----------------------------d7/h1

    a71_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d7/h1 classic game existence",default=0)
    a71_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d7/h1 spesific game existence",default=0)
    a71_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a71_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a71_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d7/h1 normals+")
    a71_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d7/h1 spesifics+")

    ###----------------------------d7/h2

    a72_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h5 classic game existence",default=0)
    a72_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d2/h5 spesific game existence",default=0)
    a72_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a72_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a72_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d7/h2 normals+")
    a72_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d7/h2 spesifics+")

    ###----------------------------d7/h3

    a73_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d7/h3 classic game existence",default=0)
    a73_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d7/h3 spesific game existence",default=0)
    a73_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a73_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a73_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d7/h3 normals+")
    a73_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d7/h3 spesifics+")

    ###----------------------------d7/h4

    a74_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d7/h4 classic game existence",default=0)
    a74_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d7/h4 spesific game existence",default=0)
    a74_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a74_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a74_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d7/h4 normals+")
    a74_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d7/h4 spesifics+")

    ###----------------------------d7/h5

    a75_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d7/h5 classic game existence",default=0)
    a75_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d7/h5 spesific game existence",default=0)
    a75_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a75_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a75_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d7/h5 normals+")
    a75_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d7/h5 spesifics+")

    ###----------------------------d8/h1

    a81_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d8/h1 classic game existence",default=0)
    a81_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d8/h1 spesific game existence",default=0)
    a81_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a81_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a81_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d8/h1 normals+")
    a81_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d8/h1 spesifics+")

    ###----------------------------d8/h2

    a82_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d8/h2 classic game existence",default=0)
    a82_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d8/h2 spesific game existence",default=0)
    a82_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a82_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a82_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d8/h2 normals+")
    a82_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d8/h2 spesifics+")

    ###----------------------------d8/h3

    a83_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d8/h3 classic game existence",default=0)
    a83_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d8/h3 spesific game existence",default=0)
    a83_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a83_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a83_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d8/h3 normals+")
    a83_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d8/h3 spesifics+")

    ###----------------------------d8/h4

    a84_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d8/h4 classic game existence",default=0)
    a84_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d8/h4 spesific game existence",default=0)
    a84_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a84_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a84_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d8/h4 normals+")
    a84_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d8/h4 spesifics+")

    ###----------------------------d8/h5

    a85_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d8/h5 classic game existence",default=0)
    a85_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d8/h5 spesific game existence",default=0)
    a85_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a85_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a85_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d8/h5 normals+")
    a85_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d8/h5 spesifics+")

    ###----------------------------d9/h1

    a91_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d9/h1 classic game existence",default=0)
    a91_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d9/h1 spesific game existence",default=0)
    a91_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a91_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a91_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d9/h1 normals+")
    a91_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d9/h1 spesifics+")

    ###----------------------------d9/h2

    a92_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d9/h2 classic game existence",default=0)
    a92_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d9/h2 spesific game existence",default=0)
    a92_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a92_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a92_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d9/h2 normals+")
    a92_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d9/h2 spesifics+")

    ###----------------------------d9/h3

    a93_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d9/h3 classic game existence",default=0)
    a93_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d9/h3 spesific game existence",default=0)
    a93_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a93_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a93_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d9/h3 normals+")
    a93_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d9/h3 spesifics+")

    ###----------------------------d9/h4

    a94_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d9/h4 classic game existence",default=0)
    a94_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d9/h4 spesific game existence",default=0)
    a94_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a94_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a94_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d9/h4 normals+")
    a94_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d9/h4 spesifics+")
    ###----------------------------d9/h5

    a95_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d9/h5 classic game existence",default=0)
    a95_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d9/h5 spesific game existence",default=0)
    a95_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a95_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a95_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d9/h5 normals+")   
    a95_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d9/h5 spesifics+")

    ###----------------------------d10/h1

    a101_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d10/h1 classic game existence",default=0)
    a101_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d10/h1 spesific game existence",default=0)
    a101_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a101_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a101_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d10/h1 normals+")
    a101_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d10/h1 spesifics+")

    ###----------------------------d10/h2

    a102_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d10/h2 classic game existence",default=0)
    a102_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d10/h2 spesific game existence",default=0)
    a102_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a102_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a102_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d10/h2 normals+") 
    a102_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d10/h2 spesifics+")

    ###----------------------------d10/h3

    a103_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d10/h3 classic game existence",default=0)
    a103_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d10/h3 spesific game existence",default=0)
    a103_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a103_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a103_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d10/h3 normals+")
    a103_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d10/h3 spesifics+")
    
    ###----------------------------d10/h4

    a104_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d10/h4 classic game existence",default=0)
    a104_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d10/h4 spesific game existence",default=0)
    a104_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a104_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a104_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d10/h4 normals+")
    a104_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d10/h4 spesifics+")

    ###----------------------------d10/h5

    a105_max_table_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d10/h5 classic game existence",default=0)
    a105_max_table_not_normal = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],verbose_name="d10/h5 spesific game existence",default=0)
    a105_place_avabiality_normal = models.BooleanField(verbose_name="place avabiality for normal game",default=1)
    a105_place_avabiality_not_normal = models.BooleanField(verbose_name="place avabiality for spesific game",default=True)

    a105_existence_of_normal_game = models.ManyToManyField("activities.classic_room", verbose_name='normal game existence',blank=True, null=True,related_name="d10/h5 normals+") 
    a105_existence_of_not_normal_game = models.ManyToManyField("activities.non_classic_activity_room", verbose_name='spesific game existence',blank=True, null=True,related_name="d10/h5 spesifics+")

    ###---------------------------- 
    phone = models.IntegerField(unique=True,verbose_name='phone')
    ranking = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+5)],verbose_name="ranking",blank=True, null=True)
    money = models.IntegerField(verbose_name="money",blank=True, null=True)
    verify = models.BooleanField(verbose_name="verify",default=True)
    verify_pic = models.ImageField(upload_to = 'uploads/placers/',verbose_name="vpic",blank=True, null=True)

    date_joined = models.DateTimeField(auto_now=True,verbose_name="date joined")
    last_login = models.DateTimeField(auto_now=True,verbose_name="last login")

    def __str__ (self):
        return str(self.place_name)

class between_two_ferns(models.Model):
    
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    message_itself = models.CharField(max_length=200, verbose_name='name',blank=True, null=True,default=None)
    creator = models.ForeignKey("account.consumer",on_delete = models.CASCADE, verbose_name='area',blank=True, null=True)
    c_time = models.DateTimeField(auto_now_add=False) 
    manager = models.ForeignKey("account.message_manager",on_delete = models.CASCADE, verbose_name='area',blank=True, null=True)
    def __str__ (self):
        return str(self.message_itself)

class message_manager(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    whos_in = models.ManyToManyField("account.consumer", verbose_name='whos in',blank=True, null=True, related_name="peoplein+" )
    chatbox = models.ManyToManyField("account.between_two_ferns", verbose_name='messages',blank=True, null=True, related_name="between_two_ferns+" )
    
    def __str__ (self):
        return str(self.id)

class between_two_ferns_2(models.Model):
    
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    message_itself = models.CharField(max_length=200, verbose_name='name',blank=True, null=True,default=None)
    creator = models.ForeignKey("account.usercore",on_delete = models.CASCADE, verbose_name='area',blank=True, null=True)
    c_time = models.DateTimeField(auto_now_add=False) 
    manager = models.ForeignKey("account.message_manager_2",on_delete = models.CASCADE, verbose_name='area',blank=True, null=True)
    def __str__ (self):
        return str(self.message_itself)

class message_manager_2(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    whos_in = models.ManyToManyField("account.usercore", verbose_name='whos in',blank=True, null=True, related_name="peoplein+" )
    chatbox = models.ManyToManyField("account.between_two_ferns_2", verbose_name='messages',blank=True, null=True, related_name="between_two_ferns+" )
    
    def __str__ (self):
        return str(self.id)

class community(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(usercore, on_delete=models.CASCADE,max_length=15,verbose_name='username',unique=True)
    name = models.CharField(max_length=200, verbose_name='name')

    email = models.EmailField(unique=True,max_length=50,verbose_name='place mail adress')
    pic1 = models.ImageField(upload_to = 'uploads/community',verbose_name="pic1",blank=True, null=True)

    phone = models.IntegerField(unique=True,verbose_name='phone')
    ranking = models.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+5)],verbose_name="ranking",blank=True, null=True)
    
    money = models.IntegerField(verbose_name="money",blank=True, null=True, default=0)
    
    verify = models.BooleanField(verbose_name="can avaliable",default=True)
    verify_pic = models.ImageField(upload_to = 'uploads/consumers/',verbose_name="vpic",blank=True, null=True)
    date_joined = models.DateTimeField(auto_now=True,verbose_name="date joined")
    
    last_login = models.DateTimeField(auto_now=True,verbose_name="last login")
    chats = models.ManyToManyField("account.message_manager_2", verbose_name='messages',blank=True, null=True, related_name="chats+" )
    p_room_offers_to_p = models.ManyToManyField("activities.placer_room_query", verbose_name='game querys placer',blank=True, null=True, related_name="proom_query+")

    def __str__ (self):
        return str(self.username)    