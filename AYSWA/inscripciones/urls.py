from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
    path('registrar/', views.registrar, name='registrar'),
    path('modificar/<int:id>/', views.modificar, name='modificar'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
    path('avance/<int:id>/', views.avance, name='avance'),
    
]