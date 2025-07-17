from django.urls import path
from aplicacion.views import *
from django.shortcuts import render
from aplicacion.modulos.views_usuario import *

app_name = "apl"

urlpatterns = [
    path("index/", vista1, name="index"),
    path("p/", vista2,name="p"),
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='eliminar_usuario'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='crear_usuario'),
]
