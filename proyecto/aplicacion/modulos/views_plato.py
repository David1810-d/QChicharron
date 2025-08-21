from django.shortcuts import render
from aplicacion.models import *
from django.views.generic import *


def listar_plato(request):
    data = {
        "platos": "platos",
        "titulo": "Listado de Platos",
        "plato": Plato.objects.all()
    }
    return render(request, 'modulos/plato.html', data)

class PlatoListView(ListView):
    model = Plato
    template_name = 'modulos/plato.html'
    context_object_name = 'platos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Platos'
        return context
    
class PlatoCreateView(CreateView):
    model = Plato
    template_name = 'forms/formulario_crear.html'
    fields = ['nombre', 'descripcion', 'precio']
    success_url = '/apps/platos/listar/'
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear     Plato'   
        context['modulo'] = "plato"
        return context

class PlatoUpdateView(UpdateView):
    model = Plato
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['nombre', 'descripcion', 'precio']
    success_url = '/apps/platos/listar/'
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class PlatoDeleteView(DeleteView):
    model = Plato
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = '/apps/platos/listar/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Plato'
        return context
