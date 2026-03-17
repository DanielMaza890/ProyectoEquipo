from django.urls import path
from .views import AlumnoList, AlumnoCreate, AlumnoUpdate, AlumnoDelete

urlpatterns = [
    path('', AlumnoList.as_view(), name='alumno_list'),
    path('crear/', AlumnoCreate.as_view(), name='alumno_create'),
    path('editar/<int:pk>/', AlumnoUpdate.as_view(), name='alumno_update'),
    path('eliminar/<int:pk>/', AlumnoDelete.as_view(), name='alumno_delete'),
]