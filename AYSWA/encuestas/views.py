from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.contrib import messages
import json

from .models import Encuesta, Pregunta, Opcion, Respuesta
from .forms import EncuestaForm, PreguntaForm, OpcionForm, RespuestaEncuestaForm


# ==================== LISTA ENCUESTAS ====================

class ListaEncuestasView(LoginRequiredMixin, ListView):
    """Lista todas las encuestas publicadas"""
    model = Encuesta
    template_name = 'encuestas/lista_encuestas.html'
    context_object_name = 'encuestas'
    login_url = 'admin:login'
    
    def get_queryset(self):
        return Encuesta.objects.filter(estado='publicada').order_by('-fecha_creacion')


# ==================== DASHBOARD ====================

class DashboardView(LoginRequiredMixin, ListView):
    """Dashboard del usuario con sus encuestas"""
    model = Encuesta
    template_name = 'encuestas/dashboard.html'
    context_object_name = 'encuestas'
    login_url = 'admin:login'
    
    def get_queryset(self):
        return Encuesta.objects.filter(autor=self.request.user).order_by('-fecha_creacion')


# simple render views for static pages created earlier (registro/elaboracion/reporte)
from django.views.decorators.http import require_GET

from .forms import ParticipanteForm


def registro_page(request):
    # maneja GET y POST en la misma vista
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participante registrado correctamente.')
            return redirect('encuestas:registro')
    else:
        form = ParticipanteForm()
    return render(request, 'encuestas/registro.html', {'form': form})

@require_GET
def elaboracion_page(request):
    return render(request, 'encuestas/elaboracion.html')

@require_GET
def reporte_page(request):
    # contar participantes
    from .models import Participante
    total = Participante.objects.count()
    return render(request, 'encuestas/reporte.html', {'total_participantes': total})


# ==================== CREAR ENCUESTA ====================

