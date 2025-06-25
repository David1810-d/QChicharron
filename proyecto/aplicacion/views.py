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


