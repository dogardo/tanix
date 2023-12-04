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

from account.forms import *
from account.models import *

from activities.models import *
from activities.forms import *

from wall.forms import *
from wall.models import *

from .forms import *
from .models import *

import uuid
import pytz

from django.utils import timezone
from django.contrib.auth.decorators import login_required

from celery.schedules import crontab
from celery.task import periodic_task

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from infinite_scroll_pagination.paginator import SeekPaginator
from django.http import Http404
from django.template.loader import render_to_string

@login_required(login_url='index')
def addpost(request):


    if request.method == "POST":
        wform = wallpostForm(request.POST, request.FILES, user=request.user)
        if wform.is_valid():

            try:

                the_usercore = request.user

                croom = wform.cleaned_data.get("croom")
                nroom = wform.cleaned_data.get("nroom")
                proom = wform.cleaned_data.get("proom")
                text = wform.cleaned_data.get("text")
                picture = wform.cleaned_data.get("picture")
                plac_es = wform.cleaned_data.get("plac_es")

                if croom:

                    current_time = timezone.now()
                    enabling_time = croom.m_time + datetime.timedelta(hours=1)

                    if enabling_time > current_time:
                        messages.warning(request,"aktivite başladıktan en az 1 saat sonra post atabilirsin.")
                        values = {

                            "wform":wform,

                        }

                        return render(request,"addposts.html",values)

                if nroom:

                    current_time = timezone.now()
                    enabling_time = nroom.m_time + datetime.timedelta(hours=1)

                    if enabling_time > current_time:
                        messages.warning(request,"aktivite başladıktan en az 1 saat sonra post atabilirsin.")
                        values = {

                            "wform":wform,

                        }

                        return render(request,"addposts.html",values)

                if proom:

                    current_time = timezone.now()
                    enabling_time = proom.m_time + datetime.timedelta(hours=1)

                    if enabling_time > current_time:
                        messages.warning(request,"aktivite başladıktan en az 1 saat sonra post atabilirsin.")
                        values = {

                            "wform":wform,

                        }

                        return render(request,"addposts.html",values)

                if request.user.user_type == 2:

                    the_user = consumer.objects.get(username_id=the_usercore.id)

                    if croom:

                        if the_user in croom.ppl_existence.all():
                            print("mekandaymış.")
                        else:
                            messages.warning(request,"seçtiğin aktivitede bulunmamışsın. bağlantılı hashtag açamazsın")  
                            values = {

                            "wform":wform,

                            }

                            return render(request,"addposts.html",values)

                    if nroom:
                        
                        if the_user in nroom.ppl_existence.all():
                            print("mekandaymış.")
                        else:
                            messages.warning(request,"seçtiğin aktivitede bulunmamışsın. bağlantılı hashtag açamazsın")  
                            values = {

                            "wform":wform,

                            }
                            return render(request,"addposts.html",values)

                    if proom:
                        
                        if the_user in proom.ppl_existence.all():
                            print("mekandaymış.")
                        else:
                            messages.warning(request,"seçtiğin aktivitede bulunmamışsın. bağlantılı hashtag açamazsın")  
                            values = {

                            "wform":wform,

                            }

                            return render(request,"addposts.html",values)

                elif request.user.user_type == 3:

                    the_user = placer.objects.get(username_id=the_usercore.id)

                    if croom:
                        if (the_user != croom.place):
                            messages.warning(request,"seçtiğin aktivite sende yapılmamış, yorum yazamazsın.")  
                            values = {

                            "wform":wform,

                            }

                            return render(request,"addposts.html",values)  

                    if nroom:
                        if (the_user != nroom.place):
                            messages.warning(request,"seçtiğin aktivite sende yapılmamış, yorum yazamazsın.")  
                            values = {

                            "wform":wform,

                            }

                            return render(request,"addposts.html",values)  

                    if proom:
                        if (the_usercore != proom.creator):
                            messages.warning(request,"seçtiğin aktivite sende yapılmamış, yorum yazamazsın.")  
                            values = {

                            "wform":wform,

                            }

                            return render(request,"addposts.html",values) 

                elif request.user.user_type == 4:

                    the_user = community.objects.get(username_id=the_usercore.id)

                    if croom:
                        messages.warning(request,"Sadece kendi düzenlediğin etkinlikler hakkında bağlantılı hashtag açabilirsin.")
                        values = {

                            "wform":wform,

                        }

                        return render(request,"addposts.html",values)  

                    if nroom:
                        messages.warning(request,"Sadece kendi düzenlediğin etkinlikler hakkında bağlantılı hashtag açabilirsin.")
                        values = {

                            "wform":wform,

                        }

                        return render(request,"addposts.html",values)  

                    if proom:
                        if (the_usercore != proom.contact):
                            messages.warning(request,"seçtiğin aktivitede düzenleyici sen değilsin. bağlantılı hashtag açamazsın")   
                            values = {

                                "wform":wform,

                            }

                            return render(request,"addposts.html",values)  
                        


                if croom:

                    if croom.place:
                        new_post = wallpost(creator=the_usercore,area=croom.place.area)
                        new_post.save()

                    elif croom.if_its_anywhere:
                        new_post = wallpost(creator=the_usercore,area=croom.if_its_anywhere)
                        new_post.save()                
                    

                    new_post.hashtag_croom = croom
                    new_post.save()

                elif nroom:

                    if nroom.place:
                        new_post = wallpost(creator=the_usercore,area=nroom.place.area)
                        new_post.save()

                    elif nroom.if_its_anywhere:
                        new_post = wallpost(creator=the_usercore,area=nroom.if_its_anywhere)
                        new_post.save()                
                    
                    new_post.hashtag_nroom = nroom
                    new_post.save()

                elif proom:

                    new_post = wallpost(creator=the_usercore,area=proom.if_its_anywhere)
                    new_post.save()

                    new_post.hashtag_proom = proom
                    new_post.save()

                elif plac_es:

                    new_post = wallpost(creator=the_usercore,area=plac_es)
                    new_post.save()

                else:
                    values = {

                        "wform":wform,

                    }
                    messages.success(request,"bir bölge seçilmedi")   
                    return render(request,"addposts.html",values)

                if picture:
                    print("5")
                    new_post.picture = picture
                    new_post.save()
                    print("6")

                if text:
                    new_post.text = text
                    new_post.save()

                print("1")
                location = places.objects.get(id=new_post.area_id)
                print("2")
                allposts = wallpost.objects.all()
                print("3")
                areaposts = [post for post in allposts if post.area == location]
                print("4")
                day = datetime.date.today()

                values = {
                    "location":location,
                    "day":day,
                    "posts":areaposts,

                }
                messages.success(request,"tmdır.")   
                return render(request,"allposts.html",values)
            
            except Exception as e:
                print("Django Error:", e)
                values = {

                    "wform":wform,

                }
                messages.success(request,"veriler sıkıntılı.")   
                return render(request,"addposts.html",values)
      
        if not wform.is_valid():
            for field, errors in wform.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error} \n")

            values = {

                "wform":wform,

            }
            messages.success(request,"veriler sıkıntılı.")   
            return render(request,"addposts.html",values)
                
    else:
        wform = wallpostForm(user=request.user)

    values = {

        "wform":wform,

    }

    messages.success(request,"beklenmeyen bir hata oluştu.")   
    return render(request,"addposts.html",values)

