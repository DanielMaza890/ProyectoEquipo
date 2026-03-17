from django.shortcuts import render
from .models import Alumno, Pago

def historial_pagos(request):
    pagos = Pago.objects.all()
    return render(request, "historial.html", {"pagos": pagos})

def reporte_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, "reporte.html", {"alumnos": alumnos})

def inicio(request): 
    return render(request, "inicio.html")
