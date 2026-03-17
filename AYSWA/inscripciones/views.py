from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumno, Inscripcion


# 1️⃣ Registrar alumno e inscripción
def registrar(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        curso = request.POST['curso']

        alumno = Alumno.objects.create(
            nombre=nombre,
            correo=correo,
            telefono=telefono
        )

        Inscripcion.objects.create(
            alumno=alumno,
            curso=curso
        )

        return redirect('lista')

    return render(request, 'inscripciones/registrar.html')


# 2️⃣ Ver lista de inscripciones
def lista(request):
    inscripciones = Inscripcion.objects.all()
    return render(request, 'inscripciones/lista.html', {'inscripciones': inscripciones})


# 3️⃣ Modificar inscripción
def modificar(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)

    if request.method == 'POST':
        inscripcion.curso = request.POST['curso']
        inscripcion.avance = request.POST['avance']
        inscripcion.save()
        return redirect('lista')

    return render(request, 'inscripciones/modificar.html', {'inscripcion': inscripcion})


# 4️⃣ Eliminar inscripción
def eliminar(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)
    inscripcion.delete()
    return redirect('lista')


# 5️⃣ Ver porcentaje de avance
def avance(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)
    return render(request, 'inscripciones/avance.html', {'inscripcion': inscripcion})