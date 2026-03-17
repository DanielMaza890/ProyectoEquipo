from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nombre