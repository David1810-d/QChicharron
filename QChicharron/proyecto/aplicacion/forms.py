from django import forms
from aplicacion.models import *
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django_select2.forms import *
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django_select2.forms import ModelSelect2Widget
from aplicacion.models import Menu, Producto, Plato, PlatoProducto




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
        widgets = {
            'stock': forms.NumberInput(attrs={
                'min': '0',     # evita negativos desde HTML
                'required': True,
            }),
        }

    # Validación a nivel de Django (backend)
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
        


class PlatoProductoForm(forms.ModelForm):
    """
    Formulario para agregar productos a un plato
    """
    class Meta:
        model = PlatoProducto
        fields = ['producto', 'cantidad', 'unidad']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-control',
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'unidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: kg, unidad, litros'
            }),
        }
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'unidad': 'Unidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo productos de tipo uso
        self.fields['producto'].queryset = Producto.objects.all()


# Formset para manejar múltiples productos en un plato
from django.forms import inlineformset_factory

PlatoProductoFormSet = inlineformset_factory(
    Plato,
    PlatoProducto,
    form=PlatoProductoForm,
    extra=1,  # Número de formularios vacíos adicionales
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class PlatoProductoForm(forms.ModelForm):
    """Formulario inline para productos del plato"""
    
    class Meta:
        model = PlatoProducto
        fields = ['producto', 'cantidad', 'unidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'unidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'unidad'
            }),
        }
    """
    Formulario para agregar productos individuales a un menú
    Usa Form en lugar de ModelForm para más control
    """
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.none(),
        required=True,
        empty_label='-- Seleccionar Producto --',
        widget=ModelSelect2Widget(
            model=Producto,
            search_fields=['nombre__icontains', 'categoria__nombre__icontains'],
            attrs={
                'data-placeholder': 'Buscar producto...',
                'class': 'form-control'
            }
        ),
        label='Producto'
    )
    
    cantidad = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'placeholder': '1.00'
        }),
        label='Cantidad',
        initial=1
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar todos los productos disponibles
        self.fields['producto'].queryset = Producto.objects.all().select_related(
            'marca', 'categoria', 'unidad'
        )
    
    def clean_cantidad(self):
        """Validación para cantidad"""
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0.")
        return cantidad