class CrearEncuestaView(LoginRequiredMixin, CreateView):
    """Crea una nueva encuesta"""
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'encuestas/crear_encuesta.html'
    login_url = 'admin:login'
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, '✅ Encuesta creada correctamente')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('encuestas:editar_encuesta', kwargs={'pk': self.object.pk})
        
        # Obtener la encuesta
        encuesta = get_object_or_404(Encuesta, pk=encuesta_pk)
        context['encuesta'] = encuesta
        context['preguntas'] = encuesta.preguntas.all().order_by('numero')
        
        # Verificar permisos
        context['es_autor'] = encuesta.autor == usuario
        context['ya_respondio'] = encuesta.respuestas.filter(usuario=usuario).exists()
        
        # Formulario de respuesta
        if encuesta.estado == 'publicada' and not context['ya_respondio']:
            context['form_respuestas'] = RespuestaEncuestaForm(encuesta=encuesta)
        
        # Datos para reporte
        if context['es_autor']:
            context['reporte'] = self._generar_reporte(encuesta)
            context['form_encuesta'] = EncuestaForm(instance=encuesta)
            context['form_pregunta'] = PreguntaForm()
            context['form_opcion'] = OpcionForm()
        
        return context
    
    def _generar_reporte(self, encuesta):
        """Genera datos de reporte para la encuesta"""
        preguntas_analisis = []
        
        for pregunta in encuesta.preguntas.all():
            respuestas = pregunta.respuestas_pregunta.all()
            analisis = {
                'pregunta': pregunta,
                'total_respuestas': respuestas.count(),
                'estadisticas': {}
            }
            
            if pregunta.tipo == 'opcion_multiple':
                for opcion in pregunta.opciones.all():
                    count = respuestas.filter(opcion_seleccionada=opcion).count()
                    pct = (count / respuestas.count() * 100) if respuestas.count() > 0 else 0
                    analisis['estadisticas'][opcion.texto] = {
                        'cantidad': count,
                        'porcentaje': round(pct, 2)
                    }
            
            elif pregunta.tipo == 'escala':
                valores = list(respuestas.filter(
                    valor_escala__isnull=False
                ).values_list('valor_escala', flat=True))
                
                if valores:
                    analisis['estadisticas']['promedio'] = round(sum(valores) / len(valores), 2)
                    analisis['estadisticas']['minimo'] = min(valores)
                    analisis['estadisticas']['maximo'] = max(valores)
                    for v in range(1, 6):
                        analisis['estadisticas'][f'valor_{v}'] = respuestas.filter(valor_escala=v).count()
            
            elif pregunta.tipo == 'texto_corto':
                analisis['respuestas_texto'] = list(respuestas.filter(
                    texto_respuesta__isnull=False
                ).values_list('texto_respuesta', flat=True))
            
            preguntas_analisis.append(analisis)
        
        return {
            'preguntas': preguntas_analisis,
            'total_respuestas': encuesta.respuestas.values('usuario').distinct().count()
        }
    
    def post(self, request, *args, **kwargs):
        """Maneja POST para responder encuesta o guardar cambios"""
        encuesta_pk = kwargs.get('pk')
        encuesta = get_object_or_404(Encuesta, pk=encuesta_pk)
        usuario = request.user
        
        # Responder encuesta
        if 'responder' in request.POST:
            if encuesta.respuestas.filter(usuario=usuario).exists():
                messages.warning(request, 'Ya has respondido esta encuesta.')
                return redirect('encuestas:consolidado', pk=encuesta_pk)
            
            form = RespuestaEncuestaForm(request.POST, encuesta=encuesta)
            if form.is_valid():
                for pregunta in encuesta.preguntas.all():
                    field_name = f'pregunta_{pregunta.id}'
                    if field_name in form.cleaned_data:
                        valor = form.cleaned_data[field_name]
                        if pregunta.tipo == 'opcion_multiple':
                            Respuesta.objects.create(
                                encuesta=encuesta, pregunta=pregunta,
                                usuario=usuario, opcion_seleccionada=valor
                            )
                        elif pregunta.tipo == 'texto_corto':
                            Respuesta.objects.create(
                                encuesta=encuesta, pregunta=pregunta,
                                usuario=usuario, texto_respuesta=valor
                            )
                        elif pregunta.tipo == 'escala':
                            Respuesta.objects.create(
                                encuesta=encuesta, pregunta=pregunta,
                                usuario=usuario, valor_escala=int(valor)
                            )
                messages.success(request, '¡Respuesta registrada exitosamente!')
                return redirect('encuestas:consolidado', pk=encuesta_pk)
        
        # Guardar cambios de encuesta (solo autor)
        if 'guardar_encuesta' in request.POST and encuesta.autor == usuario:
            form = EncuestaForm(request.POST, instance=encuesta)
            if form.is_valid():
                form.save()
                messages.success(request, 'Encuesta actualizada.')
            return redirect('encuestas:consolidado', pk=encuesta_pk)
        
        # Agregar pregunta
        if 'agregar_pregunta' in request.POST and encuesta.autor == usuario:
            form = PreguntaForm(request.POST)
            if form.is_valid():
                pregunta = form.save(commit=False)
                pregunta.encuesta = encuesta
                pregunta.save()
                messages.success(request, 'Pregunta agregada.')
            return redirect('encuestas:consolidado', pk=encuesta_pk)
        
        # Agregar opción
        if 'agregar_opcion' in request.POST and encuesta.autor == usuario:
            pregunta_id = request.POST.get('pregunta_id')
            pregunta = get_object_or_404(Pregunta, id=pregunta_id, encuesta=encuesta)
            form = OpcionForm(request.POST)
            if form.is_valid():
                opcion = form.save(commit=False)
                opcion.pregunta = pregunta
                opcion.save()
                messages.success(request, 'Opción agregada.')
            return redirect('encuestas:consolidado', pk=encuesta_pk)
        
        return redirect('encuestas:consolidado', pk=encuesta_pk)
