from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect, render

import datetime 
from account.forms import *
from account.models import *
from activities.models import *
from activities.forms import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .forms import *
from django.contrib.auth import get_user_model


###---------------------------------------------------------------------------------------------------

def register_main(request):

    return render(request,"register_main.html")
    


###---------------------------------------------------------------------------------------------------

def consumer_register(request):
    
    if request.method == "POST" or None:
        
        crform = consumer_registerForm(request.POST, request.FILES)
        
        if crform.is_valid():
            
            username = crform.cleaned_data.get("username")
            password = crform.cleaned_data.get("password")

            name = crform.cleaned_data.get("name")
            surname = crform.cleaned_data.get("surname")
            university = crform.cleaned_data.get("university")
            email = crform.cleaned_data.get("email")
            phone = crform.cleaned_data.get("phone")
            gender = crform.cleaned_data.get("gender")
            verify_pic = crform.cleaned_data.get("verify_pic")

            new_usercore = usercore(username = username ,password=password,name=name,surname=surname,
            university=university,email=email,phone=phone,gender=gender,user_type=2,verify_pic=verify_pic)

            new_usercore.set_password(password)
            new_usercore.save()

            new_consumer = consumer(id=new_usercore.id,name=name,surname=surname,
            university=university,email=email,phone=phone,gender=gender)

            consumer_in_core = usercore.objects.filter(username=new_usercore.username)
            new_consumer.username = consumer_in_core[0]
            new_consumer.save()

            new_consumer.verify=False
            new_consumer.save()

            consumer_in_core.verify=False
            consumer_in_core.save()

            messages.success(request,"hesabı oluşturduk, aktivasyon için bekleyiniz...")

            return redirect("index")

        else:
            values11 = {
            "crform" : crform,
            }
            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"cregister.html",values11)
    else:

        crform = consumer_registerForm()

        value3 = {

        "crform" : crform,
        }
    
        return render(request,"cregister.html",value3)

###---------------------------------------------------------------------------------------------------

def placer_register(request):
    
    if request.method == "POST" or None:
        
        prform = placer_registerForm(request.POST, request.FILES)
        
        if prform.is_valid():
            
            username = prform.cleaned_data.get("username")
            password = prform.cleaned_data.get("password")
            phone = prform.cleaned_data.get("phone")
            email = prform.cleaned_data.get("email")
            verify_pic= prform.cleaned_data.get("verify_pic")
            min_price = prform.cleaned_data.get("min_price")
            
            area = prform.cleaned_data.get("area")
            place_name = prform.cleaned_data.get("place_name")
            
            max_table_normal = prform.cleaned_data.get("max_table_normal")
            max_table_not_normal = prform.cleaned_data.get("max_table_not_normal")

            new_p_name = (str(place_name) + " (" + str(area) + ")")

            new_usercore = usercore(username = username ,password=password,
            phone=phone,email=email,area=area,place_name=new_p_name,
            max_table_normal=max_table_normal,max_table_not_normal=max_table_not_normal,
            user_type=3,verify_pic=verify_pic)

            new_usercore.set_password(password)
            new_usercore.save()

            new_placer = placer(id=new_usercore.id,phone=phone,email=email,
            area=area,place_name=new_p_name,max_table_normal=max_table_normal,max_table_not_normal=max_table_not_normal,
            )

            placer_in_core = usercore.objects.filter(username=new_usercore.username)
            new_placer.username = placer_in_core[0]
            new_placer.min_price = min_price

            new_placer.a11_max_table_normal = max_table_normal
            new_placer.a12_max_table_normal = max_table_normal
            new_placer.a13_max_table_normal = max_table_normal
            new_placer.a14_max_table_normal = max_table_normal
            new_placer.a15_max_table_normal = max_table_normal

            new_placer.a21_max_table_normal = max_table_normal
            new_placer.a22_max_table_normal = max_table_normal
            new_placer.a23_max_table_normal = max_table_normal
            new_placer.a24_max_table_normal = max_table_normal
            new_placer.a25_max_table_normal = max_table_normal

            new_placer.a11_max_table_not_normal = max_table_not_normal
            new_placer.a12_max_table_not_normal = max_table_not_normal
            new_placer.a13_max_table_not_normal = max_table_not_normal
            new_placer.a14_max_table_not_normal = max_table_not_normal
            new_placer.a15_max_table_not_normal = max_table_not_normal

            new_placer.a21_max_table_not_normal = max_table_not_normal
            new_placer.a22_max_table_not_normal = max_table_not_normal
            new_placer.a23_max_table_not_normal = max_table_not_normal
            new_placer.a24_max_table_not_normal = max_table_not_normal
            new_placer.a25_max_table_not_normal = max_table_not_normal

            new_placer.save()

            theplace = places.objects.get(place=area)
            theplace.existence_of_places.add(new_placer)
            theplace.save()


            new_placer.verify=False
            new_placer.save()

            placer_in_core.verify=False
            placer_in_core.save()

            messages.success(request,"hesabı oluşturduk, aktivasyon için bekleyiniz...")

            return redirect("index")

        else:
            values11 = {
            "prform" : prform,
            }
            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"pregister.html",values11)
    else:

        prform = placer_registerForm()

        value3 = {

        "prform" : prform,
        }
    
        return render(request,"pregister.html",value3)

###---------------------------------------------------------------------------------------------------

