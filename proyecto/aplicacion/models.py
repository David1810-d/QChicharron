from django.db import models
from django.utils import timezone
import datetime

# ------------------ Modelos: Administrador, Usuario, Empleado -----------------------------

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    cargo = models.CharField(max_length=50, default= "operador", choices=[('mesero', 'Mesero'), ('administrador', 'Administrador'), ('cocinero', 'Cocinero'), ("proveedor", "Proveedor")])
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
    
    stock = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)

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
    precio = models.DecimalField(max_digits=10, decimal_places=2)

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