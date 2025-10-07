from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from aplicacion.models import Plato, Producto, PlatoProducto
from aplicacion.forms import PlatoForm, PlatoProductoForm, PlatoProductoFormSet, PlatoProductoUpdateFormSet


class SuccessMessageMixinCustom:
    success_message = None

    def form_valid(self, form, formset=None):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


# ===============================
# LISTAR PLATOS
# ===============================
class PlatoListView(ListView):
    model = Plato
    template_name = 'modulos/plato.html'
    context_object_name = 'platos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Platos'
        return context


# ===============================
# CREAR PLATO
# ===============================
class PlatoCreateView(SuccessMessageMixinCustom, CreateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'forms/formulario_crear_plato.html'
    success_url = reverse_lazy('apl:listar_plato')
    success_message = "✅ El plato se ha creado correctamente"

    def get_context_data(self, **kwargs):
        if not hasattr(self, 'object'):
            self.object = None
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Plato'
        context['entidad'] = 'Plato'
        if self.request.POST:
            context['formset'] = PlatoProductoFormSet(self.request.POST)
        else:
            context['formset'] = PlatoProductoFormSet()
        context['productos'] = Producto.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        if 'agregar_producto' in request.POST:
            return self.agregar_producto_temporal(request)
        return self.procesar_formulario(request)

    def agregar_producto_temporal(self, request):
        """Agregar producto desde modal en creación."""
        producto_id = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        unidad = request.POST.get('unidad')

        if not all([producto_id, cantidad, unidad]):
            messages.error(request, 'Todos los campos son requeridos')
            return redirect(request.path)

        try:
            producto = Producto.objects.get(id=producto_id)
            if 'productos_temporal' not in request.session:
                request.session['productos_temporal'] = []

            request.session['productos_temporal'].append({
                'producto_id': int(producto_id),
                'producto_nombre': str(producto),
                'cantidad': float(cantidad),
                'unidad': unidad
            })
            request.session.modified = True
            messages.success(request, f'Producto "{producto}" agregado temporalmente')

        except Producto.DoesNotExist:
            messages.error(request, 'Producto no encontrado')
        except (ValueError, TypeError):
            messages.error(request, 'Datos inválidos')

        return redirect(request.path)

    def procesar_formulario(self, request):
        """Procesar el formulario principal de creación."""
        form = self.get_form()
        formset = PlatoProductoFormSet(request.POST)
        productos_temp = request.session.get('productos_temporal', [])

        if form.is_valid():
            plato = form.save()
            # Guardar productos temporales
            for prod_data in productos_temp:
                PlatoProducto.objects.create(
                    plato=plato,
                    producto_id=prod_data['producto_id'],
                    cantidad=prod_data['cantidad'],
                    unidad=prod_data['unidad']
                )

            formset.instance = plato
            if formset.is_valid():
                formset.save()

            if 'productos_temporal' in request.session:
                del request.session['productos_temporal']

            messages.success(request, self.success_message)
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'titulo': 'Crear Plato',
            'entidad': 'Plato',
            'productos': Producto.objects.all()
        })


# ===============================
# ACTUALIZAR PLATO
# ===============================
class PlatoUpdateView(SuccessMessageMixinCustom, UpdateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'forms/formulario_actualizar_plato.html'
    success_url = reverse_lazy('apl:listar_plato')
    success_message = "El plato se ha actualizado correctamente ✅"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Plato'
        context['entidad'] = 'Plato'

        if self.request.POST:
            context['formset'] = PlatoProductoUpdateFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = PlatoProductoUpdateFormSet(instance=self.object)

        context['productos'] = Producto.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'agregar_producto' in request.POST:
            return self.agregar_producto_inmediato(request)
        return self.procesar_formulario(request)

    def agregar_producto_inmediato(self, request):
        """Agregar producto directamente a un plato existente."""
        producto_id = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        unidad = request.POST.get('unidad')

        if not all([producto_id, cantidad, unidad]):
            messages.error(request, 'Todos los campos son requeridos')
            return redirect(request.path)

        try:
            producto = Producto.objects.get(id=producto_id)
            PlatoProducto.objects.create(
                plato=self.object,
                producto=producto,
                cantidad=float(cantidad),
                unidad=unidad
            )
            messages.success(request, f'Producto "{producto}" agregado al plato')
        except Producto.DoesNotExist:
            messages.error(request, 'Producto no encontrado')
        except (ValueError, TypeError):
            messages.error(request, 'Datos inválidos')

        return redirect(request.path)

    def procesar_formulario(self, request):
        """Procesar el formulario principal de actualización."""
        form = self.get_form()
        formset = PlatoProductoUpdateFormSet(request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            plato = form.save()
            formset.instance = plato
            formset.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'titulo': 'Editar Plato',
            'entidad': 'Plato',
            'productos': Producto.objects.all()
        })


# ===============================
# ELIMINAR PLATO (con SweetAlert)
# ===============================
@method_decorator(csrf_exempt, name="dispatch")
class PlatoDeleteView(DeleteView):
    model = Plato
    success_url = reverse_lazy('apl:listar_plato')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"})