def all_login(request):

    lform = loginForm(request.POST or None)
    allplacers = placer.objects.all()
    allcommunities = community.objects.all()
    allactivities = classic_activities.objects.all()

    if request.method == "POST" and lform.is_valid():

        username = lform.cleaned_data.get("username")
        password = lform.cleaned_data.get("password")

        user_exists =  authenticate(username = username,password=password)  

        if user_exists == None:
            messages.error(request,"Kullanıcı adı ya da şifre hatalı...")
            value1 = {

            "lform" : lform,
            }
            
            return render(request,"login.html", value1)
        
        elif user_exists.verify == False:
            messages.error(request,"Doğrulamanız Henüz Yapılmadı...")
            value1 = {

            "lform" : lform,
            }
            
            return render(request,"login.html", value1)

        elif user_exists:

            login(request,user_exists)
            messages.success(request,"Kullanıcı girişi başarıyla tamamlandı...")

            values= {
                "placer":allplacers,
                "community":allcommunities,
                "activities":allactivities,
            }

            return render(request,"index.html",values)
        
        else:

            messages.error(request,"Beklenmeyen bir hata oluştu...")

            value1 = {

            "lform" : lform,
            }
            
            return render(request,"login.html", value1)

    else:
        value1 = {

        "lform" : lform,
        }
        
        return render(request,"login.html", value1)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def all_logout(request):
    logout(request)
    messages.success(request,"Çıkış başarıyla tamamlandı...")
    return redirect("index")

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def c_profile(request,username):

    the_usercore = get_object_or_404(usercore,username=username)
    the_user = consumer.objects.get(username_id=the_usercore.id)

    me = request.user

    if me.user_type == 2:
        me_user = consumer.objects.get(username_id = me.id)
    elif me.user_type == 3:
        me_user = placer.objects.get(username_id = me.id)
    elif me.user_type == 4:
        me_user = community.objects.get(username_id = me.id)

    value1 = {
        "the_usercore": the_usercore,
        "the_user":the_user,
        "me_user":me_user,
    }

    return render(request,"profile_c.html", value1)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def wallet(request):

    the_usercore = get_object_or_404(usercore,username=request.user.username)

    if request.user.username == the_usercore.username:

        if the_usercore.user_type == 2:
            the_user = consumer.objects.get(username_id=the_usercore.id)

        elif the_usercore.user_type == 3:
            the_user = placer.objects.get(username_id=the_usercore.id)

        elif the_usercore.user_type == 4:
            the_user = community.objects.get(username_id=the_usercore.id)

        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"c_wallet.html", value1)

    else:
        messages.error(request,"kendinin olmayan hesaba bakamazsın.")
        the_usercore = request.user
        allplacers = placer.objects.all()
        allcommunities = community.objects.all()
        allactivities = classic_activities.objects.all()
        values= {
            "placer":allplacers,
            "community":allcommunities,
            "activities":allactivities,
        }

        return render(request,"index.html",values)



###---------------------------------------------------------------------------------------------------

def p_profile(request,username):

    the_usercore = get_object_or_404(usercore,username=username)
    the_user = placer.objects.get(username_id=the_usercore.id)
    
    value1 = {
        "the_usercore": the_usercore,
        "the_user":the_user
    }

    return render(request,"profile_p.html", value1)

###---------------------------------------------------------------------------------------------------

def co_profile(request,username):

    the_usercore = get_object_or_404(usercore,username=username)
    the_user = community.objects.get(username_id=the_usercore.id)

    value1 = {
        "the_usercore": the_usercore,
        "the_user":the_user
    }

    return render(request,"profile_co.html", value1)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def p_profile_update(request,username):

    the_usercore = get_object_or_404(usercore,username=username)

    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_p.html", value1)

    

    if (request.method == "POST" or None) and ((request.user == the_usercore)) :

        puform = placer_updateForm(request.POST, request.FILES)

        if puform.is_valid():

            password = puform.cleaned_data.get("password")
            phone = puform.cleaned_data.get("phone")

            pic1 = puform.cleaned_data.get("pic1")
            pic2 = puform.cleaned_data.get("pic2")
            pic3 = puform.cleaned_data.get("pic3")
            pic4 = puform.cleaned_data.get("pic4")
            pic5 = puform.cleaned_data.get("pic5")

            if password:
                the_user.password = password
                the_user.save()
            if phone:
                the_user.phone = phone
                the_user.save()
            if pic1:
                the_user.pic1 = pic1
                the_user.save()            
            if pic2:
                the_user.pic2 = pic2
                the_user.save()  
            if pic3:
                the_user.pic3 = pic3
                the_user.save()
            if pic4:
                the_user.pic4 = pic4
                the_user.save()  
            if pic5:
                the_user.pic5 = pic5
                the_user.save()
                
            messages.success(request,"güncellemeleri yaptık, hayırlısı olsun")
            value1 = {
                "the_usercore": the_usercore,
                "the_user":the_user
            }

            return render(request,"profile_p.html", value1)

        else:

            values11 = {
            "puform" : puform,
            "the_user":the_user,
            "the_usercore":the_usercore,
            }
            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"update_p.html",values11)
    
    else:

        puform = placer_updateForm()

        value3 = {
            "the_usercore":the_usercore,
            "the_user":the_user,
            "puform":puform,
        }

        return render(request,"update_p.html",value3)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def co_profile_update(request,username):

    the_usercore = get_object_or_404(usercore,username=username)

    if request.user.user_type == 2:
        the_user = consumer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 3:
        the_user = placer.objects.get(username_id=the_usercore.id)
    elif request.user.user_type == 4:
        the_user = community.objects.get(username_id=the_usercore.id)

    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_p.html", value1)

    if (request.method == "POST" or None) and ((request.user == the_usercore)) :

        couform = community_updateForm(request.POST, request.FILES)

        if couform.is_valid():

            password = couform.cleaned_data.get("password")
            phone = couform.cleaned_data.get("phone")

            pic1 = couform.cleaned_data.get("pic1")
            pic2 = couform.cleaned_data.get("pic2")
            pic3 = couform.cleaned_data.get("pic3")
            pic4 = couform.cleaned_data.get("pic4")
            pic5 = couform.cleaned_data.get("pic5")

            if password:
                the_user.password = password
                the_user.save()
            if phone:
                the_user.phone = phone
                the_user.save()
            if pic1:
                the_user.pic1 = pic1
                the_user.save()            
                
            messages.success(request,"güncellemeleri yaptık, hayırlısı olsun")
            value1 = {
                "the_usercore": the_usercore,
                "the_user":the_user
            }

            return render(request,"profile_co.html", value1)

        else:

            values11 = {
            "couform":couform,
            "the_user":the_user,
            "the_usercore":the_usercore,
            }
            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"update_co.html",values11)
    
    else:

        couform = consumer_updateForm()

        value3 = {
            "the_usercore":the_usercore,
            "the_user":the_user,
            "couform":couform,
        }

        return render(request,"update_co.html",value3)

