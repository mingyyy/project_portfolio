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
    prof=Profile.objects.all()
    pj=Project.objects.all()
    tag=Tag.objects.all()
    choices={}
    if request.method == 'POST':
        if "tag" in request.POST:
            v = request.POST["tag"]
            print(v)
            if not 'tag' in request.session:# or not request.session['tag']:
                request.session['tag'] = v
            else:
                if not v in request.session['tag']:
                    saved_list = request.session['tag']
                    saved_list.append(v)
                    request.session['tag'] = saved_list
                else:
                    saved_list= request.session['tag']
                    saved_list.remove(v)
                    request.session['tag'] = saved_list

        selected=request.session['tag']
        choices={"choices":selected}
    context={"profile":prof, "project":pj, "tags":tag, "choices":choices}
    return render(request, 'main.html', context)


def profile(request, usernum):
    prof=Profile.objects.get(id=usernum)
    pj=Project.objects.get(id=usernum)
    tag=Tag.objects.get(id=usernum)
    channel=Channel.objects.get(id=usernum)
    context={"profile":prof, "project":pj, "tag":tag, "channel":channel}
    return render(request, "profile.html")


@login_required
def edit(request):
    context = {}
    user = request.user
    if request.method == 'POST':
        print(request.FILES)
        if "save_profile" in request.POST:
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.profile.bio = request.POST["bio"]
            user.save()

            for key in request.POST.keys():
                if key[0:4] == "chan":
                    channelID = int(key[4:])
                    channel = Channel.objects.get(id=channelID)
                    channel.name = request.POST.getlist(key)[0]
                    channel.url = request.POST.getlist(key)[1]
                    channel.save()
                elif key[0:4] == "proj":
                    projectID = int(key[4:])
                    project = Project.objects.get(id=projectID)
                    project.name = request.POST.getlist(key)[0]
                    project.url = request.POST.getlist(key)[1]
                    project.description = request.POST.getlist(key)[2]
                    project.save()
                elif request.POST[key] != "":
                    user.profile.picture = request.FILES
                    user.save()

        elif "delete_items" in request.POST:
            delete_list= request.POST.getlist("delete")
            for item in delete_list:
                if item[0:4] == "proj":
                    projectID = int(item[4:])
                    Project.objects.filter(id=projectID).delete()
                elif item[0:4] == "chan":
                    channelID = int(item[4:])
                    Channel.objects.filter(id=channelID).delete()

        elif "channel_new" in request.POST:
            Channel.objects.create(name="Channel name", url="www.your-url-goes-here.com", userID=user)

        elif "project_new" in request.POST:
            Project.objects.create(name="New Project Title", description="Type your description here.", userID=user,
                                   url = "www.your-url-goes-here.com")
        elif request.FILES['picture']:
            fin = Image.open(request.FILES['picture'])
            width, height = fin.size
            img_io = BytesIO()

            if width > height:
                dif = width - height
                cut = dif/2
                left = cut
                top = 0
                right = width - cut
                bottom = height
                fin2 =fin.crop((left, top, right, bottom))

            elif width < height:
                dif = height - width
                cut = dif/2
                left = 0
                top = cut
                right = width
                bottom = height-cut
                fin2 =fin.crop((left, top, right, bottom))

            fin2.save(fp=img_io, format="JPEG")
            image = ContentFile(img_io.getvalue())
            user.profile.picture.save("image name1", InMemoryUploadedFile(image, None,"image name2",'image/jpeg',image.tell,None))
            user.profile.save()

            # thumb = InMemoryUploadedFile(fin, None, 'foo2.jpeg', 'image/jpeg', thumb_io.seek(0, os.SEEK_END), None)

    channels = Channel.objects.filter(userID=user.id)
    projects = Project.objects.filter(userID=user.id)
    tags = user.tag_set.all()

    context["channels"]=channels
    context["projects"]=projects
    context["user"]=user
    context["tags"]=tags

    return render(request, "edit.html", context)


