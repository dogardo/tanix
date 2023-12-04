from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import *
from activities.models import *
import secrets
import string



###----------------------------------------------------------------------------------------------------------------

class consumer_registerForm(forms.Form):

    username = forms.CharField(max_length=20,label="Kullanıcı İsmi")
    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parola Tekrarı",widget=forms.PasswordInput)
    university = forms.ModelChoiceField(queryset=universities.objects.all(),label="Üniversiteniz:")
    name = forms.CharField(label="İsminiz:")
    surname = forms.CharField(label="Soyisminiz:")
    email = forms.EmailField(label="email Adresiniz:")
    phone = forms.IntegerField(label="Telefon Numaranız:")
    gender = forms.ChoiceField(
        choices=[('Kadın','Kadın'),('Erkek','Erkek'),('Diğer','Diğer')]
    )
    verify_pic=forms.ImageField(label="Öğrenciliğinizi doğrulayacak herhangi bir belge yükleyiniz:")

    def clean(self):

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        name = self.cleaned_data.get("name")
        surname = self.cleaned_data.get("surname")
        university = self.cleaned_data.get("university")
        email = self.cleaned_data.get("email")
        phone = self.cleaned_data.get("phone")
        gender = self.cleaned_data.get("gender")
        verify_pic = self.cleaned_data.get("verify_pic")

        if str(username) in str(usercore.objects.all()):
            raise forms.ValidationError("Bu kullanıcı adı daha önceden alındı.")
            
        for who in usercore.objects.all():
            if str(who.email) == str(email):
                raise forms.ValidationError("Bu e-posta adresi daha önceden alındı.")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor")

        if universities.objects.filter(university_n=university) == None:
            raise forms.ValidationError("Bu üniversite kayıt yaptıramaz")
            
        for who in usercore.objects.all():
            if str(who.phone) == str(phone):
                raise forms.ValidationError("Bu telefon numarası kayıtlıdır")

        #if len(str(phone)) != 10:
            #raise forms.ValidationError("Girilen telefon numarası 10 haneli olmalıdır.")   
        
        if verify_pic == None:
            raise forms.ValidationError("Doğrulama belgesi zorunludur.")   

        value1 = {
            "username" : username,
            "password" : password,
            "name": name,
            "surname": surname,
            "university": university,
            "email": email,
            "phone": phone,
            "gender": gender,
            "verify_pic": verify_pic,
        }

        return value1

###----------------------------------------------------------------------------------------------------------------

class placer_registerForm(forms.Form):

    username = forms.CharField(max_length=20,label="Kullanıcı İsmi")
    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parola Tekrarı",widget=forms.PasswordInput)
    phone = forms.IntegerField(label="Telefon Numaranız:")
    min_price = forms.IntegerField(label="Asgari Fiyat")
    email = forms.EmailField(label="email Adresiniz:")
    area = forms.ModelChoiceField(queryset=places.objects.all(),label="Mekanınızın Konumu:")
    place_name = forms.CharField(max_length=20,label="Mekanınızın İsmi:")
    max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="Kaç adet oyunlu masayı tanı kullanabilecek?",required=True)
    max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="Kaç adet oyunsuz masayı tanı kullanabilecek?",required=True)

    verify_pic=forms.ImageField(label="Mekanınızın gerçekliğini doğrulayacak herhangi bir belge yükleyiniz:")

    def clean(self):

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        phone = self.cleaned_data.get("phone")
        email = self.cleaned_data.get("email")
        min_price = self.cleaned_data.get("min_price")
        area = self.cleaned_data.get("area")
        place_name = self.cleaned_data.get("place_name")
        max_table_normal = self.cleaned_data.get("max_table_normal")
        max_table_not_normal = self.cleaned_data.get("max_table_not_normal")
        verify_pic = self.cleaned_data.get("verify_pic")

        if str(username) in str(usercore.objects.all()):
            raise forms.ValidationError("Bu kullanıcı adı daha önceden alındı.")
            
        for who in usercore.objects.all():
            if str(who.email) == str(email):
                raise forms.ValidationError("Bu e-posta adresi daha önceden alındı.")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor")

        for who in usercore.objects.all():

            if str(who.phone) == str(phone):
                raise forms.ValidationError("Bu telefon numarası kayıtlıdır")

        if len(str(phone)) != 10:
            raise forms.ValidationError("Girilen telefon numarası 10 haneli olmalıdır.")   
        
        if verify_pic == None:
            raise forms.ValidationError("Doğrulama belgesi zorunludur.")   

        if min_price == None:
            raise forms.ValidationError("Depozito Fiyatı Girmeniz Zorunludur.")   
        
        values = {

            "username" : username,
            "password" : password,
            "email": email,
            "phone": phone,
            "area": area,
            "place_name" : place_name,
            "max_table_normal" : max_table_normal,
            "max_table_not_normal" : max_table_not_normal,
            "verify_pic": verify_pic,
            "min_price":min_price,
            }


        return values