###---------------------------------------------------------------------------------------------------


@login_required(login_url='index')
def p_profile_query(request,username):

    the_usercore = get_object_or_404(usercore,username=username)
    the_user = placer.objects.get(username_id=the_usercore.id)

    d1 = datetime.date.today()

    addoneday = datetime.timedelta(days=1)

    d2 = d1 + addoneday
    d3 = d2 + addoneday
    d4 = d3 + addoneday
    d5 = d4 + addoneday
    d6 = d5 + addoneday
    d7 = d6 + addoneday
    d8 = d7 + addoneday
    d9 = d8 + addoneday
    d10 = d9 + addoneday

    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"bunu yapmaya iznin yok.")        

        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_p.html", value1)

    if request.method == "POST" or None:

        pqform = placer_queryForm(request.POST, request.FILES)

        def get_input_value(form_data, field_name):
            value = form_data.get(field_name)
            
            if value is None:
                
                return value

            elif value:

                if value == 25:
                    value = "0"
                    return value

                else:
                    return value
                

        if pqform.is_valid():

            max_table_normal = get_input_value(pqform.cleaned_data, 'max_table_normal')

            max_table_not_normal = get_input_value(pqform.cleaned_data, 'max_table_not_normal')


            a81_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a81_max_table_not_normal')
            a81_max_table_normal = get_input_value(pqform.cleaned_data, 'a81_max_table_normal')
 
            a82_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a82_max_table_not_normal')
            a82_max_table_normal = get_input_value(pqform.cleaned_data, 'a82_max_table_normal')

            a83_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a83_max_table_not_normal')
            a83_max_table_normal = get_input_value(pqform.cleaned_data, 'a83_max_table_normal')

            a84_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a84_max_table_not_normal')
            a84_max_table_normal = get_input_value(pqform.cleaned_data, 'a84_max_table_normal')

            a85_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a85_max_table_not_normal')
            a85_max_table_normal = get_input_value(pqform.cleaned_data, 'a85_max_table_normal')

            a91_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a91_max_table_not_normal')
            a91_max_table_normal = get_input_value(pqform.cleaned_data, 'a91_max_table_normal')

            a92_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a92_max_table_not_normal')
            a92_max_table_normal = get_input_value(pqform.cleaned_data, 'a92_max_table_normal')

            a93_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a93_max_table_not_normal')
            a93_max_table_normal = get_input_value(pqform.cleaned_data, 'a93_max_table_normal')

            a94_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a94_max_table_not_normal')
            a94_max_table_normal = get_input_value(pqform.cleaned_data, 'a94_max_table_normal')

            a95_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a95_max_table_not_normal')
            a95_max_table_normal = get_input_value(pqform.cleaned_data, 'a95_max_table_normal')

            a101_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a101_max_table_not_normal')
            a101_max_table_normal = get_input_value(pqform.cleaned_data, 'a101_max_table_normal')

            a102_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a102_max_table_not_normal')
            a102_max_table_normal = get_input_value(pqform.cleaned_data, 'a102_max_table_normal')

            a103_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a103_max_table_not_normal')
            a103_max_table_normal = get_input_value(pqform.cleaned_data, 'a103_max_table_normal')

            a104_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a104_max_table_not_normal')
            a104_max_table_normal = get_input_value(pqform.cleaned_data, 'a104_max_table_normal')

            a105_max_table_not_normal = get_input_value(pqform.cleaned_data, 'a105_max_table_not_normal')
            a105_max_table_normal =get_input_value(pqform.cleaned_data, 'a105_max_table_normal')

            if max_table_normal != None:
                the_user.max_table_normal = max_table_normal
                the_user.a81_max_table_normal = max_table_normal
                the_user.a82_max_table_normal = max_table_normal
                the_user.a83_max_table_normal = max_table_normal
                the_user.a84_max_table_normal = max_table_normal
                the_user.a85_max_table_normal = max_table_normal
                the_user.a91_max_table_normal = max_table_normal
                the_user.a92_max_table_normal = max_table_normal
                the_user.a93_max_table_normal = max_table_normal
                the_user.a94_max_table_normal = max_table_normal
                the_user.a95_max_table_normal = max_table_normal
                the_user.a101_max_table_normal = max_table_normal
                the_user.a102_max_table_normal = max_table_normal
                the_user.a103_max_table_normal = max_table_normal
                the_user.a104_max_table_normal = max_table_normal
                the_user.a105_max_table_normal = max_table_normal                                               
                the_user.save()

            if max_table_not_normal != None:
                the_user.max_table_not_normal = max_table_not_normal
                the_user.a81_max_table_not_normal = max_table_not_normal
                the_user.a82_max_table_not_normal = max_table_not_normal
                the_user.a83_max_table_not_normal = max_table_not_normal
                the_user.a84_max_table_not_normal = max_table_not_normal
                the_user.a85_max_table_not_normal = max_table_not_normal
                the_user.a91_max_table_not_normal = max_table_not_normal
                the_user.a92_max_table_not_normal = max_table_not_normal
                the_user.a93_max_table_not_normal = max_table_not_normal
                the_user.a94_max_table_not_normal = max_table_not_normal
                the_user.a95_max_table_not_normal = max_table_not_normal
                the_user.a101_max_table_not_normal = max_table_not_normal
                the_user.a102_max_table_not_normal = max_table_not_normal
                the_user.a103_max_table_not_normal = max_table_not_normal
                the_user.a104_max_table_not_normal = max_table_not_normal
                the_user.a105_max_table_not_normal = max_table_not_normal                                               
                the_user.save()

            if a81_max_table_normal != None:
                the_user.a81_max_table_normal = a81_max_table_normal
                the_user.save()

            if a82_max_table_normal != None:
                the_user.a82_max_table_normal = a82_max_table_normal
                the_user.save()

            if a83_max_table_normal != None:
                the_user.a83_max_table_normal = a83_max_table_normal
                the_user.save()

            if a84_max_table_normal != None:
                the_user.a84_max_table_normal = a84_max_table_normal
                the_user.save()

            if a85_max_table_normal != None:
                the_user.a85_max_table_normal = a85_max_table_normal
                the_user.save()

            if a91_max_table_normal != None:
                the_user.a91_max_table_normal = a91_max_table_normal
                the_user.save()

            if a92_max_table_normal != None:
                the_user.a92_max_table_normal = a92_max_table_normal
                the_user.save()

            if a93_max_table_normal != None:
                the_user.a93_max_table_normal = a93_max_table_normal
                the_user.save()

            if a94_max_table_normal != None:
                the_user.a94_max_table_normal = a94_max_table_normal
                the_user.save()

            if a95_max_table_normal != None:
                the_user.a95_max_table_normal = a95_max_table_normal
                the_user.save()

            if a101_max_table_normal != None:
                the_user.a101_max_table_normal = a101_max_table_normal
                the_user.save()

            if a102_max_table_normal != None:
                the_user.a102_max_table_normal = a102_max_table_normal
                the_user.save()

            if a103_max_table_normal != None:
                the_user.a103_max_table_normal = a103_max_table_normal
                the_user.save()

            if a104_max_table_normal != None:
                the_user.a104_max_table_normal = a104_max_table_normal
                the_user.save()

            if a105_max_table_normal != None:
                the_user.a105_max_table_normal = a105_max_table_normal
                the_user.save()

            if a81_max_table_not_normal != None:
                the_user.a81_max_table_not_normal = a81_max_table_not_normal
                the_user.save()

            if a82_max_table_not_normal != None:
                the_user.a82_max_table_not_normal = a82_max_table_not_normal
                the_user.save()

            if a83_max_table_not_normal != None:
                the_user.a83_max_table_not_normal = a83_max_table_not_normal
                the_user.save()

            if a84_max_table_not_normal != None:
                the_user.a84_max_table_not_normal = a84_max_table_not_normal
                the_user.save()

            if a85_max_table_not_normal != None:
                the_user.a85_max_table_not_normal = a85_max_table_not_normal
                the_user.save()

            if a91_max_table_not_normal != None:
                the_user.a91_max_table_not_normal = a91_max_table_not_normal
                the_user.save()

            if a92_max_table_not_normal != None:
                the_user.a92_max_table_not_normal = a92_max_table_not_normal
                the_user.save()

            if a93_max_table_not_normal != None:
                the_user.a93_max_table_not_normal = a93_max_table_not_normal
                the_user.save()

            if a94_max_table_not_normal != None:
                the_user.a94_max_table_not_normal = a94_max_table_not_normal
                the_user.save()

            if a95_max_table_not_normal != None:
                the_user.a95_max_table_not_normal = a95_max_table_not_normal
                the_user.save()

            if a101_max_table_not_normal != None:
                the_user.a101_max_table_not_normal = a101_max_table_not_normal
                the_user.save()

            if a102_max_table_not_normal != None:
                the_user.a102_max_table_not_normal = a102_max_table_not_normal
                the_user.save()

            if a103_max_table_not_normal != None:
                the_user.a103_max_table_not_normal = a103_max_table_not_normal
                the_user.save()

            if a104_max_table_not_normal != None:
                the_user.a104_max_table_not_normal = a104_max_table_not_normal
                the_user.save()

            if a105_max_table_not_normal != None:
                the_user.a105_max_table_not_normal = a105_max_table_not_normal
                the_user.save()

            messages.success(request,"güncellemeleri yaptık, hayırlısı olsun")
            value1 = {
                "the_usercore": the_usercore,
                "the_user":the_user
            }

            return render(request,"profile_p.html", value1)
        
        else:

            values11 = {
            "pqform" : pqform,
            "the_user":the_user,
            "the_usercore":the_usercore,
            "d1":d1,
            "d2":d2,
            "d3":d3,
            "d4":d4,
            "d5":d5,
            "d6":d6,
            "d7":d7,
            "d8":d8,
            "d9":d9,
            "d10":d10,
            }

            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"update_pq.html",values11)
    
    else:

        pqform = placer_queryForm()

        value3 = {

            "pqform":pqform,
            "the_user":the_user,
            "the_usercore":the_usercore,
            "d1":d1,
            "d2":d2,
            "d3":d3,
            "d4":d4,
            "d5":d5,
            "d6":d6,
            "d7":d7,
            "d8":d8,
            "d9":d9,
            "d10":d10,
        }

        return render(request,"update_pq.html",value3)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def p_profile_query_ptf(request,username):

    the_usercore = get_object_or_404(usercore,username=username)
    the_user = placer.objects.get(username_id=the_usercore.id)

    d1 = datetime.date.today()

    addoneday = datetime.timedelta(days=1)

    d2 = d1 + addoneday
    d3 = d2 + addoneday
    d4 = d3 + addoneday
    d5 = d4 + addoneday
    d6 = d5 + addoneday
    d7 = d6 + addoneday
    d8 = d7 + addoneday
    d9 = d8 + addoneday
    d10 = d9 + addoneday

    valuex = {
            "the_user":the_user,
            "the_usercore":the_usercore,
            "d1":d1,
            "d2":d2,
            "d3":d3,
            "d4":d4,
            "d5":d5,
            "d6":d6,
            "d7":d7,
            "d8":d8,
            "d9":d9,
            "d10":d10,
        }

    return render(request,"update_pqptf.html",valuex)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def c_profile_update(request,username):

    the_usercore = get_object_or_404(usercore,username=username)
    the_user = consumer.objects.get(username_id=the_usercore.id)

    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1) 

    if request.method == "POST" or None:

        cuform = consumer_updateForm(request.POST, request.FILES)

        if cuform.is_valid():

            password = cuform.cleaned_data.get("password")
            phone = cuform.cleaned_data.get("phone")

            pic1 = cuform.cleaned_data.get("pic1")
            pic2 = cuform.cleaned_data.get("pic2")
            pic3 = cuform.cleaned_data.get("pic3")
            pic4 = cuform.cleaned_data.get("pic4")
            pic5 = cuform.cleaned_data.get("pic5")
            bio = cuform.cleaned_data.get("bio")

            if password:
                the_user.password = password
                the_user.save()
            if phone:
                the_user.phone = phone
                the_user.save()
            if pic1:
                the_user.pic1 = pic1
                the_user.save()            
            if pic2:
                the_user.pic2 = pic2
                the_user.save()  
            if pic3:
                the_user.pic3 = pic3
                the_user.save()
            if pic4:
                the_user.pic4 = pic4
                the_user.save()  
            if pic5:
                the_user.pic5 = pic5
                the_user.save() 

            if bio:
                the_user.bio = bio
                the_user.save()   
        
            messages.success(request,"güncellemeleri yaptık, hayırlısı olsun")
            value1 = {
                "the_usercore": the_usercore,
                "the_user":the_user
            }

            return render(request,"profile_c.html", value1)
        else:

            values11 = {
            "cuform" : cuform,
            "the_user":the_user,
            "the_usercore":the_usercore,
            }
            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"update_c.html",values11)
    
    else:

        cuform = consumer_updateForm()

        value3 = {

            "cuform":cuform,
            "the_user":the_user,
            "the_usercore":the_usercore,
        }

        return render(request,"update_c.html",value3)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def c_friends(request,username):
    
    the_usercore = get_object_or_404(usercore,username=username)
    the_user = consumer.objects.get(username_id=the_usercore.id)
    all_users = consumer.objects.all()

    if request.user.username != the_usercore.username:
        

        if request.user.user_type == 2:
            the_usercore = request.user
            the_user = consumer.objects.get(username_id=the_usercore.id)

            valuex = {
                    "the_user":the_user,
                    "the_usercore":the_usercore,
                    "all_users":all_users,
                }

            return render(request,"c_friends.html",valuex)  
           
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
    
    valuex = {
            "the_user":the_user,
            "the_usercore":the_usercore,
            "all_users":all_users,
        }

    return render(request,"c_friends.html",valuex)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def c_friends_ban(request,username,username2):
    
    the_usercore = get_object_or_404(usercore,username=username)
    the_user = consumer.objects.get(username_id=the_usercore.id)

    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1) 
    
    the_banned_usercore = get_object_or_404(usercore,username=username2)
    the_banned = consumer.objects.get(username_id=the_banned_usercore.id)
    
    the_user.ibanned.add(the_banned)
    the_banned.imbanned.add(the_user)
    
    the_banned.save()
    the_user.save()
    
    messages.success(request,"ban yapıldı...")

    the_usercore = get_object_or_404(usercore,username=username)
    the_user = consumer.objects.get(username_id=the_usercore.id)
    
    all_users = consumer.objects.all()
    
    valuex = {
            "the_user":the_user,
            "the_usercore":the_usercore,
            "all_users":all_users,
        }

    return render(request,"c_friends.html",valuex)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def c_friends_reban(request,username,username2):
    
    the_usercore = get_object_or_404(usercore,username=username)
    the_user = consumer.objects.get(username_id=the_usercore.id)
    
    the_banned_usercore = get_object_or_404(usercore,username=username2)
    the_banned = consumer.objects.get(username_id=the_banned_usercore.id)
    
    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1)

    if (request.user.username == the_usercore.username):
        the_user.ibanned.remove(the_banned)
        the_banned.save()
        the_banned.imbanned.remove(the_user)
        all_users = consumer.objects.all()
        messages.success(request,"ban kaldırıldı...")
        valuex = {
                "the_user":the_user,
                "the_usercore":the_usercore,
                "all_users":all_users,
            }

        return render(request,"c_friends.html",valuex)  
    
    else:
        messages.warning(request,"ban kaldırılamadı...")
        valuex = {
                "the_user":the_user,
                "the_usercore":the_usercore,
                "all_users":all_users,
            }

        return render(request,"c_friends.html",valuex)  
        
