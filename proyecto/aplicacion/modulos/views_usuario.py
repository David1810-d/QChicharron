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

class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'modulos/editar_usuario.html'
    fields = ['nombre', 'cedula', 'correo_electronico', 'numero_celular', 'estado', 'contraseña']
    
    def get_success_url(self):
        return '/usuarios/'
    
class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'modulos/eliminar_usuario.html'
    
    def get_success_url(self):
        return '/usuarios/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar usuario'
        return context
