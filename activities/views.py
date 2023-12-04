from contextlib import closing
from genericpath import exists
from operator import index
from urllib import request
from django.contrib import messages
import datetime
from django.db import models
from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render,HttpResponse
from .forms import *
from .models import *
from account.models import *
from account.forms import *
import uuid
import pytz
from django.utils import timezone
from django.core.paginator import Paginator, Page
from django.views.decorators.csrf import csrf_exempt
import traceback
from django.contrib.auth.decorators import login_required

from celery.schedules import crontab
from celery.task import periodic_task
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from infinite_scroll_pagination.paginator import SeekPaginator
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse

from endless_pagination.decorators import page_template
@login_required(login_url='index')
def real_classic_activities(request,id):

    the_usercore = request.user

    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    the_croom = get_object_or_404(classic_room,id=id)

    mform = message_Form(request.POST or None)

    if request.method == "POST" or None:

        if mform.is_valid():

            if ((the_user not in the_croom.ppl_existence.all())):

                messages.warning(request,"bunu yapmaya iznin yok.")    

                valuesx = {
                    "mform" : mform,
                    "room": get_object_or_404(classic_room,id=id),
                    "the_user":the_user,
                }

                return render(request,"ccactivities.html",valuesx)

            message_itself = mform.cleaned_data.get("message_itself")

            new_message = c_message(message_itself = message_itself, creator = the_user, room = the_croom)
            new_message.c_time = datetime.datetime.now()
            new_message.save()

            the_croom.chat.add(new_message)
            the_croom.save()

            messages.success(request,"mesaj eklendi")   

            valuesx = {

                "mform" : mform,
                "room": get_object_or_404(classic_room,id=id),
                "the_user":the_user,
            }

            return render(request,"ccactivities.html",valuesx)

        else:
            
            values = {
                "mform" : mform,
                "room": get_object_or_404(classic_room,id=id),
                "the_user":the_user,
            }

            messages.error(request,"Mesaj İletilemedi")
            return render(request,"ccactivities.html",values)
            
    
    values = {
                "mform" : mform,
                "room": get_object_or_404(classic_room,id=id),
                "the_user":the_user,
            }


    return render(request,"ccactivities.html",values)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def non_classic_activities(request,id): 

    the_usercore = request.user

    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    the_croom = get_object_or_404(non_classic_activity_room,id=id)

    mform = message_Form(request.POST or None)

    if request.method == "POST" or None:

        if mform.is_valid():

            if ((the_user not in the_croom.ppl_existence.all())):
                messages.warning(request,"bunu yapmaya iznin yok.")         
                values = {
                            "mform" : mform,
                            "room": get_object_or_404(non_classic_activity_room,id=id),
                            "the_user":the_user,
                            }


                return render(request,"ncactivities.html",values) 

            message_itself = mform.cleaned_data.get("message_itself")

            new_message = n_message(message_itself = message_itself, creator = the_user, room = the_croom)
            new_message.c_time = datetime.datetime.now()
            new_message.save()

            the_croom.chat.add(new_message)
            the_croom.save()

            messages.success(request,"mesaj eklendi")   

            valuesx = {
                "mform" : mform,
                "room": get_object_or_404(non_classic_activity_room,id=id),
                "the_user":the_user,
            }

            return render(request,"ncactivities.html",valuesx)

        else:
            
            values = {
                "mform" : mform,
                "room": get_object_or_404(non_classic_activity_room,id=id),
                "the_user":the_user,
            }

            messages.error(request,"Mesaj İletilemedi")
            return render(request,"ncactivities.html",values)
            
    
    values = {
                "mform" : mform,
                "room": get_object_or_404(non_classic_activity_room,id=id),
                "the_user":the_user,
                }


    return render(request,"ncactivities.html",values)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def change_croom(request,id):

    the_croom = get_object_or_404(classic_room,id=id)

    ccuform = change_classic_activity_room_user(request.POST or None, request.FILES or None)
    mform = message_Form(request.POST or None)
    
    if request.method == "POST" and ((request.user == the_croom.creator)):

        if ccuform.is_valid():

            if ((request.user != the_croom.creator)):
    
                value10 = {
                "room" : the_croom,
                "mform" : mform,
                }


                messages.error(request,"Buraya bakmaya yetkiniz yok...")
                return render(request,"ccactivities.html",value10) 

            name = ccuform.cleaned_data.get("name")
            description = ccuform.cleaned_data.get("description")

            the_croom.name = name
            the_croom.description = description
            the_croom.save()

            all_games_c = classic_room.objects.all()
            all_games_n = non_classic_activity_room.objects.all()
            

            value10 = {
            "room" : the_croom,
            "mform" : mform,
            }

            messages.success(request,"ayarlar yapıldı.")
            return render(request,"ccactivities.html",value10)

        else:
            
            ccuform = change_classic_activity_room_user()
            value10 = {
            "room" : the_croom,
            "ccuform" : ccuform, 
            }

            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"update_ccc.html",value10)
    
    elif (request.user == the_croom.creator):

        value10 = {
        "room" : the_croom,
        "ccuform" : ccuform, 
        }
        
        return render(request,"update_ccc.html",value10)
    
    else:
        
        value10 = {
        "room" : the_croom,
        "mform" : mform,
        }


        messages.error(request,"Buraya bakmaya yetkiniz yok...")
        return render(request,"ccactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def change_nroom(request,id):

    the_nroom = get_object_or_404(non_classic_activity_room,id=id)
    ncuform = change_non_classic_activity_room_user(request.POST or None, request.FILES or None)
    mform = message_Form(request.POST or None)

    if request.method == "POST" and ((request.user == the_nroom.creator)):

        if ncuform.is_valid():

            if ((request.user != the_nroom.creator)):
                        
                value10 = {
                "ncuform" : ncuform, 
                "room" : the_nroom,
                "mform":mform,
                }
                
                messages.warning(request,"bunu yapmaya iznin yok.") 
                return render(request,"ncactivities.html",value10)

            name = ncuform.cleaned_data.get("name")
            description = ncuform.cleaned_data.get("description")

            the_nroom.name = name
            the_nroom.description = description
            the_nroom.save()

            
            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }

            messages.success(request,"değişiklikler kaydedildi")
            return render(request,"ncactivities.html",value10)

        else:

            value10 = {
            "ncuform" : ncuform, 
            "room" : the_nroom,
            }

            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"update_ncc.html",value10)

    elif (request.user == the_nroom.creator):

        value10 = {
        "room" : the_nroom,
        "ncuform" : ncuform,
        }

        return render(request,"update_ncc.html",value10) 

    else:
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }

        messages.error(request,"Buraya bakmaya yetkiniz yok...")
        return render(request,"ncactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def delete_nroom(request,id):

    the_nroom = get_object_or_404(non_classic_activity_room,id=id)
    timenow = datetime.datetime.now()

    closing_timing = the_nroom.m_time - datetime.timedelta(hours=3)
    now = datetime.datetime.now(datetime.timezone.utc)
    mform = message_Form(request.POST or None)

    if now >= closing_timing:
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }

        messages.warning(request,"3 saatten az kaldı, artık silemezsin.")    
        return render(request,"ncactivities.html",value10)  
    
    if ((request.user != the_nroom.creator)):

        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }

        messages.warning(request,"bunu yapmaya iznin yok")    
        return render(request,"ncactivities.html",value10)  

    if int(timenow.timestamp()) >= int(the_nroom.closing_time.timestamp()):
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }

        messages.warning(request,"lobi kapandı, artık silemezsin.")    
        return render(request,"ncactivities.html",value10)      

    if the_nroom.place:
        for people in the_nroom.ppl_existence.all():
            people.money = people.money + the_nroom.place.min_price
            the_nroom.place.money = the_nroom.place.money - the_nroom.place.min_price
            the_nroom.place.save()
            people.save()

    the_nroom.delete()
    messages.success(request,(the_nroom.name ,"isimli odayı sildik"))

    if request.user.user_type == 2:

        all_games_c = classic_room.objects.all()
        all_games_n = non_classic_activity_room.objects.all()
        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)

        gamevalues={

            "all_games_c":all_games_c,
            "all_games_n":all_games_n,
            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
        }

        return render(request,"games.html",gamevalues)
    
    else:
        allplacers = placer.objects.all()
        allcommunities = community.objects.all()
        allactivities = classic_activities.objects.all()
        values= {
            "placer":allplacers,
            "community":allcommunities,
            "activities":allactivities,
        }

        return render(request,"index.html",values)      

###---------------------------------------burada kaldık.

@login_required(login_url='index')
def delete_croom(request,id):
    the_croom = get_object_or_404(classic_room,id=id)
    timenow = datetime.datetime.now()
    mform = message_Form(request.POST or None)

    closing_timing = the_croom.m_time - datetime.timedelta(hours=3)
    now = datetime.datetime.now(datetime.timezone.utc)

    if now >= closing_timing:
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }

        messages.warning(request,"3 saatten az kaldı, artık silemezsin.")    
        return render(request,"ccactivities.html",value10)  
    
    if ((request.user != the_croom.creator)):
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }

        messages.warning(request,"Bunu yapmaya iznin yok")    
        return render(request,"ccactivities.html",value10)      

    if int(timenow.timestamp()) >= int(the_croom.closing_time.timestamp()):
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }

        messages.warning(request,"Lobi kapandı, bunu yapmaya iznin yok.")    
        return render(request,"ccactivities.html",value10)      

    if the_croom.place:
        for people in the_croom.ppl_existence.all():
            people.money = people.money + the_croom.place.min_price
            the_croom.place.money = the_croom.place.money - the_croom.place.min_price
            the_croom.place.save()
            people.save()
            
    the_croom.delete()
    messages.success(request,(the_croom.name ,"isimli odayı sildik"))

    if request.user.user_type == 2:
        all_games_c = classic_room.objects.all()
        all_games_n = non_classic_activity_room.objects.all()
        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)

        gamevalues={

            "all_games_c":all_games_c,
            "all_games_n":all_games_n,
            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
        }
    
        return render(request,"games.html",gamevalues)
    
    else:

        allplacers = placer.objects.all()
        allcommunities = community.objects.all()
        allactivities = classic_activities.objects.all()
        values= {
            "placer":allplacers,
            "community":allcommunities,
            "activities":allactivities,
        }

        return render(request,"index.html",values)

###------------------------------------------------------

@login_required(login_url='index')
def delete_proom(request,id):

    the_proom = get_object_or_404(placer_room,id=id)
    timenow = datetime.datetime.now()
    mform = message_Form(request.POST or None)

    closing_timing = the_proom.m_time - datetime.timedelta(hours=3)
    now = datetime.datetime.now(datetime.timezone.utc)

    if now >= closing_timing:
        value10 = {
        "room" : the_proom,
        "mform":mform,
        }

        messages.warning(request,"3 saatten az kaldı, artık silemezsin.")    
        return render(request,"nactivities.html",value10)  
     
    
    if ((request.user != the_proom.creator) or (request.user != the_proom.contact)):
        value10 = {
        "room" : the_proom,
        "mform":mform,
        }

        messages.warning(request,"Bunu yapmaya iznin yok")    
        return render(request,"nactivities.html",value10)  

    if int(timenow.timestamp()) >= int(the_proom.closing_time.timestamp()):
        value10 = {
        "room" : the_proom,
        "mform":mform,
        }

        messages.warning(request,"3 saatten az kaldı, artık silemezsin.")    
        return render(request,"nactivities.html",value10)     

    for people in the_proom.ppl_existence.all():

        people.money = people.money + the_proom.entry_price
        people.save()

        
        if the_proom.contact:

            if the_proom.fee:

                the_proom.cretor.money = the_proom.creator.money - the_proom.fee
                the_proom.creator.save()

                the_communitycore = usercore.objects.get(username=the_proom.contact)
                the_community = community.objects.get(username_id=the_communitycore.id)

                the_community.money = the_community.money - the_proom.entry_price + the_proom.fee
                the_community.save()

            else:
   
                the_communitycore = usercore.objects.get(username=the_proom.contact)
                the_community = community.objects.get(username_id=the_communitycore.id)

                the_community.money = the_community.money - the_proom.entry_price
                the_community.save()

        else:
            
            the_proom.cretor.money = the_proom.creator.money - the_proom.entry_price
            the_proom.creator.save()       
        

        people.save()

    if the_proom.pay:

        the_communitycore = usercore.objects.get(username=the_proom.contact)
        the_community = community.objects.get(username_id=the_communitycore.id)

        the_community.money = the_community.money + the_proom.pay
        the_community.save()

        the_proom.creator.money = the_proom.creator.money - the_proom.pay
        the_proom.creator.save()
        
    the_proom.delete()

    messages.success(request,(the_proom.name ,"isimli odayı sildik"))

    if request.user.user_type == 2:

        all_games_c = classic_room.objects.all()
        all_games_n = non_classic_activity_room.objects.all()
        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)

        gamevalues={

            "all_games_c":all_games_c,
            "all_games_n":all_games_n,
            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
        }

        return render(request,"games.html",gamevalues)
    
    else:

        allplacers = placer.objects.all()
        allcommunities = community.objects.all()
        allactivities = classic_activities.objects.all()
        values= {
            "placer":allplacers,
            "community":allcommunities,
            "activities":allactivities,
        }

        return render(request,"index.html",values)       

###---------------------------------------------------------

@login_required(login_url='index')
def quit_nroom(request,id):

    mform = message_Form(request.POST or None)
    the_usercore = get_object_or_404(usercore,username=request.user.username)

    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    the_nroom = get_object_or_404(non_classic_activity_room,id=id)

    if ((request.user.username != the_usercore.username)) or (request.user.user_type != 2):

        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }

        messages.warning(request,"bunu yapmaya iznin yok.") 

        if request.user.user_type != 2:
            allplacers = placer.objects.all()
            allcommunities = community.objects.all()
            allactivities = classic_activities.objects.all()
            values= {
                "placer":allplacers,
                "community":allcommunities,
                "activities":allactivities,
            }

            return render(request,"index.html",values)
           
        return render(request,"ncactivities.html",value10)      

    threehour = datetime.timedelta(hours=3)
    closing_timing = the_nroom.m_time-threehour
    now = datetime.datetime.now(datetime.timezone.utc)

    if now >= closing_timing:
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }

        messages.warning(request,"3 saatten az var. lobiden çıkamazsın.")    
        return render(request,"ncactivities.html",value10)   

    if the_user in the_nroom.ppl_existence.all():

        count_ppl = the_nroom.ppl_existence.count()
        
        if count_ppl == 1:
            if the_nroom.place:
                the_user.money = the_user.money + the_nroom.place.min_price
                the_user.save()

                the_nroom.place.money = the_nroom.place.money - the_nroom.place.min_price
                the_nroom.place.save()
            the_nroom.delete()

        elif count_ppl > 1:

            if the_nroom.place:
                the_user.money = the_user.money + the_nroom.place.min_price
                the_user.save()

                the_nroom.place.money = the_nroom.place.money - the_nroom.place.min_price
                the_nroom.place.save()

            the_nroom.ppl_existence.remove(the_user)

            the_nroom.save()


            for new_creator in the_nroom.ppl_existence.all():

                core_new_creator = usercore.objects.get(username=new_creator.username)
                the_nroom.creator = core_new_creator
                the_user.in_non_classics.remove(the_nroom)
                
                the_nroom.save()
                core_new_creator.save()
                the_usercore.save()
                the_user.save()
                break
        


        messages.success(request,(the_nroom,"lobisinden başarıyla çıkıldı."))

        all_games_c = classic_room.objects.all()
        all_games_n = non_classic_activity_room.objects.all()
        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)
        timenow = datetime.datetime.now()
        
        gamevalues={

            "all_games_c":all_games_c,
            "all_games_n":all_games_n,
            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
        }

        return render(request,"games.html",gamevalues)

    else:

        messages.warning(request,"bir hata oldu, çıkış yapılamadı")

        timenow = datetime.datetime.now()
        the_nroom = the_nroom

        gamevalues={

            "timenow":timenow,
            "room":the_nroom,
        }

        return render(request,"ncactivities.html",gamevalues)
###---------------------------------------------------------------------------

@login_required(login_url='index')
def quit_croom(request,id):

    the_usercore = get_object_or_404(usercore,username=request.user.username)

    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    the_croom = get_object_or_404(classic_room,id=id)

    if ((request.user.username != the_usercore.username) or (request.user.user_type != 2)):
        messages.warning(request,"bunu yapmaya iznin yok.")
         
        if request.user.user_type != 2:
            allplacers = placer.objects.all()
            allcommunities = community.objects.all()
            allactivities = classic_activities.objects.all()
            values= {
                "placer":allplacers,
                "community":allcommunities,
                "activities":allactivities,
            }

            return render(request,"index.html",values)

        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)
        timenow = datetime.datetime.now()
        the_croom = the_croom

        gamevalues={

            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
            "room":the_croom,
        }

        return render(request,"ccactivities.html",gamevalues)

    threehour = datetime.timedelta(hours=3)
    closing_timing = the_croom.m_time-threehour
    now = datetime.datetime.now(datetime.timezone.utc)

    if now >= closing_timing:
        messages.warning(request,"3 saatten az kaldı, artık çıkamazsın.")         
        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)
        timenow = datetime.datetime.now()
        the_croom = the_croom

        gamevalues={

            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
            "room":the_croom,
        }

        return render(request,"ccactivities.html",gamevalues)
    
    if the_user in the_croom.ppl_existence.all():
       
        count_ppl = the_croom.ppl_existence.count()
        
        if count_ppl == 1:

            if the_croom.place:
                the_user.money = the_user.money + the_croom.place.min_price
                the_user.save()
                
                the_croom.place.money = the_croom.place.money - the_croom.place.min_price
                the_croom.place.save()
                
            the_croom.delete()


        elif count_ppl > 1:

            if the_croom.place:
                the_user.money = the_user.money + the_croom.place.min_price
                the_user.save()
                
                the_croom.place.money = the_croom.place.money - the_croom.place.min_price
                the_croom.place.save()

            the_croom.ppl_existence.remove(the_user)
            the_croom.save()

            for new_creator in the_croom.ppl_existence.all():
                core_new_creator = usercore.objects.get(username=new_creator.username)
                the_user.in_classics.remove(the_croom)
                the_croom.creator = core_new_creator
                the_croom.save()
                core_new_creator.save()
                the_usercore.save()
                the_user.save()
                break

        messages.success(request,(the_croom,"lobisinden başarıyla çıkıldı."))

        all_games_c = classic_room.objects.all()
        all_games_n = non_classic_activity_room.objects.all()
        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)
        timenow = datetime.datetime.now()
        
        gamevalues={

            "all_games_c":all_games_c,
            "all_games_n":all_games_n,
            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
        }

        return render(request,"games.html",gamevalues)

    else:
        messages.warning(request,"bir hata oldu, çıkış yapılamadı")

        timenow = datetime.datetime.now()
        the_croom = the_croom
        gamevalues={

            "timenow":timenow,
            "room":the_croom,
        }

        return render(request,"ccactivities.html",gamevalues)