###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def c_friends_fquery(request,username,username2):
    
    the_usercore = get_object_or_404(usercore,username=username)
    the_user = consumer.objects.get(username_id=the_usercore.id)
    
    queryaskedto_usercore = get_object_or_404(usercore,username=username2)
    queryaskedto = consumer.objects.get(username_id=queryaskedto_usercore.id)
    
    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1)
         

    if (request.user.username == the_usercore.username):
        queryaskedto.friendsquery.add(the_user)
        queryaskedto.save()
        all_users = consumer.objects.all()
        messages.success(request,"arkadaşlık isteği atıldı...")

        valuex = {
                "the_user":the_user,
                "the_usercore":the_usercore,
                "all_users":all_users,
            }

        return render(request,"c_friends.html",valuex)  

    else:
        messages.warning(request,"yetkin yok...")
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1)
    
###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def c_friends_fquery_yes(request,username,username2):

    the_usercore = get_object_or_404(usercore,username=username)
    the_user = consumer.objects.get(username_id=the_usercore.id)
    
    queryaskedby_usercore = get_object_or_404(usercore,username=username2)
    queryaskedby = consumer.objects.get(username_id=queryaskedby_usercore.id)

    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"çakal.")         
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1)     

    if (request.user.username == the_usercore.username) or (the_usercore.user_type == 1):
        
        the_user.friendsquery.remove(queryaskedby)

        queryaskedby.friends.add(the_user)
        the_user.friends.add(queryaskedby)
        queryaskedby.save()
        the_user.save()

        messages.success(request,"arkadaşlık isteği kabul edildi")
        all_users = consumer.objects.all()
        
        valuex = {
                "the_user":the_user,
                "the_usercore":the_usercore,
                "all_users":all_users,
            }

        return render(request,"c_friends.html",valuex)
    else:
        messages.warning(request,"yetkin yok...")
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1)  

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def c_friends_fquery_no(request,username,username2):

    the_usercore = get_object_or_404(usercore,username=username)
    the_user = consumer.objects.get(username_id=the_usercore.id)
    
    queryaskedby_usercore = get_object_or_404(usercore,username=username2)
    queryaskedby = consumer.objects.get(username_id=queryaskedby_usercore.id)

    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"çakal.")         
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1)

    if (request.user.username == the_usercore.username):

        the_user.friendsquery.remove(queryaskedby)
        the_user.save()
        messages.success(request,"arkadaşlık isteği reddedildi")
        all_users = consumer.objects.all()
        valuex = {
                "the_user":the_user,
                "the_usercore":the_usercore,
                "all_users":all_users,
            }

        return render(request,"c_friends.html",valuex)  
    
    else:
        messages.warning(request,"yetkin yok...")
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def c_friends_fout(request,username,username2):

    the_usercore = get_object_or_404(usercore,username=username)
    the_user = consumer.objects.get(username_id=the_usercore.id)
    all_users = consumer.objects.all()
    
    queryaskedby_usercore = get_object_or_404(usercore,username=username2)
    queryaskedby = consumer.objects.get(username_id=queryaskedby_usercore.id)

    if ((request.user.username != the_usercore.username) and (request.user.user_type != 1)):
        messages.warning(request,"çakal.")         
        return redirect("index")     

    if (request.user.username == the_usercore.username) or (the_usercore.user_type == 1):

        the_user.friends.remove(queryaskedby)
        queryaskedby.friends.remove(the_user)
        the_user.save()
        queryaskedby.save()

        messages.success(request,"arkadaşlıktan çıkartıldı")
        valuex = {
                "the_user":the_user,
                "the_usercore":the_usercore,
                "all_users":all_users,
            }

        return render(request,"c_friends.html",valuex)  
    
    else:
        messages.warning(request,"yetkin yok...")
        valuex = {
                "the_user":the_user,
                "the_usercore":the_usercore,
                "all_users":all_users,
            }

        return render(request,"c_friends.html",valuex)      

