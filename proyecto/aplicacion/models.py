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