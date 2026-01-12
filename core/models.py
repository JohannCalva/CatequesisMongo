from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_mongodb_backend.fields import ObjectIdAutoField

class Catequizando(models.Model):
    # 1. MAPEO DEL _ID
    # Tu esquema permite 'objectId' o 'string'. 
    # Como migraste de SQL con IDs tipo "1", "2", usamos CharField como Primary Key.
    id = models.CharField(
        primary_key=True, 
        max_length=50, 
        db_column='_id' # Mapea al campo _id de Mongo
    )

    # 2. CAMPOS PLANOS (Strings, Fechas, Enteros)
    cedula = models.CharField(max_length=10)
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, null=True, blank=True)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, null=True, blank=True)
    
    # Enum de Género
    class Genero(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMENINO = 'F', 'Femenino'
    
    genero = models.CharField(
        max_length=1, 
        choices=Genero.choices
    )

    fecha_nacimiento = models.DateTimeField()
    lugar_nacimiento = models.CharField(max_length=100, null=True, blank=True)
    
    numero_hijo = models.IntegerField(null=True, blank=True)
    numero_hermanos = models.IntegerField(null=True, blank=True)
    
    telefono_casa = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=200)

    # 3. CAMPOS ANIDADOS (Arrays y Objetos) -> Usamos JSONField
    # Django guardará estos objetos tal cual, y Mongo validará su estructura con tu script.
    
    padres = models.JSONField(
        default=list, 
        help_text="Array de objetos con keys: relacion, nombres, apellidos, telefono, ocupacion"
    )
    
    representante_legal = models.JSONField(
        help_text="Objeto con keys: es_uno_de_los_padres, nombres, apellidos, telefono, correo"
    )
    
    informacion_salud = models.JSONField(
        help_text="Objeto con keys: tipo_sangre, contacto_emergencia, alergias, aspectos..."
    )
    
    fe_bautismo = models.JSONField(
        help_text="Objeto con keys: fecha, parroquia, ciudad, tomo, pagina..."
    )
    
    sacramentos_realizados = models.JSONField(
        default=list, 
        blank=True,
        help_text="Array de sacramentos previos"
    )
    
    escolaridad = models.JSONField(
        null=True, 
        blank=True
    )
    
    observaciones_generales = models.TextField(null=True, blank=True)

    class Meta:
        # managed = True (por defecto) para que Django sepa que esta colección es suya
        db_table = 'catequizandos' # Nombre exacto de tu colección en Mongo
        verbose_name = 'Catequizando'
        verbose_name_plural = 'Catequizandos'

    def __str__(self):
        return f"{self.cedula} - {self.primer_apellido} {self.primer_nombre}"
    

class Nivel(models.Model):
    # 1. MAPEO DEL _ID
    # Al igual que en catequizandos, permitimos Strings por la migración SQL
    id = models.CharField(
        primary_key=True, 
        max_length=50, 
        db_column='_id'
    )

    # 2. CAMPOS OBLIGATORIOS (Según tu array 'required')
    nombre = models.CharField(max_length=100)
    libro_asignado = models.CharField(max_length=200)
    
    # Edad con validadores espejo de tu esquema BSON (min: 5, max: 18)
    edad_minima = models.IntegerField(
        validators=[
            MinValueValidator(5, message="La edad mínima no puede ser menor a 5"),
            MaxValueValidator(18, message="La edad mínima no puede ser mayor a 18")
        ]
    )

    # 3. CAMPOS OPCIONALES
    descripcion = models.TextField(null=True, blank=True)
    sacramento_asociado = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'niveles' # Nombre exacto de la colección en Mongo
        verbose_name = 'Nivel'
        verbose_name_plural = 'Niveles'

    def __str__(self):
        return f"{self.nombre} (Min: {self.edad_minima} años)"    
    

