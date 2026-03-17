from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta

class Cupon(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.IntegerField(help_text="Porcentaje de descuento (0-100)")
    fecha_expiracion = models.DateTimeField()
    activo = models.BooleanField(default=True)

    def clean(self):
        # Validación de rango de descuento
        if self.descuento is not None:
            if self.descuento < 0 or self.descuento > 100:
                raise ValidationError({'descuento': "El descuento debe estar entre 0 y 100."})
        
        # Validación de fecha: Permite el día de hoy completo
        if self.fecha_expiracion:
            # Quitamos los segundos y microsegundos para evitar errores por retraso de envío
            ahora = timezone.now().replace(second=0, microsecond=0)
            if self.fecha_expiracion < ahora:
                raise ValidationError({'fecha_expiracion': "La fecha de expiración debe ser hoy o una fecha futura."})

    def __str__(self):
        return self.codigo