from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumno, Inscripcion


# LISTAR INSCRIPCIONES
def lista_inscripciones(request):
    inscripciones = Inscripcion.objects.all()
    return render(request, 'lista.html', {'inscripciones': inscripciones})


# REGISTRAR ALUMNO E INSCRIPCIÓN
def registrar_inscripcion(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        curso = request.POST['curso']
        avance = request.POST['avance']

        alumno = Alumno.objects.create(
            nombre=nombre,
            correo=correo,
            telefono=telefono
        )

        Inscripcion.objects.create(
            alumno=alumno,
            curso=curso,
            avance=avance
        )

        return redirect('lista')

    return render(request, 'registrar.html')


# MODIFICAR INSCRIPCIÓN
def editar_inscripcion(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)

    if request.method == 'POST':
        inscripcion.curso = request.POST['curso']
        inscripcion.avance = request.POST['avance']
        inscripcion.save()
        return redirect('lista')

    return render(request, 'editar.html', {'inscripcion': inscripcion})


# ELIMINAR INSCRIPCIÓN
def eliminar_inscripcion(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)
    inscripcion.delete()
    return redirect('lista')
