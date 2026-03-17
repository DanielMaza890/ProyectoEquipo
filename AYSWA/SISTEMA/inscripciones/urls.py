from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_inscripciones, name='lista'),
    path('registrar/', views.registrar_inscripcion, name='registrar'),
    path('editar/<int:id>/', views.editar_inscripcion, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_inscripcion, name='eliminar'),
]
