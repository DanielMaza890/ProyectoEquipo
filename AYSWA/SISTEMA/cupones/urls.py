from django.urls import path
from .views import CuponListView, CuponCreateView, CuponUpdateView, CuponDeleteView

urlpatterns = [
    path('', CuponListView.as_view(), name='cupon_lista'),
    path('nuevo/', CuponCreateView.as_view(), name='cupon_crear'),
    path('editar/<int:pk>/', CuponUpdateView.as_view(), name='cupon_editar'),
    path('eliminar/<int:pk>/', CuponDeleteView.as_view(), name='cupon_eliminar'),
]