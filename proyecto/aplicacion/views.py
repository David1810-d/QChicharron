from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def vista1(request):
    return render(request, 'Adminis.html')

def vista2(request):
    return render(request, 'Compra.html')

def vista3(request):
    return render(request, 'Informe.html')

def vista4(request):
    return render(request, 'Venta.html')
#------Vistas santiago------------------------
def insumos(request):
    return render(request, 'insumos.html')
def nomina(request):
    return render(request, 'nomina.html')
def productosventa(request):
    return render(request, 'productos_ventadirecta.html')
def proveedor(request):
    return render(request, 'proveedor.html')

#----Vistas Alejandro---------------------
def plato(request):
    return render(request, "plato.html")
def pedido(request):
    return render(request, "pedido.html")
def detalle_pedido(request):
    return render(request, "detalle_pedido.html")
def empleado(request):
    return render(request, "empleado.html")
def ususario(request):
    return render(request, "usuario.html")

#----Vistas de Angel---------------------

def categpria(request):
    return render(request, "Categoria.html")
def marca(request):
    return render(request, "marca.html")
def menu(request):
    return render(request, "Menu.html")