###----------------------------------------------------------------------------------------------------------------

class loginForm(forms.Form):

    username = forms.CharField(max_length=20,label="Kullanıcı İsmi")
    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput)

###----------------------------------------------------------------------------------------------------------------

class placer_queryForm(forms.Form):

    max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="Kaç adet oyunlu masayı tanı kullanabilecek?",required=False)
    max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="Kaç adet oyunsuz masayı tanı kullanabilecek?",required=False)

    a11_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="bugün saat 9-12 oyunlu masa",required=False)
    a11_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="bugün saat 9-12 oyunsuz masa",required=False)
    a12_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="bugün saat 12-15 oyunlu masa",required=False)
    a12_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="bugün saat 9-12 oyunsuz masa",required=False)
    a13_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="bugün saat 15-18 oyunlu masa",required=False)
    a13_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="bugün saat 9-12 oyunsuz masa",required=False)
    a14_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="bugün saat 18-21 oyunlu masa",required=False)
    a14_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="bugün saat 21-22 oyunsuz masa",required=False)
    a15_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="bugün saat 21-22 oyunlu masa",required=False)
    a15_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="bugün saat 21-22 oyunsuz masa",required=False)
    a21_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="1 gün sonra saat 9-12 oyunlu masa",required=False)
    a21_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="1 gün sonra saat 9-12 oyunsuz masa",required=False)
    a22_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="1 gün sonra saat 12-15 oyunlu masa",required=False)
    a22_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="1 gün sonra saat 12-15 oyunsuz masa",required=False)
    a23_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="1 gün sonra saat 15-18 oyunlu masa",required=False)
    a23_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="1 gün sonra saat 15-18 oyunsuz masa",required=False)
    a24_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="1 gün sonra saat 18-21 oyunlu masa",required=False)
    a24_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="1 gün sonra saat 18-21 oyunsuz masa",required=False)
    a25_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="1 gün sonra saat 21-22 oyunlu masa",required=False)
    a25_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="1 gün sonra saat 21-22 oyunsuz masa",required=False)
    a31_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="2 gün sonra saat 9-12 oyunlu masa",required=False)
    a31_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="2 gün sonra saat 9-12 oyunsuz masa",required=False)
    a32_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="2 gün sonra saat 12-15 oyunlu masa",required=False)
    a32_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="2 gün sonra saat 9-12 oyunsuz masa",required=False)
    a33_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="2 gün sonra saat 15-18 oyunlu masa",required=False)
    a33_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="2 gün sonra saat 9-12 oyunsuz masa",required=False)
    a34_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="2 gün sonra saat 18-21 oyunlu masa",required=False)
    a34_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="2 gün sonra saat 21-22 oyunsuz masa",required=False)
    a35_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="2 gün sonra saat 21-22 oyunlu masa",required=False)
    a35_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="2 gün sonra saat 21-22 oyunsuz masa",required=False)
    a41_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="3 gün sonra saat 9-12 oyunlu masa",required=False)
    a41_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="3 gün sonra saat 9-12 oyunsuz masa",required=False)
    a42_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="3 gün sonra saat 12-15 oyunlu masa",required=False)
    a42_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="3 gün sonra saat 9-12 oyunsuz masa",required=False)
    a43_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="3 gün sonra saat 15-18 oyunlu masa",required=False)
    a43_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="3 gün sonra saat 9-12 oyunsuz masa",required=False)
    a44_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="3 gün sonra saat 18-21 oyunlu masa",required=False)
    a44_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="3 gün sonra saat 21-22 oyunsuz masa",required=False)
    a45_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="3 gün sonra saat 21-22 oyunlu masa",required=False)
    a45_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="3 gün sonra saat 21-22 oyunsuz masa",required=False)
    a51_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="4 gün sonra saat 9-12 oyunlu masa",required=False)
    a51_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="4 gün sonra saat 9-12 oyunsuz masa",required=False)
    a52_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="4 gün sonra saat 12-15 oyunlu masa",required=False)
    a52_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="4 gün sonra saat 9-12 oyunsuz masa",required=False)
    a53_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="4 gün sonra saat 15-18 oyunlu masa",required=False)
    a53_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="4 gün sonra saat 9-12 oyunsuz masa",required=False)
    a54_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="4 gün sonra saat 18-21 oyunlu masa",required=False)
    a54_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="4 gün sonra saat 21-22 oyunsuz masa",required=False)
    a55_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="4 gün sonra saat 21-22 oyunlu masa",required=False)
    a55_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="4 gün sonra saat 21-22 oyunsuz masa",required=False)
    a61_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="5 gün sonra saat 9-12 oyunlu masa",required=False)
    a61_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="5 gün sonra saat 9-12 oyunsuz masa",required=False)
    a62_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="5 gün sonra saat 12-15 oyunlu masa",required=False)
    a62_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="5 gün sonra saat 9-12 oyunsuz masa",required=False)
    a63_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="5 gün sonra saat 15-18 oyunlu masa",required=False)
    a63_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="5 gün sonra saat 9-12 oyunsuz masa",required=False)
    a64_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="5 gün sonra saat 18-21 oyunlu masa",required=False)
    a64_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="5 gün sonra saat 21-22 oyunsuz masa",required=False)
    a65_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="5 gün sonra saat 21-22 oyunlu masa",required=False)
    a65_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="5 gün sonra saat 21-22 oyunsuz masa",required=False)
    a71_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="6 gün sonra saat 9-12 oyunlu masa",required=False)
    a71_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="6 gün sonra saat 9-12 oyunsuz masa",required=False)
    a72_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="6 gün sonra saat 12-15 oyunlu masa",required=False)
    a72_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="6 gün sonra saat 9-12 oyunsuz masa",required=False)
    a73_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="6 gün sonra saat 15-18 oyunlu masa",required=False)
    a73_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="6 gün sonra saat 9-12 oyunsuz masa",required=False)
    a74_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="6 gün sonra saat 18-21 oyunlu masa",required=False)
    a74_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="6 gün sonra saat 21-22 oyunsuz masa",required=False)
    a75_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="6 gün sonra saat 21-22 oyunlu masa",required=False)
    a75_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="6 gün sonra saat 21-22 oyunsuz masa",required=False)
    a81_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="7 gün sonra saat 9-12 oyunlu masa",required=False)
    a81_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="7 gün sonra saat 9-12 oyunsuz masa",required=False)
    a82_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="7 gün sonra saat 12-15 oyunlu masa",required=False)
    a82_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="7 gün sonra saat 9-12 oyunsuz masa",required=False)
    a83_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="7 gün sonra saat 15-18 oyunlu masa",required=False)
    a83_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="7 gün sonra saat 9-12 oyunsuz masa",required=False)
    a84_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="7 gün sonra saat 18-21 oyunlu masa",required=False)
    a84_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="7 gün sonra saat 21-22 oyunsuz masa",required=False)
    a85_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="7 gün sonra saat 21-22 oyunlu masa",required=False)
    a85_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="7 gün sonra saat 21-22 oyunsuz masa",required=False)
    a91_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="8 gün sonra saat 9-12 oyunlu masa",required=False)
    a91_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="8 gün sonra saat 9-12 oyunsuz masa",required=False)
    a92_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="8 gün sonra saat 12-15 oyunlu masa",required=False)
    a92_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="8 gün sonra saat 9-12 oyunsuz masa",required=False)
    a93_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="8 gün sonra saat 15-18 oyunlu masa",required=False)
    a93_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="8 gün sonra saat 9-12 oyunsuz masa",required=False)
    a94_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="8 gün sonra saat 18-21 oyunlu masa",required=False)
    a94_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="8 gün sonra saat 21-22 oyunsuz masa",required=False)
    a95_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="8 gün sonra saat 21-22 oyunlu masa",required=False)
    a95_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="8 gün sonra saat 21-22 oyunsuz masa",required=False)
    a101_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="9 gün sonra saat 9-12 oyunlu masa",required=False)
    a101_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="9 gün sonra saat 9-12 oyunsuz masa",required=False)
    a102_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="9 gün sonra saat 12-15 oyunlu masa",required=False)
    a102_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="9 gün sonra saat 9-12 oyunsuz masa",required=False)
    a103_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="9 gün sonra saat 15-18 oyunlu masa",required=False)
    a103_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="9 gün sonra saat 9-12 oyunsuz masa",required=False)
    a104_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="9 gün sonra saat 18-21 oyunlu masa",required=False)
    a104_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="9 gün sonra saat 21-22 oyunsuz masa",required=False)
    a105_max_table_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="9 gün sonra saat 21-22 oyunlu masa",required=False)
    a105_max_table_not_normal = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+25)],label="9 gün sonra saat 21-22 oyunsuz masa",required=False)

    def clean(self):

        max_table_normal = self.cleaned_data.get("max_table_normal")
        max_table_not_normal = self.cleaned_data.get("max_table_not_normal")

        a11_max_table_normal = self.cleaned_data.get("a11_max_table_normal")
        a11_max_table_not_normal = self.cleaned_data.get("a11_max_table_not_normal")
        a12_max_table_normal = self.cleaned_data.get("a12_max_table_normal")
        a12_max_table_not_normal = self.cleaned_data.get("a12_max_table_not_normal")
        a13_max_table_normal = self.cleaned_data.get("a13_max_table_normal")
        a13_max_table_not_normal = self.cleaned_data.get("a13_max_table_not_normal")
        a14_max_table_normal = self.cleaned_data.get("a14_max_table_normal")
        a14_max_table_not_normal = self.cleaned_data.get("a14_max_table_not_normal")
        a15_max_table_normal = self.cleaned_data.get("a15_max_table_normal")
        a15_max_table_not_normal = self.cleaned_data.get("a15_max_table_not_normal")
        a21_max_table_normal = self.cleaned_data.get("a21_max_table_normal")
        a21_max_table_not_normal = self.cleaned_data.get("a21_max_table_not_normal")
        a22_max_table_normal = self.cleaned_data.get("a22_max_table_normal")
        a22_max_table_not_normal = self.cleaned_data.get("a22_max_table_not_normal")
        a23_max_table_normal = self.cleaned_data.get("a23_max_table_normal")
        a23_max_table_not_normal = self.cleaned_data.get("a23_max_table_not_normal")
        a24_max_table_normal = self.cleaned_data.get("a24_max_table_normal")
        a24_max_table_not_normal = self.cleaned_data.get("a24_max_table_not_normal")
        a25_max_table_normal = self.cleaned_data.get("a25_max_table_normal")
        a25_max_table_not_normal = self.cleaned_data.get("a25_max_table_not_normal")
        a31_max_table_normal = self.cleaned_data.get("a31_max_table_normal")
        a31_max_table_not_normal = self.cleaned_data.get("a31_max_table_not_normal")
        a32_max_table_normal = self.cleaned_data.get("a32_max_table_normal")
        a32_max_table_not_normal = self.cleaned_data.get("a32_max_table_not_normal")
        a33_max_table_normal = self.cleaned_data.get("a33_max_table_normal")
        a33_max_table_not_normal = self.cleaned_data.get("a33_max_table_not_normal")
        a34_max_table_normal = self.cleaned_data.get("a34_max_table_normal")
        a34_max_table_not_normal = self.cleaned_data.get("a34_max_table_not_normal")
        a35_max_table_normal = self.cleaned_data.get("a35_max_table_normal")
        a35_max_table_not_normal = self.cleaned_data.get("a35_max_table_not_normal")
        a41_max_table_normal = self.cleaned_data.get("a41_max_table_normal")
        a41_max_table_not_normal = self.cleaned_data.get("a41_max_table_not_normal")
        a42_max_table_normal = self.cleaned_data.get("a42_max_table_normal")
        a42_max_table_not_normal = self.cleaned_data.get("a42_max_table_not_normal")
        a43_max_table_normal = self.cleaned_data.get("a43_max_table_normal")
        a43_max_table_not_normal = self.cleaned_data.get("a43_max_table_not_normal")
        a44_max_table_normal = self.cleaned_data.get("a44_max_table_normal")
        a44_max_table_not_normal = self.cleaned_data.get("a44_max_table_not_normal")
        a45_max_table_normal = self.cleaned_data.get("a45_max_table_normal")
        a45_max_table_not_normal = self.cleaned_data.get("a45_max_table_not_normal")
        a51_max_table_normal = self.cleaned_data.get("a51_max_table_normal")
        a51_max_table_not_normal = self.cleaned_data.get("a51_max_table_not_normal")
        a52_max_table_normal = self.cleaned_data.get("a52_max_table_normal")
        a52_max_table_not_normal = self.cleaned_data.get("a52_max_table_not_normal")
        a53_max_table_normal = self.cleaned_data.get("a53_max_table_normal")
        a53_max_table_not_normal = self.cleaned_data.get("a53_max_table_not_normal")
        a54_max_table_normal = self.cleaned_data.get("a54_max_table_normal")
        a54_max_table_not_normal = self.cleaned_data.get("a54_max_table_not_normal")
        a55_max_table_normal = self.cleaned_data.get("a55_max_table_normal")
        a55_max_table_not_normal = self.cleaned_data.get("a55_max_table_not_normal")
        a61_max_table_normal = self.cleaned_data.get("a61_max_table_normal")
        a61_max_table_not_normal = self.cleaned_data.get("a61_max_table_not_normal")
        a62_max_table_normal = self.cleaned_data.get("a62_max_table_normal")
        a62_max_table_not_normal = self.cleaned_data.get("a62_max_table_not_normal")
        a63_max_table_normal = self.cleaned_data.get("a63_max_table_normal")
        a63_max_table_not_normal = self.cleaned_data.get("a63_max_table_not_normal")
        a64_max_table_normal = self.cleaned_data.get("a64_max_table_normal")
        a64_max_table_not_normal = self.cleaned_data.get("a64_max_table_not_normal")
        a65_max_table_normal = self.cleaned_data.get("a65_max_table_normal")
        a65_max_table_not_normal = self.cleaned_data.get("a65_max_table_not_normal")
        a71_max_table_normal = self.cleaned_data.get("a71_max_table_normal")
        a71_max_table_not_normal = self.cleaned_data.get("a71_max_table_not_normal")
        a72_max_table_normal = self.cleaned_data.get("a72_max_table_normal")
        a72_max_table_not_normal = self.cleaned_data.get("a72_max_table_not_normal")
        a73_max_table_normal = self.cleaned_data.get("a73_max_table_normal")
        a73_max_table_not_normal = self.cleaned_data.get("a73_max_table_not_normal")
        a74_max_table_normal = self.cleaned_data.get("a74_max_table_normal")
        a74_max_table_not_normal = self.cleaned_data.get("a74_max_table_not_normal")
        a75_max_table_normal = self.cleaned_data.get("a75_max_table_normal")
        a75_max_table_not_normal = self.cleaned_data.get("a75_max_table_not_normal")
        a81_max_table_normal = self.cleaned_data.get("a81_max_table_normal")
        a81_max_table_not_normal = self.cleaned_data.get("a81_max_table_not_normal")
        a82_max_table_normal = self.cleaned_data.get("a82_max_table_normal")
        a82_max_table_not_normal = self.cleaned_data.get("a82_max_table_not_normal")
        a83_max_table_normal = self.cleaned_data.get("a83_max_table_normal")
        a83_max_table_not_normal = self.cleaned_data.get("a83_max_table_not_normal")
        a84_max_table_normal = self.cleaned_data.get("a84_max_table_normal")
        a84_max_table_not_normal = self.cleaned_data.get("a84_max_table_not_normal")
        a85_max_table_normal = self.cleaned_data.get("a85_max_table_normal")
        a85_max_table_not_normal = self.cleaned_data.get("a85_max_table_not_normal")
        a91_max_table_normal = self.cleaned_data.get("a91_max_table_normal")
        a91_max_table_not_normal = self.cleaned_data.get("a91_max_table_not_normal")
        a92_max_table_normal = self.cleaned_data.get("a92_max_table_normal")
        a92_max_table_not_normal = self.cleaned_data.get("a92_max_table_not_normal")
        a93_max_table_normal = self.cleaned_data.get("a93_max_table_normal")
        a93_max_table_not_normal = self.cleaned_data.get("a93_max_table_not_normal")
        a94_max_table_normal = self.cleaned_data.get("a94_max_table_normal")
        a94_max_table_not_normal = self.cleaned_data.get("a94_max_table_not_normal")
        a95_max_table_normal = self.cleaned_data.get("a95_max_table_normal")
        a95_max_table_not_normal = self.cleaned_data.get("a95_max_table_not_normal")
        a101_max_table_normal = self.cleaned_data.get("a101_max_table_normal")
        a101_max_table_not_normal = self.cleaned_data.get("a101_max_table_not_normal")
        a102_max_table_normal = self.cleaned_data.get("a102_max_table_normal")
        a102_max_table_not_normal = self.cleaned_data.get("a102_max_table_not_normal")
        a103_max_table_normal = self.cleaned_data.get("a103_max_table_normal")
        a103_max_table_not_normal = self.cleaned_data.get("a103_max_table_not_normal")
        a104_max_table_normal = self.cleaned_data.get("a104_max_table_normal")
        a104_max_table_not_normal = self.cleaned_data.get("a104_max_table_not_normal")
        a105_max_table_normal = self.cleaned_data.get("a105_max_table_normal")
        a105_max_table_not_normal = self.cleaned_data.get("a105_max_table_not_normal")          

        value1 = {


            "max_table_normal" : max_table_normal,
            "max_table_not_normal" : max_table_not_normal,

            "a11_max_table_normal": a11_max_table_normal, 
            "a11_max_table_not_normal": a11_max_table_not_normal, 
            "a12_max_table_normal": a12_max_table_normal, 
            "a12_max_table_not_normal": a12_max_table_not_normal, 
            "a13_max_table_normal": a13_max_table_normal, 
            "a13_max_table_not_normal": a13_max_table_not_normal, 
            "a14_max_table_normal": a14_max_table_normal, 
            "a14_max_table_not_normal": a14_max_table_not_normal, 
            "a15_max_table_normal": a15_max_table_normal, 
            "a15_max_table_not_normal": a15_max_table_not_normal, 

            "a21_max_table_normal": a21_max_table_normal, 
            "a21_max_table_not_normal": a21_max_table_not_normal, 
            "a22_max_table_normal": a22_max_table_normal, 
            "a22_max_table_not_normal": a22_max_table_not_normal, 
            "a23_max_table_normal": a23_max_table_normal, 
            "a23_max_table_not_normal": a23_max_table_not_normal, 
            "a24_max_table_normal": a24_max_table_normal, 
            "a24_max_table_not_normal": a24_max_table_not_normal, 
            "a25_max_table_normal": a25_max_table_normal, 
            "a25_max_table_not_normal": a25_max_table_not_normal, 

            "a31_max_table_normal": a31_max_table_normal, 
            "a31_max_table_not_normal": a31_max_table_not_normal, 
            "a32_max_table_normal": a32_max_table_normal, 
            "a32_max_table_not_normal": a32_max_table_not_normal, 
            "a33_max_table_normal": a33_max_table_normal, 
            "a33_max_table_not_normal": a33_max_table_not_normal, 
            "a34_max_table_normal": a34_max_table_normal, 
            "a34_max_table_not_normal": a34_max_table_not_normal, 
            "a35_max_table_normal": a35_max_table_normal, 
            "a35_max_table_not_normal": a35_max_table_not_normal,

            "a41_max_table_normal": a41_max_table_normal, 
            "a41_max_table_not_normal": a41_max_table_not_normal, 
            "a42_max_table_normal": a42_max_table_normal, 
            "a42_max_table_not_normal": a42_max_table_not_normal, 
            "a43_max_table_normal": a43_max_table_normal, 
            "a43_max_table_not_normal": a43_max_table_not_normal, 
            "a44_max_table_normal": a44_max_table_normal, 
            "a44_max_table_not_normal": a44_max_table_not_normal, 
            "a45_max_table_normal": a45_max_table_normal, 
            "a45_max_table_not_normal": a45_max_table_not_normal,

            "a51_max_table_normal": a51_max_table_normal, 
            "a51_max_table_not_normal": a51_max_table_not_normal, 
            "a52_max_table_normal": a52_max_table_normal, 
            "a52_max_table_not_normal": a52_max_table_not_normal, 
            "a53_max_table_normal": a53_max_table_normal, 
            "a53_max_table_not_normal": a53_max_table_not_normal, 
            "a54_max_table_normal": a54_max_table_normal, 
            "a54_max_table_not_normal": a54_max_table_not_normal, 
            "a55_max_table_normal": a55_max_table_normal, 
            "a55_max_table_not_normal": a55_max_table_not_normal,

            "a61_max_table_normal": a61_max_table_normal, 
            "a61_max_table_not_normal": a61_max_table_not_normal, 
            "a62_max_table_normal": a62_max_table_normal, 
            "a62_max_table_not_normal": a62_max_table_not_normal, 
            "a63_max_table_normal": a63_max_table_normal, 
            "a63_max_table_not_normal": a63_max_table_not_normal, 
            "a64_max_table_normal": a64_max_table_normal, 
            "a64_max_table_not_normal": a64_max_table_not_normal, 
            "a65_max_table_normal": a65_max_table_normal, 
            "a65_max_table_not_normal": a65_max_table_not_normal, 

            "a71_max_table_normal": a71_max_table_normal, 
            "a71_max_table_not_normal": a71_max_table_not_normal, 
            "a72_max_table_normal": a72_max_table_normal, 
            "a72_max_table_not_normal": a72_max_table_not_normal, 
            "a73_max_table_normal": a73_max_table_normal, 
            "a73_max_table_not_normal": a73_max_table_not_normal, 
            "a74_max_table_normal": a74_max_table_normal, 
            "a74_max_table_not_normal": a74_max_table_not_normal, 
            "a75_max_table_normal": a75_max_table_normal, 
            "a75_max_table_not_normal": a75_max_table_not_normal,

            "a81_max_table_normal": a81_max_table_normal, 
            "a81_max_table_not_normal": a81_max_table_not_normal, 
            "a82_max_table_normal": a82_max_table_normal, 
            "a82_max_table_not_normal": a82_max_table_not_normal, 
            "a83_max_table_normal": a83_max_table_normal, 
            "a83_max_table_not_normal": a83_max_table_not_normal, 
            "a84_max_table_normal": a84_max_table_normal, 
            "a84_max_table_not_normal": a84_max_table_not_normal, 
            "a85_max_table_normal": a85_max_table_normal, 
            "a85_max_table_not_normal": a85_max_table_not_normal,

            "a91_max_table_normal": a91_max_table_normal, 
            "a91_max_table_not_normal": a91_max_table_not_normal, 
            "a92_max_table_normal": a92_max_table_normal, 
            "a92_max_table_not_normal": a92_max_table_not_normal, 
            "a93_max_table_normal": a93_max_table_normal, 
            "a93_max_table_not_normal": a93_max_table_not_normal, 
            "a94_max_table_normal": a94_max_table_normal, 
            "a94_max_table_not_normal": a94_max_table_not_normal, 
            "a95_max_table_normal": a95_max_table_normal, 
            "a95_max_table_not_normal": a95_max_table_not_normal,

            "a101_max_table_normal": a101_max_table_normal, 
            "a101_max_table_not_normal": a101_max_table_not_normal, 
            "a102_max_table_normal": a102_max_table_normal, 
            "a102_max_table_not_normal": a102_max_table_not_normal, 
            "a103_max_table_normal": a103_max_table_normal, 
            "a103_max_table_not_normal": a103_max_table_not_normal, 
            "a104_max_table_normal": a104_max_table_normal, 
            "a104_max_table_not_normal": a104_max_table_not_normal, 
            "a105_max_table_normal": a105_max_table_normal, 
            "a105_max_table_not_normal": a105_max_table_not_normal,

        }

        return value1