class Ciclo(models.Model):
    # 1. MAPEO DEL _ID
    # Mantenemos CharField para compatibilidad con tus IDs migrados ("1", "2"...)
    id = models.CharField(
        primary_key=True, 
        max_length=50, 
        db_column='_id'
    )

    # 2. CAMPOS DE DATOS
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    # 3. ENUM PARA ESTADO
    # Mapeo exacto de tu 'enum': ['ABIERTO', 'CERRADO', 'INSCRIPCIONES']
    class Estado(models.TextChoices):
        ABIERTO = 'ABIERTO', 'Abierto'
        CERRADO = 'CERRADO', 'Cerrado'
        INSCRIPCIONES = 'INSCRIPCIONES', 'Inscripciones'

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.INSCRIPCIONES
    )

    class Meta:
        db_table = 'ciclos' # Nombre exacto de la colección en Mongo
        verbose_name = 'Ciclo'
        verbose_name_plural = 'Ciclos'

    def __str__(self):
        return self.nombre

    # 4. VALIDACIÓN DE LOGICA DE NEGOCIO (Cross-field validation)
    def clean(self):
        # Validar que fecha_inicio < fecha_fin
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio >= self.fecha_fin:
                raise ValidationError({
                    'fecha_fin': "La fecha de fin debe ser posterior a la fecha de inicio."
                })
        super().clean()

    # Asegura que el validador corra al guardar desde el admin o formularios
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
class Grupo(models.Model):
    # 1. MAPEO DEL _ID
    id = models.CharField(
        primary_key=True, 
        max_length=50, 
        db_column='_id'
    )

    # 2. CAMPOS DIRECTOS
    nombre_grupo = models.CharField(max_length=100)

    # 3. RELACIONES (Foreign Keys)
    # Apuntan a los modelos Ciclo y Nivel creados anteriormente.
    # on_delete=models.PROTECT evita borrar un ciclo si tiene grupos activos.
    ciclo = models.ForeignKey(
        'Ciclo', 
        on_delete=models.PROTECT, 
        db_column='ciclo_id',
        related_name='grupos'
    )
    
    nivel = models.ForeignKey(
        'Nivel', 
        on_delete=models.PROTECT, 
        db_column='nivel_id',
        related_name='grupos'
    )

    # 4. ESTADO DEL GRUPO
    class Estado(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo'
        INACTIVO = 'INACTIVO', 'Inactivo'

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.ACTIVO
    )

    # 5. CAMPOS EMBEBIDOS (Arrays de objetos)
    # Array de objetos { "nombre": "...", "tipo": "TITULAR|AUXILIAR" }
    catequistas = models.JSONField(
        default=list,
        help_text="Lista de catequistas asignados. Keys: nombre, tipo"
    )

    # Array de objetos { "sesion_id": 1, "tema": "...", "fecha": "...", "asistencia_tomada": bool }
    sesiones = models.JSONField(
        default=list,
        blank=True,
        help_text="Planificación de sesiones."
    )

    class Meta:
        db_table = 'grupos' # Nombre exacto de la colección en Mongo
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    def __str__(self):
        return f"{self.nombre_grupo} - {self.ciclo}"
    

class Inscripcion(models.Model):
    # 1. MAPEO DEL _ID (Autogenerado por Mongo)
    id = ObjectIdAutoField(
        primary_key=True,
        db_column='_id'
    )

    # 2. RELACIONES (Foreign Keys)
    # Apuntan a Catequizando y Grupo.
    # Usamos db_column para que coincida con tu esquema ('catequizando_id', 'grupo_id')
    catequizando = models.ForeignKey(
        'Catequizando',
        on_delete=models.CASCADE,
        db_column='catequizando_id',
        related_name='inscripciones'
    )
    
    grupo = models.ForeignKey(
        'Grupo',
        on_delete=models.CASCADE,
        db_column='grupo_id',
        related_name='inscripciones'
    )

    fecha_inscripcion = models.DateTimeField()

    # 3. ENUMS DE ESTADO
    class EstadoInscripcion(models.TextChoices):
        CURSANDO = 'CURSANDO', 'Cursando'
        APROBADO = 'APROBADO', 'Aprobado'
        REPROBADO = 'REPROBADO', 'Reprobado'
        RETIRADO = 'RETIRADO', 'Retirado'

    estado_inscripcion = models.CharField(
        max_length=20,
        choices=EstadoInscripcion.choices,
        default=EstadoInscripcion.CURSANDO
    )

    class EstadoPago(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PAGADO = 'PAGADO', 'Pagado'

    estado_pago = models.CharField(
        max_length=20,
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE
    )

    # 4. CAMPOS EMBEBIDOS (JSON)
    
    # Array de objetos { "descripcion": "...", "valor": 9.5, "fecha": "..." }
    calificaciones = models.JSONField(
        default=list,
        blank=True,
        help_text="Historial de notas."
    )

    # Array de objetos { "sesion_id": 1, "estado": "PRESENTE|FALTA..." }
    registro_asistencia = models.JSONField(
        default=list,
        blank=True,
        help_text="Registro de asistencia por sesión."
    )

    # Objeto { "numero_certificado": "...", "fecha_emision": "...", ... }
    certificado_final = models.JSONField(
        null=True,
        blank=True,
        help_text="Datos del certificado si aprobó."
    )

    class Meta:
        db_table = 'inscripciones'
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        
        # Evitar que un alumno se inscriba dos veces en el mismo grupo
        constraints = [
            models.UniqueConstraint(
                fields=['catequizando', 'grupo'], 
                name='unique_inscripcion_alumno_grupo'
            )
        ]

    def __str__(self):
        return f"{self.catequizando} - {self.grupo}"