class PlatoProductoInlineForm(forms.ModelForm):
    """
    Formulario inline para agregar productos a un plato
    """
    class Meta:
        model = PlatoProducto
        fields = ['producto', 'cantidad', 'unidad']
        widgets = {
            'producto': ModelSelect2Widget(
                model=Producto,
                search_fields=['nombre__icontains', 'categoria__nombre__icontains'],
                attrs={
                    'data-placeholder': 'Buscar producto...',
                    'class': 'form-control'
                }
            ),
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
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'unidad': 'Unidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurar que trae todos los productos
        self.fields['producto'].queryset = Producto.objects.all().select_related(
            'marca', 'categoria', 'unidad'
        )
        
        # Si el producto tiene unidad, usarla por defecto
        if self.instance and self.instance.producto and self.instance.producto.unidad:
            self.fields['unidad'].initial = self.instance.producto.unidad.nombre
    
    def clean_cantidad(self):
        """Validación para cantidad"""
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0.")
        return cantidad


# Formset para manejar múltiples productos en un plato
PlatoProductoFormSet = inlineformset_factory(
    Plato,
    PlatoProducto,
    form=PlatoProductoInlineForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)
    



class PlatoProductoInlineForm(forms.ModelForm):
    """
    Formulario inline para agregar productos a un plato
    """
    class Meta:
        model = PlatoProducto
        fields = ['producto', 'cantidad', 'unidad']
        widgets = {
            'producto': ModelSelect2Widget(
                model=Producto,
                search_fields=['nombre__icontains', 'categoria__nombre__icontains'],
                attrs={
                    'data-placeholder': 'Buscar producto...',
                    'class': 'form-control'
                }
            ),
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
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'unidad': 'Unidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurar que trae todos los productos
        self.fields['producto'].queryset = Producto.objects.all().select_related(
            'marca', 'categoria', 'unidad'
        )
        
        # Si el producto tiene unidad, usarla por defecto
        if self.instance and self.instance.producto and self.instance.producto.unidad:
            self.fields['unidad'].initial = self.instance.producto.unidad.nombre
    
    def clean_cantidad(self):
        """Validación para cantidad"""
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0.")
        return cantidad


# Formset para manejar múltiples productos en un plato
PlatoProductoFormSet = inlineformset_factory(
    Plato,
    PlatoProducto,
    form=PlatoProductoInlineForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)
class MenuForm(forms.ModelForm):
    """
    Formulario para crear/editar ítems del menú
    Ahora soporta múltiples productos mediante ManyToMany
    """
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
            'onchange': 'toggleItemSelection()'
        }),
        label='Tipo de Ítem'
    )
    
    # Campo para seleccionar UN plato (se mantiene con GenericForeignKey)
    plato_id = forms.ModelChoiceField(
        queryset=Plato.objects.none(),
        required=False,
        empty_label='-- Seleccionar Plato --',
        widget=ModelSelect2Widget(
            model=Plato,
            search_fields=['nombre__icontains'],
            attrs={
                'data-placeholder': 'Buscar plato...',
                'class': 'form-control',
                'id': 'plato_id',
                'style': 'display:none;'
            }
        ),
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
            'fecha_creacion'
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
                'value': '0',
            }),
            'categoria_menu': forms.Select(attrs={
                'class': 'form-control',
            }),
            'fecha_creacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'nombre': 'Nombre del Menú',
            'descripcion': 'Descripción',
            'precio_menu': 'Precio',
            'descuento': 'Descuento (%)',
            'categoria_menu': 'Categoría del Menú',
            'fecha_creacion': 'Fecha de Creación',
            'disponible': 'Disponible',
        }
        help_texts = {
            'descuento': 'Porcentaje de descuento (0-100)',
            'precio_menu': 'Precio final del menú',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar querysets
        self.fields['plato_id'].queryset = Plato.objects.all().prefetch_related('productos')
        
        # Si estamos editando, determinar el tipo de ítem
        if self.instance and self.instance.pk:
            # Verificar si tiene productos asociados (ManyToMany)
            if self.instance.menu_productos.exists():
                self.fields['tipo_item'].initial = 'productos'
            # Verificar si tiene un plato asociado (GenericForeignKey)
            elif self.instance.content_type:
                model_class = self.instance.content_type.model_class()
                if model_class == Plato:
                    self.fields['tipo_item'].initial = 'plato'
                    if self.instance.item:
                        self.fields['plato_id'].initial = self.instance.item.id
                else:
                    self.fields['tipo_item'].initial = 'menu_simple'
            else:
                self.fields['tipo_item'].initial = 'menu_simple'
        
        # Ordenar campos
        self.order_fields([
            'tipo_item',
            'plato_id',
            'nombre',
            'descripcion',
            'precio_menu',
            'descuento',
            'categoria_menu',
            'fecha_creacion',
            'disponible',
        ])
    
    def clean_precio_menu(self):
        precio = self.cleaned_data.get('precio_menu')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio
    
    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        if descuento is None:
            return 0
        if descuento < 0:
            raise forms.ValidationError("El descuento no puede ser negativo.")
        if descuento > 100:
            raise forms.ValidationError("El descuento no puede ser mayor a 100%.")
        return descuento
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_item = cleaned_data.get('tipo_item')
        plato_id = cleaned_data.get('plato_id')
        
        # Solo validar plato aquí, los productos se validan en el formset
        if tipo_item == 'plato' and not plato_id:
            raise forms.ValidationError(
                'Debe seleccionar un plato cuando el tipo es "Plato Compuesto".'
            )
        
        return cleaned_data
    
    def save(self, commit=True):
        menu = super().save(commit=False)
        
        tipo_item = self.cleaned_data.get('tipo_item')
        
        # Limpiar relaciones anteriores
        if tipo_item == 'productos':
            # Los productos se manejan con el formset
            menu.content_type = None
            menu.object_id = None
        
        elif tipo_item == 'plato':
            plato = self.cleaned_data.get('plato_id')
            if plato:
                menu.content_type = ContentType.objects.get_for_model(Plato)
                menu.object_id = plato.id
            else:
                menu.content_type = None
                menu.object_id = None
        
        elif tipo_item == 'menu_simple':
            menu.content_type = None
            menu.object_id = None
        
        if commit:
            menu.save()
            self.save_m2m()
        
        return menu