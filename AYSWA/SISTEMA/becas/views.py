from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.http import JsonResponse
from .models import SolicitudBeca
from .forms import SolicitudBecaForm, FiltroSolicitudesForm


def home(request):
    """Página principal"""
    total = SolicitudBeca.objects.count()
    aprobadas = SolicitudBeca.objects.filter(estado='aprobada').count()
    pendientes = SolicitudBeca.objects.filter(estado='pendiente').count()
    rechazadas = SolicitudBeca.objects.filter(estado='rechazada').count()

    context = {
        'total': total,
        'aprobadas': aprobadas,
        'pendientes': pendientes,
        'rechazadas': rechazadas,
    }
    return render(request, 'becas/home.html', context)


def solicitar_beca(request):
    """Formulario para nueva solicitud"""
    if request.method == 'POST':
        form = SolicitudBecaForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.puntaje = solicitud.calcular_puntaje()
            solicitud.save()
            messages.success(request, f'¡Solicitud enviada exitosamente! Tu folio es: {solicitud.id:06d}')
            return redirect('confirmacion', pk=solicitud.pk)
    else:
        form = SolicitudBecaForm()

    return render(request, 'becas/solicitar.html', {'form': form})


def confirmacion(request, pk):
    """Página de confirmación tras enviar solicitud"""
    solicitud = get_object_or_404(SolicitudBeca, pk=pk)
    return render(request, 'becas/confirmacion.html', {'solicitud': solicitud})


def panel_admin(request):
    """Panel de administración para procesar solicitudes"""
    form_filtro = FiltroSolicitudesForm(request.GET)
    solicitudes = SolicitudBeca.objects.all()

    if form_filtro.is_valid():
        estado = form_filtro.cleaned_data.get('estado')
        tipo_beca = form_filtro.cleaned_data.get('tipo_beca')
        buscar = form_filtro.cleaned_data.get('buscar')

        if estado:
            solicitudes = solicitudes.filter(estado=estado)
        if tipo_beca:
            solicitudes = solicitudes.filter(tipo_beca=tipo_beca)
        if buscar:
            solicitudes = solicitudes.filter(
                Q(nombre__icontains=buscar) |
                Q(apellido_paterno__icontains=buscar) |
                Q(curp__icontains=buscar)
            )

    context = {
        'solicitudes': solicitudes,
        'form_filtro': form_filtro,
        'total_filtradas': solicitudes.count(),
    }
    return render(request, 'becas/panel_admin.html', context)


def detalle_solicitud(request, pk):
    """Ver y procesar una solicitud individual"""
    solicitud = get_object_or_404(SolicitudBeca, pk=pk)

    if request.method == 'POST':
        accion = request.POST.get('accion')
        observaciones = request.POST.get('observaciones', '')

        if accion in ['aprobada', 'rechazada']:
            solicitud.estado = accion
            solicitud.observaciones_admin = observaciones
            solicitud.save()
            msg = '✅ Beca APROBADA' if accion == 'aprobada' else '❌ Beca RECHAZADA'
            messages.success(request, f'{msg} para {solicitud.nombre_completo}')
            return redirect('panel_admin')

    return render(request, 'becas/detalle_solicitud.html', {'solicitud': solicitud})


def procesar_masivo(request):
    """Aprobación automática masiva basada en puntaje"""
    if request.method == 'POST':
        umbral = int(request.POST.get('umbral', 60))
        pendientes = SolicitudBeca.objects.filter(estado='pendiente')

        aprobadas = 0
        rechazadas = 0
        for s in pendientes:
            if s.puntaje >= umbral:
                s.estado = 'aprobada'
                s.observaciones_admin = f'Aprobación automática. Puntaje: {s.puntaje}'
                aprobadas += 1
            else:
                s.estado = 'rechazada'
                s.observaciones_admin = f'Rechazo automático. Puntaje insuficiente: {s.puntaje}'
                rechazadas += 1
            s.save()

        messages.success(request, f'Procesamiento completado: {aprobadas} aprobadas, {rechazadas} rechazadas.')
        return redirect('panel_admin')

    return redirect('panel_admin')


def estadisticas(request):
    total = SolicitudBeca.objects.count()

    # Conteos directos por estado
    aprobadas = SolicitudBeca.objects.filter(estado='aprobada').count()
    rechazadas = SolicitudBeca.objects.filter(estado='rechazada').count()
    pendientes = SolicitudBeca.objects.filter(estado='pendiente').count()

    # Conteos por tipo de beca
    por_tipo = SolicitudBeca.objects.values('tipo_beca').annotate(
        total=Count('id'),
        aprobadas=Count('id', filter=Q(estado='aprobada')),
        rechazadas=Count('id', filter=Q(estado='rechazada')),
    )

    # Promedios
    promedio_general = SolicitudBeca.objects.aggregate(avg=Avg('promedio'))['avg'] or 0
    promedio_aprobados = SolicitudBeca.objects.filter(estado='aprobada').aggregate(avg=Avg('promedio'))['avg'] or 0
    promedio_puntaje = SolicitudBeca.objects.aggregate(avg=Avg('puntaje'))['avg'] or 0

    # Top 10 aprobados por puntaje
    top_aprobados = SolicitudBeca.objects.filter(estado='aprobada').order_by('-puntaje')[:10]

    # Por nivel de estudio
    por_nivel = SolicitudBeca.objects.values('nivel_estudio').annotate(
        total=Count('id'),
        aprobadas=Count('id', filter=Q(estado='aprobada')),
    )

    context = {
        'total': total,
        'aprobadas': aprobadas,
        'rechazadas': rechazadas,
        'pendientes': pendientes,
        'por_tipo': por_tipo,
        'por_nivel': por_nivel,
        'promedio_general': round(float(promedio_general), 2),
        'promedio_aprobados': round(float(promedio_aprobados), 2),
        'promedio_puntaje': round(float(promedio_puntaje), 1),
        'top_aprobados': top_aprobados,
    }
    return render(request, 'becas/estadisticas.html', context)