@login_required(login_url='index')
def message_chat(request,username,username2):

    the_usercore = get_object_or_404(usercore,username=username)
    the_user = consumer.objects.get(username_id=the_usercore.id)

    messageto_usercore = get_object_or_404(usercore,username=username2)
    messageto = consumer.objects.get(username_id=messageto_usercore.id)
    all_users = consumer.objects.all()

    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"çakal.")         
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1)  

    if the_user in messageto.imbanned.all():
        messages.warning(request,"kişinin engelini kaldırırsan yazabilirsin...")         
        valuex = {
                "the_user":the_user,
                "the_usercore":the_usercore,
                "all_users":all_users,
            }

        return render(request,"c_friends.html",valuex)    

    if messageto in the_user.imbanned.all():
        messages.warning(request,"kişi seni engellemiş, üzgünüz...")         
        valuex = {
                "the_user":the_user,
                "the_usercore":the_usercore,
                "all_users":all_users,
            }

        return render(request,"c_friends.html",valuex)  

    for chat in the_user.chats.all():

        #eğer herhangi bir chat varsa

        msg_manager = message_manager.objects.get(id=chat.id) 
        for people in msg_manager.whos_in.all():

                #chatteki kişilerden diğeri response edilense onu bul ve tanımla

            if people == messageto:
                real_msg_manager = msg_manager

                mform = message_Form(request.POST or None)

                if request.method == "POST" or None:
                    if mform.is_valid():
                        message_itself = mform.cleaned_data.get("message_itself")

                        new_message = between_two_ferns(message_itself=message_itself,creator=the_user,
                        manager=real_msg_manager)
                        new_message.c_time = datetime.datetime.now()
                        new_message.save()
                        real_msg_manager.chatbox.add(new_message)
                        real_msg_manager.save()
                        
                valuex = {
                    "the_user":the_user,
                    "messageto":messageto,
                    "real_msg_manager":real_msg_manager,
                    "mform":mform,
                        }     
                messages.success(request,"mesajlaşabilirsiniz")         
                return render(request,"message_box.html",valuex)

    real_msg_manager = message_manager()
    real_msg_manager.save()
    real_msg_manager.whos_in.add(the_user)
    real_msg_manager.whos_in.add(messageto)
    real_msg_manager.save()
    the_user.chats.add(real_msg_manager)
    messageto.chats.add(real_msg_manager)
    the_user.save()
    messageto.save()
    mform = message_Form(request.POST or None)
    
        
    valuex = {
        "the_user":the_user,
        "messageto":messageto,
        "real_msg_manager":real_msg_manager,
        "mform":mform,
        }

    messages.success(request,"mesajlaşma bloğu oluşturuldu")  
    return render(request,"message_box.html",valuex)

