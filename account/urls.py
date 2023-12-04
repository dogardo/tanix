from django.contrib import admin
from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('p/', all_placers,name="all_placers"),
    path('c/', all_consumers,name="all_consumers"),
    path('co/', all_communities,name="all_communities"),

    path('register/', register_main,name="register"),

    path('p/register/', placer_register,name="register"),
    path('c/register/', consumer_register,name="c_register"),
    path('co/register/', community_register,name="community_register"),
    
    path('login/', all_login,name="all_login"),
    path('logout/',all_logout,name="all_logout"),
    path('forgot/',all_forgot,name="all_forgot"),

    path('p/<str:username>/', p_profile,name="p_profile"),
    path('c/<str:username>/', c_profile,name="c_profile"),
    path('co/<str:username>/', co_profile,name="co_profile"),

    path('my/wallet/', wallet,name="wallet"),

    path('c/<str:username>/message/<str:username2>/',message_chat,name="send_message"),
    path('pc/<str:username>/message/<str:username2>/',message_chat_pc,name="send_message_pc"),

    path('c/<str:username>/friends/', c_friends,name="c_friends"),
    path('p/<str:username>/messages/', placer_messages,name="placer_messages"),

    path('c/<str:username>/friends/fquery/<str:username2>/', c_friends_fquery,name="c_friends_fquery"),
    path('c/<str:username>/friends/fout/<str:username2>/', c_friends_fout,name="c_friends_fout"),

    path('c/<str:username>/friends/fquery/<str:username2>/yes/', c_friends_fquery_yes,name="c_friends_fquery_yes"),
    path('c/<str:username>/friends/fquery/<str:username2>/no/', c_friends_fquery_no,name="c_friends_fquery_no"),

    path('c/<str:username>/friends/ban/<str:username2>/', c_friends_ban,name="c_friends_ban"),
    path('c/<str:username>/friends/reban/<str:username2>/', c_friends_reban,name="c_friends_reban"),

    path('p/update/<str:username>/', p_profile_update,name="p_profile_update"),
    path('c/update/<str:username>/', c_profile_update,name="c_profile_update"),
    path('co/update/<str:username>/', co_profile_update,name="co_profile_update"),

    path('p/query/<str:username>/', p_profile_query,name="p_profile_query"),
    path('p/query/<str:username>/ptf', p_profile_query_ptf,name="p_profile_query_ptf"),
    
    path('verifier/', verify_screen,name="verify_screen"),
    path('verifier/<str:username>/y', verify_y,name="verify_y"),
    path('verifier/<str:username>/n', verify_n,name="verify_n"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
