from django import forms
from .models import Cupon

class CuponForm(forms.ModelForm):
    class Meta:
        model = Cupon
        fields = ['codigo', 'descuento', 'fecha_expiracion', 'activo']
        widgets = {
            'fecha_expiracion': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local', 
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Esto asegura que el valor inicial se muestre correctamente al editar
        if self.instance and self.instance.fecha_expiracion:
            self.initial['fecha_expiracion'] = self.instance.fecha_expiracion.strftime('%Y-%m-%dT%H:%M')