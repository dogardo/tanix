from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import *
from activities.models import *
from account.models import *
from django.utils import timezone
import secrets
import string



class wallpostForm(forms.Form):

    croom = forms.ModelChoiceField(queryset=classic_room.objects.none(), label="Hangi Etkinliğinize Ait Post Atacaksınız?", required=False, empty_label="-----")
    nroom = forms.ModelChoiceField(queryset=non_classic_activity_room.objects.none(), label="Hangi Etkinliğinize Ait Post Atacaksınız?", required=False, empty_label="-----")
    proom = forms.ModelChoiceField(queryset=placer_room.objects.none(), label="Hangi Etkinliğinize Ait Post Atacaksınız?", required=False, empty_label="-----")
    
    plac_es = forms.ModelChoiceField(queryset=places.objects.all() ,label="Konum?", required=False, empty_label="-----")
    text = forms.CharField(max_length=300, min_length=0, label="Post",required=False)
    picture = forms.ImageField(label="Görsel",required=False,widget=forms.FileInput)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(wallpostForm, self).__init__(*args, **kwargs)

        # Kullanıcıya ait consumer nesnesini alın
        try:
            consumer_obj = consumer.objects.get(username__username=user.username)
        except consumer.DoesNotExist:
            consumer_obj = None

        try:
            placer_obj = placer.objects.get(username__username=user.username)
        except placer.DoesNotExist:
            placer_obj = None

        try:
            community_obj = community.objects.get(username__username=user.username)
        except community.DoesNotExist:
            community_obj = None


        # Consumer nesnesi varsa ilgili classic_room, non_classic_activity_room ve placer_room queryset'lerini oluşturun
        if consumer_obj:
            croom_queryset = consumer_obj.in_classics.all()
            nroom_queryset = consumer_obj.in_non_classics.all()
            proom_queryset = consumer_obj.in_placer_rooms.all()

            # Seçim alanlarına queryset'leri ekleyin
            self.fields['croom'].queryset = croom_queryset
            self.fields['nroom'].queryset = nroom_queryset
            self.fields['proom'].queryset = proom_queryset

        if placer_obj:
            croom_queryset = placer_obj.existence_of_normal_game.all()
            nroom_queryset = placer_obj.existence_of_not_normal_game.all()

            the_usercore = usercore.objects.get(username=placer_obj.username)
            proom_queryset = placer_room.objects.filter(creator=the_usercore)

            self.fields['croom'].queryset = croom_queryset
            self.fields['nroom'].queryset = nroom_queryset
            self.fields['proom'].queryset = proom_queryset

        if community_obj:
            proom_queryset = placer_room.objects.filter(contact=community_obj.username)

            self.fields['proom'].queryset = proom_queryset


    def clean(self):
        cleaned_data = super().clean()

        croom = cleaned_data.get("croom")
        nroom = cleaned_data.get("nroom")
        proom = cleaned_data.get("proom")

        text = cleaned_data.get("text")
        picture = cleaned_data.get("picture")
        plac_es = cleaned_data.get("plac_es")

        if croom is None:
            cleaned_data["croom"] = "-----"

        if nroom is None:
            cleaned_data["nroom"] = "-----"

        if proom is None:
            cleaned_data["proom"] = "-----"
        
        if plac_es is None:
            cleaned_data["plac_es"] = "-----"
    
        if text:
            if (len(text) > 300) or (len(text) < 0):
                raise forms.ValidationError("Yazı, 300 karakteri geçemez")

        if (croom and nroom):
            raise forms.ValidationError("Sadece tek bir etkinlik seçebilirsiniz.")

        if (croom and proom):
            raise forms.ValidationError("Sadece tek bir etkinlik seçebilirsiniz.")

        if (nroom and proom):
            raise forms.ValidationError("Sadece tek bir etkinlik seçebilirsiniz.")     
        
        if (croom and proom and nroom):
            raise forms.ValidationError("Sadece tek bir etkinlik seçebilirsiniz.")

        if (croom and plac_es):
            raise forms.ValidationError("Hem konum hem etkinlik seçemezsiniz.")

        if (nroom and plac_es):
            raise forms.ValidationError("Hem konum hem etkinlik seçemezsiniz.")

        if (proom and plac_es):
            raise forms.ValidationError("Hem konum hem etkinlik seçemezsiniz.")
               
        value1 = {
            "croom": croom,
            "nroom": nroom,
            "proom": proom,
            "text": text,
            "picture": picture,
            "plac_es": plac_es,
        }

        return value1