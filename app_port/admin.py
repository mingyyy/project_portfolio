from django.contrib import admin
from .models import Profile, Project, Tag, Channel

# Register your models here.
admin.site.register(Project)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Channel)