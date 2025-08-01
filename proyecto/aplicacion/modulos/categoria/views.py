from django.shortcuts import render
from aplicacion.models import *
from aplicacion.templates.modulos import *
from  django.views.generic import *

def listar_categoria(request): 
    data= {
        "categorias":"categorias",
        "titulo":"Listado de Categorías",
        "categoria": Categoria.objects.all()  
          }
    return render(request, 'modulos/categoria.html', data)

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'modulos/categoria.html'
    context_object_name = 'categorias'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado_de_Categorías'
        return super().get_context_data(**kwargs)
    
class CategoriaCreateView(CreateView):
    model = Categoria
    template_name = 'forms/formulario_crear.html'
    fields = ['nombre', 'descripcion']
    success_url = '/apps/categorias/listar/'

    def form_valid(self, form):
        return super().form_valid(form)

class CategoriaUpdateView(UpdateView):
    model = Categoria
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['nombre', 'descripcion']
    success_url = '/apps/categorias/listar/'

    def form_valid(self, form):
        return super().form_valid(form)

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = '/apps/categorias/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Categoría'
        return context
    