def deletepost(request,id):
        
    if request.user:

        the_post = get_object_or_404(wallpost,id=id)
        the_usercore = usercore.objects.get(id=request.user.id)

        if the_usercore != the_post.creator:
            messages.error(request,"Bu senin postun değil.")
            
            xxx = allposts(request,the_post.area.id,extra_context=None)
            return xxx 

        else:
            the_post.delete()

            xxx = allposts(request,the_post.area.id,extra_context=None)
            return xxx 

    else:
        xxx = allposts(request,the_post.area.id,extra_context=None)    
        return xxx  

def likepost(request,id):

    if request.user:
        the_post = get_object_or_404(wallpost,id=id)
        the_usercore = usercore.objects.get(id=request.user.id)

        if the_usercore not in the_post.likes.all():
            the_post.likes.add(the_usercore)     
            the_post.save()   
        
        xxx = allposts(request,the_post.area.id,extra_context=None)
        return xxx 
    
    else:
        xxx = allposts(request,the_post.area.id,extra_context=None)
        return xxx 
        

def unlikepost(request,id):

    if request.user:
        the_post = get_object_or_404(wallpost,id=id)
        the_usercore = usercore.objects.get(id=request.user.id)

        if the_usercore in the_post.likes.all():
            the_post.likes.remove(the_usercore)
            the_post.save()
                    
        xxx = allposts(request,the_post.area.id,extra_context=None)
        return xxx 

    else:
        
        xxx = allposts(request,the_post.area.id,extra_context=None) 
        return xxx 


def create_allposts_context(request, area_id):

    location = get_object_or_404(places, id=area_id)

    allposts = wallpost.objects.all()

    allposts_list = list(allposts)

    filtered_posts = [
        post for post in allposts_list if post.area.id == location.id
    ]

    sorted_posts = sorted(filtered_posts, key=lambda post: post.id ,reverse=True)

    day = datetime.date.today()
    
    return {

        "location": location,
        "day": day,
        "areaposts": filtered_posts,
        "sorted_posts": sorted_posts
    }

def allposts(request, area_id, extra_context=None):

    context = create_allposts_context(request, area_id)

    sorted_posts = context["sorted_posts"]

    paginator = Paginator(sorted_posts, per_page=6, orphans=1) 
    page = request.GET.get('page', 1)

    try:
        paginated_posts = paginator.page(page)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'has_next': False})
        raise Http404

    data = {
        'posts': [vars(post) for post in paginated_posts]
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(data)

    if extra_context is not None:
        context.update(extra_context)

    context1 = {
        'posts': paginated_posts,
        'page_template': "areaposts.html",
    }

    context1.update(context)

    
    return render(request, "allposts.html", context1)

def load_more_posts(request, area_id):

    print(area_id)
    page = request.GET.get('page', 1)
    per_page = 6

    context = create_allposts_context(request, area_id)
    sorted_posts = context["sorted_posts"]

    paginator = Paginator(sorted_posts, per_page)

    try:
        paginated_posts = paginator.page(page)
    except EmptyPage:
        return JsonResponse({'has_next': False})

    context1 = {
        'xpostsx': paginated_posts,
    }

    context1.update(context)

    html_content = render_to_string('allposts_partial.html', context1)

    return JsonResponse({'html_content': html_content})

def myposts(request):

    day = datetime.date.today()
    allposts = wallpost.objects.all()

    the_usercore = request.user
    
    ownposts = [post for post in allposts if post.creator == the_usercore]
    
    incposts = []
    for post in ownposts:
        if post.hashtag_croom and the_usercore in post.hashtag_croom.ppl_existence.all():
            incposts.append(post)

    innposts = []
    for post in ownposts:
        if post.hashtag_nroom and the_usercore in post.hashtag_nroom.ppl_existence.all():
            innposts.append(post)

    inpposts = []
    for post in ownposts:
        if post.hashtag_proom and the_usercore in post.hashtag_proom.ppl_existence.all():
            inpposts.append(post)

    values = {

        "incposts":incposts,
        "innposts":innposts,
        "inpposts":inpposts,
        "day":day,
    }

    return redirect(request,"myposts",**values)

def toggle_like(request, post_id):
    post = wallpost.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    likes_count = post.likes.count()
    return JsonResponse({'is_liked': is_liked, 'likes_count': likes_count})

def allwalls(request):
    allplaces = places.objects.all()

    values = {
        "allplaces":allplaces,
    }

    return render(request,"allwalls.html",values)