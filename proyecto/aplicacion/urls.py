from django.urls import path
from aplicacion.views import *
from django.shortcuts import render
from aplicacion.modelos.views_usuario import UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView

app_name = "apl"

urlpatterns = [
    path("index/", vista1, name="index"),
    path("p/", vista2,name="p"),
    path("prueba/", vista3, name="prueba"),
    path("usuario/", UsuarioListView.as_view(), name="usuario_list"),
    path("usuario/crear/", UsuarioCreateView.as_view(), name="usuario_create"),
    path("usuario/actualizar/<int:pk>/", UsuarioUpdateView.as_view(), name="usuario_update"),
    path("usuario/eliminar/<int:pk>/", UsuarioDeleteView.as_view(), name="usuario_delete"),
]