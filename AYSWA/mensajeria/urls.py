from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),  # 🔥 ESTO ES CLAVE
    path('conversaciones/', views.conversaciones, name='conversaciones'),
    path('mensajes/<int:usuario_id>/', views.obtener_mensajes, name='mensajes'),
    path('enviar/', views.enviar_mensaje, name='enviar'),
]