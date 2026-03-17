from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Encuesta(models.Model):
    """Modelo para las encuestas"""
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicada', 'Publicada'),
        ('cerrada', 'Cerrada'),
    ]
    
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título de la encuesta'
    )
    descripcion = models.TextField(
        verbose_name='Descripción',
        blank=True
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='encuestas_creadas',
        verbose_name='Autor'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='borrador',
        verbose_name='Estado'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    fecha_modification = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de modificación'
    )
    fecha_apertura = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de apertura'
    )
    fecha_cierre = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de cierre'
    )
    
    class Meta:
        verbose_name = 'Encuesta'
        verbose_name_plural = 'Encuestas'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo
    
    @property
    def esta_activa(self):
        """Verifica si la encuesta está activa"""
        return self.estado == 'publicada'
    
    @property
    def total_respuestas(self):
        """Retorna el total de respuestas de la encuesta"""
        return self.respuestas.count()


class Pregunta(models.Model):
    """Modelo para las preguntas de la encuesta"""
    TIPO_CHOICES = [
        ('opcion_multiple', 'Opción múltiple'),
        ('texto_corto', 'Texto corto'),
        ('escala', 'Escala (1-5)'),
    ]
    
    encuesta = models.ForeignKey(
        Encuesta,
        on_delete=models.CASCADE,
        related_name='preguntas',
        verbose_name='Encuesta'
    )
    numero = models.IntegerField(
        verbose_name='Número de pregunta'
    )
    texto = models.TextField(
        verbose_name='Texto de la pregunta'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='opcion_multiple',
        verbose_name='Tipo de pregunta'
    )
    obligatoria = models.BooleanField(
        default=True,
        verbose_name='Es obligatoria'
    )
    
    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['encuesta', 'numero']
        unique_together = ('encuesta', 'numero')
    
    def __str__(self):
        return f"{self.encuesta.titulo} - P{self.numero}: {self.texto[:50]}"


class Opcion(models.Model):
    """Modelo para las opciones de respuesta"""
    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='opciones',
        verbose_name='Pregunta'
    )
    texto = models.CharField(
        max_length=200,
        verbose_name='Texto de opción'
    )
    orden = models.IntegerField(
        verbose_name='Orden'
    )
    
    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'
        ordering = ['pregunta', 'orden']
        unique_together = ('pregunta', 'orden')
    
    def __str__(self):
        return self.texto


class Participante(models.Model):
    """Modelo para registrar participantes en el sistema"""
    nombre = models.CharField(max_length=200, verbose_name='Nombre completo')
    correo = models.EmailField(verbose_name='Correo electrónico', unique=True)
    departamento = models.CharField(max_length=100, verbose_name='Departamento')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
        ordering = ['-fecha_registro']

    def __str__(self):
        return self.nombre


class Respuesta(models.Model):
    """Modelo para almacenar las respuestas de usuarios"""
    encuesta = models.ForeignKey(
        Encuesta,
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name='Encuesta'
    )
    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='respuestas_pregunta',
        verbose_name='Pregunta'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Usuario'
    )
    opcion_seleccionada = models.ForeignKey(
        Opcion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Opción seleccionada'
    )
    texto_respuesta = models.TextField(
        null=True,
        blank=True,
        verbose_name='Respuesta texto'
    )
    valor_escala = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Valor escala',
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    fecha_respuesta = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de respuesta'
    )
    
    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ['-fecha_respuesta']
    
    def __str__(self):
        return f"Respuesta a {self.pregunta} - {self.fecha_respuesta.strftime('%d/%m/%Y')}"
