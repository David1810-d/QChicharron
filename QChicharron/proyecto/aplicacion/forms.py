from django import forms
from aplicacion.models import *
from django.forms import ModelForm, inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django_select2.forms import *
from django.core.exceptions import ValidationError


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            'nivel_prioridad': forms.NumberInput(attrs={'min': '0', 'required': True}),
        }

    def clean_nivel_prioridad(self):
        nivel_prioridad = self.cleaned_data.get('nivel_prioridad')
        if nivel_prioridad is not None and nivel_prioridad < 0:
            raise forms.ValidationError("El nivel de prioridad no puede ser negativo.")
        return nivel_prioridad

# ==================== VENTA ====================
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['pedido', 'total', 'metodo_pago', 'estado', 'admin']
        widgets = {
            'total': forms.NumberInput(attrs={'min': '0', 'step': '0.01', 'required': True}),
        }

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
        if Venta.objects.filter(pedido=pedido, estado="pagado").exists():
            raise forms.ValidationError(f"El pedido {pedido.id} ya tiene una venta registrada.")
        return cleaned_data

# ==================== COMPRA ====================
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'producto', 'cantidad', 'fecha', 'precio', 'unidad']  
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': '0', 'required': True}),
            'precio': forms.NumberInput(attrs={'min': '0', 'step': '0.01', 'required': True}),
        }

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

# ==================== INFORME ====================
class InformeForm(forms.Form):
    fecha_inicio = forms.DateField(required=True)
    fecha_fin = forms.DateField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de inicio no puede ser mayor que la fecha fin.")

# ==================== PLATO Y SUS PRODUCTOS ====================
class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class PlatoProductoInlineForm(forms.ModelForm):
    """Formulario inline para productos dentro de un plato"""
    class Meta:
        model = PlatoProducto
        fields = ['producto', 'cantidad', 'unidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '1.00'
            }),
            'unidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: kg, unidad, litros'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.all()
        if self.instance and self.instance.producto and self.instance.producto.unidad:
            self.fields['unidad'].initial = self.instance.producto.unidad.nombre
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0.")
        return cantidad

# Formset para manejar productos en un plato
PlatoProductoFormSet = inlineformset_factory(
    Plato,
    PlatoProducto,
    form=PlatoProductoInlineForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)

# ==================== MENÚ ====================
class MenuForm(forms.ModelForm):
    """Formulario principal para crear/editar menús"""
    TIPO_ITEM_CHOICES = [
        ('', '-- Seleccionar --'),
        ('productos', 'Productos Individuales (Múltiples)'),
        ('plato', 'Plato Compuesto'),
        ('menu_simple', 'Menú Simple'),
    ]
    
    tipo_item = forms.ChoiceField(
        choices=TIPO_ITEM_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'tipo_item',
        }),
        label='Tipo de Ítem'
    )
    
    plato_id = forms.ModelChoiceField(
        queryset=Plato.objects.all(),
        required=False,
        empty_label='-- Seleccionar Plato --',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'plato_id',
        }),
        label='Plato'
    )
    
    class Meta:
        model = Menu
        fields = [
            'nombre', 
            'descripcion', 
            'precio_menu', 
            'descuento', 
            'categoria_menu', 
            'disponible',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Combo Especial',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe el ítem del menú...',
                'rows': 4,
            }),
            'precio_menu': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
            }),
            'descuento': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0.00',
            }),
            'categoria_menu': forms.Select(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre del Menú',
            'descripcion': 'Descripción',
            'precio_menu': 'Precio',
            'descuento': 'Descuento (%)',
            'categoria_menu': 'Categoría del Menú',
            'disponible': 'Disponible',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando, determinar el tipo
        if self.instance and self.instance.pk:
            if self.instance.menu_productos.exists():
                self.fields['tipo_item'].initial = 'productos'
            elif self.instance.content_type:
                model_class = self.instance.content_type.model_class()
                if model_class == Plato:
                    self.fields['tipo_item'].initial = 'plato'
                    if self.instance.item:
                        self.fields['plato_id'].initial = self.instance.item.id
            else:
                self.fields['tipo_item'].initial = 'menu_simple'
    
    def clean_precio_menu(self):
        precio = self.cleaned_data.get('precio_menu')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio
    
    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        if descuento is None:
            return 0
        if descuento < 0 or descuento > 100:
            raise forms.ValidationError("El descuento debe estar entre 0 y 100%.")
        return descuento
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_item = cleaned_data.get('tipo_item')
        plato_id = cleaned_data.get('plato_id')
        
        if tipo_item == 'plato' and not plato_id:
            raise forms.ValidationError('Debe seleccionar un plato.')
        
        return cleaned_data
    
    def save(self, commit=True):
        menu = super().save(commit=False)
        tipo_item = self.cleaned_data.get('tipo_item')
        
        if tipo_item == 'productos':
            menu.content_type = None
            menu.object_id = None
        elif tipo_item == 'plato':
            plato = self.cleaned_data.get('plato_id')
            if plato:
                menu.content_type = ContentType.objects.get_for_model(Plato)
                menu.object_id = plato.id
        elif tipo_item == 'menu_simple':
            menu.content_type = None
            menu.object_id = None
        
        if commit:
            menu.save()
            self.save_m2m()
        
        return menu

# Formulario para productos individuales del menú
class MenuProductoInlineForm(forms.ModelForm):
    """Formulario inline para productos dentro de un menú"""
    class Meta:
        model = MenuProducto
        fields = ['producto', 'cantidad', 'orden']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '1.00'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.all()
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0.")
        return cantidad

# Formset para productos en el menú
MenuProductoFormSet = inlineformset_factory(
    Menu,
    MenuProducto,
    form=MenuProductoInlineForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)