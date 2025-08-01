from django.urls import path,include
from aplicacion.views import *
from django.shortcuts import render
from aplicacion.modulos.views_usuario import *
from aplicacion.modulos.categoria.views import *
from aplicacion.modulos.views_plato import *
from aplicacion.modulos.views_pedido import *
from aplicacion.modulos.views_empleado import *


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
    path('categorias/eliminar/<int:id>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
    #_________________________ Modulos de Plato __________________________
    path('platos/listar/', PlatoListView.as_view(), name='listar_plato'),
    path('platos/crear/', PlatoCreateView.as_view(), name='crear_plato'),
    path('platos/editar/<int:pk>/', PlatoUpdateView.as_view(), name='editar_plato'),
    path('platos/eliminar/<int:pk>/', PlatoDeleteView.as_view(), name='eliminar_plato'),
    #_________________________ Modulos de Pedido __________________________
    path('pedidos/listar/', PedidoListView.as_view(), name='listar_pedido'),
    path('pedidos/crear/', PedidoCreateView.as_view(), name='crear_pedido'),
    path('pedidos/editar/<int:pk>/', PedidoUpdateView.as_view(), name='editar_pedido'),
    path('pedidos/eliminar/<int:pk>/', PedidoDeleteView.as_view(), name='eliminar_pedido'),
    #_________________________ Modulos de Empleado __________________________
    path('empleados/listar/', EmpleadoListView.as_view(), name='listar_empleado'),
    path('empleados/crear/', EmpleadoCreateView.as_view(), name='crear_empleado'),
    path('empleados/editar/<int:pk>/', EmpleadoUpdateView.as_view(), name='editar_empleado'),
    path('empleados/eliminar/<int:pk>/', EmpleadoDeleteView.as_view(), name='eliminar_empleado'),
]
