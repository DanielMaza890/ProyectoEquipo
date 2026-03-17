from django.db import models

class SolicitudBeca(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    TIPO_BECA_CHOICES = [
        ('academica', 'Académica'),
        ('deportiva', 'Deportiva'),
        ('cultural', 'Cultural'),
        ('economica', 'Económica'),
    ]

    NIVEL_ESTUDIO_CHOICES = [
        ('preparatoria', 'Preparatoria'),
        ('licenciatura', 'Licenciatura'),
        ('maestria', 'Maestría'),
        ('doctorado', 'Doctorado'),
    ]

    # Datos personales
    nombre = models.CharField(max_length=100, verbose_name="Nombre(s)")
    apellido_paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=100, verbose_name="Apellido Materno")
    curp = models.CharField(max_length=18, unique=True, verbose_name="CURP")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    direccion = models.TextField(verbose_name="Dirección")

    # Datos académicos
    nivel_estudio = models.CharField(max_length=20, choices=NIVEL_ESTUDIO_CHOICES, verbose_name="Nivel de Estudio")
    institucion = models.CharField(max_length=200, verbose_name="Institución Educativa")
    promedio = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Promedio")
    semestre_actual = models.IntegerField(verbose_name="Semestre / Grado Actual")

    # Datos socioeconómicos
    ingreso_familiar_mensual = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ingreso Familiar Mensual ($)")
    numero_dependientes = models.IntegerField(verbose_name="Número de Dependientes en el Hogar")
    trabaja_actualmente = models.BooleanField(default=False, verbose_name="¿Trabaja actualmente?")

    # Tipo de beca
    tipo_beca = models.CharField(max_length=20, choices=TIPO_BECA_CHOICES, verbose_name="Tipo de Beca Solicitada")
    motivo = models.TextField(verbose_name="Motivo de la Solicitud")

    # Control
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado")
    puntaje = models.IntegerField(default=0, verbose_name="Puntaje Calculado")
    observaciones_admin = models.TextField(blank=True, null=True, verbose_name="Observaciones del Administrador")

    class Meta:
        verbose_name = "Solicitud de Beca"
        verbose_name_plural = "Solicitudes de Becas"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} - {self.tipo_beca} ({self.estado})"

    def calcular_puntaje(self):
        """Calcula puntaje automático basado en criterios"""
        puntaje = 0

        # Promedio (máx 40 puntos)
        if self.promedio >= 9.5:
            puntaje += 40
        elif self.promedio >= 9.0:
            puntaje += 35
        elif self.promedio >= 8.5:
            puntaje += 30
        elif self.promedio >= 8.0:
            puntaje += 25
        elif self.promedio >= 7.0:
            puntaje += 15
        else:
            puntaje += 5

        # Nivel socioeconómico (máx 40 puntos)
        ingreso_per_capita = float(self.ingreso_familiar_mensual) / max(self.numero_dependientes, 1)
        if ingreso_per_capita < 2000:
            puntaje += 40
        elif ingreso_per_capita < 4000:
            puntaje += 30
        elif ingreso_per_capita < 6000:
            puntaje += 20
        elif ingreso_per_capita < 10000:
            puntaje += 10
        else:
            puntaje += 0

        # No trabaja (10 puntos extra)
        if not self.trabaja_actualmente:
            puntaje += 10

        # Nivel de estudio (10 puntos)
        if self.nivel_estudio in ['maestria', 'doctorado']:
            puntaje += 5
        else:
            puntaje += 10

        return puntaje

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"