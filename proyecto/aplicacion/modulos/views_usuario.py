from django.shortcuts import render
from aplicacion.models import *
from aplicacion.modulos.views_usuario import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.shortcuts import render


def prueba(request):
     data={
         'usuario':'usuario',
         'titulo':'lista de Usuarios',
         'usuarios': Usuario.objects.all()
     }
     return render(request, 'modulos/prueba.html',data) 
 
class UsuarioListView(ListView):
    model= Usuario 
    template_name = 'modulos/prueba.html'
    context_object_name = 'usuarios'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de usuarios'
        context['usuario'] = 'usuario'
        return context