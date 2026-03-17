from django.shortcuts import render # Herramienta para generar la página HTML
from .models import Alumno # Importamos tu tabla de alumnos

def reporte_escolar(request):
    # 1. Consultamos todos los alumnos guardados en la base de datos
    alumnos = Alumno.objects.all()
    
    # 2. Obtenemos el conteo total de registros
    total = alumnos.count()
    
    # 3. Filtramos: buscamos cuántos tienen calificación menor a 70
    # "__lt" significa "Less Than" (menor que)
    reprobados = alumnos.filter(calificacion__lt=70).count()
    
    # 4. Filtramos: buscamos cuántos tienen la casilla 'ha_desertado' marcada
    desertores = alumnos.filter(ha_desertado=True).count()

    # 5. Calculamos porcentajes matemáticos (Parte / Total * 100)
    # Usamos una validación para que si el total es 0, el programa no explote
    p_reprobados = (reprobados / total * 100) if total > 0 else 0
    p_desercion = (desertores / total * 100) if total > 0 else 0

    # 6. Guardamos todo en un "Contexto" (un paquete de datos para el HTML)
    context = {
        'total': total,
        'reprobados': reprobados,
        'p_reprobados': p_reprobados,
        'desertores': desertores,
        'p_desercion': p_desercion,
    }
    
    # 7. Enviamos esos datos al archivo visual 'reporte.html'
    return render(request, 'alumnos/reporte.html', context)