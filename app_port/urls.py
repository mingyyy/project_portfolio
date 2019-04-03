from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = "app_port"
urlpatterns = [
    path('', views.main, name='main'),
    path('edit/<int:user.id>', views.edit, name='edit'),
    path('profile/<int:user.id>', views.profile, name='profile'),
]