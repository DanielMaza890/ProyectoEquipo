from django.db import models

# Create your models here.
from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    carrera = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.matricula}"


class Pago(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="pagos")
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    concepto = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.alumno.nombre} - {self.concepto} - {self.monto}"
