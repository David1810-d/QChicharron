from django.db import models

# Create your models here.
    
class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.nombre 
    
class Compra(models.Model):
    proveedor = models.CharField(max_length=100)
    factura = models.CharField(max_length=50)
    fecha_compra = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Compra {self.factura} - {self.proveedor}"
    
class Informe(models.Model):
    tipo = models.CharField(max_length=50, choices=[('ventas', 'Ventas'), ('compras', 'Compras'), ('nomina', 'Nómina')])
    fecha_generado = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()
    generado_por = models.ForeignKey('Administrador', on_delete=models.SET_NULL, null=True)

    def _str_(self):
        return f"Informe de {self.tipo} - {self.fecha_generado.strftime('%Y-%m-%d')}"
    
class Venta(models.Model):
    cliente = models.CharField(max_length=100)
    factura = models.CharField(max_length=50)
    fecha_venta = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Venta {self.factura} - {self.cliente}"


#------------------Modelos Santiago-----------------------------
#-----------------------Insumo----------------------------------
    
class Insumo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Insumo", unique=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Proveedor")
    imagen = models.ImageField(upload_to='insumos/%y/%m/%d', null=True, blank=True, verbose_name="Imagen del Insumo")
    unidad_medida = models.CharField(max_length=20, verbose_name="Unidad de Medida")  # Ej: kg, litros, unidades
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad en Stock")
    fecha_ingreso = models.DateField(verbose_name="Fecha de Ingreso")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
        ordering = ['nombre']

#------------------------------Producto ventadirecta--------------------------------------------
class ProductoVentaDirecta(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto", unique=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Proveedor")
    imagen = models.ImageField(upload_to='productos_directos/%y/%m/%d', null=True, blank=True, verbose_name="Imagen del Producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de Venta")
    stock = models.PositiveIntegerField(verbose_name="Stock Disponible")
    fecha_ingreso = models.DateField(verbose_name="Fecha de Ingreso")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto para Venta Directa"
        verbose_name_plural = "Productos para Venta Directa"
        ordering = ['nombre']
#-----------------------------Proveeedor---------------------------------------------------------
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Proveedor", unique=True)
    nit = models.CharField(max_length=50, verbose_name="NIT", unique=True)
    telefono = models.CharField(max_length=20, verbose_name="Teléfono de Contacto")
    correo = models.EmailField(verbose_name="Correo Electrónico")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], verbose_name="Estado")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']
#-----------------------------------Nomina---------------------------------------------------
class Nomina(models.Model):
    empleado = models.CharField(max_length=100, verbose_name="Nombre del Empleado")  # Se puede cambiar por ForeignKey a un modelo Empleado
    fecha_pago = models.DateField(verbose_name="Fecha de Pago")
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salario Base")
    horas_extra = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Horas Extra")
    descuentos = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Descuentos")
    salario_neto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salario Neto")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")

    def __str__(self):
        return f"{self.empleado} - {self.fecha_pago}"

    class Meta:
        verbose_name = "Registro de Nómina"
        verbose_name_plural = "Nóminas"
        ordering = ['-fecha_pago']
#---------------------------------------------------Listo el pollo-------------------------

#------------------Modelos Alejandro-----------------------------
#-----------------------Plato------------------------------------

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Plato(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del plato", unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ingredientes = models.TextField(verbose_name="Ingredientes")
    imagen = models.ImageField(upload_to="platos/%y/%m/%d", null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
    
#-----------------------Pedido------------------------------------
class Pedido(models.Model):
    mesa_numero = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ("pendiente", "Pendiente"),
        ("en preparación", "En preparación"),
        ("listo", "Listo"),
        ("entregado", "Entregado")
    ], default="pendiente")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido Mesa {self.mesa_numero} - {self.fecha.date()}"
    
#-----------------------Detalle del pedido-------------------------
#-----------------------Relacion entre pedido y plato--------------

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre}"
    
#-----------------------Empleado------------------------------------
 
class Empleado(models.Model):
    ROLES = (
        ("mesero", "Mesero"),
        ("cocinero", "Cocinero"),
        ("cajero", "Cajero"),
        ("admin", "Administrador"),
    )
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    cargo = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"   
    
#-----------------------Usuario------------------------------------
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)  # en producción deberías encriptar

    def __str__(self):
        return self.nombre
