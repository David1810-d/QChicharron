from django.shortcuts import render
from django.urls import reverse_lazy
from aplicacion.models import *
from aplicacion.modulos.views_menu import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView   

def listar_menu(request):
    data = {
        "menus": "menus",
        "titulo": "Listado de Menús",
        "menu": Menu.objects.all()
    }
    return render(request, 'modulos/menu.html', data)

class MenuListView(ListView):
    model = Menu
    template_name = 'modulos/menu.html'
    context_object_name = 'menus'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Menús'
        context['menu'] = 'menu'
        return context

class MenuCreateView(CreateView):
    model = Menu
    template_name = 'forms/formulario_crear.html'
    fields = ['nombre', 'descripcion', 'precio']
    
    def get_success_url(self):
        return reverse_lazy('apl:menu_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nuevo Menú'
        return context

class MenuUpdateView(UpdateView):
    model = Menu
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['nombre', 'descripcion', 'precio']
    
    def get_success_url(self):
        return reverse_lazy('apl:menu_list')

class MenuDeleteView(DeleteView):
    model = Menu
    template_name = 'forms/confirmar_eliminacion.html'
    
    def get_success_url(self):
        return reverse_lazy('apl:menu_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Menú'
        return context
    
    def get(self, request, *args, **kwargs):
        # Renderiza solo el contenido para el modal
        self.object = self.get_object()
        return render(request, self.template_name, {'object': self.object})
