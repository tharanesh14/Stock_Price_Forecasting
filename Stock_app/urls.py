from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('abc',views.abc, name="abc"),
    path('register', views.registerapi.as_view(), name='register'),
    path('login', views.loginapi.as_view(), name='login'),
    path('logout', views.LogoutAPIView.as_view(), name='logout'),
]