###---------------------------------------------------------------------------
@login_required(login_url='index')
def quit_proom(request,id):

    the_usercore = get_object_or_404(usercore,username=request.user.username)

    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    the_proom = get_object_or_404(placer_room,id=id)

    threehour = datetime.timedelta(hours=3)
    closing_timing = the_proom.m_time-threehour
    now = datetime.datetime.now(datetime.timezone.utc)

    if now >= the_proom.c_time:
        
        messages.warning(request,"3 saatten az kaldı, artık çıkamazsın.")         
        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)
        timenow = datetime.datetime.now()

        gamevalues={

            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
            "room":the_proom,
        }

        return render(request,"pactivities.html",gamevalues)  
    
    if ((request.user.username != the_usercore.username) and (request.user.user_type != 2)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)
        timenow = datetime.datetime.now()
        the_nroom = the_nroom

        gamevalues={

            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
            "room":the_proom,
        }

        return render(request,"ncactivities.html",gamevalues)

    if the_user in the_proom.ppl_existence.all():
       
        the_user.in_placer_rooms.remove(the_proom)
        the_proom.ppl_existence.remove(the_user)

        the_user.money = the_user.money + the_proom.entry_price

        if the_proom.contact:

            if the_proom.fee:

                the_proom.cretor.money = the_proom.creator.money - the_proom.fee
                the_proom.creator.save()

                the_communitycore = usercore.objects.get(username=the_proom.contact)
                the_community = community.objects.get(username_id=the_communitycore.id)

                the_community.money = the_community.money - the_proom.entry_price + the_proom.fee
                the_community.save()

            else:
   
                the_communitycore = usercore.objects.get(username=the_proom.contact)
                the_community = community.objects.get(username_id=the_communitycore.id)

                the_community.money = the_community.money - the_proom.entry_price
                the_community.save()

        else:
            
            the_proom.cretor.money = the_proom.creator.money - the_proom.entry_price
            the_proom.creator.save() 


        the_proom.save()
        the_user.save()

        
        all_games_c = classic_room.objects.all()
        all_games_n = non_classic_activity_room.objects.all()
        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)
        timenow = datetime.datetime.now()
        
        gamevalues={

            "all_games_c":all_games_c,
            "all_games_n":all_games_n,
            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
        }

        messages.success(request,(the_proom,"lobisinden başarıyla çıkıldı."))
        return render(request,"games.html",gamevalues)

    else:

        messages.warning(request,"bir hata oldu, lobiden çıkış yapılamadı")
        timenow = datetime.datetime.now()

        gamevalues={

            "timenow":timenow,
            "room":the_proom,
        }

        return render(request,"ncactivities.html",gamevalues)

###--------------------------------------------------burada kaldık.

