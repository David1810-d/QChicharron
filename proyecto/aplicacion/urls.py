from django.urls import path
from aplicacion.views import *
from django.shortcuts import render

app_name = "apl"

urlpatterns = [
    path("index/", vista1, name="index"),
]