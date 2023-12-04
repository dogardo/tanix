from asyncio.windows_events import NULL
from tkinter import Widget
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import *
from activities.models import *
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget,AdminSplitDateTime

class add_classic_activity_room_user(forms.Form):

    name = forms.CharField(label="Oda İsmi:")
    description = forms.CharField(label="Açıklama:")
    place = forms.ModelChoiceField(queryset=placer.objects.filter(verify=True), label="Gideceğiniz Mekan", required=False, empty_label="-----")
    m_time = forms.DateTimeField()
    if_its_anywhere = forms.ModelChoiceField(queryset=places.objects.all(), label="Buluşacağınız spesifik yer", required=False, empty_label="-----")
    game_type = forms.ModelChoiceField(queryset=classic_activities.objects.all(), label="Oyun Tipi")

    def clean(self):

        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        place = cleaned_data.get("place")
        m_time = cleaned_data.get("m_time")
        if_its_anywhere = cleaned_data.get("if_its_anywhere")
        game_type = cleaned_data.get("game_type")


        if place:
            try:
                place_obj = placer.objects.get(place_name=place)
            except placer.DoesNotExist:
                raise forms.ValidationError("Geçerli bir mekan seçin.")
            cleaned_data['place'] = place_obj.id
            cleaned_data['if_its_anywhere'] = "-----"
            print(place_obj.id)

        if if_its_anywhere:
            cleaned_data['place'] = None
            print(if_its_anywhere)


        if place and if_its_anywhere:
            raise forms.ValidationError("Hem mekan hem de spesifik yer belirtemezsiniz.")


        values = {
            "name": name,
            "description": description,
            "place": place,
            "m_time": m_time,
            "if_its_anywhere": if_its_anywhere,
            "game_type": game_type,
        }

        return values

class add_non_classic_activity_room_user(forms.Form):


    name = forms.CharField(label="Oda İsmi:")
    description = forms.CharField(label="Açıklama:")
    place = forms.ModelChoiceField(queryset=placer.objects.filter(verify=True),label="Gideceğiniz Mekan",required=False, empty_label="-----")
    m_time = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    if_its_anywhere = forms.ModelChoiceField(queryset=places.objects.all(),label="Buluşacağınız spesifik yer",required=False, empty_label="-----")
    game_type = forms.CharField(label="Oyun Tipi")
    max_ppl_existence = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+30)],label="maksimum kişi sayısı")

    def clean(self):

        cleaned_data = super().clean()

        name = self.cleaned_data.get("name")
        description = self.cleaned_data.get("description")
        place =  self.cleaned_data.get("place")
        m_time =  self.cleaned_data.get("m_time")
        if_its_anywhere =  self.cleaned_data.get("if_its_anywhere")
        game_type = self.cleaned_data.get("game_type")
        max_ppl_existence = self.cleaned_data.get("max_ppl_existence")


        if place:
            try:
                place_obj = placer.objects.get(place_name=place)
            except placer.DoesNotExist:
                raise forms.ValidationError("Geçerli bir mekan seçin.")
            
            cleaned_data['place'] = place_obj.id
            cleaned_data['if_its_anywhere'] = "-----"
            print(place_obj.id)

        if if_its_anywhere:
            cleaned_data['place'] = None
            print(if_its_anywhere)

        if place and if_its_anywhere:
            raise forms.ValidationError("hem mekan hem de spesifik yer belirtemezsiniz.")

        if (max_ppl_existence) > 30 and if_its_anywhere:
            raise forms.ValidationError("spesifik bir konumda, en fazla 30 kişi buluşabilirsiniz.")

        if (max_ppl_existence) > 6 and place:
            raise forms.ValidationError("mekanda, en fazla 6 kişi buluşabilirsiniz.")
                       
            
        values = {

            "name": name,
            "description": description,
            "place":place,
            "m_time":m_time,
            "if_its_anywhere":if_its_anywhere,
            "game_type":game_type,
            "max_ppl_existence":max_ppl_existence,
        }

        return values 

