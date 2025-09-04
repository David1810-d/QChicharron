from django.shortcuts import render
from django.http import HttpResponse
from aplicacion.templates import *
from aplicacion.models import *

# Create your views here.

def vista1(request):
    return render(request, 'index.html')

def vista2(request):
    return render(request, 'aside/body.html') 

def vista3(request):
    return render(request, 'modulos/prueba.html')