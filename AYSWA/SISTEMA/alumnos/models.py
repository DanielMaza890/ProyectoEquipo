from django.db import models # Importa las herramientas de base de datos de Django

class Alumno(models.Model):
    # 'verbose_name' es el nombre que se mostrará en la página web
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo") 
    calificacion = models.FloatField(default=0, verbose_name="Calificación Actual") 
    ha_desertado = models.BooleanField(default=False, verbose_name="¿Ha desertado?") 

    @property
    def esta_reprobado(self):
        # Lógica: Menor a 70 es reprobado
        return self.calificacion < 70 

    def __str__(self):
        # Cómo se identifica al alumno en las listas
        return self.nombre

    class Meta:
        # Esto traduce los nombres de la tabla en el Admin
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"