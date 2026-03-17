from django.contrib import admin
from .models import SolicitudBeca

@admin.register(SolicitudBeca)
class SolicitudBecaAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'curp', 'tipo_beca', 'promedio', 'puntaje', 'estado', 'fecha_solicitud']
    list_filter = ['estado', 'tipo_beca', 'nivel_estudio']
    search_fields = ['nombre', 'apellido_paterno', 'curp', 'email']
    readonly_fields = ['puntaje', 'fecha_solicitud']
    list_editable = ['estado']