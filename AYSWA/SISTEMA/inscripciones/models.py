from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    def __str__(self):
        return self.nombre

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    avance = models.IntegerField(default=0)  # porcentaje 0-100
    def __str__(self):
        return f"{self.alumno.nombre} - {self.curso}"


