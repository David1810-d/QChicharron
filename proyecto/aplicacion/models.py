from django.db import models
from django.utils import timezone
import datetime

# ------------------ Modelos: Administrador, Usuario, Empleado -----------------------------

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    correo_electronico = models.EmailField()
    numero_celular = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])
    contraseña = models.CharField(max_length=255)

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

# ---------------------------- Proveedor, Marca, Categoría -----------------------------

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

# ---------------------------- Producto y Compra -----------------------------

class Producto(models.Model):
    TIPO_USO = (
        ('plato', 'Plato'),
        ('venta', 'Venta directa'),
    )

    id_producto = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField(default=datetime.date.today)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    tipo_uso = models.CharField(max_length=10, choices=TIPO_USO)

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    id_factura = models.CharField(max_length=20, primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField(default=datetime.date.today)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.id_factura

# ---------------------------- Mesa y Pedido -----------------------------

class Mesa(models.Model):
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        return f"Mesa {self.id} - {self.ubicacion}"

class Pedido(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)  # ← CORREGIDO
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('entregado', 'Entregado')
    ])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa.id}"

# ---------------------------- Menú y Plato -----------------------------

class Menu(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

# ---------------------------- Relaciones: PedidoProducto, PedidoMenu, PlatoProducto -----------------------------

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Producto {self.producto.nombre} en pedido {self.pedido.id}"

class PedidoMenu(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.cantidad}x {self.menu.nombre} en pedido {self.pedido.id}"

class PlatoProducto(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.cantidad} {self.unidad} de {self.producto.nombre} para {self.plato.nombre}"

# ---------------------------- Venta -----------------------------

class Venta(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.date.today)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    admin = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True)

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
