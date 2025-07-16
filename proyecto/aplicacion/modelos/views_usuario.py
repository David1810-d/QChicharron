from django.shortcuts import render
from aplicacion.models import *
from aplicacion.modelos import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

def prueba(request):
    data={
        'usuario': 'usuario',
        'Titulo': 'Lista de Usuarios',
        'usuarios': Usuario.objects.all()
    }
    return render(request, 'prueba.html', data)

class UsuarioListView(ListView):
    model = Usuario
    template_name = 'modulos/prueba.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Titulo'] = 'Lista de Usuarios'
        context['usuario'] = 'usuario'
        return context
    
class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'usuario_form.html'
    fields = ['nombre', 'cedula', 'correo_electronico', 'numero_celular', 'estado', 'contraseña']
    success_url = '/usuarios/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Titulo'] = 'Crear Usuario'
        context['usuario'] = 'usuario'
        return context

class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'usuario_form.html'
    fields = ['nombre', 'cedula', 'correo_electronico', 'numero_celular', 'estado', 'contraseña']
    success_url = '/usuarios/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Titulo'] = 'Actualizar Usuario'
        context['usuario'] = 'usuario'
        return context
    
class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuario_confirm_delete.html'
    success_url = '/usuarios/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Titulo'] = 'Eliminar Usuario'
        context['usuario'] = 'usuario'
        return context