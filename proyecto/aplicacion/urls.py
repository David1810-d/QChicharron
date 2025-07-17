from django.urls import path
from aplicacion.views import *
from django.shortcuts import render
from aplicacion.modulos.views_usuario import *

app_name = "apl"

urlpatterns = [
    path("index/", vista1, name="index"),
    path("p/", vista2,name="p"),
    path("prueba/", vista3, name="prueba"),
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
]
