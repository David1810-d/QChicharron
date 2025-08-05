from django.urls import path,include
from aplicacion.views import *
from django.shortcuts import render
from aplicacion.modulos.views_usuario import *
from aplicacion.modulos.views_marca import *
from aplicacion.modulos.views_menu import *
from aplicacion.modulos.views_categoria import *

app_name = "apl"

urlpatterns = [

    path("index/", vista1, name="index"),
    #_________________________ Modulos de Usuario __________________________
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='eliminar_usuario'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='crear_usuario'),
    #_________________________ Modulos de Categoria __________________________
    path('categorias/listar/', CategoriaListView.as_view(), name='listar_categoria'),
    path('categorias/crear/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('categorias/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
    #
        # URLs para Marca
    path('marcas/listar/', MarcaListView.as_view(), name='marca_list'),
    path('marcas/crear/', MarcaCreateView.as_view(), name='marca_create'),
    path('marcas/actualizar/<int:pk>/', MarcaUpdateView.as_view(), name='marca_update'),
    path('marcas/eliminar/<int:pk>/', MarcaDeleteView.as_view(), name='marca_delete'),
    
    # También puedes usar la función si prefieres
    # path('marcas/listar/', listar_marca, name='marca_list'),
    
    # URLs para Menu
    path('menus/listar/', MenuListView.as_view(), name='menu_list'),
    path('menus/crear/', MenuCreateView.as_view(), name='menu_create'),
    path('menus/actualizar/<int:pk>/', MenuUpdateView.as_view(), name='menu_update'),
    path('menus/eliminar/<int:pk>/', MenuDeleteView.as_view(), name='menu_delete'),
]
