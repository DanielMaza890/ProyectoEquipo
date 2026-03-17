from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Cupon
from .forms import CuponForm  # Importar el nuevo formulario

class CuponListView(ListView):
    model = Cupon
    template_name = 'cupones/lista.html'
    context_object_name = 'cupones'

class CuponCreateView(CreateView):
    model = Cupon
    form_class = CuponForm  # Usar form_class en lugar de fields
    template_name = 'cupones/form.html'
    success_url = reverse_lazy('cupon_lista')

class CuponUpdateView(UpdateView):
    model = Cupon
    form_class = CuponForm  # Usar form_class en lugar de fields
    template_name = 'cupones/form.html'
    success_url = reverse_lazy('cupon_lista')

class CuponDeleteView(DeleteView):
    model = Cupon
    template_name = 'cupones/confirmar_eliminacion.html'
    success_url = reverse_lazy('cupon_lista')