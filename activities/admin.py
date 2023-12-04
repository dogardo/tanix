from django.contrib import admin
from .models import *

admin.site.register(places)
admin.site.register(universities)

#-------------------------------------------------------------------------ÖZEL ADMİN PANELİ DÜZGÜNLEŞTİRME----------------------------#

@admin.register(classic_activities)
class activity_panel(admin.ModelAdmin):

    list_display=["id","activity_name","activity_capacity","activity_picture","activity_cd"] #paneli özelleştiren
    list_display_links=["id","activity_name"]  #basmalı yapan
    search_fields=["activity_name"] #arama çubuğu oluşturan
    list_filter= ["activity_cd"] #sağda panel oluşturan
    
    class Meta:
        model=classic_activities

@admin.register(classic_room)
class activity_panel2(admin.ModelAdmin):

    list_display=["id","name","description","place","m_time","c_time","closing_time","if_its_anywhere","creator","game_type","entrance","ok_avab_1","ok_avab_2","max_ppl_existence"]
    list_display_links=["id","name"]  #basmalı yapan
    search_fields=["name"] #arama çubuğu oluşturan
    
    class Meta:
        model=classic_room

@admin.register(non_classic_activity_room)
class activity_panel3(admin.ModelAdmin):

    list_display=["id","name","description","place","m_time","c_time","closing_time","if_its_anywhere","creator","game_type","entrance","ok_avab_1","ok_avab_2"]
    list_display_links=["id","name"]  #basmalı yapan
    search_fields=["name"] #arama çubuğu oluşturan
    
    class Meta:
        model=non_classic_activity_room

@admin.register(placer_room)
class activity_panel4(admin.ModelAdmin):

    list_display=["id","creator","name","description","m_time","c_time","closing_time","if_its_anywhere","game_type"]
    list_display_links=["id","name"]  #basmalı yapan
    search_fields=["name"] #arama çubuğu oluşturan
    
    class Meta:
        model=placer_room

@admin.register(placer_room_query)
class activity_panel5(admin.ModelAdmin):

    list_display=["id","creator","name","description","m_time","c_time","closing_time","if_its_anywhere","game_type"]
    list_display_links=["id","name"]  #basmalı yapan
    search_fields=["name"] #arama çubuğu oluşturan
    
    class Meta:
        model=placer_room_query