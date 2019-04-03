from django import forms
from .models import Project, Tag, Channel

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'url']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'url']