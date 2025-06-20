from django.db import models

# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre