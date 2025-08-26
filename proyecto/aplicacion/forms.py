from django import forms
from aplicacion.models import *
from django.forms import inlineformset_factory
from django_select2.forms import *

#class MensajeForm(forms.ModelForm):
#   class Meta:
#       model = Mensaje
#       fields = ['nombre', 'contenido']

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio']


class PlatoProductoForm(forms.ModelForm):
    class Meta:
        model = PlatoProducto
        fields = ['producto', 'cantidad', 'unidad']
        widgets = {
            'producto': Select2Widget,
        }

PlatoProductoFormSet = inlineformset_factory(
    Plato,
    PlatoProducto,
    form=PlatoProductoForm,
    extra=1,
    can_delete=True
)