###---------------------------------------------------------------------------------------------------

def community_register(request):
    
    if request.method == "POST" or None:
        
        crform = community_registerForm(request.POST, request.FILES)
        
        if crform.is_valid():
            
            username = crform.cleaned_data.get("username")
            password = crform.cleaned_data.get("password")

            name = crform.cleaned_data.get("name")
            email = crform.cleaned_data.get("email")
            phone = crform.cleaned_data.get("phone")
            verify_pic = crform.cleaned_data.get("verify_pic")

            new_usercore = usercore(username = username ,password=password,
            email=email,phone=phone,user_type=4,verify_pic=verify_pic)

            new_usercore.set_password(password)
            new_usercore.save()

            new_consumer = community(id=new_usercore.id,name=name,
            email=email,phone=phone)

            consumer_in_core = usercore.objects.filter(username=new_usercore.username)
            new_consumer.username = consumer_in_core[0]
            new_consumer.save()

            new_consumer.verify=False
            new_consumer.save()
            consumer_in_core.verify=False
            consumer_in_core.save()

            messages.success(request,"hesabı oluşturduk, aktivasyon için bekleyiniz...")
            return redirect("index")

        else:
            values11 = {
            "crform" : crform,
            }
            messages.error(request,"Beklenmeyen bir hata oluştu.")
            return render(request,"comregister.html",values11)
    else:

        crform = consumer_registerForm()

        value3 = {

        "crform" : crform,
        }
    
        return render(request,"comregister.html",value3)
                    

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def all_placers(request):

    users = placer.objects.all()

    value = {
        "users":users,
    }

    return render(request,"placers.html",value)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def all_consumers(request):

    users = consumer.objects.all()

    value = {
        "users":users,
    }

    return render(request,"consumers.html",value)

