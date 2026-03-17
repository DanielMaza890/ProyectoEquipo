from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('solicitar/', views.solicitar_beca, name='solicitar_beca'),
    path('confirmacion/<int:pk>/', views.confirmacion, name='confirmacion'),
    path('admin-panel/', views.panel_admin, name='panel_admin'),
    path('admin-panel/solicitud/<int:pk>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('admin-panel/procesar-masivo/', views.procesar_masivo, name='procesar_masivo'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
]