from django import forms
from aplicacion.models import *
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django_select2.forms import *

#class MensajeForm(forms.ModelForm):
#   class Meta:
#       model = Mensaje
#       fields = ['nombre', 'contenido']
#ewfergergf


class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio']


class PlatoProductoForm(forms.ModelForm):
    class Meta:
        model = PlatoProducto
        fields = ['producto', 'cantidad', 'unidad']
        widgets = {
            'producto': Select2Widget,
        }

PlatoProductoFormSet = inlineformset_factory(
    Plato,
    PlatoProducto,
    form=PlatoProductoForm,
    extra=1,
    can_delete=True
)
#sdfgdfhfg

# Formularios para crear nuevas foreign keys
class CrearMarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'descripcion', 'pais_origen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pais_origen': forms.TextInput(attrs={'class': 'form-control'})
        }

class CrearCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class CrearProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'nit']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'})
        }

class CrearUnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'})
        }

# Widget personalizado para Select2 con opción de crear nuevo
class Select2WithCreateWidget(ModelSelect2Widget):
    def __init__(self, *args, **kwargs):
        self.create_url = kwargs.pop('create_url', None)
        self.create_text = kwargs.pop('create_text', 'Crear nuevo')
        super().__init__(*args, **kwargs)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        if self.create_url:
            attrs['data-create-url'] = self.create_url
            attrs['data-create-text'] = self.create_text
        return attrs


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'categoria', 'proveedor', 'tipo_uso', 'unidad', 'stock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Asegurar que los selects traen datos de la base
        self.fields['marca'].queryset = Marca.objects.all()
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['proveedor'].queryset = Proveedor.objects.all()
        self.fields['unidad'].queryset = Unidad.objects.all()

        # Opcional: poner placeholders amigables
        self.fields['marca'].empty_label = "Seleccione una marca"
        self.fields['categoria'].empty_label = "Seleccione una categoría"
        self.fields['proveedor'].empty_label = "Seleccione un proveedor"
        self.fields['unidad'].empty_label = "Seleccione una unidad"



class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'forms/formulario_crear.html'
    success_url = reverse_lazy('apl:producto_list')
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'marca': Select2WithCreateWidget(
                model=Marca,
                search_fields=['nombre__icontains'],
                create_url='crear_marca_ajax',
                create_text='+ Crear nueva marca'
            ),
            'categoria': Select2WithCreateWidget(
                model=Categoria,
                search_fields=['nombre__icontains'],
                create_url='crear_categoria_ajax',
                create_text='+ Crear nueva categoría'
            ),
            'proveedor': Select2WithCreateWidget(
                model=Proveedor,
                search_fields=['nombre__icontains'],
                create_url='crear_proveedor_ajax',
                create_text='+ Crear nuevo proveedor'
            ),
            'unidad': Select2WithCreateWidget(
                model=Unidad,
                search_fields=['nombre__icontains'],
                create_url='crear_unidad_ajax',
                create_text='+ Crear nueva unidad'
            ),
        }
        


class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['usuario', 'nivel_prioridad']

    def clean_nivel_prioridad(self):
        nivel = self.cleaned_data.get('nivel_prioridad')
        if nivel is not None and nivel < 0:
            raise forms.ValidationError("El nivel de prioridad debe ser positivo.")
        return nivel


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        # no incluyo `fecha` porque es auto_now_add
        fields = ["pedido", "total", "metodo_pago", "estado", "admin"]

    def clean_total(self):
        total = self.cleaned_data.get("total")
        if total <= 0:
            raise forms.ValidationError("El total debe ser mayor que 0.")
        return total

    def clean(self):
        cleaned_data = super().clean()
        pedido = cleaned_data.get("pedido")

        if pedido is None:
            raise forms.ValidationError("Debes seleccionar un pedido.")

        # validación: un pedido no puede tener más de una venta pagada
        if Venta.objects.filter(pedido=pedido, estado="pagado").exists():
            raise forms.ValidationError(
                f"El pedido {pedido.id} ya tiene una venta registrada como pagada."
            )

        return cleaned_data


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'producto', 'cantidad', 'fecha']

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        precio = cleaned_data.get('precio_unitario')

        if cantidad and cantidad <= 0:
            self.add_error('cantidad', "La cantidad debe ser positiva.")

        if precio and precio <= 0:
            self.add_error('precio_unitario', "El precio debe ser positivo.")


class InformeForm(forms.Form):
    fecha_inicio = forms.DateField(required=True)
    fecha_fin = forms.DateField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de inicio no puede ser mayor que la fecha fin.")