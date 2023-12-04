from django.contrib import admin
from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',games,name="games"),
    path('load-more-data/', load_more_data, name='load_more_data'),

    path('fast/',games_fast,name="games_fast"),
    path('load-more-data-2/', load_more_data_2, name='load_more_data_2'),

    path('in/',games_in,name="games_in"),
    path('load-more-data-3/', load_more_data_3, name='load_more_data_3'),

    path('in/r',games_in_real,name="games_in_real"),
    path('load-more-data-4/', load_more_data_4, name='load_more_data_4'),

    path('in/o/',games_in_o,name="games_in_o"),
    path('load-more-data-5/', load_more_data_5, name='load_more_data_5'),

    path('p/',games_p,name="games_p"),

    path('q/',games_q,name="games_q"),
    
    path('p/q/',placer_query_rooms_now, name="placer_query_rooms_now"),
    path('p/n/',pcom_rooms_now, name="pcom_rooms_now"),
    path('p/o/',pcom_rooms_old, name="pcom_rooms_old"),

    path('<int:id>c/', real_classic_activities,name="classic_activites"),
    path('<int:id>n/', non_classic_activities,name="non_classic_activities"),
    path('<int:id>p/', placer_activities,name="placer_activities"),
    

    path('p/q/<int:id>/', placer_query_activities,name="placer_query_activities"),
    path('p/q/<int:id>/y', placer_query_activities_y,name="placer_query_activities_y"),
    path('p/q/<int:id>/n', placer_query_activities_n,name="placer_query_activities_n"),

    path('add/', add_choose,name="add_choose"),
    path('add/c/', add_classic_room,name="add_classic_room"),
    path('add/n/', add_non_classic_room,name="add_non_classic_room"),
    path('add/p/', add_placer_room_view,name="add_placer_room"),

    path('add/p/q/', add_placer_query_room_view,name="add_placer_query_room_view"),
    path('delete/p/q/<int:id>', delete_placer_query_room_view,name="delete_placer_query_room_view"),
    

    path('update/<int:id>c/', change_croom,name="change_croom"),
    path('update/<int:id>n/', change_nroom,name="change_nroom"),
    path('update/<int:id>p/', change_placer_room_view,name="change_placer_room_view"),

    path('delete/<int:id>c/', delete_croom,name="delete_croom"),
    path('delete/<int:id>n/', delete_nroom,name="delete_nroom"),
    path('delete/<int:id>p/', delete_proom,name="delete_proom"),

    path('quit/<int:id>c/', quit_croom,name="quit_croom"),
    path('quit/<int:id>n/', quit_nroom,name="quit_nroom"),
    path('quit/<int:id>p/', quit_proom,name="quit_proom"),

    path('back/<int:id>c/', croom_query_back,name="croom_query_back"),
    path('back/<int:id>n/', nroom_query_back,name="nroom_query_back"),
    path('back/<int:id>p/', proom_query_back,name="proom_query_back"),

    path('request/<int:id>c/', request_croom,name="request_croom"),
    path('request/<int:id>n/', request_nroom,name="request_nroom"),
    path('request/<int:id>p/', request_proom,name="request_proom"),

    path('request/<int:id>n/<str:username>/y', request_nroom_y,name="request_nroom_y"),
    path('request/<int:id>n/<str:username>/n', request_nroom_n,name="request_nroom_n"),

    path('request/<int:id>c/<str:username>/y', request_croom_y,name="request_croom_y"),
    path('request/<int:id>c/<str:username>/n', request_croom_n,name="request_croom_n"),

    path('request/<int:id>p/<str:username>/y', request_proom_y,name="request_proom_y"),
    path('request/<int:id>p/<str:username>/n', request_proom_n,name="request_proom_n"),

    path('<int:id>c/invite/<str:username>', invite_croom,name="invite_croom"),
    path('<int:id>c/invite/<str:username>/y', invite_croom_y,name="invite_croom_y"),
    path('<int:id>c/invite/<str:username>/n', invite_croom_n,name="invite_croom_n"),

    path('<int:id>n/invite/<str:username>', invite_nroom,name="invite_nroom"),
    path('<int:id>n/invite/<str:username>/y', invite_nroom_y,name="invite_nroom_y"),
    path('<int:id>n/invite/<str:username>/n', invite_nroom_n,name="invite_nroom_n"),

    path('<int:id>p/invite/<str:username>', invite_proom,name="invite_proom"),
    path('<int:id>p/invite/<str:username>/y', invite_proom_y,name="invite_nroom_y"),
    path('<int:id>p/invite/<str:username>/n', invite_proom_n,name="invite_proom_n"), 



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
