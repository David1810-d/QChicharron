from django.shortcuts import render, redirect
from aplicacion.models import *
from django.views.generic import *
from aplicacion.forms import PlatoForm, PlatoProductoFormSet
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
    form_class = PlatoForm
    template_name = 'forms/formulario_crear_plato.html'
    success_url = reverse_lazy('apl:listar_plato')

def get(self, request, *args, **kwargs):
    self.object = None
    form = self.get_form()
    # Inicializar formset vacío
    formset = PlatoProductoFormSet(queryset=PlatoProducto.objects.none())
    return render(request, self.template_name, {
        'form': form,
        'formset': formset,
        'titulo': 'Crear Plato',
        'entidad': 'Plato'
    })

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = PlatoProductoFormSet(self.request.POST)

        if form.is_valid() and formset.is_valid():
            plato = form.save()
            formset.instance = plato
            formset.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'titulo': 'Crear Plato',
            'entidad': 'Plato'
        })

class PlatoUpdateView(UpdateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'forms/formulario_actualizar_plato.html'
    success_url = reverse_lazy('apl:listar_plato')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = PlatoProductoFormSet(instance=self.object)
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'titulo': 'Editar Plato',
            'entidad': 'Plato'
        })

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = PlatoProductoFormSet(self.request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            plato = form.save()
            formset.instance = plato
            formset.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'titulo': 'Editar Plato',
            'entidad': 'Plato'
        })
    

@method_decorator(csrf_exempt, name="dispatch")
class PlatoDeleteView(DeleteView):
    model = Plato
    success_url = reverse_lazy('apl:listar_plato')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"})