###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def all_communities(request):

    users = community.objects.all()

    value = {
        "users":users,
    }

    return render(request,"communities.html",value)
    
###---------------------------------------------------------------------------------------------------

@login_required(login_url='index')
def message_chat_pc(request,username,username2):

    the_usercore = get_object_or_404(usercore,username=username)
    messageto_usercore = get_object_or_404(usercore,username=username2)

    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1)

    the_user = placer.objects.get(username_id=the_usercore.id)

    for chat in the_usercore.chats.all():

        #eğer herhangi bir chat varsa

        msg_manager = message_manager_2.objects.get(id=chat.id) 

        for people in msg_manager.whos_in.all():

                #chatteki kişilerden diğeri response edilense onu bul ve tanımla

            if people == messageto_usercore:
                real_msg_manager = msg_manager

                mform = message_Form(request.POST or None)

                if request.method == "POST" or None:
                    if mform.is_valid():
                        message_itself = mform.cleaned_data.get("message_itself")

                        new_message = between_two_ferns_2(message_itself=message_itself,creator=the_usercore,
                        manager=real_msg_manager)
                        new_message.c_time = datetime.datetime.now()
                        new_message.save()
                        real_msg_manager.chatbox.add(new_message)
                        real_msg_manager.save()
                        
                valuex = {
                    "the_user":the_usercore,
                    "messageto":messageto_usercore,
                    "real_msg_manager":real_msg_manager,
                    "mform":mform,
                        }     
                messages.success(request,"mesajlaşabilirsiniz")         
                return render(request,"message_box_2.html",valuex)

    real_msg_manager = message_manager_2()
    real_msg_manager.save()
    real_msg_manager.whos_in.add(the_usercore)
    real_msg_manager.whos_in.add(messageto_usercore)
    real_msg_manager.save()
    the_usercore.chats.add(real_msg_manager)
    messageto_usercore.chats.add(real_msg_manager)
    the_usercore.save()
    messageto_usercore.save()
    mform = message_Form(request.POST or None)
    
        
    valuex = {
        "the_user":the_usercore,
        "messageto":messageto_usercore,
        "real_msg_manager":real_msg_manager,
        "mform":mform,
        }

    messages.success(request,"mesajlaşma bloğu oluşturuldu")  
    return render(request,"message_box_2.html",valuex)
   

