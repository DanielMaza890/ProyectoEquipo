from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre


class Parcial(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    numero = models.IntegerField()
    calificacion = models.FloatField()

    def __str__(self):
        return f"{self.alumno.nombre} - Parcial {self.numero}"