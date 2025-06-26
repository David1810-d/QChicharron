"""
URL configuration for apps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from aplicacion.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Adminis/',Adminis),
    path('Compra/',Compra),
    path('Informe/',Informe),
    path('Venta/',Venta),
    path('proveedor/',proveedor),
    path('insumos/',insumos),
    path('productos_venta/',productosventa),
    path('nomina/',nomina),
    path("plato/", plato),
    path("pedido/", pedido),
    path("detalle_pedido/", detalle_pedido),
    path("empleado/", empleado),
    path("usuario/", ususario),
    path("marca/", marca),
    path("categoria/", categpria),
    path("menu/", menu),
]
