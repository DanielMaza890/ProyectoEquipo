from django import forms
from django.forms import inlineformset_factory, formset_factory
from .models import Encuesta, Pregunta, Opcion, Respuesta, Participante


class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nombre', 'correo', 'departamento']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre Completo'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}),
            'departamento': forms.TextInput(attrs={'placeholder': 'Departamento'}),
        }


class EncuestaForm(forms.ModelForm):
    """Formulario para crear y editar encuestas"""
    
    class Meta:
        model = Encuesta
        fields = ['titulo', 'descripcion', 'estado', 'fecha_apertura', 'fecha_cierre']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título de la encuesta',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describa el propósito de la encuesta'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_apertura': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_cierre': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'titulo': 'Título de la encuesta',
            'descripcion': 'Descripción',
            'estado': 'Estado',
            'fecha_apertura': 'Fecha de apertura',
            'fecha_cierre': 'Fecha de cierre',
        }


class PreguntaForm(forms.ModelForm):
    """Formulario para crear y editar preguntas"""
    
    class Meta:
        model = Pregunta
        fields = ['numero', 'texto', 'tipo', 'obligatoria']
        widgets = {
            'numero': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese la pregunta'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'obligatoria': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'numero': 'Número de pregunta',
            'texto': 'Texto de la pregunta',
            'tipo': 'Tipo de pregunta',
            'obligatoria': 'Es obligatoria',
        }


class OpcionForm(forms.ModelForm):
    """Formulario para opciones de respuesta"""
    
    class Meta:
        model = Opcion
        fields = ['texto', 'orden']
        widgets = {
            'texto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la opción'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
        }
        labels = {
            'texto': 'Opción',
            'orden': 'Orden',
        }


class RespuestaEncuestaForm(forms.Form):
    """Formulario dinámico para responder encuestas"""
    
    def __init__(self, encuesta, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encuesta = encuesta
        
        for pregunta in encuesta.preguntas.all():
            if pregunta.tipo == 'opcion_multiple':
                self.fields[f'pregunta_{pregunta.id}'] = forms.ModelChoiceField(
                    queryset=pregunta.opciones.all(),
                    widget=forms.RadioSelect(attrs={
                        'class': 'form-check-input'
                    }),
                    label=pregunta.texto,
                    required=pregunta.obligatoria,
                    empty_label=None
                )
            elif pregunta.tipo == 'texto_corto':
                self.fields[f'pregunta_{pregunta.id}'] = forms.CharField(
                    widget=forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese su respuesta'
                    }),
                    label=pregunta.texto,
                    required=pregunta.obligatoria,
                    max_length=500
                )
            elif pregunta.tipo == 'escala':
                self.fields[f'pregunta_{pregunta.id}'] = forms.ChoiceField(
                    choices=[(i, str(i)) for i in range(1, 6)],
                    widget=forms.RadioSelect(attrs={
                        'class': 'form-check-input'
                    }),
                    label=pregunta.texto,
                    required=pregunta.obligatoria,
                    help_text='Escala del 1 (menor) al 5 (mayor)'
                )
