from django.shortcuts import render, HttpResponse
from account.models import placer,community
from activities.models import classic_activities

def index(request):

    allplacers = placer.objects.all()
    allcommunities = community.objects.all()
    allactivities = classic_activities.objects.all()
    values= {
        "placer":allplacers,
        "community":allcommunities,
        "activities":allactivities,
    }

    return render(request,"index.html",values)

def about(request):
    return render(request,"about.html")