@login_required(login_url='index')
def placer_messages(request,username):

    the_usercore = get_object_or_404(usercore,username=username)
    
    if ((request.user.username != the_usercore.username)):
        messages.warning(request,"bunu yapmaya iznin yok.")         
        value1 = {
            "the_usercore": the_usercore,
            "the_user":the_user
        }

        return render(request,"profile_c.html", value1)
    
    all_communities = community.objects.all()
    the_user = placer.objects.get(username_id=the_usercore.id)

    value = {
        "the_usercore":the_usercore,
        "all_communities":all_communities,
    }

    return render(request,"p_messages.html",value)

def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def mailsend(subject,message,mail):

    sender_email = "xxx"
    receiver_email = mail
    password = "xxx"

    # E-posta içeriği
    subject = subject
    message = message

    # E-posta oluşturma
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # SMTP sunucusuna bağlanma ve e-posta gönderme
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        print("E-posta gönderildi!")
    except Exception as e:
        print("E-posta gönderilirken bir hata oluştu:", str(e))
    finally:
        if server is not None:
            server.quit()

def authenticate_with_email(username, email):
    User = get_user_model()

    try:
        user = User.objects.get(username=username, email=email)
        return user
    except User.DoesNotExist:
        return None
    
def all_forgot(request):

    fform = forgotForm(request.POST or None)

    if request.method == "POST" and fform.is_valid():
        # Form verilerini al
        username = fform.cleaned_data.get("username")
        email = fform.cleaned_data.get("email")

        # Kullanıcıyı doğrula
        user_exists = authenticate_with_email(username, email)

        if user_exists is None:

            values = {
                "fform" : fform,
            }

            messages.error(request, "Kullanıcı adı veya e-posta adresi hatalı")
            return render(request,"forgot.html", values)

        elif user_exists:
            # Yeni şifreyi oluştur
            password = generate_password(8)

            # Parolayı güncelle
            user_exists.set_password(password)
            user_exists.save()

            subject = "Tanı: Şifre Yenileme"
            message = "yeni şifreniz: " + str(password) 

            the_usercore = get_object_or_404(usercore,username=username)

            mail = the_usercore.email
            mailsend(subject,message,str(mail))

            messages.success(request,"yeni şifre mail adresinize yollandı.")
            return redirect("index")
        
            # Diğer işlemler ve mesajları ekle

        else:
            messages.error(request, "Beklenmeyen bir hata oluştu...")

    else:
        value1 = {

        "fform" : fform,
        }
        
        return render(request,"forgot.html", value1)
    

@login_required(login_url='index')
def verify_screen(request):

    user = request.user

    if request.user.user_type == 1:

        the_usercores = usercore.objects.all()
        
        value1 = {
            "user":user,
            "the_usercores": the_usercores,
        }

        return render(request,"verifier.html", value1)
    
    else:
        messages.success(request,"..!..")
        return redirect(request,"logout")
    
@login_required(login_url='index')
def verify_y(request,username):

    if request.user.user_type == 1:

        the_usercore = get_object_or_404(usercore,username=username)

        if the_usercore.user_type == 2:
            the_user = consumer.objects.get(username_id=the_usercore.id)
            the_user.verify = True
            the_user.save()

            the_usercore.verify = True
            the_usercore.save()

        elif the_usercore.user_type == 3:
            the_user = placer.objects.get(username_id=the_usercore.id)
            the_user.verify = True
            the_user.save()

            the_usercore.verify = True
            the_usercore.save()

        elif the_usercore.user_type == 4:
            the_user = community.objects.get(username_id=the_usercore.id)
            the_user.verify = True
            the_user.save()

            the_usercore.verify = True
            the_usercore.save()

        else:        

            the_usercores = usercore.objects.all()
            value1 = {
            "the_usercores": the_usercores,
            }

            messages.success(request,"hata oluştu")
            return render(request,"verifier.html", value1)

        the_usercores = usercore.objects.all()
        value1 = {
        "the_usercores": the_usercores,
        }
        messages.success(request,"done!")
        return render(request,"verifier.html", value1)
    
    else:
        messages.success(request,"..!..")
        return redirect(request,"logout")

@login_required(login_url='index')
def verify_n(request,username):

    if request.user.user_type == 1:

        the_usercore = get_object_or_404(usercore,username=username)

        if the_usercore.user_type == 2:
            the_user = consumer.objects.get(username_id=the_usercore.id)
            the_user.verify = False
            the_user.save()

            the_usercore.verify = False
            the_usercore.save()

        elif the_usercore.user_type == 3:
            the_user = placer.objects.get(username_id=the_usercore.id)
            the_user.verify = False
            the_user.save()

            the_usercore.verify = False
            the_usercore.save()

        elif the_usercore.user_type == 4:
            the_user = community.objects.get(username_id=the_usercore.id)
            the_user.verify = False
            the_user.save()

            the_usercore.verify = False
            the_usercore.save()
        else:        

            the_usercores = usercore.objects.all()
            value1 = {
            "the_usercores": the_usercores,
            }

            messages.success(request,"hata oluştu")
            return render(request,"verifier.html", value1)

        the_usercores = usercore.objects.all()
        value1 = {
        "the_usercores": the_usercores,
        }
        messages.success(request,"done!")
        return render(request,"verifier.html", value1)
    
    else:
        messages.success(request,"..!..")
        return redirect(request,"logout")

