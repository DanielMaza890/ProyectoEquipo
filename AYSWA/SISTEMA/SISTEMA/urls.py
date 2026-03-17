from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas del profesor
    path('inscripciones/', include('inscripciones.urls')),
    path('alumnos/', include('alumnos.urls')),
    path('becas/', include('becas.urls')),
    path('cupones/', include('SISTEMA.cupones.urls')),

    # Tu app
    path('', include('alumnosJavier.urls')),
]
