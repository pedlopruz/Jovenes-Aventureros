from django import forms
from .models import *

class SocioForm(forms.ModelForm):
    
    class Meta:
        model = Socios
        fields = ['nombre', 'apellido','dni', 'fecha_nacimiento', 'telefono', 'codigo_postal','ciudad', 'provincia', 'socio', 'talla_camiseta']