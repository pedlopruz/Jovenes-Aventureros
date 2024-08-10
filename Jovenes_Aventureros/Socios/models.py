from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
BAJA = "BAJA"
MEDIA_BAJA = "MEDIA-BAJA"
MEDIA_ALTA = "MEDIA-ALTA"
ALTA = "ALTA"

DIFICULTAD = [
    (BAJA, "BAJA"),
    (MEDIA_BAJA, "MEDIA-BAJA"),
    (MEDIA_ALTA, "MEDIA-ALTA"),
    (ALTA, "ALTA"),
]

class Socios(models.Model):
    id = models.AutoField(primary_key=True)
    numero_socio = models.IntegerField(default=0)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)
    dni = models.CharField(max_length=20)
    fecha_nacimiento = models.CharField(max_length=16)
    telefono = models.CharField(max_length=20)
    codigo_postal = models.CharField(max_length=20, default=14550)
    ciudad = models.CharField(max_length=30, default="Montilla")
    provincia = models.CharField(max_length=35, default="Córdoba")
    socio = models.BooleanField(default=False)
    talla_camiseta = models.CharField(max_length=4, choices=TALLA, default=S)
    regalo = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.nombre}, {self.apellidos}"
    

class Inscripciones(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    destino = models.CharField(max_length=30, blank=False)
    fecha = models.CharField(max_length=16, blank=False)
    distancia = models.IntegerField(default=0)
    dificultad = models.CharField(max_length=20, choices=DIFICULTAD, default=BAJA)
    precio_socio = models.PositiveIntegerField()
    precio_no_socio = models.PositiveIntegerField()
    finalizada = models.BooleanField(default=False)
    recaudacion_socios = models.IntegerField(default=0)
    recaudacion_no_socios = models.IntegerField(default=0)
    pago_metalico = models.IntegerField(default=0)
    pago_banco = models.IntegerField(default=0)
    total_socios = models.IntegerField(default=0)
    total_no_socios = models.IntegerField(default=0)
    total_guias = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.nombre}"
    

class Inscripcion_Socio(models.Model):
    id = models.AutoField(primary_key=True)
    inscripcion = models.ForeignKey(Inscripciones, on_delete=models.CASCADE)
    socios = models.ForeignKey(Socios, on_delete=models.CASCADE)
    precio = models.PositiveIntegerField(default=0)
    numero_bus = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(2)])
    asiento_bus = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(110)])
    pago = models.BooleanField(default=False)
    guia = models.BooleanField(default=False)
    

