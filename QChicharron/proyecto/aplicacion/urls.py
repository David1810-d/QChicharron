from django.urls import path,include
from aplicacion.views import *
from django.shortcuts import render
from aplicacion.modulos.views_usuario import *
from aplicacion.modulos.views_marca import *
from aplicacion.modulos.views_menu import *
from aplicacion.modulos.views_categoria import *
from aplicacion.modulos.views_categoria import *
from aplicacion.modulos.views_plato import *
from aplicacion.modulos.views_pedido import *
from aplicacion.modulos.views_empleado import *
from aplicacion.modulos.views_productos import *
from aplicacion.modulos.views_proveedor import *
from aplicacion.modulos.views_nomina import *
from aplicacion.modulos.views_mesa import *
from aplicacion.modulos.views_administrador import *
from aplicacion.modulos.views_compra import *
from aplicacion.modulos.views_venta import *
from aplicacion.modulos.views_informe import *
from aplicacion.modulos.views_unidad import *

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
    

    # URLs para Menu
    path('menus/listar/', MenuListView.as_view(), name='menu_list'),
    path('menus/crear/', MenuCreateView.as_view(), name='menu_create'),
    path('menus/actualizar/<int:pk>/', MenuUpdateView.as_view(), name='menu_update'),
    path('menus/eliminar/<int:pk>/', MenuDeleteView.as_view(), name='menu_delete'),

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
    #_________________________ Modulos de Producto __________________________
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('productos/editar/<str:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('productos/eliminar/<str:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),
    
        # NUEVAS URLs AJAX PARA CREAR FOREIGN KEYS

path('ajax/crear-marca/', crear_marca_ajax, name='crear_marca_ajax'),
path('ajax/crear-categoria/', crear_categoria_ajax, name='crear_categoria_ajax'),
path('ajax/crear-proveedor/', crear_proveedor_ajax, name='crear_proveedor_ajax'),
path('ajax/crear-unidad/', crear_unidad_ajax, name='crear_unidad_ajax'),
    #_________________________ Modulos de Proveedor __________________________
    path('proveedores/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/crear/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('proveedores/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='editar_proveedor'),
    path('proveedores/eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='eliminar_proveedor'),
    #_________________________ Modulos de Nomina __________________________
    path('nominas/', NominaListView.as_view(), name='nomina_list'),
    path('nominas/crear/', NominaCreateView.as_view(), name='crear_nomina'),
    path('nominas/editar/<int:pk>/', NominaUpdateView.as_view(), name='editar_nomina'),
    path('nominas/eliminar/<int:pk>/', NominaDeleteView.as_view(), name='eliminar_nomina'),
    #_________________________ Modulos de Mesa __________________________
        path('mesas/', MesaListView.as_view(), name='mesa_list'),
    path('mesas/crear/', MesaCreateView.as_view(), name='crear_mesa'),
    path('mesas/editar/<int:pk>/', MesaUpdateView.as_view(), name='editar_mesa'),
    path('mesas/eliminar/<int:pk>/', MesaDeleteView.as_view(), name='eliminar_mesa'),
    #_________________________ Modulos de Administrador __________________________
    path('administradores/listar/', AdministradorListView.as_view(), name='administrador_listar'),
    path('administradores/crear/', AdministradorCreateView.as_view(), name='administrador_crear'),
    path('administradores/editar/<int:pk>/', AdministradorUpdateView.as_view(), name='administrador_editar'),
    path('administradores/eliminar/<int:pk>/', AdministradorDeleteView.as_view(), name='administrador_eliminar'),
    #_________________________ Modulos de Compra __________________________
    path('compras/listar/', CompraListView.as_view(), name='compra_listar'),
    path('compras/crear/', CompraCreateView.as_view(), name='compra_crear'),
    path('compras/editar/<str:pk>/', CompraUpdateView.as_view(), name='compra_editar'),
    path('compras/eliminar/<str:pk>/', CompraDeleteView.as_view(), name='compra_eliminar'),
    #_________________________ Modulos de Venta __________________________
    path('ventas/listar/', VentaListView.as_view(), name='venta_listar'),
    path('ventas/crear/', VentaCreateView.as_view(), name='venta_crear'),
    path('ventas/editar/<int:pk>/', VentaUpdateView.as_view(), name='venta_editar'),
    path('ventas/eliminar/<int:pk>/', VentaDeleteView.as_view(), name='venta_eliminar'),
    #_________________________ Modulos de Informe  __________________________
    path('informes/listar/', InformeListView.as_view(), name='informe_listar'),
    path('informes/crear/', InformeCreateView.as_view(), name='informe_crear'),
    path('informes/editar/<int:pk>/', InformeUpdateView.as_view(), name='informe_editar'),
    path('informes/eliminar/<int:pk>/', InformeDeleteView.as_view(), name='informe_eliminar'),
    #_________________________ Modulos de Unidad  __________________________
        # Unidades
    path('unidades/', UnidadListView.as_view(), name='unidad_list'),
    path('unidades/crear/', UnidadCreateView.as_view(), name='crear_unidad'),
    path('unidades/editar/<int:pk>/', UnidadUpdateView.as_view(), name='editar_unidad'),
    path('unidades/eliminar/<int:pk>/', UnidadDeleteView.as_view(), name='eliminar_unidad'),
]