###----------------------------------------------------------------------------------------------------------------
  
class placer_updateForm(forms.Form):

    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput,required=False)
    confirm = forms.CharField(max_length=20,label="Parola Tekrarı",widget=forms.PasswordInput,required=False)
    
    phone = forms.IntegerField(label="Telefon Numaranız:",required=False)
    
    pic1 = forms.ImageField(label="Profil Fotoğrafınız",required=False)
    pic2 = forms.ImageField(label="Fotoğraf",required=False)
    pic3 = forms.ImageField(label="Fotoğraf",required=False)
    pic4 = forms.ImageField(label="Fotoğraf",required=False)
    pic5 = forms.ImageField(label="Fotoğraf",required=False)

    def clean(self):

        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        pic1 = self.cleaned_data.get("pic1")
        pic2 = self.cleaned_data.get("pic2")
        pic3 = self.cleaned_data.get("pic3")
        pic4 = self.cleaned_data.get("pic4")
        pic5 = self.cleaned_data.get("pic5")

        phone = self.cleaned_data.get("phone")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor")
       
        for who in usercore.objects.all():
            if str(who.phone) == str(phone):
                raise forms.ValidationError("Bu telefon numarası kayıtlıdır")

        #if len(str(phone)) != 10:
            #raise forms.ValidationError("Girilen telefon numarası 10 haneli olmalıdır.")   
        

        value1 = {

            "password" : password,
            "phone": phone,

            "pic1":pic1,
            "pic2":pic2,
            "pic3":pic3,
            "pic4":pic4,
            "pic5":pic5,

        }

        return value1

