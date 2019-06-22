from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('fetch/',views.fetch, name='fetch'),
    path('cgpa/',views.cgpa, name='cgpa'),
    path('attendance/',views.attendance, name='attendance'),
    path('logout/',views.logout, name='logout'),
    path('about/',views.personalData, name='personalData'),

]
