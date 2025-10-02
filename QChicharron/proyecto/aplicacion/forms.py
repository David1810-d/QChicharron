from django import forms
from aplicacion.models import *
from django.forms import ModelForm, inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django_select2.forms import *
from django.core.exceptions import ValidationError
#jijija
from aplicacion.models import (
    Plato,
    PlatoProducto,
    Menu,
    Pedido,
    PedidoDetalle,
    Producto,
    Marca,
    Categoria,
    Proveedor,
    Unidad,
)
#jijija
class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio']


class PlatoProductoForm(forms.ModelForm):
    class Meta:
        model = PlatoProducto
        fields = ['producto', 'cantidad', 'unidad']
        widgets = {
            'producto': Select2Widget(attrs={'class': 'select2'}),
        }
        
class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['mesa', 'estado']  # campos del pedido que quieres mostrar

# Formset para agregar menús y cantidades al pedido
PedidoDetalleFormSet = inlineformset_factory(
    Pedido,
    PedidoDetalle,
    fields=['menu', 'cantidad'],
    extra=1,       # cuántos campos extra mostrar al cargar
)        

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

#mis cambios de producto
    #xd
    #mis cambios de producto
    #xd
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'categoria', 'proveedor', 'tipo_uso', 'unidad', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'tipo_uso': forms.Select(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'required': True,
            }),
        }

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Asegurar que los selects traen datos de la base
        self.fields['marca'].queryset = Marca.objects.all()
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['proveedor'].queryset = Proveedor.objects.all()
        self.fields['unidad'].queryset = Unidad.objects.all()

        # Placeholders amigables
        self.fields['marca'].empty_label = "Seleccione una marca"
        self.fields['categoria'].empty_label = "Seleccione una categoría"
        self.fields['proveedor'].empty_label = "Seleccione un proveedor"
        self.fields['unidad'].empty_label = "Seleccione una unidad"


# Formularios para los modales
class MarcaModalForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'pais_origen', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class CategoriaModalForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class ProveedorModalForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'nit']


class UnidadModalForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ['nombre', 'descripcion']

# Administrador
class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['usuario', 'nivel_prioridad']
        widgets = {
            'nivel_prioridad': forms.NumberInput(attrs={
                'min': '0',
                'required': True,
            }),
        }

    # Validación a nivel de Django (backend)
    def clean_nivel_prioridad(self):
        nivel_prioridad = self.cleaned_data.get('nivel_prioridad')
        print(f"DEBUG: nivel_prioridad = {nivel_prioridad}, tipo: {type(nivel_prioridad)}")  # Para debug
        
        if nivel_prioridad is not None and nivel_prioridad < 0:
            raise forms.ValidationError("El nivel de prioridad no puede ser negativo.")
        return nivel_prioridad
    
    def clean(self):
        cleaned_data = super().clean()
        nivel_prioridad = cleaned_data.get('nivel_prioridad')
        
        # Validación adicional en clean general
        if nivel_prioridad is not None and nivel_prioridad < 0:
            raise forms.ValidationError("El nivel de prioridad no puede ser negativo.")
        
        return cleaned_data
#hasta aqui van mis cambios 

# Venta
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['pedido', 'total', 'metodo_pago', 'estado', 'admin']
        widgets = {
            'total': forms.NumberInput(attrs={
                'min': '0',
                'step': '0.01',  # para valores con decimales
                'required': True,
            }),
        }

    # Validación a nivel de Django (backend)
    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is not None and total < 0:
            raise forms.ValidationError("El total no puede ser negativo.")
        return total

    def clean(self):
        cleaned_data = super().clean()
        pedido = cleaned_data.get('pedido')

        if pedido is None:
            raise forms.ValidationError("Debes seleccionar un pedido.")

        # Validación: un pedido no puede tener más de una venta pagada
        if Venta.objects.filter(pedido=pedido, estado="pagado").exists():
            raise forms.ValidationError(
                f"El pedido {pedido.id} ya tiene una venta registrada como pagada."
            )

        return cleaned_data


# Compra
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'producto', 'cantidad', 'fecha', 'precio', 'unidad']  
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'min': '0',
                'required': True,
            }),
            'precio': forms.NumberInput(attrs={
                'min': '0',
                'step': '0.01',  # para valores con decimales
                'required': True,
            }),
        }

    # Validación a nivel de Django (backend)
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
        return cantidad

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio


class InformeForm(forms.Form):
    fecha_inicio = forms.DateField(required=True)
    fecha_fin = forms.DateField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de inicio no puede ser mayor que la fecha fin.")