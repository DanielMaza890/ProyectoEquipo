from django.urls import path
from . import views

app_name = 'encuestas'

urlpatterns = [
    path('registro/', views.registro_page, name='registro'),
    path('elaboracion/', views.elaboracion_page, name='elaboracion'),
    path('reporte/', views.reporte_page, name='reporte'),
    # existing class-based views could also be included here
]