###----------------------------------------------------------------------------------------------------------------

class consumer_updateForm(forms.Form):

    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput,required=False)
    confirm = forms.CharField(max_length=20,label="Parola Tekrarı",widget=forms.PasswordInput,required=False)
    
    phone = forms.IntegerField(label="Telefon Numaranız:",required=False)
    
    pic1 = forms.ImageField(label="Profil Fotoğrafınız",required=False)
    pic2 = forms.ImageField(label="Fotoğraf",required=False)
    pic3 = forms.ImageField(label="Fotoğraf",required=False)
    pic4 = forms.ImageField(label="Fotoğraf",required=False)
    pic5 = forms.ImageField(label="Fotoğraf",required=False)
    bio = forms.CharField(max_length=1000,label="Bio")

    def clean(self):

        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        pic1 = self.cleaned_data.get("pic1")
        pic2 = self.cleaned_data.get("pic2")
        pic3 = self.cleaned_data.get("pic3")
        pic4 = self.cleaned_data.get("pic4")
        pic5 = self.cleaned_data.get("pic5")
        bio = self.cleaned_data.get("bio")

        phone = self.cleaned_data.get("phone")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor")
       
        for who in usercore.objects.all():
            if str(who.phone) == str(phone):
                raise forms.ValidationError("Bu telefon numarası kayıtlıdır")

        #if len(str(phone)) != 10:
            #raise forms.ValidationError("Girilen telefon numarası 10 haneli olmalıdır.")   
        

        value1 = {

            "password" : password,
            "phone": phone,

            "pic1":pic1,
            "pic2":pic2,
            "pic3":pic3,
            "pic4":pic4,
            "pic5":pic5,

            "bio":bio,

        }

        return value1

