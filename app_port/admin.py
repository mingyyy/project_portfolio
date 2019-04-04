from django.contrib import admin

from .models import Channel, Project, Tag, Profile

# Register your models here.
admin.site.register([Channel, Project, Tag, Profile])

