from django.contrib import admin
from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', allwalls, name='allwalls'),
    path('<int:area_id>/', allposts, name='allposts'),
    path('<int:area_id>/load-more-posts/', load_more_posts, name='load_more_posts'),

    path('<int:id>/',allposts,name="allposts"),
    path('delete/<int:id>/',deletepost,name="deletepost"),
    path('like/<int:id>/',likepost,name="likepost"),
    path('unlike/<int:id>/',unlikepost,name="unlikepost"),
    path('my/',myposts,name="myposts"),
    path('add/',addpost,name="addpost"),
    path('toggle-like/<int:post_id>/', toggle_like, name='toggle_like'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
