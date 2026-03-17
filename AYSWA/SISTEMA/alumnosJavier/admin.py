from django.contrib import admin
from .models import Alumno, Pago

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "matricula", "carrera")

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("alumno", "fecha", "monto", "concepto")
