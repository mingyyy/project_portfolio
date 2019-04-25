from .models import Tag, User
from django import forms


class TagForm(forms.Form):
    CHOICES = (
        ('Java', 'Java'),
        ('Javascript', 'Javascript'),
        ('Python', 'Python'),
        ('PHP', 'PHP'),
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('Cyptocurrency', 'Cyptocurrency'),
    )
    picked = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple(), label="Select tags:")
    # class Meta:
    #     model = Tag
    #     exclude = ["users"]

