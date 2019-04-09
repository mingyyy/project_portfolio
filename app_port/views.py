from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib import messages
from .models import Profile, Project, Tag, Channel
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Project, Channel, Tag
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Logged out.')


def main(request):
    prof=Profile.objects.filter(ready=True) # Query_set
    tag = Tag.objects.all()
    choices = {}
    profile_set, project_set, userids, readylist = [],[],[],[]
    # collect id for ready is True
    for x in prof:
        readylist.append(x.user.id)

    if request.method == 'POST':
        if "tag" in request.POST:
            v = request.POST["tag"]
            if not 'tag' in request.session or not request.session['tag']:
                request.session['tag'] = [v]
            else:
                saved_list = request.session['tag']
                if not v in request.session['tag']:
                    saved_list.append(v)
                    request.session['tag'] = saved_list
                else:
                    saved_list.remove(v)
                    request.session['tag'] = saved_list
            selected = request.session['tag']
        choices = {"choices":selected}

        for s in selected:
            selected_tags = Tag.objects.filter(name=s)
            for t in selected_tags:
                for v in t.users.all().values():
                    if v["id"] in readylist:
                        if len(profile_set) == 0:
                            userids.append(v["id"])

    userids=set(userids)
    for i in userids:
        prof = Profile.objects.filter(id=int(i))
        profile_set.append(prof)

    # project is a dict of key=id, value=queryset of project objects
    # profile_set is a list of queryset
    profile_chosen = {"profile_chosen": profile_set}

    context = {"profile": prof, "tags": tag, "choices": choices, "profile_chosen": profile_chosen}
    return render(request, 'main.html', context)


def profile(request, profile_userid):
    # usernum is the chosen user's id
    prof=Profile.objects.get(id=profile_userid)
    pj=Project.objects.get(id=profile_userid)
    tag=Tag.objects.get(id=profile_userid)
    channel=Channel.objects.get(id=profile_userid)
    context={"profile":prof, "project":pj, "tag":tag, "channel":channel}
    return render(request, "profile.html")


@login_required
def edit(request):
    context = {}
    user = request.user

    def save_profile(request, user):
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.profile.bio = request.POST["bio"]
        user.save()

        for key in request.POST.keys():
            if key[0:4] == "chan" and key != "channel_delete":
                channelID = int(key[4:])
                channel = Channel.objects.get(id=channelID)
                channel.name = request.POST.getlist(key)[0]
                channel.url = request.POST.getlist(key)[1]
                channel.save()
            elif key[0:4] == "proj" and key != "project_delete":
                projectID = int(key[4:])
                project = Project.objects.get(id=projectID)
                project.name = request.POST.getlist(key)[0]
                project.url = request.POST.getlist(key)[1]
                project.description = request.POST.getlist(key)[2]
                project.save()


    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)

        if "delete_channel" in request.POST:
            save_profile(request, user)

            delete_list= request.POST.getlist("delete")
            for item in delete_list:
                if item[0:4] == "chan":
                    channelID = int(item[4:])
                    Channel.objects.filter(id=channelID).delete()

        elif "delete_project" in request.POST:
            save_profile(request, user)

            delete_list= request.POST.getlist("delete")
            for item in delete_list:
                if item[0:4] == "proj":
                    projectID = int(item[4:])
                    Project.objects.filter(id=projectID).delete()


        elif "new_channel" in request.POST:
            save_profile(request, user)

            Channel.objects.create(name="Channel name", url="www.your-url-goes-here.com", userID=user)

        elif "new_project" in request.POST:
            save_profile(request, user)

            Project.objects.create(name="New Project Title", description="Type your description here.", userID=user,
                                   url = "www.your-url-goes-here.com")

        elif "picture" in request.FILES:
            fin1 = Image.open(request.FILES['picture'])
            width, height = fin1.size
            img_io = BytesIO()

            if width >= height:
                dif = width - height
                cut = dif/2
                left = cut
                top = 0
                right = width - cut
                bottom = height

            elif width < height:
                dif = height - width
                cut = dif/2
                left = 0
                top = cut
                right = width
                bottom = height-cut

            fin2 = fin1.crop((left, top, right, bottom)).resize((400,400), Image.LANCZOS)
            fin2.save(fp=img_io, format="JPEG")
            image = ContentFile(img_io.getvalue())
            user.profile.picture.save("image name1", InMemoryUploadedFile(image, None,"image name2",'image/jpeg',image.tell,None))
            user.profile.save()

            # thumb = InMemoryUploadedFile(fin1, None, 'foo2.jpeg', 'image/jpeg', thumb_io.seek(0, os.SEEK_END), None)

    channels = Channel.objects.filter(userID=user.id)
    projects = Project.objects.filter(userID=user.id)
    tags = user.tag_set.all()

    context["channels"]=channels
    context["projects"]=projects
    context["user"]=user
    context["tags"]=tags

    return render(request, "edit.html", context)


