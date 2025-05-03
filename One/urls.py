from django.urls import path
from . import views
from One import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('menu/', views.get_menu, name='get_menu'),
]