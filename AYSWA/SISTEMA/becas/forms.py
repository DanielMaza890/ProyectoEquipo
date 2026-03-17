from django import forms
from .models import SolicitudBeca

class SolicitudBecaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de Nacimiento"
    )

    class Meta:
        model = SolicitudBeca
        exclude = ['estado', 'puntaje', 'fecha_solicitud', 'observaciones_admin']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Carlos'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABCD123456HXXXXX00', 'maxlength': 18}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10 dígitos'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nivel_estudio': forms.Select(attrs={'class': 'form-select'}),
            'institucion': forms.TextInput(attrs={'class': 'form-control'}),
            'promedio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '10'}),
            'semestre_actual': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'ingreso_familiar_mensual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'numero_dependientes': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'trabaja_actualmente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo_beca': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Explica por qué mereces esta beca...'}),
        }

    def clean_curp(self):
        curp = self.cleaned_data['curp'].upper()
        if len(curp) != 18:
            raise forms.ValidationError("El CURP debe tener exactamente 18 caracteres.")
        return curp

    def clean_promedio(self):
        promedio = self.cleaned_data['promedio']
        if promedio < 0 or promedio > 100:
            raise forms.ValidationError("El promedio debe estar entre 0 y 100.")
        return promedio


class FiltroSolicitudesForm(forms.Form):
    estado = forms.ChoiceField(
        choices=[('', 'Todos'), ('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tipo_beca = forms.ChoiceField(
        choices=[('', 'Todos'), ('academica', 'Académica'), ('deportiva', 'Deportiva'),
                 ('cultural', 'Cultural'), ('economica', 'Económica')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    buscar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por nombre o CURP...'})
    )