class change_classic_activity_room_user(forms.Form):

    name = forms.CharField(label="Oda İsmi:")
    description = forms.CharField(label="Açıklama:")

    def clean(self):

        name = self.cleaned_data.get("name")
        description = self.cleaned_data.get("description")

        values = {

            "name": name,
            "description": description,
        }

        return values 

class change_non_classic_activity_room_user(forms.Form):

    name = forms.CharField(label="Oda İsmi:")
    description = forms.CharField(label="Açıklama:")

    def clean(self):

        name = self.cleaned_data.get("name")
        description = self.cleaned_data.get("description")
            
        values = {

            "name": name,
            "description": description,
        }
        return values 

class message_Form(forms.Form):
    message_itself = forms.CharField(max_length=200,label="Mesajınız")
    
class add_placer_room(forms.Form):

    name = forms.CharField(label="Oda İsmi:")
    entry_price = forms.CharField(label="Entry Price")
    game_type = forms.CharField(label="Oyun Tipi")
    description = forms.CharField(label="Açıklama:")
    m_time = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    max_ppl_existence = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+50)],label="maksimum kişi sayısı")

    def clean(self):

        name = self.cleaned_data.get("name")
        description = self.cleaned_data.get("description")
        m_time =  self.cleaned_data.get("m_time")
        game_type = self.cleaned_data.get("game_type")
        entry_price = self.cleaned_data.get("entry_price")
        max_ppl_existence = self.cleaned_data.get("max_ppl_existence")

        ##---------    

        values = {

            "name": name,
            "description": description,
            "m_time":m_time,
            "game_type":game_type,
            "entry_price":entry_price,
            "max_ppl_existence":max_ppl_existence,

        }

        return values 

class change_placer_room(forms.Form):

    name = forms.CharField(label="Oda İsmi:")
    description = forms.CharField(label="Açıklama:")
    max_ppl_existence = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+50)],label="maksimum kişi sayısı")


    def clean(self):

        name = self.cleaned_data.get("name")
        description = self.cleaned_data.get("description")
        max_ppl_existence = self.cleaned_data.get("max_ppl_existence")

        ##---------    

        values = {

            "name": name,
            "description": description,
            "max_ppl_existence":max_ppl_existence,

        }

        return values 

class add_placer_query_room(forms.Form):

    name = forms.CharField(label="Oda İsmi:")
    entry_price = forms.CharField(label="Entry Price")

    fee = forms.IntegerField(label="fee",required=False)
    pay = forms.IntegerField(label="pay",required=False)

    game_type = forms.CharField(label="Oyun Tipi")
    description = forms.CharField(label="Açıklama:")
    m_time = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    max_ppl_existence = forms.IntegerField(validators=[MinValueValidator(+0), MaxValueValidator(+50)],label="maksimum kişi sayısı")
    if_its_anywhere = forms.ModelChoiceField(queryset=placer.objects.all(),label="Gideceğiniz Mekan",required=False, empty_label=None)
    room_node = forms.CharField(label="Not:")


    def clean(self):

        name = self.cleaned_data.get("name")
        description = self.cleaned_data.get("description")
        m_time =  self.cleaned_data.get("m_time")
        game_type = self.cleaned_data.get("game_type")
        entry_price = self.cleaned_data.get("entry_price")
        max_ppl_existence = self.cleaned_data.get("max_ppl_existence")
        if_its_anywhere = self.cleaned_data.get("if_its_anywhere")
        room_node = self.cleaned_data.get("room_node")
        fee = self.cleaned_data.get("fee")
        pay = self.cleaned_data.get("pay")

        ##---------    

        values = {

            "name": name,
            "description": description,
            "m_time":m_time,
            "game_type":game_type,
            "entry_price":entry_price,
            "max_ppl_existence":max_ppl_existence,
            "if_its_anywhere":if_its_anywhere,
            "room_node":room_node,
            "fee": fee,
            "pay": pay,

        }

        return values 
