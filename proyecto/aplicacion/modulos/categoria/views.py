from django.shortcuts import render
from aplicacion.models import *
from aplicacion.modulos.categoria.views import *
from  django.views.generic import *

def listar_categoria(request): 
    data= {
        "categorias":"categorias",
        "titulo":"Listado de Categorías",
        "categoria": Categoria.objects.all()  
          }
    return render(request, 'categoria/listar_categoria.html', data)

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria/listar_categoria.html'
    context_object_name = 'categorias'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado_de_Categorías'
        return super().get_context_data(**kwargs)
    
class CategoriaCreateView(CreateView):
    model = Categoria
    template_name = 'categoria/crear_categoria.html'
    fields = ['nombre', 'descripcion']
    success_url = '/apps/categorias/listar/'

    def form_valid(self, form):
        return super().form_valid(form)

class CategoriaUpdateView(UpdateView):
    model = Categoria
    template_name = 'categoria/editar_categoria.html'
    fields = ['nombre', 'descripcion']
    success_url = '/apps/categorias/listar/'

    def form_valid(self, form):
        return super().form_valid(form)

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'categoria/eliminar_categoria.html'
    success_url = '/apps/categorias/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Categoría'
        return context
    