@login_required(login_url='index')
def request_nroom(request,id):

    the_usercore = get_object_or_404(usercore,username=request.user.username)

    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    the_nroom = get_object_or_404(non_classic_activity_room,id=id)
    mform = message_Form(request.POST or None)

    if ((request.user.user_type != 2)):
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }
        
        messages.warning(request,"bunu yapmaya iznin yok.") 
        return render(request,"ncactivities.html",value10)

    if the_nroom.place:
        if the_nroom.place.min_price > the_user.money:
            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            messages.warning(request,"bakiyen yok, yükleyip tekrar dene") 
            return render(request,"ncactivities.html",value10)

    if the_nroom.creator in the_user.ibanned.all():
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }
        
        messages.warning(request,"engel yemişsin.") 
        return render(request,"ncactivities.html",value10)

    the_nroom.offers.add(the_user)

    value10 = {
    "room" : the_nroom,
    "mform":mform,
    }
    
    messages.warning(request,"başarıyla istek atıldı.") 
    return render(request,"ncactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def request_nroom_n(request,id,username):

    mform = message_Form(request.POST or None)
    the_nroom = get_object_or_404(non_classic_activity_room,id=id)

    if ((request.user != the_nroom.creator) and (request.user.user_type != 2)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }
        
        return render(request,"ncactivities.html",value10)
    
    
    if request.user.user_type == 2:
        the_offerer_core = get_object_or_404(usercore,username=username)
        the_offerer = consumer.objects.get(username_id=the_offerer_core.id)

        the_usercore = usercore.objects.get(username=request.user.username)
        the_user = consumer.objects.get(username_id=the_usercore.id)

        if (the_usercore == the_nroom.creator) and (the_nroom.max_ppl_existence >= the_nroom.ppl_existence):
            the_nroom.offers.remove(the_offerer)
            the_nroom.save()

            messages.success(request,"kişi başarıyla reddedildi")
            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            return render(request,"ncactivities.html",value10)
        
        else:
            messages.error(request,"hata")

            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            return render(request,"ncactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index') 
def request_nroom_y(request,id,username):


    the_nroom = get_object_or_404(non_classic_activity_room,id=id)
    mform = message_Form(request.POST or None)

    if ((request.user != the_nroom.creator) and (request.user.user_type != 2)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }
        
        return render(request,"ncactivities.html",value10)
    
    if request.user.user_type == 2:

        the_offerer_core = get_object_or_404(usercore,username=username)
        the_offerer = consumer.objects.get(username_id=the_offerer_core.id)

        the_usercore = usercore.objects.get(username=request.user.username)
        the_user = consumer.objects.get(username_id=the_usercore.id)

        if the_nroom.place:
            if the_nroom.place.min_price > the_offerer.money:
                the_offerer.n_room_offers.remove(the_nroom)   
                messages.warning(request,"kişinin yeterli bakiyesi kalmamış, reddedildi")
                value10 = {
                "room" : the_nroom,
                "mform":mform,
                }
                
                return render(request,"ncactivities.html",value10)    


        if (the_usercore == the_nroom.creator) and (the_nroom.max_ppl_existence >= the_nroom.ppl_existence.count()):
            if the_nroom.place:
                                
                                
                the_placer = placer.objects.get(username_id=the_nroom.place.id)
                the_placer.money = the_placer.money + the_nroom.place.min_price
                the_placer.save()

                the_offerer.money = the_offerer.money - the_nroom.place.min_price

            the_nroom.offers.remove(the_offerer)
            the_nroom.ppl_existence.add(the_offerer)
            the_offerer.in_non_classics.add(the_nroom)
            the_offerer.save()
            the_nroom.save()

            messages.success(request,"kişi başarıyla eklendi")
            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            return render(request,"ncactivities.html",value10)
        
        else:

            messages.error(request,"hata")

            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            return render(request,"ncactivities.html",value10)

###-------------------------------------------------buradayız

@login_required(login_url='index')
def request_croom(request,id):

    mform = message_Form(request.POST or None)
    the_usercore = get_object_or_404(usercore,username=request.user.username)
    the_croom = get_object_or_404(classic_room,id=id)

    if ((request.user.user_type != 2)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }
        
        return render(request,"ccactivities.html",value10)
    
    if request.user.user_type == 2:

        the_user = consumer.objects.get(username_id=the_usercore.id)
        


        if the_croom.place:
            if the_croom.place.min_price > the_user.money:
                messages.warning(request,"bakiyen yok, bakiye yükleyip tekrar dene")
                value10 = {
                "room" : the_croom,
                "mform":mform,
                }
                
                return render(request,"ccactivities.html",value10)

        if the_croom.creator in the_user.ibanned.all():
            messages.warning(request,"kişi seni engellemiş, lobiye davet atamazsın. üzgünüz...")         
            value10 = {
            "room" : the_croom,
            "mform":mform,
            }
            
            return render(request,"ccactivities.html",value10)

        the_croom.offers.add(the_user)

        messages.success(request,(the_croom.name,"lobisine başarıyla istek atıldı"))
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }
        
        return render(request,"ccactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def request_croom_n(request,id,username):

    mform = message_Form(request.POST or None)
    the_croom = get_object_or_404(classic_room,id=id)

    if ((request.user != the_croom.creator) and (request.user.user_type != 2)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }
        
        return render(request,"ccactivities.html",value10)
    
    if request.user.user_type == 2:

        the_offerer_core = get_object_or_404(usercore,username=username)
        the_offerer = consumer.objects.get(username_id=the_offerer_core.id)


        the_usercore = usercore.objects.get(username=request.user.username)
        the_user = consumer.objects.get(username_id=the_usercore.id)

        if (the_usercore == the_croom.creator):
            the_croom.offers.remove(the_offerer)
            the_croom.save()

            messages.success(request,"kişi başarıyla silindi")
            value10 = {
            "room" : the_croom,
            "mform":mform,
            }
            
            return render(request,"ccactivities.html",value10)
        else:
            messages.error(request,"hata")

            value10 = {
            "room" : the_croom,
            "mform":mform,
            }
            
            return render(request,"ccactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def request_croom_y(request,id,username):

    the_croom = get_object_or_404(classic_room,id=id)
    mform = message_Form(request.POST or None)

    if ((request.user != the_croom.creator) and (request.user.user_type != 2)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }
        
        return render(request,"ccactivities.html",value10)
    
    if request.user.user_type == 2:

        the_offerer_core = get_object_or_404(usercore,username=username)
        the_offerer = consumer.objects.get(username_id=the_offerer_core.id)

        the_usercore = usercore.objects.get(username=request.user.username)
        the_user = consumer.objects.get(username_id=the_usercore.id)

        


        if the_croom.place:

            if the_croom.place.min_price > the_offerer.money:
                the_offerer.c_room_offers.remove(the_croom)   
                messages.warning(request,"kişinin yeterli bakiyesi kalmamış, reddedildi")
                value10 = {
                "room" : the_croom,
                "mform":mform,
                }
                
                return render(request,"ccactivities.html",value10)

        if (the_usercore == the_croom.creator) and (the_croom.max_ppl_existence > the_croom.ppl_existence.count()):

            if the_croom.place:

                the_placer = placer.objects.get(username_id=the_croom.place.id)
                the_placer.money = the_placer.money + the_croom.place.min_price
                the_placer.save()

                the_offerer.money = the_offerer.money - the_croom.place.min_price
                the_offerer.save()
                
            the_croom.offers.remove(the_offerer)
            the_croom.ppl_existence.add(the_offerer)
            the_offerer.in_classics.add(the_croom)
            the_offerer.save()
            the_croom.save()

            messages.success(request,"kişi başarıyla eklendi")
            value10 = {
            "room" : the_croom,
            "mform":mform,
            }
            
            return render(request,"ccactivities.html",value10)
           
        else:

            messages.error(request,"hata")
            value10 = {
            "room" : the_croom,
            "mform":mform,
            }
            
            return render(request,"ccactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def add_choose(request):
    return render(request,"add_choose.html")



@login_required(login_url='index')
def add_classic_room(request): 

    all_activities = classic_activities.objects.all()
    placers_all = placer.objects.all()
    areas_all = places.objects.all()

    if request.user.user_type != 2:
        allplacers = placer.objects.all()
        allcommunities = community.objects.all()
        allactivities = classic_activities.objects.all()
        values= {
            "placer":allplacers,
            "community":allcommunities,
            "activities":allactivities,
        }
        messages.success(request,"no.")
        return render(request,"index.html",values)

    if request.method == "POST":

        cccform = add_classic_activity_room_user(request.POST)

        if cccform.is_valid():

            creator = request.user

            name = cccform.cleaned_data.get("name")
            description = cccform.cleaned_data.get("description")
            place =  cccform.cleaned_data.get("place")
            m_time =  cccform.cleaned_data.get("m_time")
            if_its_anywhere = cccform.cleaned_data.get("if_its_anywhere")
            game_type = cccform.cleaned_data.get("game_type")



            xv = classic_activities.objects.get(activity_name=game_type)
            pplmax = xv.activity_capacity


            ###---------fiyat zımbırtısı baş

            the_user = consumer.objects.get(username_id=creator.id)
            
            if place:

                if place.verify == False:
                    messages.warning(request,"henüz mekan hazır değil.")
                    allplacers = placer.objects.all()
                    allcommunities = community.objects.all()
                    allactivities = classic_activities.objects.all()
                    values= {
                        "placer":allplacers,
                        "community":allcommunities,
                        "activities":allactivities,
                    }

                    return render(request,"index.html",values)  

                if place.min_price > the_user.money:
                    messages.warning(request,"bakiyen yok, bakiye yükleyip tekrar dene")
                    allplacers = placer.objects.all()
                    allcommunities = community.objects.all()
                    allactivities = classic_activities.objects.all()
                    values= {
                        "placer":allplacers,
                        "community":allcommunities,
                        "activities":allactivities,
                    }

                    return render(request,"index.html",values)

            timenow = timezone.now()
            sixhour = timezone.timedelta(hours=6)
            sixlater = timenow + sixhour

            if sixlater >= m_time:
                messages.warning(request,"lobi en az 6 saat önceden hazır olmalıdır.")
                allplacers = placer.objects.all()
                allcommunities = community.objects.all()
                allactivities = classic_activities.objects.all()
                values= {
                    "placer":allplacers,
                    "community":allcommunities,
                    "activities":allactivities,
                }

                return render(request,"index.html",values)              

                
            ###---------fiyat zımbırtısı son



            ###---------time requests

            #m_time - 2 saat = closing time 

            time_change_2 = datetime.timedelta(hours=2)
            closing_time = m_time - time_change_2
            timenow = datetime.datetime.now()

            #eğer closing time şu ana eşit ya da gerideyse hata ver

            if int(timenow.timestamp()) >= int(closing_time.timestamp()):
                value10 = {
                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,                }
                messages.error(request,('lobi, en az iki saat önceden hazır olmalıdır.'))
                return render(request,"add_ccc.html",value10)

            ###---------
            #    
            the_time_now = datetime.datetime.now()
            addoneday = datetime.timedelta(days=1)

            q1_1 = the_time_now.replace(hour=9)
            q1_2 = the_time_now.replace(hour=12)
            q1_3 = the_time_now.replace(hour=15)
            q1_4 = the_time_now.replace(hour=18)
            q1_5 = the_time_now.replace(hour=21)
            q1_6 = the_time_now.replace(hour=22)     

            #----g2

            q2_1 = q1_1 + addoneday
            q2_2 = q1_2 + addoneday
            q2_3 = q1_3 + addoneday
            q2_4 = q1_4 + addoneday
            q2_5 = q1_5 + addoneday
            q2_6 = q1_6 + addoneday

            #----g3
        
            q3_1 = q2_1 + addoneday
            q3_2 = q2_2 + addoneday
            q3_3 = q2_3 + addoneday
            q3_4 = q2_4 + addoneday
            q3_5 = q2_5 + addoneday
            q3_6 = q2_6 + addoneday

            #----g4

            q4_1 = q3_1 + addoneday
            q4_2 = q3_2 + addoneday
            q4_3 = q3_3 + addoneday
            q4_4 = q3_4 + addoneday
            q4_5 = q3_5 + addoneday
            q4_6 = q3_6 + addoneday

            #----g5

            q5_1 = q4_1 + addoneday
            q5_2 = q4_2 + addoneday
            q5_3 = q4_3 + addoneday
            q5_4 = q4_4 + addoneday
            q5_5 = q4_5 + addoneday
            q5_6 = q4_6 + addoneday

            #----g6

            q6_1 = q5_1 + addoneday
            q6_2 = q5_2 + addoneday
            q6_3 = q5_3 + addoneday
            q6_4 = q5_4 + addoneday
            q6_5 = q5_5 + addoneday
            q6_6 = q5_6 + addoneday

            #----g7

            q7_1 = q6_1 + addoneday
            q7_2 = q6_2 + addoneday
            q7_3 = q6_3 + addoneday
            q7_4 = q6_4 + addoneday
            q7_5 = q6_5 + addoneday
            q7_6 = q6_6 + addoneday
            
            #----g8

            q8_1 = q7_1 + addoneday
            q8_2 = q7_2 + addoneday
            q8_3 = q7_3 + addoneday
            q8_4 = q7_4 + addoneday
            q8_5 = q7_5 + addoneday
            q8_6 = q7_6 + addoneday      

            #----g9

            q9_1 = q8_1 + addoneday
            q9_2 = q8_2 + addoneday
            q9_3 = q8_3 + addoneday
            q9_4 = q8_4 + addoneday
            q9_5 = q8_5 + addoneday
            q9_6 = q8_6 + addoneday            
            
            #----g10

            q10_1 = q9_1 + addoneday
            q10_2 = q9_2 + addoneday
            q10_3 = q9_3 + addoneday
            q10_4 = q9_4 + addoneday
            q10_5 = q9_5 + addoneday
            q10_6 = q9_6 + addoneday

            if int(q1_1.timestamp()) <= int(m_time.timestamp()) <= int(q7_5.timestamp()):
                print("okey")

            else:
                value10 = {
                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,                }
                messages.error(request,('9.00-22.00 arası, en fazla 7 gün sonrası için lobi oluşturabilirsiniz.'))

                return render(request,"add_ccc.html",value10)               

            ###---------


                
            ###---------

            nearoom= classic_room(creator=creator,name=name,description=description,
            place=place,m_time=m_time,closing_time=closing_time,
            if_its_anywhere=if_its_anywhere,game_type=game_type,max_ppl_existence=game_type.activity_capacity)

            ##---------

            valuexx = classic_activities.objects.filter(activity_name=nearoom.game_type).values_list("activity_capacity",flat=True)

            
            ##---------

            nearoom.save()

            ##--- manytomanies

            if request.user.user_type == 2:

                consumer_in_core = consumer.objects.get(username_id=request.user.id)
                nearoom.ppl_existence.add(consumer_in_core) #consumer'ın id'si lobiye eklendi

                consumer_in_core.in_classics.add(nearoom)
                consumer_in_core.save()


    
            ##--- manytomanies

            the_time_now = datetime.datetime.now()
            addoneday = datetime.timedelta(days=1)

            #----g1

            q1_1 = the_time_now.replace(hour=9)
            q1_2 = the_time_now.replace(hour=12)
            q1_3 = the_time_now.replace(hour=15)
            q1_4 = the_time_now.replace(hour=18)
            q1_5 = the_time_now.replace(hour=21)
            q1_6 = the_time_now.replace(hour=22)     

            #----g2

            q2_1 = q1_1 + addoneday
            q2_2 = q1_2 + addoneday
            q2_3 = q1_3 + addoneday
            q2_4 = q1_4 + addoneday
            q2_5 = q1_5 + addoneday
            q2_6 = q1_6 + addoneday

            #----g3
        
            q3_1 = q2_1 + addoneday
            q3_2 = q2_2 + addoneday
            q3_3 = q2_3 + addoneday
            q3_4 = q2_4 + addoneday
            q3_5 = q2_5 + addoneday
            q3_6 = q2_6 + addoneday

            #----g4

            q4_1 = q3_1 + addoneday
            q4_2 = q3_2 + addoneday
            q4_3 = q3_3 + addoneday
            q4_4 = q3_4 + addoneday
            q4_5 = q3_5 + addoneday
            q4_6 = q3_6 + addoneday

            #----g5

            q5_1 = q4_1 + addoneday
            q5_2 = q4_2 + addoneday
            q5_3 = q4_3 + addoneday
            q5_4 = q4_4 + addoneday
            q5_5 = q4_5 + addoneday
            q5_6 = q4_6 + addoneday

            #----g6

            q6_1 = q5_1 + addoneday
            q6_2 = q5_2 + addoneday
            q6_3 = q5_3 + addoneday
            q6_4 = q5_4 + addoneday
            q6_5 = q5_5 + addoneday
            q6_6 = q5_6 + addoneday

            #----g7

            q7_1 = q6_1 + addoneday
            q7_2 = q6_2 + addoneday
            q7_3 = q6_3 + addoneday
            q7_4 = q6_4 + addoneday
            q7_5 = q6_5 + addoneday
            q7_6 = q6_6 + addoneday
            
            #----g8

            q8_1 = q7_1 + addoneday
            q8_2 = q7_2 + addoneday
            q8_3 = q7_3 + addoneday
            q8_4 = q7_4 + addoneday
            q8_5 = q7_5 + addoneday
            q8_6 = q7_6 + addoneday      

            #----g9

            q9_1 = q8_1 + addoneday
            q9_2 = q8_2 + addoneday
            q9_3 = q8_3 + addoneday
            q9_4 = q8_4 + addoneday
            q9_5 = q8_5 + addoneday
            q9_6 = q8_6 + addoneday            
            
            #----g10

            q10_1 = q9_1 + addoneday
            q10_2 = q9_2 + addoneday
            q10_3 = q9_3 + addoneday
            q10_4 = q9_4 + addoneday
            q10_5 = q9_5 + addoneday
            q10_6 = q9_6 + addoneday
            
            if placer.objects.filter(place_name=place).exists():

                placer_chosen = placer.objects.get(place_name=place)
                print("okey2")
                #---eğer zaman dilimi bugün 9-12 arasıysa
                if int(q1_1.timestamp()) <= int(m_time.timestamp()) < int(q1_2.timestamp()):

                    if placer_chosen and (placer_chosen.a11_max_table_normal <= placer_chosen.a11_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:
                        placer_chosen.a11_existence_of_normal_game.add(nearoom) 
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 

       
            
                #---eğer zaman dilimi bugün 12-15 arasıysa
                elif int(q1_2.timestamp()) <= int(m_time.timestamp()) < int(q1_3.timestamp()):

                    if placer_chosen and (placer_chosen.a12_max_table_normal <= placer_chosen.a12_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a12_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 



                #---eğer zaman dilimi bugün 15-18 arasıysa
                elif int(q1_3.timestamp()) <= int(m_time.timestamp()) < int(q1_4.timestamp()):

                    if placer_chosen and (placer_chosen.a13_max_table_normal <= placer_chosen.a13_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a13_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 



                #---eğer zaman dilimi bugün 18-21 arasıysa
                elif int(q1_4.timestamp()) <= int(m_time.timestamp()) < int(q1_5.timestamp()):

                    if placer_chosen and (placer_chosen.a14_max_table_normal <= placer_chosen.a14_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a14_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 



                #---eğer zaman dilimi bugün 21-22 arasıysa
                elif int(q1_5.timestamp()) <= int(m_time.timestamp()) < int(q1_6.timestamp()):

                    if placer_chosen and (placer_chosen.a15_max_table_normal <= placer_chosen.a15_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a15_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 



                #---eğer zaman dilimi yarın 9-12 arasıysa

                elif int(q2_1.timestamp()) <= int(m_time.timestamp()) < int(q2_2.timestamp()):

                    if placer_chosen and (placer_chosen.a21_max_table_normal <= placer_chosen.a21_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a21_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 



                #---eğer zaman dilimi yarın 12-15 arasıysa
                elif int(q2_2.timestamp()) <= int(m_time.timestamp()) < int(q2_3.timestamp()):

                    if placer_chosen and (placer_chosen.a22_max_table_normal <= placer_chosen.a22_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a22_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi yarın 15-18 arasıysa
                elif int(q2_3.timestamp()) <= int(m_time.timestamp()) < int(q2_4.timestamp()):

                    if placer_chosen and (placer_chosen.a23_max_table_normal <= placer_chosen.a23_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a23_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi yarın 18-21 arasıysa
                elif int(q2_4.timestamp()) <= int(m_time.timestamp()) < int(q2_5.timestamp()):
                    if placer_chosen and (placer_chosen.a24_max_table_normal <= placer_chosen.a24_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a24_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi yarın 21-22 arasıysa
                elif int(q2_5.timestamp()) <= int(m_time.timestamp()) < int(q2_6.timestamp()):
                    if placer_chosen and (placer_chosen.a25_max_table_normal <= placer_chosen.a25_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a25_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 



                #---eğer zaman dilimi 1 gün sonra 9-12 arasıysa

                elif int(q3_1.timestamp()) <= int(m_time.timestamp()) < int(q3_2.timestamp()):

                    if placer_chosen and (placer_chosen.a31_max_table_normal <= placer_chosen.a31_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a31_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 1 gün sonra 12-15 arasıysa
                elif int(q3_2.timestamp()) <= int(m_time.timestamp()) < int(q3_3.timestamp()):

                    if placer_chosen and (placer_chosen.a32_max_table_normal <= placer_chosen.a32_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a32_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 1 gün sonra 15-18 arasıysa
                elif int(q3_3.timestamp()) <= int(m_time.timestamp()) < int(q3_4.timestamp()):

                    if placer_chosen and (placer_chosen.a33_max_table_normal <= placer_chosen.a33_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a33_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 1 gün sonra 18-21 arasıysa
                elif int(q3_4.timestamp()) <= int(m_time.timestamp()) < int(q3_5.timestamp()):
                    if placer_chosen and (placer_chosen.a34_max_table_normal <= placer_chosen.a34_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a34_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 1 gün sonra 21-22 arasıysa

                elif int(q3_5.timestamp()) <= int(m_time.timestamp()) < int(q3_6.timestamp()):
                    if placer_chosen and (placer_chosen.a35_max_table_normal <= placer_chosen.a35_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a35_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 2 gün sonra 9-12 arasıysa

                elif int(q4_1.timestamp()) <= int(m_time.timestamp()) < int(q4_2.timestamp()):

                    if placer_chosen and (placer_chosen.a41_max_table_normal <= placer_chosen.a41_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a41_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 2 gün sonra 12-15 arasıysa
                elif int(q4_2.timestamp()) <= int(m_time.timestamp()) < int(q4_3.timestamp()):

                    if placer_chosen and (placer_chosen.a42_max_table_normal <= placer_chosen.a42_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a42_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 2 gün sonra 15-18 arasıysa
                elif int(q4_3.timestamp()) <= int(m_time.timestamp()) < int(q4_4.timestamp()):

                    if placer_chosen and (placer_chosen.a43_max_table_normal <= placer_chosen.a43_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a43_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 2 gün sonra 18-21 arasıysa
                elif int(q4_4.timestamp()) <= int(m_time.timestamp()) < int(q4_5.timestamp()):
                    if placer_chosen and (placer_chosen.a44_max_table_normal <= placer_chosen.a44_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a44_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 2 gün sonra 21-22 arasıysa

                elif int(q4_5.timestamp()) <= int(m_time.timestamp()) < int(q4_6.timestamp()):
                    if placer_chosen and (placer_chosen.a45_max_table_normal <= placer_chosen.a45_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a45_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 



                #---eğer zaman dilimi 3 gün sonra 9-12 arasıysa

                elif int(q5_1.timestamp()) <= int(m_time.timestamp()) < int(q5_2.timestamp()):

                    if placer_chosen and (placer_chosen.a51_max_table_normal <= placer_chosen.a51_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a51_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 3 gün sonra 12-15 arasıysa
                elif int(q5_2.timestamp()) <= int(m_time.timestamp()) < int(q5_3.timestamp()):

                    if placer_chosen and (placer_chosen.a52_max_table_normal <= placer_chosen.a52_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a52_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 3 gün sonra 15-18 arasıysa
                elif int(q5_3.timestamp()) <= int(m_time.timestamp()) < int(q5_4.timestamp()):

                    if placer_chosen and (placer_chosen.a53_max_table_normal <= placer_chosen.a53_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a53_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 3 gün sonra 18-21 arasıysa
                elif int(q5_4.timestamp()) <= int(m_time.timestamp()) < int(q5_5.timestamp()):
                    if placer_chosen and (placer_chosen.a54_max_table_normal <= placer_chosen.a54_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a54_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 3 gün sonra 21-22 arasıysa

                elif int(q5_5.timestamp()) <= int(m_time.timestamp()) < int(q5_6.timestamp()):
                    if placer_chosen and (placer_chosen.a55_max_table_normal <= placer_chosen.a55_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a55_existence_of_normal_game.add(nearoom)         
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 4 gün sonra 9-12 arasıysa

                elif int(q6_1.timestamp()) <= int(m_time.timestamp()) < int(q6_2.timestamp()):

                    if placer_chosen and (placer_chosen.a61_max_table_normal <= placer_chosen.a61_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a61_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 4 gün sonra 12-15 arasıysa
                elif int(q6_2.timestamp()) <= int(m_time.timestamp()) < int(q6_3.timestamp()):

                    if placer_chosen and (placer_chosen.a62_max_table_normal <= placer_chosen.a62_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a62_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 4 gün sonra 15-18 arasıysa
                elif int(q6_3.timestamp()) <= int(m_time.timestamp()) < int(q6_4.timestamp()):

                    if placer_chosen and (placer_chosen.a63_max_table_normal <= placer_chosen.a63_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a63_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 4 gün sonra 18-21 arasıysa
                elif int(q6_4.timestamp()) <= int(m_time.timestamp()) < int(q6_5.timestamp()):
                    if placer_chosen and (placer_chosen.a64_max_table_normal <= placer_chosen.a64_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a64_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 4 gün sonra 21-22 arasıysa

                elif int(q6_5.timestamp()) <= int(m_time.timestamp()) < int(q6_6.timestamp()):
                    if placer_chosen and (placer_chosen.a65_max_table_normal <= placer_chosen.a65_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a65_existence_of_normal_game.add(nearoom)        
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 5 gün sonra 9-12 arasıysa

                elif int(q7_1.timestamp()) <= int(m_time.timestamp()) < int(q7_2.timestamp()):

                    if placer_chosen and (placer_chosen.a71_max_table_normal <= placer_chosen.a71_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a71_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 5 gün sonra 12-15 arasıysa
                elif int(q7_2.timestamp()) <= int(m_time.timestamp()) < int(q7_3.timestamp()):

                    if placer_chosen and (placer_chosen.a72_max_table_normal <= placer_chosen.a72_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a72_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 5 gün sonra 15-18 arasıysa
                elif int(q7_3.timestamp()) <= int(m_time.timestamp()) < int(q7_4.timestamp()):

                    if placer_chosen and (placer_chosen.a73_max_table_normal <= placer_chosen.a73_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a73_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 5 gün sonra 18-21 arasıysa
                elif int(q7_4.timestamp()) <= int(m_time.timestamp()) < int(q7_5.timestamp()):
                    if placer_chosen and (placer_chosen.a74_max_table_normal <= placer_chosen.a74_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a74_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 5 gün sonra 21-22 arasıysa

                elif int(q7_5.timestamp()) <= int(m_time.timestamp()) < int(q7_6.timestamp()):
                    if placer_chosen and (placer_chosen.a75_max_table_normal <= placer_chosen.a75_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a75_existence_of_normal_game.add(nearoom)  
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 




                #---eğer zaman dilimi 6 gün sonra 9-12 arasıysa

                elif int(q8_1.timestamp()) <= int(m_time.timestamp()) < int(q8_2.timestamp()):

                    if placer_chosen and (placer_chosen.a81_max_table_normal <= placer_chosen.a81_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a81_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 6 gün sonra 12-15 arasıysa
                elif int(q8_2.timestamp()) <= int(m_time.timestamp()) < int(q8_3.timestamp()):

                    if placer_chosen and (placer_chosen.a82_max_table_normal <= placer_chosen.a82_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a82_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 6 gün sonra 15-18 arasıysa
                elif int(q8_3.timestamp()) <= int(m_time.timestamp()) < int(q8_4.timestamp()):

                    if placer_chosen and (placer_chosen.a83_max_table_normal <= placer_chosen.a83_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a83_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 6 gün sonra 18-21 arasıysa
                elif int(q8_4.timestamp()) <= int(m_time.timestamp()) < int(q8_5.timestamp()):
                    if placer_chosen and (placer_chosen.a84_max_table_normal <= placer_chosen.a84_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a84_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 6 gün sonra 21-22 arasıysa

                elif int(q8_5.timestamp()) <= int(m_time.timestamp()) < int(q8_6.timestamp()):
                    if placer_chosen and (placer_chosen.a85_max_table_normal <= placer_chosen.a85_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a85_existence_of_normal_game.add(nearoom)  
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 7 gün sonra 9-12 arasıysa

                elif int(q9_1.timestamp()) <= int(m_time.timestamp()) < int(q9_2.timestamp()):

                    if placer_chosen and (placer_chosen.a91_max_table_normal <= placer_chosen.a91_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a91_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 7 gün sonra 12-15 arasıysa
                elif int(q9_2.timestamp()) <= int(m_time.timestamp()) < int(q9_3.timestamp()):

                    if placer_chosen and (placer_chosen.a92_max_table_normal <= placer_chosen.a92_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a92_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 7 gün sonra 15-18 arasıysa
                elif int(q9_3.timestamp()) <= int(m_time.timestamp()) < int(q9_4.timestamp()):

                    if placer_chosen and (placer_chosen.a93_max_table_normal <= placer_chosen.a93_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a93_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 7 gün sonra 18-21 arasıysa
                elif int(q9_4.timestamp()) <= int(m_time.timestamp()) < int(q9_5.timestamp()):
                    if placer_chosen and (placer_chosen.a94_max_table_normal <= placer_chosen.a94_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a94_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 7 gün sonra 21-22 arasıysa

                elif int(q9_5.timestamp()) <= int(m_time.timestamp()) < int(q9_6.timestamp()):
                    if placer_chosen and (placer_chosen.a95_max_table_normal <= placer_chosen.a95_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a95_existence_of_normal_game.add(nearoom)  
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 8 gün sonra 9-12 arasıysa

                elif int(q10_1.timestamp()) <= int(m_time.timestamp()) < int(q10_2.timestamp()):

                    if placer_chosen and (placer_chosen.a101_max_table_normal <= placer_chosen.a101_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a101_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 8 gün sonra 12-15 arasıysa
                elif int(q10_2.timestamp()) <= int(m_time.timestamp()) < int(q10_3.timestamp()):

                    if placer_chosen and (placer_chosen.a102_max_table_normal <= placer_chosen.a102_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a102_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 8 gün sonra 15-18 arasıysa
                elif int(q10_3.timestamp()) <= int(m_time.timestamp()) < int(q10_4.timestamp()):

                    if placer_chosen and (placer_chosen.a103_max_table_normal <= placer_chosen.a103_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a103_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 8 gün sonra 18-21 arasıysa
                elif int(q10_4.timestamp()) <= int(m_time.timestamp()) < int(q10_5.timestamp()):
                    if placer_chosen and (placer_chosen.a104_max_table_normal <= placer_chosen.a104_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a104_existence_of_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 8 gün sonra 21-22 arasıysa

                elif int(q10_5.timestamp()) <= int(m_time.timestamp()) < int(q10_6.timestamp()):
                    if placer_chosen and (placer_chosen.a105_max_table_normal <= placer_chosen.a105_existence_of_normal_game.count()):

                        value10 = {

                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ccc.html",value10)

                    else:

                        placer_chosen.a105_existence_of_normal_game.add(nearoom)  
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                else:

                    value10 = {

                        "cccform" : cccform,
        "all_activities" : all_activities,
        "placers_all":placers_all,
        "areas_all" : areas_all,
                    }

                    nearoom.delete()

                    messages.error(request,("hata"))
                    return render(request,"add_ccc.html",value10)                    

                placer_chosen.save()

            ##--- manytomanies
            
            nearoom.save()
            all_games_c = classic_room.objects.all()
            all_games_n = non_classic_activity_room.objects.all()
            consumer_in_core =  consumer.objects.filter(username_id=request.user.id)

            gamevalues={

                "all_games_c":all_games_c,
                "all_games_n":all_games_n,
                "consumer_in_core":consumer_in_core,
                "timenow":timenow,
            }

            messages.success(request,"Tamamdır, lobiyi oluşturduk")
            return render(request,"games.html",gamevalues)
    
        else:

    # Form geçersiz ise hataları kontrol edin
            errors = cccform.errors.as_data()  # Hataları alın

            for field, error_list in errors.items():
                # Her bir alan için hata listesini döngü ile gezin
                for error in error_list:
                    # Hata listesindeki her bir hatayı alın
                    field_name = field  # Alan adını alın
                    error_message = error.message  # Hata mesajını alın
                    # İstediğiniz şekilde hataları işleyin veya görüntüleyin
                    print(cccform.errors)

                cccform = add_classic_activity_room_user()
                value10 = {
                                "cccform" : cccform,
                "all_activities" : all_activities,
                "placers_all":placers_all,
                "areas_all" : areas_all,            }

                
                messages.error(request,"Beklenmeyen bir hata oluştu. 1")
                return render(request,"add_ccc.html",value10)

    else:

        cccform = add_classic_activity_room_user()
        value10 = {
                            "cccform" : cccform,
            "all_activities" : all_activities,
            "placers_all":placers_all,
            "areas_all" : areas_all,        }
        return render(request,"add_ccc.html",value10)

###---------------------------------------------------------------------------

def create_game_context(request):
    all_games_c = classic_room.objects.all()
    all_games_n = non_classic_activity_room.objects.all()
    all_games_p = placer_room.objects.all()

    consumer_in_core = consumer.objects.filter(username_id=request.user.id)

    timenow = timezone.now()
    threelater = timenow + datetime.timedelta(hours=3)
    sixlater = timenow + datetime.timedelta(hours=6)

    # Tüm oyunları toplu bir şekilde alın
    all_games = list(all_games_c) + list(all_games_n) + list(all_games_p)

    # Filtrelenmiş oyunları alın (zaman kontrolü yapılacak)
    filtered_games = [game for game in all_games if game.m_time > timenow]

    # Etkinliklerde kullanıcı var mı kontrol edin ve filtreyi uygulayın
    filtered_again_1 = [
        game for game in filtered_games if not any(request.user.id == consumer.username_id for consumer in game.ppl_existence.all())
    ]

    filtered_again_2 = [game for game in filtered_again_1 if game.m_time > threelater]

    filtered_again_3 = [
        game for game in filtered_again_2 if not any(request.user.id == consumer.username_id for consumer in game.offers.all())
    ]

    # Etkinlikleri tarihe göre sıralayın
    sorted_games = sorted(filtered_again_3, key=lambda game: game.m_time)

    return {
        "all_games_c": all_games_c,
        "all_games_n": all_games_n,
        "all_games_p": all_games_p,
        "consumer_in_core": consumer_in_core,
        "timenow": timenow,
        "threelater": threelater,
        "sixlater": sixlater,
        "sorted_games": sorted_games,
    }

def games(request, template='games.html', extra_context=None):
    game_context = create_game_context(request)
    sorted_games = game_context["sorted_games"]


    paginator = Paginator(sorted_games, per_page=6, orphans=1)  # 5 etkinlik per sayfa
    page = request.GET.get('page', 1)

    try:
        paginated_games = paginator.page(page)
        print("1")
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'has_next': False})
        raise Http404

    data = {
        'games': [vars(game) for game in paginated_games]
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("3")
        return JsonResponse(data)

    page_template = template

    if extra_context is not None:
        print("4")
        context.update(extra_context)

    context = {
        'games': paginated_games,
        'page_template': page_template,
    }

    # game_context değerlerini context'e ekleyin
    context.update(game_context)

    return render(request, template, context)

def load_more_data(request):
    page = request.GET.get('page', 1)  # Sayfa numarasını isteğe ekle
    per_page = 6  # Her sayfada gösterilecek etkinlik sayısı
    
    

    game_context = create_game_context(request)
    sorted_games = game_context["sorted_games"]

    paginator = Paginator(sorted_games, per_page)

    try:

        paginated_games = paginator.page(page)
    except EmptyPage:

        return JsonResponse({'has_next': False})

    context = {'xgamesx': paginated_games}

    context.update(game_context)

    # Yeni oyunları içeren HTML içeriğini oluştur
    html_content = render_to_string('game_cards_partial.html', context)

    return JsonResponse({'html_content': html_content})

###---------------------------------------------------------------------------
@login_required(login_url='index')
def create_game_context_2(request):

    all_games_c = classic_room.objects.all()
    all_games_n = non_classic_activity_room.objects.all()
    all_games_p = placer_room.objects.all()

    consumer_in_core = consumer.objects.filter(username_id=request.user.id)

    timenow = timezone.now()
    threelater = timenow + datetime.timedelta(hours=3)
    sixlater = timenow + datetime.timedelta(hours=6)

    # Tüm oyunları toplu bir şekilde alın
    all_games = list(all_games_c) + list(all_games_n) + list(all_games_p)

    # Filtrelenmiş oyunları alın (zaman kontrolü yapılacak)
    filtered_games = [game for game in all_games if game.m_time > timenow]

    # Etkinliklerde kullanıcı var mı kontrol edin ve filtreyi uygulayın
    filtered_again_1 = [
        game for game in filtered_games if not any(request.user.id == consumer.username_id for consumer in game.ppl_existence.all())
    ]

    filtered_again_2 = [game for game in filtered_again_1 if  threelater > game.m_time > timenow]

    filtered_again_3 = [
        game for game in filtered_again_2 if not any(request.user.id == consumer.username_id for consumer in game.offers.all())
    ]

    # Etkinlikleri tarihe göre sıralayın
    sorted_games = sorted(filtered_again_3, key=lambda game: game.m_time)

    return {
        "all_games_c": all_games_c,
        "all_games_n": all_games_n,
        "all_games_p": all_games_p,
        "consumer_in_core": consumer_in_core,
        "timenow": timenow,
        "threelater": threelater,
        "sixlater": sixlater,
        "sorted_games": sorted_games,
    }

@login_required(login_url='index')
def games_fast(request, template='games_fast.html', extra_context=None):
    game_context = create_game_context_2(request)
    sorted_games = game_context["sorted_games"]


    paginator = Paginator(sorted_games, per_page=6, orphans=1)  # 5 etkinlik per sayfa
    page = request.GET.get('page', 1)

    try:
        paginated_games = paginator.page(page)
        print("1")
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'has_next': False})
        raise Http404

    data = {
        'games': [vars(game) for game in paginated_games]
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("3")
        return JsonResponse(data)

    page_template = template

    if extra_context is not None:
        print("4")
        context.update(extra_context)

    context = {
        'games': paginated_games,
        'page_template': page_template,
    }

    # game_context değerlerini context'e ekleyin

    context.update(game_context)

    return render(request, template, context)

@login_required(login_url='index')
def load_more_data_2(request):
    page = request.GET.get('page', 1)  # Sayfa numarasını isteğe ekle
    per_page = 6  # Her sayfada gösterilecek etkinlik sayısı
    
    

    game_context = create_game_context_2(request)
    sorted_games = game_context["sorted_games"]

    paginator = Paginator(sorted_games, per_page)

    try:

        paginated_games = paginator.page(page)
    except EmptyPage:

        return JsonResponse({'has_next': False})

    context = {'xgamesx': paginated_games}

    context.update(game_context)

    # Yeni oyunları içeren HTML içeriğini oluştur
    html_content = render_to_string('game_cards_partial_fast.html', context)

    return JsonResponse({'html_content': html_content})

###---------------------------------------------------------------------------

@login_required(login_url='index')
def create_game_context_3(request):

    all_games_c = classic_room.objects.all()
    all_games_n = non_classic_activity_room.objects.all()
    all_games_p = placer_room.objects.all()

    consumer_in_core = consumer.objects.filter(username_id=request.user.id)

    timenow = timezone.now()
    threelater = timenow + datetime.timedelta(hours=3)
    sixlater = timenow + datetime.timedelta(hours=6)
    threebefore = timenow + datetime.timedelta(hours=-3)

    # Tüm oyunları toplu bir şekilde alın
    all_games = list(all_games_c) + list(all_games_n) + list(all_games_p)

    # Filtrelenmiş oyunları alın (zaman kontrolü yapılacak)

    # Etkinliklerde kullanıcı var mı kontrol edin ve filtreyi uygulayın
    filtered_games  = [
        game for game in all_games if any(request.user.id == consumer.username_id for consumer in game.offers.all())
    ]

    # Etkinlikleri tarihe göre sıralayın
    sorted_games = sorted(filtered_games, key=lambda game: game.m_time)

    return {
        "all_games_c": all_games_c,
        "all_games_n": all_games_n,
        "all_games_p": all_games_p,
        "consumer_in_core": consumer_in_core,
        "timenow": timenow,
        "threelater": threelater,
        "sixlater": sixlater,
        "sorted_games": sorted_games,
        "threebefore": threebefore,
    }

@login_required(login_url='index')
def games_in(request, template='games_in.html', extra_context=None):
    game_context = create_game_context_3(request)
    sorted_games = game_context["sorted_games"]

    paginator = Paginator(sorted_games, per_page=6, orphans=1)  # 5 etkinlik per sayfa
    page = request.GET.get('page', 1)

    try:
        paginated_games = paginator.page(page)
        print("1")
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'has_next': False})
        raise Http404

    data = {
        'games': [vars(game) for game in paginated_games]
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("3")
        return JsonResponse(data)

    page_template = template

    if extra_context is not None:
        print("4")
        context.update(extra_context)

    context = {
        'games': paginated_games,
        'page_template': page_template,
    }

    # game_context değerlerini context'e ekleyin

    context.update(game_context)

    return render(request, template, context)

@login_required(login_url='index')
def load_more_data_3(request):

    page = request.GET.get('page', 1)  # Sayfa numarasını isteğe ekle
    per_page = 6  # Her sayfada gösterilecek etkinlik sayısı

    game_context = create_game_context_3(request)
    sorted_games = game_context["sorted_games"]

    paginator = Paginator(sorted_games, per_page)

    try:

        paginated_games = paginator.page(page)
    except EmptyPage:

        return JsonResponse({'has_next': False})

    context = {'xgamesx': paginated_games}

    context.update(game_context)

    # Yeni oyunları içeren HTML içeriğini oluştur
    html_content = render_to_string('game_cards_partial_in.html', context)

    return JsonResponse({'html_content': html_content})

###---------------------------------------------------------------------------

@login_required(login_url='index')
def create_game_context_4(request):

    all_games_c = classic_room.objects.all()
    all_games_n = non_classic_activity_room.objects.all()
    all_games_p = placer_room.objects.all()

    consumer_in_core = consumer.objects.filter(username_id=request.user.id)

    timenow = timezone.now()
    threelater = timenow + datetime.timedelta(hours=3)
    sixlater = timenow + datetime.timedelta(hours=6)
    sixbefore = timenow + datetime.timedelta(hours=-6)
    threebefore = timenow + datetime.timedelta(hours=-3)

    # Tüm oyunları toplu bir şekilde alın
    all_games = list(all_games_c) + list(all_games_n) + list(all_games_p)

    # Filtrelenmiş oyunları alın (zaman kontrolü yapılacak)

    # Etkinliklerde kullanıcı var mı kontrol edin ve filtreyi uygulayın
    filtered_again_1 = [
        game for game in all_games if not any(request.user.id == consumer.username_id for consumer in game.offers.all())
    ]

    filtered_again_2 = [game for game in filtered_again_1 if game.m_time > threebefore]

    filtered_again_3 = [
        game for game in filtered_again_2 if any(request.user.id == consumer.username_id for consumer in game.ppl_existence.all())
    ]

    # Etkinlikleri tarihe göre sıralayın
    sorted_games = sorted(filtered_again_3, key=lambda game: game.m_time)

    return {
        "all_games_c": all_games_c,
        "all_games_n": all_games_n,
        "all_games_p": all_games_p,
        "consumer_in_core": consumer_in_core,
        "timenow": timenow,
        "threelater": threelater,
        "sixlater": sixlater,
        "sorted_games": sorted_games,
        "sixbefore": sixbefore,
        "threebefore":threebefore,
    }

@login_required(login_url='index')
def games_in_real(request, template='games_in_real.html', extra_context=None):
    game_context = create_game_context_4(request)
    sorted_games = game_context["sorted_games"]

    paginator = Paginator(sorted_games, per_page=6, orphans=1)  # 5 etkinlik per sayfa
    page = request.GET.get('page', 1)

    try:
        paginated_games = paginator.page(page)
        print("1")
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'has_next': False})
        raise Http404

    data = {
        'games': [vars(game) for game in paginated_games]
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("3")
        return JsonResponse(data)

    page_template = template

    if extra_context is not None:
        print("4")
        context.update(extra_context)

    context = {
        'games': paginated_games,
        'page_template': page_template,
    }

    # game_context değerlerini context'e ekleyin

    context.update(game_context)

    return render(request, template, context)

@login_required(login_url='index')
def load_more_data_4(request):
    page = request.GET.get('page', 1)  # Sayfa numarasını isteğe ekle
    per_page = 6  # Her sayfada gösterilecek etkinlik sayısı

    game_context = create_game_context_4(request)
    sorted_games = game_context["sorted_games"]

    paginator = Paginator(sorted_games, per_page)

    try:

        paginated_games = paginator.page(page)
    except EmptyPage:

        return JsonResponse({'has_next': False})

    context = {'xgamesx': paginated_games}

    context.update(game_context)

    # Yeni oyunları içeren HTML içeriğini oluştur
    html_content = render_to_string('game_cards_partial_in_real.html', context)

    return JsonResponse({'html_content': html_content})

###---------------------------------------------------------------------------

@login_required(login_url='index')
def create_game_context_5(request):

    all_games_c = classic_room.objects.all()
    all_games_n = non_classic_activity_room.objects.all()
    all_games_p = placer_room.objects.all()

    consumer_in_core = consumer.objects.filter(username_id=request.user.id)

    timenow = timezone.now()
    threelater = timenow + datetime.timedelta(hours=3)
    sixlater = timenow + datetime.timedelta(hours=6)
    sixbefore = timenow + datetime.timedelta(hours=-6)
    threebefore = timenow + datetime.timedelta(hours=-3)

    # Tüm oyunları toplu bir şekilde alın
    all_games = list(all_games_c) + list(all_games_n) + list(all_games_p)

    # Filtrelenmiş oyunları alın (zaman kontrolü yapılacak)

    # Etkinliklerde kullanıcı var mı kontrol edin ve filtreyi uygulayın
    filtered_again_1 = [
        game for game in all_games if not any(request.user.id == consumer.username_id for consumer in game.offers.all())
    ]

    filtered_again_2 = [game for game in filtered_again_1 if game.m_time < threebefore]

    filtered_again_3 = [
        game for game in filtered_again_2 if any(request.user.id == consumer.username_id for consumer in game.ppl_existence.all())
    ]

    # Etkinlikleri tarihe göre sıralayın
    sorted_games = sorted(filtered_again_3, key=lambda game: game.m_time, reverse=True)

    return {
        "all_games_c": all_games_c,
        "all_games_n": all_games_n,
        "all_games_p": all_games_p,
        "consumer_in_core": consumer_in_core,
        "timenow": timenow,
        "threelater": threelater,
        "sixlater": sixlater,
        "sorted_games": sorted_games,
        "sixbefore": sixbefore,
        "threebefore":threebefore,
    }

@login_required(login_url='index')
def games_in_o(request, template='games_c_o.html', extra_context=None):
    game_context = create_game_context_5(request)
    sorted_games = game_context["sorted_games"]

    paginator = Paginator(sorted_games, per_page=6, orphans=1) 
    page = request.GET.get('page', 1)

    try:
        paginated_games = paginator.page(page)
        print("1")
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'has_next': False})
        raise Http404

    data = {
        'games': [vars(game) for game in paginated_games]
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("3")
        return JsonResponse(data)

    page_template = template

    if extra_context is not None:
        print("4")
        context.update(extra_context)

    context = {
        'games': paginated_games,
        'page_template': page_template,
    }

    # game_context değerlerini context'e ekleyin

    context.update(game_context)

    return render(request, template, context)

@login_required(login_url='index')
def load_more_data_5(request):
    page = request.GET.get('page', 1)  # Sayfa numarasını isteğe ekle
    per_page = 6  # Her sayfada gösterilecek etkinlik sayısı

    game_context = create_game_context_4(request)
    sorted_games = game_context["sorted_games"]

    paginator = Paginator(sorted_games, per_page)

    try:

        paginated_games = paginator.page(page)
    except EmptyPage:

        return JsonResponse({'has_next': False})

    context = {'xgamesx': paginated_games}

    context.update(game_context)

    # Yeni oyunları içeren HTML içeriğini oluştur
    html_content = render_to_string('game_cards_partial_c_o.html', context)

    return JsonResponse({'html_content': html_content})

###---------------------------------------------------------------------------
























@periodic_task(run_every=crontab(hour=0, minute=0))
def daily_mtmquery():

    for the_placer in placer.objects.all():

        #---------------h1

        the_placer.a11_max_table_normal = the_placer.a21_max_table_normal
        the_placer.a11_max_table_not_normal = the_placer.a21_max_table_not_normal
        the_placer.a11_place_avabiality_not_normal = the_placer.a21_place_avabiality_not_normal
        the_placer.a11_existence_of_normal_game = the_placer.a21_existence_of_normal_game
        the_placer.a11_existence_of_not_normal_game = the_placer.a21_existence_of_not_normal_game

        the_placer.a21_max_table_normal = the_placer.a31_max_table_normal
        the_placer.a21_max_table_not_normal = the_placer.a31_max_table_not_normal
        the_placer.a21_place_avabiality_not_normal = the_placer.a31_place_avabiality_not_normal
        the_placer.a21_existence_of_normal_game = the_placer.a31_existence_of_normal_game
        the_placer.a21_existence_of_not_normal_game = the_placer.a31_existence_of_not_normal_game

        the_placer.a31_max_table_normal = the_placer.a41_max_table_normal
        the_placer.a31_max_table_not_normal = the_placer.a41_max_table_not_normal
        the_placer.a31_place_avabiality_not_normal = the_placer.a41_place_avabiality_not_normal
        the_placer.a31_existence_of_normal_game = the_placer.a41_existence_of_normal_game
        the_placer.a31_existence_of_not_normal_game = the_placer.a41_existence_of_not_normal_game

        the_placer.a41_max_table_normal = the_placer.a51_max_table_normal
        the_placer.a41_max_table_not_normal = the_placer.a51_max_table_not_normal
        the_placer.a41_place_avabiality_not_normal = the_placer.a51_place_avabiality_not_normal
        the_placer.a41_existence_of_normal_game = the_placer.a51_existence_of_normal_game
        the_placer.a41_existence_of_not_normal_game = the_placer.a51_existence_of_not_normal_game

        the_placer.a51_max_table_normal = the_placer.a61_max_table_normal
        the_placer.a51_max_table_not_normal = the_placer.a61_max_table_not_normal
        the_placer.a51_place_avabiality_not_normal = the_placer.a61_place_avabiality_not_normal
        the_placer.a51_existence_of_normal_game = the_placer.a61_existence_of_normal_game
        the_placer.a51_existence_of_not_normal_game = the_placer.a61_existence_of_not_normal_game

        the_placer.a61_max_table_normal = the_placer.a71_max_table_normal
        the_placer.a61_max_table_not_normal = the_placer.a71_max_table_not_normal
        the_placer.a61_place_avabiality_not_normal = the_placer.a71_place_avabiality_not_normal
        the_placer.a61_existence_of_normal_game = the_placer.a71_existence_of_normal_game
        the_placer.a61_existence_of_not_normal_game = the_placer.a71_existence_of_not_normal_game

        the_placer.a71_max_table_normal = the_placer.a81_max_table_normal
        the_placer.a71_max_table_not_normal = the_placer.a81_max_table_not_normal
        the_placer.a71_place_avabiality_not_normal = the_placer.a81_place_avabiality_not_normal
        the_placer.a71_existence_of_normal_game = the_placer.a81_existence_of_normal_game
        the_placer.a71_existence_of_not_normal_game = the_placer.a81_existence_of_not_normal_game

        the_placer.a81_max_table_normal = the_placer.a91_max_table_normal
        the_placer.a81_max_table_not_normal = the_placer.a91_max_table_not_normal
        the_placer.a81_place_avabiality_not_normal = the_placer.a91_place_avabiality_not_normal
        the_placer.a81_existence_of_normal_game = the_placer.a91_existence_of_normal_game
        the_placer.a81_existence_of_not_normal_game = the_placer.a91_existence_of_not_normal_game

        the_placer.a91_max_table_normal = the_placer.a101_max_table_normal
        the_placer.a91_max_table_not_normal = the_placer.a101_max_table_not_normal
        the_placer.a91_place_avabiality_not_normal = the_placer.a101_place_avabiality_not_normal
        the_placer.a91_existence_of_normal_game = the_placer.a101_existence_of_normal_game
        the_placer.a91_existence_of_not_normal_game = the_placer.a101_existence_of_not_normal_game

        the_placer.a101_max_table_normal = the_placer.max_table_normal
        the_placer.a101_max_table_not_normal = the_placer.max_table_not_normal
        the_placer.a101_place_avabiality_not_normal = the_placer.place_avabiality_not_normal
        the_placer.a101_existence_of_normal_game.clear()
        the_placer.a101_existence_of_not_normal_game.clear()

        #---------------h2

        the_placer.a12_max_table_normal = the_placer.a22_max_table_normal
        the_placer.a12_max_table_not_normal = the_placer.a22_max_table_not_normal
        the_placer.a12_place_avabiality_not_normal = the_placer.a22_place_avabiality_not_normal
        the_placer.a12_existence_of_normal_game = the_placer.a22_existence_of_normal_game
        the_placer.a12_existence_of_not_normal_game = the_placer.a22_existence_of_not_normal_game

        the_placer.a22_max_table_normal = the_placer.a32_max_table_normal
        the_placer.a22_max_table_not_normal = the_placer.a32_max_table_not_normal
        the_placer.a22_place_avabiality_not_normal = the_placer.a32_place_avabiality_not_normal
        the_placer.a22_existence_of_normal_game = the_placer.a32_existence_of_normal_game
        the_placer.a22_existence_of_not_normal_game = the_placer.a32_existence_of_not_normal_game

        the_placer.a32_max_table_normal = the_placer.a42_max_table_normal
        the_placer.a32_max_table_not_normal = the_placer.a42_max_table_not_normal
        the_placer.a32_place_avabiality_not_normal = the_placer.a42_place_avabiality_not_normal
        the_placer.a32_existence_of_normal_game = the_placer.a42_existence_of_normal_game
        the_placer.a32_existence_of_not_normal_game = the_placer.a42_existence_of_not_normal_game

        the_placer.a42_max_table_normal = the_placer.a52_max_table_normal
        the_placer.a42_max_table_not_normal = the_placer.a52_max_table_not_normal
        the_placer.a42_place_avabiality_not_normal = the_placer.a52_place_avabiality_not_normal
        the_placer.a42_existence_of_normal_game = the_placer.a52_existence_of_normal_game
        the_placer.a42_existence_of_not_normal_game = the_placer.a52_existence_of_not_normal_game

        the_placer.a52_max_table_normal = the_placer.a62_max_table_normal
        the_placer.a52_max_table_not_normal = the_placer.a62_max_table_not_normal
        the_placer.a52_place_avabiality_not_normal = the_placer.a62_place_avabiality_not_normal
        the_placer.a52_existence_of_normal_game = the_placer.a62_existence_of_normal_game
        the_placer.a52_existence_of_not_normal_game = the_placer.a62_existence_of_not_normal_game

        the_placer.a62_max_table_normal = the_placer.a72_max_table_normal
        the_placer.a62_max_table_not_normal = the_placer.a72_max_table_not_normal
        the_placer.a62_place_avabiality_not_normal = the_placer.a72_place_avabiality_not_normal
        the_placer.a62_existence_of_normal_game = the_placer.a72_existence_of_normal_game
        the_placer.a62_existence_of_not_normal_game = the_placer.a72_existence_of_not_normal_game

        the_placer.a72_max_table_normal = the_placer.a82_max_table_normal
        the_placer.a72_max_table_not_normal = the_placer.a82_max_table_not_normal
        the_placer.a72_place_avabiality_not_normal = the_placer.a82_place_avabiality_not_normal
        the_placer.a72_existence_of_normal_game = the_placer.a82_existence_of_normal_game
        the_placer.a72_existence_of_not_normal_game = the_placer.a82_existence_of_not_normal_game

        the_placer.a82_max_table_normal = the_placer.a92_max_table_normal
        the_placer.a82_max_table_not_normal = the_placer.a92_max_table_not_normal
        the_placer.a82_place_avabiality_not_normal = the_placer.a92_place_avabiality_not_normal
        the_placer.a82_existence_of_normal_game = the_placer.a92_existence_of_normal_game
        the_placer.a82_existence_of_not_normal_game = the_placer.a92_existence_of_not_normal_game

        the_placer.a92_max_table_normal = the_placer.a102_max_table_normal
        the_placer.a92_max_table_not_normal = the_placer.a102_max_table_not_normal
        the_placer.a92_place_avabiality_not_normal = the_placer.a102_place_avabiality_not_normal
        the_placer.a92_existence_of_normal_game = the_placer.a102_existence_of_normal_game
        the_placer.a92_existence_of_not_normal_game = the_placer.a102_existence_of_not_normal_game

        the_placer.a102_max_table_normal = the_placer.max_table_normal
        the_placer.a102_max_table_not_normal = the_placer.max_table_not_normal
        the_placer.a102_place_avabiality_not_normal = the_placer.place_avabiality_not_normal
        the_placer.a102_existence_of_normal_game.clear()
        the_placer.a102_existence_of_not_normal_game.clear()

        #---------------h3

        the_placer.a13_max_table_normal = the_placer.a23_max_table_normal
        the_placer.a13_max_table_not_normal = the_placer.a23_max_table_not_normal
        the_placer.a13_place_avabiality_not_normal = the_placer.a23_place_avabiality_not_normal
        the_placer.a13_existence_of_normal_game = the_placer.a23_existence_of_normal_game
        the_placer.a13_existence_of_not_normal_game = the_placer.a23_existence_of_not_normal_game

        the_placer.a23_max_table_normal = the_placer.a33_max_table_normal
        the_placer.a23_max_table_not_normal = the_placer.a33_max_table_not_normal
        the_placer.a23_place_avabiality_not_normal = the_placer.a33_place_avabiality_not_normal
        the_placer.a23_existence_of_normal_game = the_placer.a33_existence_of_normal_game
        the_placer.a23_existence_of_not_normal_game = the_placer.a33_existence_of_not_normal_game

        the_placer.a33_max_table_normal = the_placer.a43_max_table_normal
        the_placer.a33_max_table_not_normal = the_placer.a43_max_table_not_normal
        the_placer.a33_place_avabiality_not_normal = the_placer.a43_place_avabiality_not_normal
        the_placer.a33_existence_of_normal_game = the_placer.a43_existence_of_normal_game
        the_placer.a33_existence_of_not_normal_game = the_placer.a43_existence_of_not_normal_game

        the_placer.a43_max_table_normal = the_placer.a53_max_table_normal
        the_placer.a43_max_table_not_normal = the_placer.a53_max_table_not_normal
        the_placer.a43_place_avabiality_not_normal = the_placer.a53_place_avabiality_not_normal
        the_placer.a43_existence_of_normal_game = the_placer.a53_existence_of_normal_game
        the_placer.a43_existence_of_not_normal_game = the_placer.a53_existence_of_not_normal_game

        the_placer.a53_max_table_normal = the_placer.a63_max_table_normal
        the_placer.a53_max_table_not_normal = the_placer.a63_max_table_not_normal
        the_placer.a53_place_avabiality_not_normal = the_placer.a63_place_avabiality_not_normal
        the_placer.a53_existence_of_normal_game = the_placer.a63_existence_of_normal_game
        the_placer.a53_existence_of_not_normal_game = the_placer.a63_existence_of_not_normal_game

        the_placer.a63_max_table_normal = the_placer.a73_max_table_normal
        the_placer.a63_max_table_not_normal = the_placer.a73_max_table_not_normal
        the_placer.a63_place_avabiality_not_normal = the_placer.a73_place_avabiality_not_normal
        the_placer.a63_existence_of_normal_game = the_placer.a73_existence_of_normal_game
        the_placer.a63_existence_of_not_normal_game = the_placer.a73_existence_of_not_normal_game

        the_placer.a73_max_table_normal = the_placer.a83_max_table_normal
        the_placer.a73_max_table_not_normal = the_placer.a83_max_table_not_normal
        the_placer.a73_place_avabiality_not_normal = the_placer.a83_place_avabiality_not_normal
        the_placer.a73_existence_of_normal_game = the_placer.a83_existence_of_normal_game
        the_placer.a73_existence_of_not_normal_game = the_placer.a83_existence_of_not_normal_game

        the_placer.a83_max_table_normal = the_placer.a93_max_table_normal
        the_placer.a83_max_table_not_normal = the_placer.a93_max_table_not_normal
        the_placer.a83_place_avabiality_not_normal = the_placer.a93_place_avabiality_not_normal
        the_placer.a83_existence_of_normal_game = the_placer.a93_existence_of_normal_game
        the_placer.a83_existence_of_not_normal_game = the_placer.a93_existence_of_not_normal_game

        the_placer.a93_max_table_normal = the_placer.a103_max_table_normal
        the_placer.a93_max_table_not_normal = the_placer.a103_max_table_not_normal
        the_placer.a93_place_avabiality_not_normal = the_placer.a103_place_avabiality_not_normal
        the_placer.a93_existence_of_normal_game = the_placer.a103_existence_of_normal_game
        the_placer.a93_existence_of_not_normal_game = the_placer.a103_existence_of_not_normal_game

        the_placer.a103_max_table_normal = the_placer.max_table_normal
        the_placer.a103_max_table_not_normal = the_placer.max_table_not_normal
        the_placer.a103_place_avabiality_not_normal = the_placer.place_avabiality_not_normal
        the_placer.a103_existence_of_normal_game.clear()
        the_placer.a103_existence_of_not_normal_game.clear()

        #---------------h4

        the_placer.a14_max_table_normal = the_placer.a24_max_table_normal
        the_placer.a14_max_table_not_normal = the_placer.a24_max_table_not_normal
        the_placer.a14_place_avabiality_not_normal = the_placer.a24_place_avabiality_not_normal
        the_placer.a14_existence_of_normal_game = the_placer.a24_existence_of_normal_game
        the_placer.a14_existence_of_not_normal_game = the_placer.a24_existence_of_not_normal_game

        the_placer.a24_max_table_normal = the_placer.a34_max_table_normal
        the_placer.a24_max_table_not_normal = the_placer.a34_max_table_not_normal
        the_placer.a24_place_avabiality_not_normal = the_placer.a34_place_avabiality_not_normal
        the_placer.a24_existence_of_normal_game = the_placer.a34_existence_of_normal_game
        the_placer.a24_existence_of_not_normal_game = the_placer.a34_existence_of_not_normal_game

        the_placer.a34_max_table_normal = the_placer.a44_max_table_normal
        the_placer.a34_max_table_not_normal = the_placer.a44_max_table_not_normal
        the_placer.a34_place_avabiality_not_normal = the_placer.a44_place_avabiality_not_normal
        the_placer.a34_existence_of_normal_game = the_placer.a44_existence_of_normal_game
        the_placer.a34_existence_of_not_normal_game = the_placer.a44_existence_of_not_normal_game

        the_placer.a44_max_table_normal = the_placer.a54_max_table_normal
        the_placer.a44_max_table_not_normal = the_placer.a54_max_table_not_normal
        the_placer.a44_place_avabiality_not_normal = the_placer.a54_place_avabiality_not_normal
        the_placer.a44_existence_of_normal_game = the_placer.a54_existence_of_normal_game
        the_placer.a44_existence_of_not_normal_game = the_placer.a54_existence_of_not_normal_game

        the_placer.a54_max_table_normal = the_placer.a64_max_table_normal
        the_placer.a54_max_table_not_normal = the_placer.a64_max_table_not_normal
        the_placer.a54_place_avabiality_not_normal = the_placer.a64_place_avabiality_not_normal
        the_placer.a54_existence_of_normal_game = the_placer.a64_existence_of_normal_game
        the_placer.a54_existence_of_not_normal_game = the_placer.a64_existence_of_not_normal_game

        the_placer.a64_max_table_normal = the_placer.a74_max_table_normal
        the_placer.a64_max_table_not_normal = the_placer.a74_max_table_not_normal
        the_placer.a64_place_avabiality_not_normal = the_placer.a74_place_avabiality_not_normal
        the_placer.a64_existence_of_normal_game = the_placer.a74_existence_of_normal_game
        the_placer.a64_existence_of_not_normal_game = the_placer.a74_existence_of_not_normal_game

        the_placer.a74_max_table_normal = the_placer.a84_max_table_normal
        the_placer.a74_max_table_not_normal = the_placer.a84_max_table_not_normal
        the_placer.a74_place_avabiality_not_normal = the_placer.a84_place_avabiality_not_normal
        the_placer.a74_existence_of_normal_game = the_placer.a84_existence_of_normal_game
        the_placer.a74_existence_of_not_normal_game = the_placer.a84_existence_of_not_normal_game

        the_placer.a84_max_table_normal = the_placer.a94_max_table_normal
        the_placer.a84_max_table_not_normal = the_placer.a94_max_table_not_normal
        the_placer.a84_place_avabiality_not_normal = the_placer.a94_place_avabiality_not_normal
        the_placer.a84_existence_of_normal_game = the_placer.a94_existence_of_normal_game
        the_placer.a84_existence_of_not_normal_game = the_placer.a94_existence_of_not_normal_game

        the_placer.a94_max_table_normal = the_placer.a104_max_table_normal
        the_placer.a94_max_table_not_normal = the_placer.a104_max_table_not_normal
        the_placer.a94_place_avabiality_not_normal = the_placer.a104_place_avabiality_not_normal
        the_placer.a94_existence_of_normal_game = the_placer.a104_existence_of_normal_game
        the_placer.a94_existence_of_not_normal_game = the_placer.a104_existence_of_not_normal_game

        the_placer.a104_max_table_normal = the_placer.max_table_normal
        the_placer.a104_max_table_not_normal = the_placer.max_table_not_normal
        the_placer.a104_place_avabiality_not_normal = the_placer.place_avabiality_not_normal
        the_placer.a104_existence_of_normal_game.clear()
        the_placer.a104_existence_of_not_normal_game.clear()

        #---------------h5

        the_placer.a15_max_table_normal = the_placer.a25_max_table_normal
        the_placer.a15_max_table_not_normal = the_placer.a25_max_table_not_normal
        the_placer.a15_place_avabiality_not_normal = the_placer.a25_place_avabiality_not_normal
        the_placer.a15_existence_of_normal_game = the_placer.a25_existence_of_normal_game
        the_placer.a15_existence_of_not_normal_game = the_placer.a25_existence_of_not_normal_game

        the_placer.a25_max_table_normal = the_placer.a35_max_table_normal
        the_placer.a25_max_table_not_normal = the_placer.a35_max_table_not_normal
        the_placer.a25_place_avabiality_not_normal = the_placer.a35_place_avabiality_not_normal
        the_placer.a25_existence_of_normal_game = the_placer.a35_existence_of_normal_game
        the_placer.a25_existence_of_not_normal_game = the_placer.a35_existence_of_not_normal_game

        the_placer.a35_max_table_normal = the_placer.a45_max_table_normal
        the_placer.a35_max_table_not_normal = the_placer.a45_max_table_not_normal
        the_placer.a35_place_avabiality_not_normal = the_placer.a45_place_avabiality_not_normal
        the_placer.a35_existence_of_normal_game = the_placer.a45_existence_of_normal_game
        the_placer.a35_existence_of_not_normal_game = the_placer.a45_existence_of_not_normal_game

        the_placer.a45_max_table_normal = the_placer.a55_max_table_normal
        the_placer.a45_max_table_not_normal = the_placer.a55_max_table_not_normal
        the_placer.a45_place_avabiality_not_normal = the_placer.a55_place_avabiality_not_normal
        the_placer.a45_existence_of_normal_game = the_placer.a55_existence_of_normal_game
        the_placer.a45_existence_of_not_normal_game = the_placer.a55_existence_of_not_normal_game

        the_placer.a55_max_table_normal = the_placer.a65_max_table_normal
        the_placer.a55_max_table_not_normal = the_placer.a65_max_table_not_normal
        the_placer.a55_place_avabiality_not_normal = the_placer.a65_place_avabiality_not_normal
        the_placer.a55_existence_of_normal_game = the_placer.a65_existence_of_normal_game
        the_placer.a55_existence_of_not_normal_game = the_placer.a65_existence_of_not_normal_game

        the_placer.a65_max_table_normal = the_placer.a75_max_table_normal
        the_placer.a65_max_table_not_normal = the_placer.a75_max_table_not_normal
        the_placer.a65_place_avabiality_not_normal = the_placer.a75_place_avabiality_not_normal
        the_placer.a65_existence_of_normal_game = the_placer.a75_existence_of_normal_game
        the_placer.a65_existence_of_not_normal_game = the_placer.a75_existence_of_not_normal_game

        the_placer.a75_max_table_normal = the_placer.a85_max_table_normal
        the_placer.a75_max_table_not_normal = the_placer.a85_max_table_not_normal
        the_placer.a75_place_avabiality_not_normal = the_placer.a85_place_avabiality_not_normal
        the_placer.a75_existence_of_normal_game = the_placer.a85_existence_of_normal_game
        the_placer.a75_existence_of_not_normal_game = the_placer.a85_existence_of_not_normal_game

        the_placer.a85_max_table_normal = the_placer.a95_max_table_normal
        the_placer.a85_max_table_not_normal = the_placer.a95_max_table_not_normal
        the_placer.a85_place_avabiality_not_normal = the_placer.a95_place_avabiality_not_normal
        the_placer.a85_existence_of_normal_game = the_placer.a95_existence_of_normal_game
        the_placer.a85_existence_of_not_normal_game = the_placer.a95_existence_of_not_normal_game

        the_placer.a95_max_table_normal = the_placer.a105_max_table_normal
        the_placer.a95_max_table_not_normal = the_placer.a105_max_table_not_normal
        the_placer.a95_place_avabiality_not_normal = the_placer.a105_place_avabiality_not_normal
        the_placer.a95_existence_of_normal_game = the_placer.a105_existence_of_normal_game
        the_placer.a95_existence_of_not_normal_game = the_placer.a105_existence_of_not_normal_game

        the_placer.a105_max_table_normal = the_placer.max_table_normal
        the_placer.a105_max_table_not_normal = the_placer.max_table_not_normal
        the_placer.a105_place_avabiality_not_normal = the_placer.place_avabiality_not_normal
        the_placer.a105_existence_of_normal_game.clear()
        the_placer.a105_existence_of_not_normal_game.clear()

        the_placer.save()

###---------------------------------------------------------------------------

@login_required(login_url='index')
def add_non_classic_room(request):

    if request.user.user_type != 2:
        allplacers = placer.objects.all()
        allcommunities = community.objects.all()
        allactivities = classic_activities.objects.all()
        values= {
            "placer":allplacers,
            "community":allcommunities,
            "activities":allactivities,
        }
        messages.success(request,"no.")
        return render(request,"index.html",values)
    
    if request.method == "POST" or None:

        nccform = add_non_classic_activity_room_user(request.POST)

        if nccform.is_valid():

            creator = request.user

            name = nccform.cleaned_data.get("name")
            description = nccform.cleaned_data.get("description")
            place =  nccform.cleaned_data.get("place")
            m_time =  nccform.cleaned_data.get("m_time")
            if_its_anywhere = nccform.cleaned_data.get("if_its_anywhere")
            game_type = nccform.cleaned_data.get("game_type")
            max_ppl_existence = nccform.cleaned_data.get("max_ppl_existence")

            ###---------fiyat zımbırtısı baş

            the_user = consumer.objects.get(username_id=creator.id)
            if place:
                if place.verify == False:
                    messages.warning(request,"henüz mekan hazır değil.")
                    allplacers = placer.objects.all()
                    allcommunities = community.objects.all()
                    allactivities = classic_activities.objects.all()
                    values= {
                        "placer":allplacers,
                        "community":allcommunities,
                        "activities":allactivities,
                    }

                    return render(request,"index.html",values)                   

                if place.min_price > the_user.money:
                    messages.warning(request,"bakiyen yok, bakiye yükleyip tekrar dene")
                    allplacers = placer.objects.all()
                    allcommunities = community.objects.all()
                    allactivities = classic_activities.objects.all()
                    values= {
                        "placer":allplacers,
                        "community":allcommunities,
                        "activities":allactivities,
                    }

                    return render(request,"index.html",values)

            timenow = timezone.now()
            sixhour = timezone.timedelta(hours=6)
            sixlater = timenow + sixhour

            if sixlater >= m_time:
                messages.warning(request,"lobi en az 6 saat önceden hazır olmalıdır.")
                allplacers = placer.objects.all()
                allcommunities = community.objects.all()
                allactivities = classic_activities.objects.all()
                values= {
                    "placer":allplacers,
                    "community":allcommunities,
                    "activities":allactivities,
                }

                return render(request,"index.html",values)        
            
            ###---------fiyat zımbırtısı son

            ###---------time requests

            #m_time - 2 saat = closing time 

            time_change_2 = datetime.timedelta(hours=2)
            closing_time = m_time - time_change_2
            timenow = datetime.datetime.now()

            #eğer closing time şu ana eşit ya da gerideyse hata ver

            if int(timenow.timestamp()) >= int(closing_time.timestamp()):

                value10 = {
                "nccform" : nccform,
                }
                messages.error(request,('lobi, en az iki saat önceden hazır olmalıdır.'))
                return render(request,"add_ncc.html",value10)

            ###---------

            the_time_now = datetime.datetime.now()
            addoneday = datetime.timedelta(days=1)

            q1_1 = the_time_now.replace(hour=9)
            q1_2 = the_time_now.replace(hour=12)
            q1_3 = the_time_now.replace(hour=15)
            q1_4 = the_time_now.replace(hour=18)
            q1_5 = the_time_now.replace(hour=21)
            q1_6 = the_time_now.replace(hour=22)     

            #----g2

            q2_1 = q1_1 + addoneday
            q2_2 = q1_2 + addoneday
            q2_3 = q1_3 + addoneday
            q2_4 = q1_4 + addoneday
            q2_5 = q1_5 + addoneday
            q2_6 = q1_6 + addoneday

            #----g3
        
            q3_1 = q2_1 + addoneday
            q3_2 = q2_2 + addoneday
            q3_3 = q2_3 + addoneday
            q3_4 = q2_4 + addoneday
            q3_5 = q2_5 + addoneday
            q3_6 = q2_6 + addoneday

            #----g4

            q4_1 = q3_1 + addoneday
            q4_2 = q3_2 + addoneday
            q4_3 = q3_3 + addoneday
            q4_4 = q3_4 + addoneday
            q4_5 = q3_5 + addoneday
            q4_6 = q3_6 + addoneday

            #----g5

            q5_1 = q4_1 + addoneday
            q5_2 = q4_2 + addoneday
            q5_3 = q4_3 + addoneday
            q5_4 = q4_4 + addoneday
            q5_5 = q4_5 + addoneday
            q5_6 = q4_6 + addoneday

            #----g6

            q6_1 = q5_1 + addoneday
            q6_2 = q5_2 + addoneday
            q6_3 = q5_3 + addoneday
            q6_4 = q5_4 + addoneday
            q6_5 = q5_5 + addoneday
            q6_6 = q5_6 + addoneday

            #----g7

            q7_1 = q6_1 + addoneday
            q7_2 = q6_2 + addoneday
            q7_3 = q6_3 + addoneday
            q7_4 = q6_4 + addoneday
            q7_5 = q6_5 + addoneday
            q7_6 = q6_6 + addoneday
            
            #----g8

            q8_1 = q7_1 + addoneday
            q8_2 = q7_2 + addoneday
            q8_3 = q7_3 + addoneday
            q8_4 = q7_4 + addoneday
            q8_5 = q7_5 + addoneday
            q8_6 = q7_6 + addoneday      

            #----g9

            q9_1 = q8_1 + addoneday
            q9_2 = q8_2 + addoneday
            q9_3 = q8_3 + addoneday
            q9_4 = q8_4 + addoneday
            q9_5 = q8_5 + addoneday
            q9_6 = q8_6 + addoneday            
            
            #----g10

            q10_1 = q9_1 + addoneday
            q10_2 = q9_2 + addoneday
            q10_3 = q9_3 + addoneday
            q10_4 = q9_4 + addoneday
            q10_5 = q9_5 + addoneday
            q10_6 = q9_6 + addoneday

            if int(q1_1.timestamp()) <= int(m_time.timestamp()) <= int(q7_5.timestamp()):
                print("okey")

            else:

                value10 = {
                "nccform" : nccform,
                }
                messages.error(request,('9.00-22.00 arası, en fazla 7 gün sonrası için lobi oluşturabilirsiniz.'))

                return render(request,"add_ncc.html",value10)     

            nearoom= non_classic_activity_room(creator=creator,name=name,description=description,
            place=place,m_time=m_time, closing_time=closing_time,
            if_its_anywhere=if_its_anywhere,
            game_type=game_type,max_ppl_existence=max_ppl_existence,)
            
            nearoom.save()

            ##--- manytomanies

            if request.user.user_type == 2:

                consumer_in_core = consumer.objects.get(username_id=request.user.id)
                nearoom.ppl_existence.add(consumer_in_core) #consumer'ın id'si lobiye eklendi
                consumer_in_core.in_non_classics.add(nearoom)
                consumer_in_core.save()

    
            the_time_now = datetime.datetime.now()
            addoneday = datetime.timedelta(days=1)

            #----g1

            q1_1 = the_time_now.replace(hour=9)
            q1_2 = the_time_now.replace(hour=12)
            q1_3 = the_time_now.replace(hour=15)
            q1_4 = the_time_now.replace(hour=18)
            q1_5 = the_time_now.replace(hour=21)
            q1_6 = the_time_now.replace(hour=22)     

            #----g2

            q2_1 = q1_1 + addoneday
            q2_2 = q1_2 + addoneday
            q2_3 = q1_3 + addoneday
            q2_4 = q1_4 + addoneday
            q2_5 = q1_5 + addoneday
            q2_6 = q1_6 + addoneday

            #----g3
        
            q3_1 = q2_1 + addoneday
            q3_2 = q2_2 + addoneday
            q3_3 = q2_3 + addoneday
            q3_4 = q2_4 + addoneday
            q3_5 = q2_5 + addoneday
            q3_6 = q2_6 + addoneday

            #----g4

            q4_1 = q3_1 + addoneday
            q4_2 = q3_2 + addoneday
            q4_3 = q3_3 + addoneday
            q4_4 = q3_4 + addoneday
            q4_5 = q3_5 + addoneday
            q4_6 = q3_6 + addoneday

            #----g5

            q5_1 = q4_1 + addoneday
            q5_2 = q4_2 + addoneday
            q5_3 = q4_3 + addoneday
            q5_4 = q4_4 + addoneday
            q5_5 = q4_5 + addoneday
            q5_6 = q4_6 + addoneday

            #----g6

            q6_1 = q5_1 + addoneday
            q6_2 = q5_2 + addoneday
            q6_3 = q5_3 + addoneday
            q6_4 = q5_4 + addoneday
            q6_5 = q5_5 + addoneday
            q6_6 = q5_6 + addoneday

            #----g7

            q7_1 = q6_1 + addoneday
            q7_2 = q6_2 + addoneday
            q7_3 = q6_3 + addoneday
            q7_4 = q6_4 + addoneday
            q7_5 = q6_5 + addoneday
            q7_6 = q6_6 + addoneday
            
            #----g8

            q8_1 = q7_1 + addoneday
            q8_2 = q7_2 + addoneday
            q8_3 = q7_3 + addoneday
            q8_4 = q7_4 + addoneday
            q8_5 = q7_5 + addoneday
            q8_6 = q7_6 + addoneday      

            #----g9

            q9_1 = q8_1 + addoneday
            q9_2 = q8_2 + addoneday
            q9_3 = q8_3 + addoneday
            q9_4 = q8_4 + addoneday
            q9_5 = q8_5 + addoneday
            q9_6 = q8_6 + addoneday            
            
            #----g10

            q10_1 = q9_1 + addoneday
            q10_2 = q9_2 + addoneday
            q10_3 = q9_3 + addoneday
            q10_4 = q9_4 + addoneday
            q10_5 = q9_5 + addoneday
            q10_6 = q9_6 + addoneday
            
            if placer.objects.filter(place_name=place).exists():

                print("okey2")

                placer_chosen = placer.objects.get(place_name=place)
                consumer_in_core = consumer.objects.get(username_id=request.user.id)

                #---eğer zaman dilimi bugün 9-12 arasıysa
                if int(q1_1.timestamp()) <= int(m_time.timestamp()) < int(q1_2.timestamp()):

                    if placer_chosen and (placer_chosen.a11_max_table_not_normal <= placer_chosen.a11_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:
                        placer_chosen.a11_existence_of_not_normal_game.add(nearoom) 
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 

            
                #---eğer zaman dilimi bugün 12-15 arasıysa
                elif int(q1_2.timestamp()) <= int(m_time.timestamp()) < int(q1_3.timestamp()):

                    if placer_chosen and (placer_chosen.a12_max_table_not_normal <= placer_chosen.a12_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:
                        placer_chosen.a12_existence_of_not_normal_game.add(nearoom) 
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 

                #---eğer zaman dilimi bugün 15-18 arasıysa
                elif int(q1_3.timestamp()) <= int(m_time.timestamp()) < int(q1_4.timestamp()):

                    if placer_chosen and (placer_chosen.a13_max_table_not_normal <= placer_chosen.a13_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a13_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi bugün 18-21 arasıysa
                elif int(q1_4.timestamp()) <= int(m_time.timestamp()) < int(q1_5.timestamp()):

                    if placer_chosen and (placer_chosen.a14_max_table_not_normal <= placer_chosen.a14_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a14_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi bugün 21-22 arasıysa
                elif int(q1_5.timestamp()) <= int(m_time.timestamp()) < int(q1_6.timestamp()):

                    if placer_chosen and (placer_chosen.a15_max_table_not_normal <= placer_chosen.a15_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a15_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi yarın 9-12 arasıysa

                elif int(q2_1.timestamp()) <= int(m_time.timestamp()) < int(q2_2.timestamp()):

                    if placer_chosen and (placer_chosen.a21_max_table_not_normal <= placer_chosen.a21_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a21_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi yarın 12-15 arasıysa
                elif int(q2_2.timestamp()) <= int(m_time.timestamp()) < int(q2_3.timestamp()):

                    if placer_chosen and (placer_chosen.a22_max_table_not_normal <= placer_chosen.a22_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a22_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi yarın 15-18 arasıysa
                elif int(q2_3.timestamp()) <= int(m_time.timestamp()) < int(q2_4.timestamp()):

                    if placer_chosen and (placer_chosen.a23_max_table_not_normal <= placer_chosen.a23_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a23_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi yarın 18-21 arasıysa
                elif int(q2_4.timestamp()) <= int(m_time.timestamp()) < int(q2_5.timestamp()):
                    if placer_chosen and (placer_chosen.a24_max_table_not_normal <= placer_chosen.a24_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a24_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi yarın 21-22 arasıysa
                elif int(q2_5.timestamp()) <= int(m_time.timestamp()) < int(q2_6.timestamp()):
                    if placer_chosen and (placer_chosen.a25_max_table_not_normal <= placer_chosen.a25_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a25_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 



                #---eğer zaman dilimi 1 gün sonra 9-12 arasıysa

                elif int(q3_1.timestamp()) <= int(m_time.timestamp()) < int(q3_2.timestamp()):

                    if placer_chosen and (placer_chosen.a31_max_table_not_normal <= placer_chosen.a31_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a31_existence_of_not_normal_game.add(nearoom)

                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 



                #---eğer zaman dilimi 1 gün sonra 12-15 arasıysa
                elif int(q3_2.timestamp()) <= int(m_time.timestamp()) < int(q3_3.timestamp()):

                    if placer_chosen and (placer_chosen.a32_max_table_not_normal <= placer_chosen.a32_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a32_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 1 gün sonra 15-18 arasıysa
                elif int(q3_3.timestamp()) <= int(m_time.timestamp()) < int(q3_4.timestamp()):

                    if placer_chosen and (placer_chosen.a33_max_table_not_normal <= placer_chosen.a33_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a33_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 1 gün sonra 18-21 arasıysa
                elif int(q3_4.timestamp()) <= int(m_time.timestamp()) < int(q3_5.timestamp()):
                    if placer_chosen and (placer_chosen.a34_max_table_not_normal <= placer_chosen.a34_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a34_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 1 gün sonra 21-22 arasıysa

                elif int(q3_5.timestamp()) <= int(m_time.timestamp()) < int(q3_6.timestamp()):
                    if placer_chosen and (placer_chosen.a35_max_table_not_normal <= placer_chosen.a35_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a35_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 2 gün sonra 9-12 arasıysa

                elif int(q4_1.timestamp()) <= int(m_time.timestamp()) < int(q4_2.timestamp()):

                    if placer_chosen and (placer_chosen.a41_max_table_not_normal <= placer_chosen.a41_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a41_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 2 gün sonra 12-15 arasıysa
                elif int(q4_2.timestamp()) <= int(m_time.timestamp()) < int(q4_3.timestamp()):

                    if placer_chosen and (placer_chosen.a42_max_table_not_normal <= placer_chosen.a42_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a42_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 2 gün sonra 15-18 arasıysa
                elif int(q4_3.timestamp()) <= int(m_time.timestamp()) < int(q4_4.timestamp()):

                    if placer_chosen and (placer_chosen.a43_max_table_not_normal <= placer_chosen.a43_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a43_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 2 gün sonra 18-21 arasıysa
                elif int(q4_4.timestamp()) <= int(m_time.timestamp()) < int(q4_5.timestamp()):
                    if placer_chosen and (placer_chosen.a44_max_table_not_normal <= placer_chosen.a44_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a44_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 2 gün sonra 21-22 arasıysa

                elif int(q4_5.timestamp()) <= int(m_time.timestamp()) < int(q4_6.timestamp()):
                    if placer_chosen and (placer_chosen.a45_max_table_not_normal <= placer_chosen.a45_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a45_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 



                #---eğer zaman dilimi 3 gün sonra 9-12 arasıysa

                elif int(q5_1.timestamp()) <= int(m_time.timestamp()) < int(q5_2.timestamp()):

                    if placer_chosen and (placer_chosen.a51_max_table_not_normal <= placer_chosen.a51_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a51_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 3 gün sonra 12-15 arasıysa
                elif int(q5_2.timestamp()) <= int(m_time.timestamp()) < int(q5_3.timestamp()):

                    if placer_chosen and (placer_chosen.a52_max_table_not_normal <= placer_chosen.a52_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a52_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 3 gün sonra 15-18 arasıysa
                elif int(q5_3.timestamp()) <= int(m_time.timestamp()) < int(q5_4.timestamp()):

                    if placer_chosen and (placer_chosen.a53_max_table_not_normal <= placer_chosen.a53_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a53_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 3 gün sonra 18-21 arasıysa
                elif int(q5_4.timestamp()) <= int(m_time.timestamp()) < int(q5_5.timestamp()):
                    if placer_chosen and (placer_chosen.a54_max_table_not_normal <= placer_chosen.a54_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a54_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 3 gün sonra 21-22 arasıysa

                elif int(q5_5.timestamp()) <= int(m_time.timestamp()) < int(q5_6.timestamp()):
                    if placer_chosen and (placer_chosen.a55_max_table_not_normal <= placer_chosen.a55_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a55_existence_of_not_normal_game.add(nearoom)         
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 4 gün sonra 9-12 arasıysa

                elif int(q6_1.timestamp()) <= int(m_time.timestamp()) < int(q6_2.timestamp()):

                    if placer_chosen and (placer_chosen.a61_max_table_not_normal <= placer_chosen.a61_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a61_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 4 gün sonra 12-15 arasıysa
                elif int(q6_2.timestamp()) <= int(m_time.timestamp()) < int(q6_3.timestamp()):

                    if placer_chosen and (placer_chosen.a62_max_table_not_normal <= placer_chosen.a62_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a62_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 4 gün sonra 15-18 arasıysa
                elif int(q6_3.timestamp()) <= int(m_time.timestamp()) < int(q6_4.timestamp()):

                    if placer_chosen and (placer_chosen.a63_max_table_not_normal <= placer_chosen.a63_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a63_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 4 gün sonra 18-21 arasıysa
                elif int(q6_4.timestamp()) <= int(m_time.timestamp()) < int(q6_5.timestamp()):
                    if placer_chosen and (placer_chosen.a64_max_table_not_normal <= placer_chosen.a64_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a64_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 4 gün sonra 21-22 arasıysa

                elif int(q6_5.timestamp()) <= int(m_time.timestamp()) < int(q6_6.timestamp()):
                    if placer_chosen and (placer_chosen.a65_max_table_not_normal <= placer_chosen.a65_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a65_existence_of_not_normal_game.add(nearoom)        
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 5 gün sonra 9-12 arasıysa

                elif int(q7_1.timestamp()) <= int(m_time.timestamp()) < int(q7_2.timestamp()):

                    if placer_chosen and (placer_chosen.a71_max_table_not_normal <= placer_chosen.a71_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a71_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 5 gün sonra 12-15 arasıysa
                elif int(q7_2.timestamp()) <= int(m_time.timestamp()) < int(q7_3.timestamp()):

                    if placer_chosen and (placer_chosen.a72_max_table_not_normal <= placer_chosen.a72_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a72_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 5 gün sonra 15-18 arasıysa
                elif int(q7_3.timestamp()) <= int(m_time.timestamp()) < int(q7_4.timestamp()):

                    if placer_chosen and (placer_chosen.a73_max_table_not_normal <= placer_chosen.a73_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a73_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 5 gün sonra 18-21 arasıysa
                elif int(q7_4.timestamp()) <= int(m_time.timestamp()) < int(q7_5.timestamp()):
                    if placer_chosen and (placer_chosen.a74_max_table_not_normal <= placer_chosen.a74_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a74_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 5 gün sonra 21-22 arasıysa

                elif int(q7_5.timestamp()) <= int(m_time.timestamp()) < int(q7_6.timestamp()):
                    if placer_chosen and (placer_chosen.a75_max_table_not_normal <= placer_chosen.a75_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a75_existence_of_not_normal_game.add(nearoom)  
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 




                #---eğer zaman dilimi 6 gün sonra 9-12 arasıysa

                elif int(q8_1.timestamp()) <= int(m_time.timestamp()) < int(q8_2.timestamp()):

                    if placer_chosen and (placer_chosen.a81_max_table_not_normal <= placer_chosen.a81_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a81_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 6 gün sonra 12-15 arasıysa
                elif int(q8_2.timestamp()) <= int(m_time.timestamp()) < int(q8_3.timestamp()):

                    if placer_chosen and (placer_chosen.a82_max_table_not_normal <= placer_chosen.a82_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a82_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 6 gün sonra 15-18 arasıysa
                elif int(q8_3.timestamp()) <= int(m_time.timestamp()) < int(q8_4.timestamp()):

                    if placer_chosen and (placer_chosen.a83_max_table_not_normal <= placer_chosen.a83_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a83_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 6 gün sonra 18-21 arasıysa
                elif int(q8_4.timestamp()) <= int(m_time.timestamp()) < int(q8_5.timestamp()):
                    if placer_chosen and (placer_chosen.a84_max_table_not_normal <= placer_chosen.a84_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a84_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 6 gün sonra 21-22 arasıysa

                elif int(q8_5.timestamp()) <= int(m_time.timestamp()) < int(q8_6.timestamp()):
                    if placer_chosen and (placer_chosen.a85_max_table_not_normal <= placer_chosen.a85_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a85_existence_of_not_normal_game.add(nearoom)  
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 7 gün sonra 9-12 arasıysa

                elif int(q9_1.timestamp()) <= int(m_time.timestamp()) < int(q9_2.timestamp()):

                    if placer_chosen and (placer_chosen.a91_max_table_not_normal <= placer_chosen.a91_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a91_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 7 gün sonra 12-15 arasıysa
                elif int(q9_2.timestamp()) <= int(m_time.timestamp()) < int(q9_3.timestamp()):

                    if placer_chosen and (placer_chosen.a92_max_table_not_normal <= placer_chosen.a92_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a92_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 7 gün sonra 15-18 arasıysa
                elif int(q9_3.timestamp()) <= int(m_time.timestamp()) < int(q9_4.timestamp()):

                    if placer_chosen and (placer_chosen.a93_max_table_not_normal <= placer_chosen.a93_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a93_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 7 gün sonra 18-21 arasıysa
                elif int(q9_4.timestamp()) <= int(m_time.timestamp()) < int(q9_5.timestamp()):
                    if placer_chosen and (placer_chosen.a94_max_table_not_normal <= placer_chosen.a94_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a94_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 7 gün sonra 21-22 arasıysa

                elif int(q9_5.timestamp()) <= int(m_time.timestamp()) < int(q9_6.timestamp()):
                    if placer_chosen and (placer_chosen.a95_max_table_not_normal <= placer_chosen.a95_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a95_existence_of_not_normal_game.add(nearoom)  
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 8 gün sonra 9-12 arasıysa

                elif int(q10_1.timestamp()) <= int(m_time.timestamp()) < int(q10_2.timestamp()):

                    if placer_chosen and (placer_chosen.a101_max_table_not_normal <= placer_chosen.a101_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a101_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 8 gün sonra 12-15 arasıysa
                elif int(q10_2.timestamp()) <= int(m_time.timestamp()) < int(q10_3.timestamp()):

                    if placer_chosen and (placer_chosen.a102_max_table_not_normal <= placer_chosen.a102_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a102_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 8 gün sonra 15-18 arasıysa
                elif int(q10_3.timestamp()) <= int(m_time.timestamp()) < int(q10_4.timestamp()):

                    if placer_chosen and (placer_chosen.a103_max_table_not_normal <= placer_chosen.a103_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a103_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 8 gün sonra 18-21 arasıysa
                elif int(q10_4.timestamp()) <= int(m_time.timestamp()) < int(q10_5.timestamp()):
                    if placer_chosen and (placer_chosen.a104_max_table_not_normal <= placer_chosen.a104_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a104_existence_of_not_normal_game.add(nearoom)
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 


                #---eğer zaman dilimi 8 gün sonra 21-22 arasıysa

                elif int(q10_5.timestamp()) <= int(m_time.timestamp()) < int(q10_6.timestamp()):
                    if placer_chosen and (placer_chosen.a105_max_table_not_normal <= placer_chosen.a105_existence_of_not_normal_game.count()):

                        value10 = {
                        "nccform" : nccform,
                        }

                        nearoom.delete()

                        messages.error(request,("bu kafede,bu saat için rezervasyon yapabileceğiniz masa kalmamıştır."))
                        return render(request,"add_ncc.html",value10)

                    else:

                        placer_chosen.a105_existence_of_not_normal_game.add(nearoom)  
                        print(placer_chosen.min_price)
                        consumer_in_core.money = consumer_in_core.money - placer_chosen.min_price
                        consumer_in_core.save() 

                else:

                    value10 = {
                    "nccform" : nccform,
                    }

                    nearoom.delete()

                    messages.error(request,("hata"))
                    return render(request,"add_ncc.html",value10)


                placer_chosen.save()

            nearoom.save()



                
            all_games_c = classic_room.objects.all()
            all_games_n = non_classic_activity_room.objects.all()
            consumer_in_core =  consumer.objects.filter(username_id=request.user.id)

            gamevalues={

                "all_games_c":all_games_c,
                "all_games_n":all_games_n,
                "consumer_in_core":consumer_in_core,
                "timenow":timenow,
            }

            messages.success(request,"Tamamdır, lobiyi oluşturduk")
            return render(request,"games.html",gamevalues)

        else:
            print(nccform.errors)
            nccform = add_non_classic_activity_room_user()
            value10 = {
            "nccform" : nccform,
            }
            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"add_ncc.html",value10)

    else:

        nccform = add_non_classic_activity_room_user()
        value10 = {
        "nccform" : nccform,
        }
        return render(request,"add_ncc.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def invite_croom(request,username,id):

    the_croom = get_object_or_404(classic_room,id=id)
    mform = message_Form(request.POST or None)

    if (request.user.user_type != 2):

        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }
        
        return render(request,"ccactivities.html",value10)
    
    if request.user.user_type == 2:

        offerto_core = get_object_or_404(usercore,username=username)
        offerto = consumer.objects.get(username_id=offerto_core.id)  


        if the_croom.max_ppl_existence <= the_croom.ppl_existence.count():
            messages.warning(request,"kişi sayısı doldu, davet yollayamazsınız...")
            value10 = {
            "room" : the_croom,
            "mform":mform,
            }
            
            return render(request,"ccactivities.html",value10)

        if str(request.user.username) != str(the_croom.creator):
            messages.warning(request,"yetkili değilsiniz...")
            value10 = {
            "room" : the_croom,
            "mform":mform,
            }
            
            return render(request,"ccactivities.html",value10)

        if the_croom.creator in offerto.ibanned.all():
            messages.warning(request,"kişi seni engellemiş. davet atamazsın.")
            value10 = {
            "room" : the_croom,
            "mform":mform,
            }
            
            return render(request,"ccactivities.html",value10)

        offerto.c_room_offers.add(the_croom)
        offerto.save()
        messages.warning(request,"başarıyla yollandı..")
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }
        
        return render(request,"ccactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def invite_croom_y(request,username,id):


    
    the_croom = get_object_or_404(classic_room,id=id)
    mform = message_Form(request.POST or None)

    if (request.user.user_type != 2):

        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }
        
        return render(request,"ccactivities.html",value10)
    
    if request.user.user_type == 2:
        offerto_core = get_object_or_404(usercore,username=username)
        offerto = consumer.objects.get(username_id=offerto_core.id)  

        if str(request.user.username) != str(offerto.username):
            messages.warning(request,"hainlik yapma...")
            value10 = {
            "room" : the_croom,
            "mform":mform,
            }
            
            return render(request,"ccactivities.html",value10)

        if the_croom.max_ppl_existence <= the_croom.ppl_existence.count():
            messages.warning(request,"artık çok geç, kişiler doldu...")
            value10 = {
            "room" : the_croom,
            "mform":mform,
            }
            
            return render(request,"ccactivities.html",value10)

        if the_croom.place:
            if the_croom.place.min_price > offerto.money:



                offerto.c_room_offers.remove(the_croom)   
                messages.warning(request,"kişinin yeterli bakiyesi kalmamış, reddedildi")
                return redirect("index")       
            elif the_croom.place.min_price < offerto.money:

                the_placer = placer.objects.get(username_id=the_croom.place.id)
                the_placer.money = the_placer.money + the_croom.place.min_price
                the_placer.save()

                offerto.money = offerto.money - the_croom.place.min_price
                offerto.save()

        offerto.c_room_offers.remove(the_croom)
        offerto.in_classics.add(the_croom)
        the_croom.ppl_existence.add(offerto)


        the_croom.save()
        offerto.save()

        messages.success(request,"davet onaylandı")
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }
        
        return render(request,"ccactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def invite_croom_n(request,username,id):

    the_croom = get_object_or_404(classic_room,id=id)
    mform = message_Form(request.POST or None)

    if (request.user.user_type != 2):

        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }
        
        return render(request,"ccactivities.html",value10)
    
    if request.user.user_type == 2:
        offerto_core = get_object_or_404(usercore,username=username)
        offerto = consumer.objects.get(username_id=offerto_core.id)  

        if str(request.user.username) != str(offerto.username):
            messages.warning(request,"hainlik yapma...")       
            value10 = {
            "room" : the_croom,
            "mform":mform,
            }
            
            return render(request,"ccactivities.html",value10)

        offerto.c_room_offers.remove(the_croom)

        the_croom.save()
        offerto.save()

        messages.success(request,"davet reddedildi")
        value10 = {
        "room" : the_croom,
        "mform":mform,
        }
        
        return render(request,"ccactivities.html",value10)

###-----------------------------------------------buradayız

@login_required(login_url='index')
def invite_nroom(request,username,id):

    the_nroom = get_object_or_404(non_classic_activity_room,id=id)
    mform = message_Form(request.POST or None)


    if (request.user.user_type != 2):

        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }
        
        return render(request,"ncactivities.html",value10)

    if request.user.user_type == 2:   

        offerto_core = get_object_or_404(usercore,username=username)
        offerto = consumer.objects.get(username_id=offerto_core.id)  

        if the_nroom.max_ppl_existence <= the_nroom.ppl_existence.count():
            messages.warning(request,"kişi sayısı doldu, davet yollayamazsınız...")
            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            return render(request,"ncactivities.html",value10)

        if str(request.user.username) != str(the_nroom.creator):
            messages.warning(request,"yetkili değilsiniz...")
            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            return render(request,"ncactivities.html",value10)

        if the_nroom.creator in offerto.ibanned.all():
            messages.warning(request,"kişi seni engellemiş. davet atamazsın.")         
            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            return render(request,"ncactivities.html",value10)

        offerto.n_room_offers.add(the_nroom)
        offerto.save()
        messages.warning(request,"başarıyla yollandı..")
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }
        
        return render(request,"ncactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def invite_nroom_y(request,username,id):

    the_nroom = get_object_or_404(non_classic_activity_room,id=id)
    mform = message_Form(request.POST or None)


    if (request.user.user_type != 2):

        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }
        
        return render(request,"ncactivities.html",value10)

    if request.user.user_type == 2:   

        offerto_core = get_object_or_404(usercore,username=username)
        offerto = consumer.objects.get(username_id=offerto_core.id)  

        if str(request.user.username) != str(offerto.username):
            messages.warning(request,"hainlik yapma...")
            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            return render(request,"ncactivities.html",value10)

        if the_nroom.max_ppl_existence <= the_nroom.ppl_existence.count():
            messages.warning(request,"artık çok geç, kişiler doldu...")
            messages.warning(request,"bunu yapmaya iznin yok.")         
            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            return render(request,"ncactivities.html",value10)

        if the_nroom.place:
            if the_nroom.place.min_price > offerto.money:
                offerto.n_room_offers.remove(the_nroom)   
                messages.warning(request,"kişinin yeterli bakiyesi kalmamış, reddedildi")
                return redirect("index") 
            elif the_nroom.place.min_price < offerto.money:

                the_placer = placer.objects.get(username_id=the_nroom.place.id)
                the_placer.money = the_placer.money + the_nroom.place.min_price
                the_placer.save()

                offerto.money = offerto.money - the_nroom.place.min_price

            offerto.n_room_offers.remove(the_nroom)
            offerto.in_non_classics.add(the_nroom)
            the_nroom.ppl_existence.add(offerto)

            the_nroom.save()
            offerto.save()

            messages.success(request,"davet onaylandı")
            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            return render(request,"ncactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')

def invite_nroom_n(request,username,id):
    the_nroom = get_object_or_404(non_classic_activity_room,id=id)
    mform = message_Form(request.POST or None)


    if (request.user.user_type != 2):

        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }
        
        return render(request,"ncactivities.html",value10)

    if request.user.user_type == 2:   
        offerto_core = get_object_or_404(usercore,username=username)
        offerto = consumer.objects.get(username_id=offerto_core.id)  

        if str(request.user.username) != str(offerto.username):
            messages.warning(request,"hainlik yapma...")
            value10 = {
            "room" : the_nroom,
            "mform":mform,
            }
            
            return render(request,"ncactivities.html",value10)

        offerto.n_room_offers.remove(the_nroom)

        the_nroom.save()
        offerto.save()

        messages.success(request,"davet reddedildi")
        value10 = {
        "room" : the_nroom,
        "mform":mform,
        }
        
        return render(request,"ncactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def add_placer_room_view(request):

    if request.user.user_type != 3:
        allplacers = placer.objects.all()
        allcommunities = community.objects.all()
        allactivities = classic_activities.objects.all()
        values= {
            "placer":allplacers,
            "community":allcommunities,
            "activities":allactivities,
        }
        messages.success(request,"no.")
        return render(request,"index.html",values)

    if request.method == "POST" or None:

        prrform = add_placer_room(request.POST)

        if prrform.is_valid():

            name = prrform.cleaned_data.get("name")
            description = prrform.cleaned_data.get("description")
            m_time =  prrform.cleaned_data.get("m_time")
            game_type = prrform.cleaned_data.get("game_type")
            max_ppl_existence = prrform.cleaned_data.get("max_ppl_existence")
            entry_price = prrform.cleaned_data.get("entry_price")

            the_usercore = usercore.objects.get(username=request.user.username)
            the_user = placer.objects.get(username_id=request.user.id)

            #m_time - 2 saat = closing time 

            time_change_3 = datetime.timedelta(hours=3)
            closing_time = m_time - time_change_3
            timenow = datetime.datetime.now()

            #eğer closing time şu ana eşit ya da gerideyse hata ver

            timenow = timezone.now()
            sixhour = timezone.timedelta(hours=6)
            sixlater = timenow + sixhour

            if sixlater >= m_time:
                messages.warning(request,"lobi en az 6 saat önceden hazır olmalıdır.")
                return redirect("index")          
                       
            if int(timenow.timestamp()) >= int(closing_time.timestamp()):

                value10 = {
                "prrform":prrform,
                }

                messages.error(request,('lobi, en az üç saat önceden hazır olmalıdır.'))
                return render(request,"add_prr.html",value10)

            ###---------

            nearoom= placer_room(creator=request.user,name=name,description=description,
            m_time=m_time,closing_time=closing_time,
            game_type=game_type,max_ppl_existence=max_ppl_existence,
            entry_price=entry_price)
            
            nearoom.save()

            nearoom.if_its_anywhere = the_user.area

            nearoom.save()


            ##--- manytomanies

            messages.success(request,"Tamamdır, lobiyi oluşturduk")
            return render(request,"index.html")

        else:

            prrform = add_placer_room()

            value10 = {
            "prrform":prrform,
            }

            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"add_prr.html",value10)

    else:
        
        prrform = add_placer_room()

        value10 = {
            "prrform":prrform,
            }

        return render(request,"add_prr.html",value10)

###--------------------------------------------------------------------------

@login_required(login_url='index')
def change_placer_room_view(request,id):

    the_proom = get_object_or_404(placer_room,id=id)

    if (request.user.user_type == 4):
        if the_proom.contact:
            if str(request.user.username) != str(the_proom.contact):
                messages.warning(request,"bunu yapmaya iznin yok.")         
                value10 = {
                "room" : the_proom,
                }
                
                return render(request,"pactivities.html",value10)

    elif (request.user.user_type == 3):
        if str(request.user.username) != str(the_proom.creator):  
            messages.warning(request,"bunu yapmaya iznin yok.")         
            value10 = {
            "room" : the_proom,
            }
            
            return render(request,"pactivities.html",value10)
      
    else:
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)

    if request.method == "POST" or None:

        prrform = change_placer_room(request.POST)

        if prrform.is_valid():

            name = prrform.cleaned_data.get("name")
            description = prrform.cleaned_data.get("description")
            max_ppl_existence = prrform.cleaned_data.get("max_ppl_existence")

            #m_time - 2 saat = closing time 

            time_change_3 = datetime.timedelta(hours=3)
            timenow = datetime.datetime.now()

            if name:
                the_proom.name = name
            
            if description:
                the_proom.description = description
            
            if max_ppl_existence:
                the_proom.max_ppl_existence = max_ppl_existence

            the_proom.save()

            ##--- manytomanies

            messages.success(request,"Tamamdır, değişiklikleri hallettik")      
            value10 = {
            "room" : the_proom,
            }
            
            return render(request,"pactivities.html",value10)


        else:

            prrform = add_placer_room()

            value10 = {
            "prrform":prrform,
            }

            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"update_prr.html",value10)

    else:
        
        prrform = add_placer_room()

        value10 = {
            "prrform":prrform,
        }

        return render(request,"update_prr.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def request_proom(request,id):

    the_usercore = get_object_or_404(usercore,username=request.user.username)
    the_proom = get_object_or_404(placer_room,id=id)

    if (request.user.user_type != 2):

        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)
    
    if request.user.user_type == 2:       
        the_user = consumer.objects.get(username_id=the_usercore.id)
        if the_proom.entry_price > the_user.money:
            messages.warning(request,"bakiyen yok, bakiye yükleyip tekrar dene")
            value10 = {
            "room" : the_proom,
            }
            
            return render(request,"pactivities.html",value10)

        the_proom.offers.add(the_user)
        the_proom.save()

        the_user.save()

        messages.success(request,(the_proom.name,"lobisine başarıyla istek atıldı"))
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def request_proom_n(request,id,username):
    the_proom = get_object_or_404(placer_room,id=id)

    the_offerer_core = get_object_or_404(usercore,username=username)
    the_offerer = consumer.objects.get(username_id=the_offerer_core.id)

    the_usercore = usercore.objects.get(username=request.user.username)
    
    if request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    if (request.user.user_type == 2):

        messages.warning(request,"bunu yapmaya iznin yok.")         
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)
    
    if (request.user.user_type == 3) or (request.user.user_type == 4):

        if ((request.user.username != the_usercore.username)):
            messages.warning(request,"bunu yapmaya iznin yok.")          
            value10 = {
            "room" : the_proom,
            }
            
            return render(request,"pactivities.html",value10)
        
        if the_proom.contact == None:
            if (the_usercore == the_proom.creator):
                the_proom.offers.remove(the_offerer)
                the_proom.save()

                messages.success(request,"kişi başarıyla silindi")
                value10 = {
                "room" : the_proom,
                }
                
                return render(request,"pactivities.html",value10)     
            else:
                messages.warning(request,"bunu yapmaya iznin yok.")          
                value10 = {
                "room" : the_proom,
                }
                
                return render(request,"pactivities.html",value10)                
        
        elif the_proom.contact:
            if str(the_usercore.username) == str(the_proom.contact):
                the_proom.offers.remove(the_offerer)
                the_proom.save()
                messages.success(request,"kişi başarıyla silindi")
                value10 = {
                "room" : the_proom,
                }
                
                return render(request,"pactivities.html",value10)     
            else:
                messages.warning(request,"bunu yapmaya iznin yok.")          
                value10 = {
                "room" : the_proom,
                }
                
                return render(request,"pactivities.html",value10)     
            
        elif str(request.user.username) == str(the_offerer.username):
            the_proom.offers.remove(the_offerer)
            the_proom.save()
            messages.success(request,"kişi başarıyla silindi")
            value10 = {
            "room" : the_proom,
            }
            
            return render(request,"pactivities.html",value10)          
            
        else:
            messages.error(request,"hata")
            value10 = {
            "room" : the_proom,
            }
            
            return render(request,"pactivities.html",value10)      

###---------------------------------------------------------------------------

@login_required(login_url='index')
def request_proom_y(request,id,username):

    the_proom = get_object_or_404(placer_room,id=id)

    the_offerer_core = get_object_or_404(usercore,username=username)
    the_offerer = consumer.objects.get(username_id=the_offerer_core.id)


    the_usercore = usercore.objects.get(username=request.user.username)
    
    if request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)


    if the_proom.entry_price > the_offerer.money:
        the_proom.offers.remove(the_offerer)
        the_proom.save()
        messages.warning(request,"kişinin yeterli bakiyesi kalmamış, reddedildi")     
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)    

    if (the_proom.max_ppl_existence > the_proom.ppl_existence.count()):

        if the_proom.contact:

            if str(the_usercore.username) == str(the_proom.contact):

                if the_proom.fee:

                    the_placer = placer.objects.get(username_id=the_proom.creator.id)
                    the_placer.money = the_proom.fee + the_placer.money
                    the_placer.save()

                    the_communitycore = usercore.objects.get(username=the_proom.contact)
                    the_community = community.objects.get(username_id=the_communitycore.id)
                    the_community.money = the_proom.entry_price - the_proom.fee + the_community.money
                    the_community.save()

                else:

                    the_placer = placer.objects.get(username_id=the_proom.creator.id)
                    the_placer.money = the_proom.entry_price + the_placer.money
                    the_placer.save()

                the_offerer.money = the_offerer.money - the_proom.entry_price
                the_proom.offers.remove(the_offerer)
                the_proom.ppl_existence.add(the_offerer)
                the_offerer.in_placer_rooms.add(the_proom)
                the_offerer.save()
                the_proom.save()
            else: 
                messages.warning(request,"bunu yapmaya iznin yok.")          
                value10 = {
                "room" : the_proom,
                }
                
                return render(request,"pactivities.html",value10)
            
        elif the_proom.contact == None:

            if (the_usercore == the_proom.creator):
                the_offerer.money = the_offerer.money - the_proom.entry_price

                the_placer = placer.objects.get(username_id=the_proom.creator.id)
                the_placer.money = the_proom.entry_price + the_placer.money
                the_placer.save()
                                            
                the_proom.offers.remove(the_offerer)
                the_proom.ppl_existence.add(the_offerer)
                the_offerer.in_placer_rooms.add(the_proom)
                the_offerer.save()
                the_proom.save()       

            else:
                messages.warning(request,"bunu yapmaya iznin yok.")          
                value10 = {
                "room" : the_proom,
                }
                
                return render(request,"pactivities.html",value10)
            
        messages.success(request,"kişi başarıyla eklendi")         
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)
    

    else:
        messages.error(request,"hata")     
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10) 

###---------------------------------------------------------------------------

def placer_activities(request,id): 

    the_usercore = request.user
    the_proom = get_object_or_404(placer_room,id=id)

    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)

    all_consumers = consumer.objects.all()

    values = {
                "room": get_object_or_404(placer_room,id=id),
                "all_consumers":all_consumers,
                }


    return render(request,"pactivities.html",values)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def invite_proom(request,username,id):

    the_proom = get_object_or_404(placer_room,id=id)

    offerto_core = get_object_or_404(usercore,username=username)
    offerto = consumer.objects.get(username_id=offerto_core.id)  

    if the_proom.max_ppl_existence <= the_proom.ppl_existence.count():
        messages.warning(request,"kişi sayısı doldu, davet yollayamazsınız...")         
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)

    if str(request.user.username) != str(the_proom.creator):
        messages.warning(request,"bunu yapmaya iznin yok.")          
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)

    offerto.p_room_offers.add(the_proom)
    offerto.save()
    messages.warning(request,"başarıyla yollandı..")       
    value10 = {
    "room" : the_proom,
    }
    
    return render(request,"pactivities.html",value10)


###---------------------------------------------------------------------------

def invite_proom_y(request,username,id):

    the_proom = get_object_or_404(placer_room,id=id)

    offerto_core = get_object_or_404(usercore,username=username)
    offerto = consumer.objects.get(username_id=offerto_core.id)  

    if str(request.user.username) != str(offerto.username):
        messages.warning(request,"hainlik yapma...")
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)


    if the_proom.max_ppl_existence <= the_proom.ppl_existence.count():
        messages.warning(request,"artık çok geç, kişiler doldu...")
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)

    if the_proom.entry_price > offerto.money:
        offerto.p_room_offers.remove(the_proom)   
        messages.warning(request,"kişinin yeterli bakiyesi kalmamış, reddedildi")
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)

    elif the_proom.entry_price < offerto.money:

        offerto.money = offerto.money - the_proom.entry_price

        if the_proom.fee:

            the_placer = placer.objects.get(username_id=the_proom.creator.id)
            the_placer.money = the_proom.fee + the_placer.money
            the_placer.save()

            the_communitycore = usercore.objects.get(username=the_proom.contact)
            the_community = community.objects.get(username_id=the_communitycore.id)
            the_community.money = the_proom.entry_price - the_proom.fee + the_community.money
            the_community.save()

        else:

            the_placer = placer.objects.get(username_id=the_proom.creator.id)
            the_placer.money = the_proom.entry_price + the_placer.money
            the_placer.save()

    offerto.p_room_offers.remove(the_proom)
    offerto.in_placer_rooms.add(the_proom)
    the_proom.ppl_existence.add(offerto)

    the_proom.save()
    offerto.save()

    messages.success(request,"davet onaylandı")
    value10 = {
    "room" : the_proom,
    }
    
    return render(request,"pactivities.html",value10)


###---------------------------------------------------------------------------

@login_required(login_url='index')
def invite_proom_n(request,username,id):

    the_proom = get_object_or_404(placer_room,id=id)

    offerto_core = get_object_or_404(usercore,username=username)
    offerto = consumer.objects.get(username_id=offerto_core.id)  

    if str(request.user.username) != str(offerto.username):
        messages.warning(request,"hainlik yapma...")
        value10 = {
        "room" : the_proom,
        }
        
        return render(request,"pactivities.html",value10)

    offerto.p_room_offers.remove(the_proom)

    the_proom.save()
    offerto.save()

    messages.success(request,"davet reddedildi")
    value10 = {
    "room" : the_proom,
    }
    
    return render(request,"pactivities.html",value10)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def games_p(request):

    the_placer = get_object_or_404(placer,id=request.user.id)
    all_games_p = placer_room.objects.all()

    timenow=datetime.datetime.now()
    
    value11={
        "all_games_p":all_games_p,
        "timenow":timenow,
    }

    return render(request,"games_p.html",value11)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def games_q(request):

    the_placer = get_object_or_404(placer,id=request.user.id)

    all_games_pq = placer_room_query.objects.all()

    timenow=datetime.datetime.now()
    
    value11={
        "the_placer":the_placer,
        "all_games_pq":all_games_pq,
        "timenow":timenow,
    }

    return render(request,"games_q.html",value11)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def add_placer_query_room_view(request):

    if request.user.user_type != 4:
        allplacers = placer.objects.all()
        allcommunities = community.objects.all()
        allactivities = classic_activities.objects.all()
        values= {
            "placer":allplacers,
            "community":allcommunities,
            "activities":allactivities,
        }
        messages.success(request,"hoş değil.")
        return render(request,"index.html",values)        





    if request.method == "POST" or None:

        prrform = add_placer_query_room(request.POST)

        if prrform.is_valid():

            name = prrform.cleaned_data.get("name")
            description = prrform.cleaned_data.get("description")
            m_time =  prrform.cleaned_data.get("m_time")
            game_type = prrform.cleaned_data.get("game_type")
            max_ppl_existence = prrform.cleaned_data.get("max_ppl_existence")
            entry_price = prrform.cleaned_data.get("entry_price")
            if_its_anywhere = prrform.cleaned_data.get("if_its_anywhere")
            room_node = prrform.cleaned_data.get("room_node")

            fee = prrform.cleaned_data.get("fee")
            pay = prrform.cleaned_data.get("pay")

            the_usercore = usercore.objects.get(username=request.user.username)
            the_user = community.objects.get(username_id=request.user.id)

            #m_time - 2 saat = closing time 

            time_change_3 = datetime.timedelta(hours=3)
            closing_time = m_time - time_change_3
            timenow = datetime.datetime.now()

            #eğer closing time şu ana eşit ya da gerideyse hata ver

            timenow = timezone.now()
            sixhour = timezone.timedelta(hours=6)
            sixlater = timenow + sixhour
            
            if sixlater >= m_time:
                messages.warning(request,"lobi en az 6 saat önceden hazır olmalıdır.")
                return redirect("index")          
            
            if int(timenow.timestamp()) >= int(closing_time.timestamp()):

                value10 = {
                "prrform":prrform,
                }

                messages.error(request,('lobi, en az üç saat önceden hazır olmalıdır.'))
                return render(request,"add_prr_q.html",value10)

            if if_its_anywhere.verify == False:
                
                messages.warning(request,"henüz mekan hazır değil.")
                allplacers = placer.objects.all()
                allcommunities = community.objects.all()
                allactivities = classic_activities.objects.all()
                values= {
                    "placer":allplacers,
                    "community":allcommunities,
                    "activities":allactivities,
                }

                return render(request,"index.html",values)    
            ###---------

            if pay:
                if the_user.money < pay:

                    value10= {"prrform":prrform,
                    }

                    messages.error(request,('yeterli bakiye yok. yükleyip tekrar deneyiniz.'))
                    return render(request,"add_prr_q.html",value10)

                
            nearoom= placer_room_query(creator=request.user,name=name,description=description,
            m_time=m_time,closing_time=closing_time,
            game_type=game_type,max_ppl_existence=max_ppl_existence,
            entry_price=entry_price,if_its_anywhere=if_its_anywhere,room_node=room_node)

            nearoom.save()

            if pay:
                nearoom.pay = int(pay)
                nearoom.save()
            
            if fee:
                nearoom.entry_price = int(entry_price) + int(fee)
                nearoom.fee = fee
                nearoom.save()

            the_usercore = usercore.objects.get(username=request.user.username)
            the_user = community.objects.get(username_id=the_usercore.id)

            the_user.p_room_offers_to_p.add(nearoom)
            the_user.save()


            ##--- manytomanies

            messages.success(request,"Tamamdır, lobiyi oluşturduk")
            return render(request,"index.html")

        else:

            prrform = add_placer_query_room()

            value10 = {
            "prrform":prrform,
            }

            messages.error(request,"Beklenmeyen bir hata oluştu.")
            print(str(Exception))
            return render(request,"add_prr_q.html",value10)
        


    else:
        
        prrform = add_placer_query_room()

        value10 = {
            "prrform":prrform,
            }

        return render(request,"add_prr_q.html",value10)

@login_required(login_url='index')
def placer_query_rooms_now(request):

    the_usercore = get_object_or_404(usercore,username=request.user.username)

    if (the_usercore.user_type != 4) and (request.user.username != the_usercore.username):
        messages.warning(request,"izniniz yok")
        return render(request,"games_pqn.html",value11)
    
    all_games_pq = placer_room_query.objects.all()
    timenow=datetime.datetime.now()

    #------- önemli 

    community_in_core =  community.objects.filter(username_id=request.user.id)

    #-------
    
    value11={

        "all_games_pq":all_games_pq,
        "community_in_core":community_in_core,
        "timenow":timenow,
    }

    return render(request,"games_pqn.html",value11)


@login_required(login_url='index')
def pcom_rooms_now(request):

    the_usercore = get_object_or_404(usercore,username=request.user.username)

    if (the_usercore.user_type != 4) and (request.user.username != the_usercore.username):
        messages.warning(request,"izniniz yok")
        return render(request,"games_pqn.html",value11)
    
    all_games_p = placer_room.objects.all()
    timenow=datetime.datetime.now()

    #------- önemli 

    community_in_core =  community.objects.filter(username_id=request.user.id)

    #-------
    
    value11={

        "all_games_p":all_games_p,
        "community_in_core":community_in_core,
        "timenow":timenow,
    }

    return render(request,"games_pcn.html",value11)

@login_required(login_url='index')
def pcom_rooms_old(request):

    the_usercore = get_object_or_404(usercore,username=request.user.username)

    if (the_usercore.user_type != 4) and (request.user.username != the_usercore.username):
        messages.warning(request,"izniniz yok")
        return render(request,"games_pqn.html",value11)
    
    all_games_p = placer_room.objects.all()
    timenow=datetime.datetime.now()

    #------- önemli 

    community_in_core =  community.objects.filter(username_id=request.user.id)

    #-------
    
    value11={

        "all_games_p":all_games_p,
        "community_in_core":community_in_core,
        "timenow":timenow,
    }

    return render(request,"games_pco.html",value11)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def delete_placer_query_room_view(request,id):

    the_pqroom = get_object_or_404(placer_room_query,id=id)
    timenow = datetime.datetime.now()

    if ((request.user != the_pqroom.creator) and (request.user.user_type != 1)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        return redirect("index")  
    
    the_pqroom.delete()
    messages.success(request,(the_pqroom.name ,"isimli oda davetini geri çektik"))
    return redirect("index")

###---------------------------------------------------------------------------

@login_required(login_url='index')
def placer_query_activities(request,id): 

    the_usercore = request.user
    the_pqroom = get_object_or_404(placer_room_query,id=id)

    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    all_consumers = consumer.objects.all()

    values = {
                "room": get_object_or_404(placer_room_query,id=id),
                "the_user":the_user,
                "all_consumers":all_consumers,
                }


    return render(request,"pqactivities.html",values)

###---------------------------------------------------------------------------

@login_required(login_url='index')
def placer_query_activities_y(request,id): 

    the_usercore = request.user
    the_pqroom = get_object_or_404(placer_room_query,id=id)


    if (request.user.user_type != 3) and (str(request.user.username) != str(the_pqroom.if_its_anywhere)):

        messages.warning(request, "izniniz yok.")
        allplacers = placer.objects.all()
        allcommunities = community.objects.all()
        allactivities = classic_activities.objects.all()

        values= {
            "placer":allplacers,
            "community":allcommunities,
            "activities":allactivities,
        }

        return render(request,"index.html",values)

    the_user = placer.objects.get(username_id=the_usercore.id)

    the_communitycore = usercore.objects.get(username=the_pqroom.contact)
    the_community = community.objects.get(username_id=the_communitycore.id)

    if the_pqroom.pay:
        if the_community.money < the_pqroom.pay:
            messages.warning(request, "kişinin yeterli bakiyesi kalmamış. bakiye yüklemesini rica edebilirsiniz.")
            allplacers = placer.objects.all()
            allcommunities = community.objects.all()
            allactivities = classic_activities.objects.all()

            values= {
                "placer":allplacers,
                "community":allcommunities,
                "activities":allactivities,
            }

            return render(request,"index.html",values)          

    
    if the_user == the_pqroom.if_its_anywhere:

        nearoom = placer_room(name=the_pqroom.name, description=the_pqroom.description,
        game_type=the_pqroom.game_type, if_its_anywhere=the_pqroom.if_its_anywhere.area,
        m_time=the_pqroom.m_time, c_time= the_pqroom.c_time,closing_time=the_pqroom.closing_time,
        creator=request.user,contact=str(the_pqroom.creator),max_ppl_existence=the_pqroom.max_ppl_existence,
        entry_price=the_pqroom.entry_price
        )
        nearoom.save()

        if the_pqroom.fee:
            nearoom.fee = the_pqroom.fee
            nearoom.save()
            
        if the_pqroom.pay:
            nearoom.pay = the_pqroom.pay
            nearoom.save()

            the_community.money = the_community.money - the_pqroom.pay
            the_community.save()

            the_pqroom.creator.money = the_pqroom.creator.money + the_pqroom.pay
            the_pqroom.creator.save()

        the_pqroom.delete()


        messages.success(request,"aktivite başarıyla onaylandı, gerisi diğerlerinde.")
        timenow = datetime.datetime.now()
        the_proom = nearoom

        gamevalues={

            "timenow":timenow,
            "room":the_proom,
        }

        return render(request,"pactivities.html",gamevalues)  
    
    else:

        messages.warning(request, "beklenmedik bir hata oluştu. tekrar deneyiniz.")
        allplacers = placer.objects.all()
        allcommunities = community.objects.all()
        allactivities = classic_activities.objects.all()
        values= {
            "placer":allplacers,
            "community":allcommunities,
            "activities":allactivities,
        }

        return render(request,"index.html",values)

@login_required(login_url='index')
def placer_query_activities_n(request,id): 

    the_usercore = request.user
    the_pqroom = get_object_or_404(placer_room_query,id=id)

    if (request.user.user_type != 3) and (str(request.user.username) != str(the_pqroom.if_its_anywhere)):

        messages.warning(request, "izniniz yok.")
        allplacers = placer.objects.all()
        allcommunities = community.objects.all()
        allactivities = classic_activities.objects.all()

        values= {
            "placer":allplacers,
            "community":allcommunities,
            "activities":allactivities,
        }

        return render(request,"index.html",values)
    
    the_user = placer.objects.get(username_id=the_usercore.id)

    if the_user == the_pqroom.if_its_anywhere:

        the_pqroom.delete()

        messages.success(request,"aktivite önerisi reddedildi.")
        return render(request,"index.html")
    
    else:
        
        messages.warning(request, "beklenmedik bir hata oluştu. tekrar deneyiniz.")
        return render(request,"index.html")

def croom_query_back(request,id):

    the_croom = get_object_or_404(classic_room,id=id)
    the_usercore = get_object_or_404(usercore,username=request.user.username)

    if ((request.user.username != the_usercore.username) or (request.user.user_type != 2)):

        messages.warning(request,"bunu yapmaya iznin yok.")
         
        if request.user.user_type != 2:
            allplacers = placer.objects.all()
            allcommunities = community.objects.all()
            allactivities = classic_activities.objects.all()
            values= {
                "placer":allplacers,
                "community":allcommunities,
                "activities":allactivities,
            }

            return render(request,"index.html",values)
        
    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    if the_user in the_croom.offers.all():
        the_croom.offers.remove(the_user)
        the_user.c_room_offers.remove(the_croom)
        the_croom.save()
        the_user.save()

        messages.success(request,(the_croom,"istek başarıyla geri çekildi"))

        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)
        timenow = datetime.datetime.now()
        gamevalues={

            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
            "room":the_croom,
        }

        return render(request,"ccactivities.html",gamevalues)

def proom_query_back(request,id):
    
    the_proom = get_object_or_404(placer_room,id=id)
    the_usercore = get_object_or_404(usercore,username=request.user.username)

    if ((request.user.username != the_usercore.username) or (request.user.user_type != 2)):

        messages.warning(request,"bunu yapmaya iznin yok.")
         
        if request.user.user_type != 2:
            allplacers = placer.objects.all()
            allcommunities = community.objects.all()
            allactivities = classic_activities.objects.all()
            values= {
                "placer":allplacers,
                "community":allcommunities,
                "activities":allactivities,
            }

            return render(request,"index.html",values)
        
    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    if the_user in the_proom.offers.all():
        the_proom.offers.remove(the_user)
        the_user.p_room_offers.remove(the_proom)
        the_proom.save()
        the_user.save()

        messages.success(request,(the_proom,"istek başarıyla geri çekildi"))

        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)
        timenow = datetime.datetime.now()
        gamevalues={

            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
            "room":the_proom,
        }

        return render(request,"pactivities.html",gamevalues)

def nroom_query_back(request,id):
    
    the_nroom = get_object_or_404(non_classic_activity_room,id=id)
    the_usercore = get_object_or_404(usercore,username=request.user.username)

    if ((request.user.username != the_usercore.username) or (request.user.user_type != 2)):

        messages.warning(request,"bunu yapmaya iznin yok.")
         
        if request.user.user_type != 2:
            allplacers = placer.objects.all()
            allcommunities = community.objects.all()
            allactivities = classic_activities.objects.all()
            values= {
                "placer":allplacers,
                "community":allcommunities,
                "activities":allactivities,
            }

            return render(request,"index.html",values)
        
    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    if the_user in the_nroom.offers.all():
        the_nroom.offers.remove(the_user)
        the_user.n_room_offers.remove(the_nroom)
        the_nroom.save()
        the_user.save()

        messages.success(request,(the_nroom,"istek başarıyla geri çekildi"))

        consumer_in_core =  consumer.objects.filter(username_id=request.user.id)
        timenow = datetime.datetime.now()
        gamevalues={

            "consumer_in_core":consumer_in_core,
            "timenow":timenow,
            "room":the_nroom,
        }

        return render(request,"ccactivities.html",gamevalues)
