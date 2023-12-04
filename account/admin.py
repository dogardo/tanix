from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

from django.core.paginator import Paginator
from django.core.cache import cache


class AccountInLine1(admin.StackedInline):
    model = consumer 
    can_delete = True
    verbose_name_plural = 'Accounts'

class AccountInLine2(admin.StackedInline):
    model = placer 
    can_delete = True
    verbose_name_plural = 'Accounts'

@admin.register(usercore)
class account_panel0(admin.ModelAdmin):
    list_display=["id","username","email","user_type","verify_pic","verify"]
    class Meta:
        model=usercore

@admin.register(consumer)
class account_panel1(admin.ModelAdmin):
    list_display=["id","username","email","name","surname","pic1","pic2","pic3","pic4","pic5","gender","university","phone","ranking","money","verify","can_enter_game"]
    list_display_links=["id"] 
    list_filter= ["username","email"] 
    class Meta:
        model=consumer

@admin.register(placer)
class account_panel2(admin.ModelAdmin):
    list_display=["id","min_price","username","email","place_name","pic1","pic2","pic3","pic4","pic5","max_table_normal","max_table_not_normal","place_avabiality_normal","place_avabiality_not_normal","area","acc_can_open_normal_game","acc_can_open_not_normal_game","phone","ranking","money","verify"]
    list_display_links=["id"] 
    list_filter= ["username","email"] 
    class Meta:
        model=placer

@admin.register(community)
class account_panel3(admin.ModelAdmin):
    list_display=["id","username","email","pic1","phone","ranking","money","verify"]
    list_display_links=["id"] 
    list_filter= ["username","email"] 
    class Meta:
        model=community

@admin.register(message_manager)
class account_panel1(admin.ModelAdmin):
    list_display=["id"]
    list_display_links=["id"] 
    class Meta:
        model=message_manager