###----------------------------------------------------------------------------------------------------------------

class community_updateForm(forms.Form):

    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput,required=False)
    confirm = forms.CharField(max_length=20,label="Parola Tekrarı",widget=forms.PasswordInput,required=False)
    
    phone = forms.IntegerField(label="Telefon Numaranız:",required=False)
    
    pic1 = forms.ImageField(label="Profil Fotoğrafınız",required=False)


    def clean(self):

        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        pic1 = self.cleaned_data.get("pic1")

        phone = self.cleaned_data.get("phone")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor")
       
        for who in usercore.objects.all():
            if str(who.phone) == str(phone):
                raise forms.ValidationError("Bu telefon numarası kayıtlıdır")

        #if len(str(phone)) != 10:
            #raise forms.ValidationError("Girilen telefon numarası 10 haneli olmalıdır.")   
        

        value1 = {

            "password" : password,
            "phone": phone,

            "pic1":pic1,
        }

        return value1


class community_registerForm(forms.Form):

    username = forms.CharField(max_length=20,label="Kullanıcı İsmi")
    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parola Tekrarı",widget=forms.PasswordInput)
    name = forms.CharField(label="İsminiz:")
    email = forms.EmailField(label="email Adresiniz:")
    phone = forms.IntegerField(label="Telefon Numaranız:")
    verify_pic=forms.ImageField(label="Öğrenciliğinizi doğrulayacak herhangi bir belge yükleyiniz:")

    def clean(self):

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        name = self.cleaned_data.get("name")
        email = self.cleaned_data.get("email")
        phone = self.cleaned_data.get("phone")
        verify_pic = self.cleaned_data.get("verify_pic")

        if str(username) in str(usercore.objects.all()):
            raise forms.ValidationError("Bu kullanıcı adı daha önceden alındı.")
            
        for who in usercore.objects.all():
            if str(who.email) == str(email):
                raise forms.ValidationError("Bu e-posta adresi daha önceden alındı.")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor")
            
        for who in usercore.objects.all():
            if str(who.phone) == str(phone):
                raise forms.ValidationError("Bu telefon numarası kayıtlıdır") 
        
        if verify_pic == None:
            raise forms.ValidationError("Doğrulama belgesi zorunludur.")   

        value1 = {
            "username" : username,
            "password" : password,
            "name": name,
            "email": email,
            "phone": phone,
            "verify_pic": verify_pic,
        }

        return value1


class forgotForm(forms.Form):

    username = forms.CharField(max_length=20,label="Kullanıcı İsmi")
    email = forms.EmailField(label="email Adresiniz:")

    def clean(self):

        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")

        value1 = {
            "username" : username,
            "email": email,

        }

        return value1