from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from aplicacion.models import Mesa

class MesaListView(ListView):
    model = Mesa
    template_name = 'modulos/mesa.html'
    context_object_name = 'mesa'  # <-- CAMBIO: coincide con el template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Mesas'
        return context

class MesaCreateView(CreateView):
    model = Mesa
    template_name = 'forms/formulario_crear.html'
    fields = ['numero', 'capacidad', 'ubicacion']
    success_url = reverse_lazy('apl:mesa_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Mesa'
        context['modulo'] = 'mesa'
        return context

class MesaUpdateView(UpdateView):
    model = Mesa
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['numero', 'capacidad', 'ubicacion']
    success_url = reverse_lazy('apl:mesa_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Mesa'
        context['modulo'] = 'mesa'
        return context

class MesaDeleteView(DeleteView):
    model = Mesa
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = reverse_lazy('apl:mesa_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Mesa'
        return context