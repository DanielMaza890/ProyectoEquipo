from django.contrib import admin # Importa el panel de control de Django
from .models import Alumno # Trae el modelo Alumno que definimos antes

# Registra el modelo Alumno para que aparezca en el panel de administrador
# Esto te permitirá agregar nombres y calificaciones manualmente.
admin.site.register(Alumno)