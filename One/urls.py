from django.urls import path
from . import views
from One import views
urlpatterns = [
    path('register/', views.index, name='index'),
]