from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from aplicacion.models import Producto, Marca, Categoria, Proveedor, Unidad
from aplicacion.forms import ProductoForm  # Importa tu formulario personalizado si quieres usarlo
import json

# TUS VISTAS ORIGINALES - NO CAMBIAR
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
    template_name = 'forms/formulario_crear_producto.html'  # Cambiar esta línea
    form_class = ProductoForm  # Y esta línea

    def get_success_url(self):
        return reverse_lazy('apl:producto_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear producto'
        context['modulo'] = "producto"
        return context


class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'forms/formulario_actualizacion.html'
    form_class = ProductoForm

    def get_success_url(self):
        return reverse_lazy('apl:producto_list')


class ProductoDeleteView(DeleteView):
    model = Producto
    success_url = reverse_lazy('apl:producto_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"})


# NUEVAS VISTAS AJAX PARA CREAR FOREIGN KEYS
@require_POST
def crear_marca_ajax(request):
    """Vista AJAX para crear nueva marca"""
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        descripcion = data.get('descripcion', '').strip()
        pais_origen = data.get('pais_origen', '').strip()
        
        if not nombre:
            return JsonResponse({
                'success': False,
                'error': 'El nombre de la marca es requerido'
            })
        
        if not pais_origen:
            return JsonResponse({
                'success': False,
                'error': 'El país de origen es requerido'
            })
        
        # Verificar si ya existe
        if Marca.objects.filter(nombre=nombre).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ya existe una marca con este nombre'
            })
        
        # Crear nueva marca
        marca = Marca.objects.create(
            nombre=nombre,
            descripcion=descripcion if descripcion else None,
            pais_origen=pais_origen
        )
        
        return JsonResponse({
            'success': True,
            'id': marca.id,
            'text': str(marca)  # Para Select2
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_POST
def crear_categoria_ajax(request):
    """Vista AJAX para crear nueva categoría"""
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        descripcion = data.get('descripcion', '').strip()
        
        if not nombre:
            return JsonResponse({
                'success': False,
                'error': 'El nombre de la categoría es requerido'
            })
        
        if Categoria.objects.filter(nombre=nombre).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ya existe una categoría con este nombre'
            })
        
        categoria = Categoria.objects.create(
            nombre=nombre,
            descripcion=descripcion if descripcion else None
        )
        
        return JsonResponse({
            'success': True,
            'id': categoria.id,
            'text': str(categoria)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_POST
def crear_proveedor_ajax(request):
    """Vista AJAX para crear nuevo proveedor"""
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        nit = data.get('nit', '').strip()
        
        if not nombre or not nit:
            return JsonResponse({
                'success': False,
                'error': 'El nombre y el NIT del proveedor son requeridos'
            })
        
        if Proveedor.objects.filter(nombre=nombre).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ya existe un proveedor con este nombre'
            })
        
        if Proveedor.objects.filter(nit=nit).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ya existe un proveedor con este NIT'
            })
        
        proveedor = Proveedor.objects.create(
            nombre=nombre,
            nit=nit
        )
        
        return JsonResponse({
            'success': True,
            'id': proveedor.id,
            'text': str(proveedor)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_POST
def crear_unidad_ajax(request):
    """Vista AJAX para crear nueva unidad"""
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        descripcion = data.get('descripcion', '').strip()
        
        if not nombre:
            return JsonResponse({
                'success': False,
                'error': 'El nombre de la unidad es requerido'
            })
        
        if Unidad.objects.filter(nombre=nombre).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ya existe una unidad con este nombre'
            })
        
        unidad = Unidad.objects.create(
            nombre=nombre,
            descripcion=descripcion if descripcion else None
        )
        
        return JsonResponse({
            'success': True,
            'id': unidad.id,
            'text': str(unidad)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })