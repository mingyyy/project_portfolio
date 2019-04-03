from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = "app_port"
urlpatterns = [

    path('', views.main, name='main'),
]