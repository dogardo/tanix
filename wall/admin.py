from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(wallpost)
class activity_panel(admin.ModelAdmin):

    list_display=["id","creator","picture","text","area"] #paneli özelleştiren
    list_display_links=["id","creator"]  #basmalı yapan
    search_fields=["id"] #arama çubuğu oluşturan
    list_filter= ["id"] #sağda panel oluşturan
    
    class Meta:
        model=wallpost