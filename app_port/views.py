from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, Channel, Tag

# Create your views here.

def main(request):
    return render(request, "main.html")

@login_required
def edit(request):
    context = {}
    user = request.user

    if request.method == 'POST':
        if "bio_saved" in request.POST:
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.profile.bio = request.POST["bio"]
            user.save()

        if "projects_saved" in request.POST:
            print(request.POST)
            projectID = request.POST["projectID"]
            project = Project.objects.get(id=projectID)
            project.name = request.POST["project_name"]
            project.description = request.POST["project_description"]
            project.url = request.POST["project_url"]
            project.save()

        if "project_new" in request.POST:
            Project.objects.create(name="New Project Title", description="Type your description here.", userID=user,
                                   url = "www.your-url-goes-here.com")

        if "project_delete" in request.POST:
            projectID = request.POST["projectID"]
            Project.objects.filter(id=projectID).delete()

        if "channels_saved" in request.POST:
            channelID = request.POST["channelID"]
            channel = Channel.objects.get(id=channelID)
            channel.name = request.POST["channel_name"]
            channel.url = request.POST["channel_url"]
            channel.save()

        if "channel_new" in request.POST:
            Channel.objects.create(name="Channel name", url="www.your-url-goes-here.com", userID=user)

        if "channel_delete" in request.POST:
            channelID = request.POST["channelID"]
            Channel.objects.filter(id=channelID).delete()




    channels = Channel.objects.filter(userID=user.id)
    projects = Project.objects.filter(userID=user.id)
    tags = user.tag_set.all()

    context["channels"]=channels
    context["projects"]=projects
    context["user"]=user
    context["tags"]=tags

    return render(request, "edit.html", context)

