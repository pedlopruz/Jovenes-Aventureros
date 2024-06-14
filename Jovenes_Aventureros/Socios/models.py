from django.db import models

# Create your models here.

XS = "XS"
S = "S"
M = "M"
L = "L"
XL = "XL"
XXL = "XXL"

TALLA = [
    (XS, "XS"),
    (S, "S"),
    (M, "M"),
    (L, "L"),
    (XL, "XL"),
    (XXL, "XXL"),
]

class Socios(models.Model):
    id = models.AutoField(primary_key=True)
    numero_socio = models.IntegerField(default=0)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=20)
    fecha_nacimiento = models.CharField(max_length=16)
    telefono = models.CharField(max_length=20)
    codigo_postal = models.CharField(max_length=20, default=0)
    ciudad = models.CharField(max_length=30)
    provincia = models.CharField(max_length=35)
    socio = models.BooleanField(default=False)
    talla_camiseta = models.CharField(max_length=4, choices=TALLA, default=S)

    def __str__(self):
        return f"{self.nombre}, {self.apellido}"
