from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import datetime
import uuid

# ------------------ Modelos: Administrador, Usuario, Empleado -----------------------------

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    cargo = models.CharField(max_length=50, default= "operador", choices=[('mesero', 'Mesero'), ('administrador', 'Administrador'), ('cocinero', 'Cocinero'), ("proveedor", "Proveedor")])
    correo_electronico = models.EmailField()
    numero_celular = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])
    contraseña = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(default=datetime.date.today)
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])

    def __str__(self):
        return f"{self.usuario.nombre}"

class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nivel_prioridad = models.IntegerField()

    def __str__(self):
        return f"Admin {self.usuario.nombre}"

# ---------------------------- Proveedor, Marca, Categoría, unidad-----------------------------

class Proveedor(models.Model):
    nit = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    pais_origen = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Unidad(models.Model):
    nombre = models.CharField(max_length=50)  # Ej: kg, L, unidades
    descripcion = models.CharField(max_length=100, blank=True, null=True)  # opcional

    def __str__(self):
        return self.nombre



# ---------------------------- Producto y Compra -----------------------------

class Producto(models.Model):

    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True) 
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, null=False, blank=False)

    tipo_uso = models.CharField(
        max_length=20,
        choices=[('plato', 'Plato'), ('venta', 'Venta')],
    )
    
    stock = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0,)

    def reducir_stock(self, cantidad):

            if self.stock >= cantidad:
                self.stock -= cantidad
                self.save()
            else:
                raise ValueError("No hay suficiente stock")
    

    def __str__(self):

        return f"{self.nombre} ({self.stock})"

      


class SalidaInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=200)  # Ej: "venta", "cocina", "merma", etc.


class Compra(models.Model):
    id_factura = models.CharField(max_length=20, primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField(default=datetime.date.today)
    precio = models.DecimalField(max_digits=10, decimal_places=2 )
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        
        if not self.id_factura:
            self.id_factura = str(uuid.uuid4())[:8]

        if self.pk:  
            try:
                old = Compra.objects.get(pk=self.pk)
                diferencia = self.cantidad - old.cantidad
                if diferencia != 0:
                    self.producto.stock = (self.producto.stock or 0) + diferencia
                    self.producto.save()
            except Compra.DoesNotExist:
                
                self.producto.stock = (self.producto.stock or 0) + self.cantidad
                self.producto.save()
        else:  
            self.producto.stock = (self.producto.stock or 0) + self.cantidad
            self.producto.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        
        self.producto.stock = (self.producto.stock or 0) - self.cantidad
        self.producto.save()
        super().delete(*args, **kwargs)
        

    def __str__(self):
        return self.id_factura

# ---------------------------- Mesa y Pedido -----------------------------

class Mesa(models.Model):
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Mesa {self.id} - {self.ubicacion}"

class Pedido(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)  # ← CORREGIDO
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'), 
        ('entregado', 'Entregado')
    ])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa.id}"

# ---------------------------- Menú  -----------------------------
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class MenuProducto(models.Model):
    """
    Tabla intermedia para la relación ManyToMany entre Menu y Producto
    Permite agregar múltiples productos a un menú con sus cantidades
    """
    menu = models.ForeignKey(
        'Menu', 
        on_delete=models.CASCADE,
        related_name='menu_productos',
        verbose_name='Menú'
    )
    producto = models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE,
        related_name='productos_menu',
        verbose_name='Producto'
    )
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Cantidad',
        help_text='Cantidad del producto en el menú'
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de presentación en el menú'
    )
    fecha_agregado = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha Agregado'
    )
    
    class Meta:
        verbose_name = 'Producto del Menú'
        verbose_name_plural = 'Productos del Menú'
        ordering = ['orden', 'fecha_agregado']
        unique_together = ['menu', 'producto']  # No repetir el mismo producto en un menú
    
    def __str__(self):
        return f"{self.menu.nombre} - {self.producto.nombre} ({self.cantidad})"
    
    def get_subtotal(self):
        """Calcula el subtotal basado en el precio del producto"""
        if hasattr(self.producto, 'precio') and self.producto.precio:
            return self.cantidad * self.producto.precio
        return Decimal('0.00')


# REEMPLAZAR tu modelo Menu actual con este:
# ---------------------------- Menú  -----------------------------
class Menu(models.Model):
    """
    Modelo que puede referenciar tanto Productos como Platos
    usando una relación polimórfica
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio_menu = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    # Campos para la relación polimórfica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    item = GenericForeignKey('content_type', 'object_id')
    
    # Campos adicionales específicos del menú
    categoria_menu = models.CharField(
        max_length=50,
        choices=[
            ('entrada', 'Entrada'),
            ('plato_principal', 'Plato Principal'),
            ('postre', 'Postre'),
            ('bebida', 'Bebida'),
            ('combo', 'Combo')
        ],
        default='plato_principal'
    )
    
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Mantener campo precio original para compatibilidad temporal
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Relación many-to-many con productos (SOLO UNA VEZ)
    productos = models.ManyToManyField(
        'Producto',
        through='MenuProducto',
        related_name='menus_disponibles',
        blank=True
    )
    
    class Meta:
        verbose_name = "Ítem del Menú"
        verbose_name_plural = "Ítems del Menú"
        ordering = ['categoria_menu', 'nombre']
    
    def get_precio_final(self):
        """Obtiene el precio final considerando descuentos"""
        if self.precio_menu:
            precio_base = self.precio_menu
        elif self.precio:
            precio_base = self.precio
        elif hasattr(self.item, 'precio'):
            precio_base = self.item.precio
        else:
            precio_base = 0
        
        descuento_aplicado = precio_base * (self.descuento / 100)
        return precio_base - descuento_aplicado
    
    def get_tipo_item(self):
        """Retorna el tipo de ítem (producto o plato)"""
        if self.content_type:
            return self.content_type.model
        return "menu_simple"
    
    def get_stock_disponible(self):
        """Si el ítem es un producto, retorna el stock disponible"""
        if self.get_tipo_item() == 'producto' and self.item:
            return self.item.stock
        return None
    
    def puede_servirse(self):
        """Verifica si el ítem del menú puede servirse"""
        if not self.disponible:
            return False
        
        if not self.item:
            return True
        
        if self.get_tipo_item() == 'producto':
            return self.item.stock > 0
        
        if self.get_tipo_item() == 'plato':
            for plato_producto in self.item.platoproducto_set.all():
                if plato_producto.producto.stock < plato_producto.cantidad:
                    return False
        
        return True
    
    def __str__(self):
        precio = self.get_precio_final()
        if self.item:
            tipo = self.get_tipo_item().title()
            return f"{self.nombre} ({tipo}) - ${precio}"
        else:
            return f"{self.nombre} - ${precio}"



# ---------------------------- Menú y Plato -----------------------------
class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)

    productos = models.ManyToManyField(
        Producto,
        through="PlatoProducto",
        related_name="platos"
    )

    def __str__(self):
        return self.nombre

# ELIMINAR ESTO DE MODELS.PY:
# PlatoProductoFormSet = inlineformset_factory(...)



# ---------------------------- Menú y Plato -----------------------------
class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)

    productos = models.ManyToManyField(
        Producto,
        through="PlatoProducto",
        related_name="platos"
    )

    def __str__(self):
        return self.nombre


# ---------------------------- Relaciones: PedidoProducto, PedidoMenu, PlatoProducto -----------------------------

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE,
        related_name="pedidos_producto"
    )

    def __str__(self):
        return f"Producto {self.producto.nombre} en pedido {self.pedido.id}"


class PedidoMenu(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    menu = models.ForeignKey(
        Menu, 
        on_delete=models.CASCADE,
        related_name="pedidos_menu"
    )
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.cantidad}x {self.menu.nombre} en pedido {self.pedido.id}"


class PlatoProducto(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE,
        related_name="platos_producto"
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.cantidad} {self.unidad} de {self.producto.nombre} para {self.plato.nombre}"


# ---------------------------- Venta -----------------------------

class Venta(models.Model):
    METODOS_PAGO = [
        ("efectivo", "Efectivo"),
        ("tarjeta", "Tarjeta"),
        ("online", "Online"),
    ]
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO, default="efectivo")
    estado = models.CharField(max_length=20, choices=[
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("cancelado", "Cancelado"),
    ], default="pendiente")
    admin = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        
        if not self.pk:  # Solo la primera vez que se crea la venta
            for detalle in self.pedido.detallepedido_set.all():
                producto = detalle.producto
                cantidad = detalle.cantidad
                producto.stock = (producto.stock or 0) - cantidad
                producto.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        
        for detalle in self.pedido.detallepedido_set.all():
            producto = detalle.producto
            cantidad = detalle.cantidad
            producto.stock = (producto.stock or 0) + cantidad
            producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Venta #{self.id} - Pedido {self.pedido.id}"

# ---------------------------- Nómina -----------------------------
 
class Nomina(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.DecimalField(max_digits=10, decimal_places=2)
    admin = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.pago}"
# ---------------------------- Informe -----------------------------
class Informe(models.Model):
    TIPO_INFORME_CHOICES = [
        ('venta', 'Informe de Ventas'),
        ('compra', 'Informe de Compras'),
        ('nomina', 'Informe de Nómina'),
        ('personalizado', 'Otro'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_INFORME_CHOICES)
    fecha_creacion = models.DateField(default=timezone.now)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    creado_por = models.ForeignKey('Administrador', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.tipo}) - {self.fecha_inicio} a {self.fecha_fin}"   

