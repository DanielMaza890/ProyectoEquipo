from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("historial/", views.historial_pagos, name="historial_pagos"),
    path("reporte/", views.reporte_alumnos, name="reporte_alumnos"),
]
