from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Alumno

class AlumnoList(ListView): model = Alumno
class AlumnoCreate(CreateView): 
    model = Alumno
    fields = ['nombre', 'matricula']
    success_url = reverse_lazy('alumno_list')
class AlumnoUpdate(UpdateView): 
    model = Alumno
    fields = ['nombre', 'matricula']
    success_url = reverse_lazy('alumno_list')
class AlumnoDelete(DeleteView): 
    model = Alumno
    success_url = reverse_lazy('alumno_list')
