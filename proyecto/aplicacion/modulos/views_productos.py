from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from aplicacion.models import Producto

class ProductoListView(ListView):
    model = Producto
    template_name = 'modulos/producto.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de productos'
        context['modelo'] = 'producto'
        return context
  

class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'forms/formulario_crear.html'
    fields = ['nombre', 'marca', 'categoria', 'proveedor', 'tipo_uso', 'tipo_medida', 'stock_unidades', 'stock_kg']

    def get_success_url(self):
        return reverse_lazy('apl:producto_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear producto'
        return context


class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['nombre', 'marca', 'categoria', 'proveedor', 'tipo_uso', 'tipo_medida', 'stock_unidades', 'stock_kg']

    def get_success_url(self):
        return reverse_lazy('apl:producto_list')


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'forms/confirmar_eliminacion.html'

    def get_success_url(self):
        return reverse_lazy('apl:producto_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar producto'
        return context
