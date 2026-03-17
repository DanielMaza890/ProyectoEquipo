from django.contrib import admin
from .models import Encuesta, Pregunta, Opcion, Respuesta


class PreguntaInline(admin.TabularInline):
    """Inline para preguntas en el admin"""
    model = Pregunta
    extra = 1
    fields = ['numero', 'texto', 'tipo', 'obligatoria']


class OpcionInline(admin.TabularInline):
    """Inline para opciones en el admin"""
    model = Opcion
    extra = 1
    fields = ['texto', 'orden']


@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    """Configuración del admin para Encuesta"""
    list_display = ['titulo', 'autor', 'estado', 'fecha_creacion', 'total_respuestas']
    list_filter = ['estado', 'fecha_creacion', 'autor']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_modification']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'descripcion', 'autor')
        }),
        ('Estado', {
            'fields': ('estado', 'fecha_apertura', 'fecha_cierre')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_modification'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [PreguntaInline]
    
    def get_readonly_fields(self, request, obj=None):
        """Solo lectura para create/update"""
        if obj:  # Editing an existing object
            return self.readonly_fields + ['autor']
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        super().save_model(request, obj, form, change)


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    """Configuración del admin para Pregunta"""
    list_display = ['encuesta', 'numero', 'texto', 'tipo', 'obligatoria']
    list_filter = ['encuesta', 'tipo', 'obligatoria']
    search_fields = ['encuesta__titulo', 'texto']
    
    fieldsets = (
        ('Encuesta', {
            'fields': ('encuesta',)
        }),
        ('Contenido', {
            'fields': ('numero', 'texto', 'tipo')
        }),
        ('Configuración', {
            'fields': ('obligatoria',)
        }),
    )
    
    inlines = [OpcionInline]


@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    """Configuración del admin para Opción"""
    list_display = ['pregunta', 'texto', 'orden']
    list_filter = ['pregunta__encuesta', 'pregunta']
    search_fields = ['pregunta__texto', 'texto']
    
    fieldsets = (
        ('Pregunta', {
            'fields': ('pregunta',)
        }),
        ('Opción', {
            'fields': ('texto', 'orden')
        }),
    )


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    """Configuración del admin para Respuesta"""
    list_display = ['encuesta', 'pregunta', 'usuario', 'fecha_respuesta']
    list_filter = ['encuesta', 'fecha_respuesta', 'usuario']
    search_fields = ['encuesta__titulo', 'usuario__username', 'pregunta__texto']
    readonly_fields = ['encuesta', 'pregunta', 'usuario', 'fecha_respuesta']
    
    def has_add_permission(self, request):
        """No permitir agregar respuestas desde admin"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """No permitir eliminar respuestas"""
        return False
    
    fieldsets = (
        ('Información de respuesta', {
            'fields': ('encuesta', 'pregunta', 'usuario', 'fecha_respuesta')
        }),
        ('Contenido de la respuesta', {
            'fields': ('opcion_seleccionada', 'texto_respuesta', 'valor_escala'),
            'classes': ('collapse',)
        }),
    )
