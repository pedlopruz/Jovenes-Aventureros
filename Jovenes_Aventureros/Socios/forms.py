from django import forms
from .models import *

class SocioForm(forms.ModelForm):
    
    class Meta:
        model = Socios
        fields = ['nombre', 'apellido','dni', 'fecha_nacimiento', 'telefono', 'codigo_postal','ciudad', 'provincia', 'socio', 'talla_camiseta', 'regalo']

class NoSocioForm(forms.ModelForm):
    
    class Meta:
        model = Socios
        fields = ['nombre', 'apellido','dni', 'fecha_nacimiento', 'telefono', 'codigo_postal','ciudad', 'provincia', 'socio', 'talla_camiseta']

class InscripcionForm(forms.ModelForm):
    
    class Meta:
        model = Inscripciones
        fields = ['nombre', 'destino','fecha', 'distancia', 'dificultad', 'precio_socio','precio_no_socio']

class Inscripcion_SocioForm(forms.Form):

    asiento_bus = forms.IntegerField(label="Seleccione asiento:",validators=[MinValueValidator(1),MaxValueValidator(110)])

class Inscripcion_Socio_B_Form(forms.Form):

    asiento_bus = forms.IntegerField(label="Seleccione asiento:",validators=[MinValueValidator(21),MaxValueValidator(110)])

