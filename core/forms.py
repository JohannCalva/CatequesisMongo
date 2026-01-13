from django import forms
from .models import Catequizando, Nivel, Ciclo, Grupo, Inscripcion

ESTADO_GENERAL = [
    ('ABIERTO', 'Abierto'),
    ('CERRADO', 'Cerrado'),
    ('INSCRIPCIONES', 'Inscripciones'),
]

# Updating to match Model choices if possible, or keep simple strings
ESTADO_GRUPO = [
    ('ACTIVO', 'Activo'),
    ('INACTIVO', 'Inactivo'),
]

ESTADO_INSCRIPCION = [
    ('CURSANDO', 'Cursando'),
    ('APROBADO', 'Aprobado'),
    ('REPROBADO', 'Reprobado'),
    ('RETIRADO', 'Retirado'),
]

ESTADO_PAGO = [
    ('PAGADO', 'Pagado'),
    ('PENDIENTE', 'Pendiente'),
]

# Form options
ESTADO_ASISTENCIA = [
    ('PRESENTE', 'Presente'),
    ('FALTA', 'Falta'),
    ('JUSTIFICADA', 'Justificada'),
]


OPCIONES_ANIO = [
    ('', 'Seleccione un año...'), # Opción vacía por si es required=False
    ('1RO', '1RO'),
    ('2DO', '2DO'),
    ('3RO', '3RO'),
    ('4TO', '4TO'),
    ('5TO', '5TO'),
    ('6TO', '6TO'),
    ('7MO', '7MO'),
    ('8VO', '8VO'),
    ('9NO', '9NO'),
    ('10MO', '10MO'),
    ('1BGU', '1BGU'),
    ('2BGU', '2BGU'),
    ('3BGU', '3BGU'),
]

OPCIONES_SANGRE = [
    ('', 'Seleccione...'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]

OPCIONES_GENERO = [
    ('M', 'Masculino'),
    ('F', 'Femenino')
]

class CatequizandoUpdateMiniForm(forms.Form):
    telefono = forms.CharField(
        min_length=10,
        max_length=10, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09...'})
    )
    telefono = forms.CharField(
        min_length=10,
        max_length=10, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09...'})
    )
    
    direccion = forms.CharField(
        max_length=200, 
        required=False,
        label="Dirección", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    escuelacolegio = forms.CharField(
        max_length=150, 
        required=False, 
        label="Institución Educativa",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    anioencurso = forms.ChoiceField(
        choices=OPCIONES_ANIO,
        required=False,
        label="Año en Curso",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tiposangre = forms.ChoiceField(
        choices=OPCIONES_SANGRE,
        label="Tipo de Sangre",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    alergia = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Usamos Textarea para comentarios para que se vea más grande
    comentario = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )


# ==========================================
# 3. Formulario de Registro Completo (SP)
# ==========================================

class CatequizandoSPForm(forms.Form):

    # -----------------------
    # A) Datos de la Persona
    # -----------------------
    cedula = forms.CharField(
        max_length=10, 
        label="Cédula", 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'minlength': '10', 
            'maxlength': '10',
            'title': 'La cédula debe tener 10 dígitos numéricos',
            'inputmode': 'numeric'
        })
    )
    primernombre = forms.CharField(max_length=50, label="Primer Nombre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    segundonombre = forms.CharField(max_length=50, required=False, label="Segundo Nombre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    primerapellido = forms.CharField(max_length=50, label="Primer Apellido", widget=forms.TextInput(attrs={'class': 'form-control'}))
    segundoapellido = forms.CharField(max_length=50, label="Segundo Apellido", widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    fechanacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    genero = forms.ChoiceField(
        choices=OPCIONES_GENERO, 
        label="Género",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    telefono = forms.CharField(
        max_length=10, 
        required=False, 
        label="Teléfono", 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'minlength': '10',
            'maxlength': '10',
            'inputmode': 'numeric'
        })
    )

    # -----------------------
    # B) Dirección
    # -----------------------
    direccion = forms.CharField(
        max_length=200, 
        label="Dirección", 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calle Principal y Secundaria, Sector'
        })
    )

    # -----------------------
    # C) Catequizando
    # -----------------------
    lugar_nacimiento = forms.CharField(
        max_length=150, 
        label="Lugar de Nacimiento", 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ciudad, País'
        })
    )
    numerohijo = forms.IntegerField(label="Número de Hijo", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    numerohermanos = forms.IntegerField(label="Número de Hermanos", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    escuelacolegio = forms.CharField(
        max_length=150, 
        required=False, 
        label="Institución Educativa",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    anioencurso = forms.ChoiceField(
        choices=OPCIONES_ANIO, 
        required=False, 
        label="Año en Curso",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tiposangre = forms.ChoiceField(
        choices=OPCIONES_SANGRE,
        label="Tipo de Sangre",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    contacto_emergencia = forms.CharField(
        max_length=100, 
        required=False, 
        label="Contacto de Emergencia",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre y Teléfono'})
    )
    
    alergia = forms.CharField(max_length=50, required=False, label="Alergia", widget=forms.TextInput(attrs={'class': 'form-control'}))
    comentario = forms.CharField(
        max_length=100, 
        required=False, 
        label="Comentario",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    # -----------------------
    # D) Datos Familiares (Simplificados)
    # -----------------------
    nombrespadre = forms.CharField(
        max_length=100, 
        label="Nombres Padre", 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    apellidospadre = forms.CharField(
        max_length=100, 
        required=False, 
        label="Apellidos Padre", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    telefonopadre = forms.CharField(
        max_length=10, 
        required=False, 
        label="Teléfono Padre", 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'minlength': '10',
            'maxlength': '10',
            'inputmode': 'numeric'
        })
    )
    correopadre = forms.EmailField(max_length=50, required=False, label="Correo Padre", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    ocupacionpadre = forms.CharField(max_length=100, required=False, label="Ocupación Padre", widget=forms.TextInput(attrs={'class': 'form-control'}))

    cedulamadre = forms.CharField(
        max_length=10, 
        required=False, 
        label="Cédula de la Madre", 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'minlength': '10',
            'maxlength': '10',
            'inputmode': 'numeric'
        })
    )
    nombresmadre = forms.CharField(
        max_length=100, 
        required=False, 
        label="Nombres Madre", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    apellidosmadre = forms.CharField(
        max_length=100, 
        required=False, 
        label="Apellidos Madre", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    telefonomadre = forms.CharField(
        max_length=10, 
        required=False, 
        label="Teléfono Madre", 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'minlength': '10',
            'maxlength': '10',
            'inputmode': 'numeric'
        })
    )
    correomadre = forms.EmailField(max_length=50, required=False, label="Correo Madre", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    ocupacionmadre = forms.CharField(max_length=100, required=False, label="Ocupación Madre", widget=forms.TextInput(attrs={'class': 'form-control'}))

    # -----------------------
    # E) Fe de Bautismo
    # -----------------------
    ciudadbautismo = forms.CharField(
        label="Ciudad de Bautismo",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    parroquiabautismoid = forms.CharField(
        label="Parroquia de Bautismo",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fechabautismo = forms.DateField(
        label="Fecha Bautismo",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    numerotomo = forms.IntegerField(
        label="Número de Tomo", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    paginatomo = forms.IntegerField(
        label="Página Tomo", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    sacerdotebautismo = forms.CharField(
        label="Sacerdote",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    padrinobautismo = forms.CharField(
        label="Padrino",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    madrinabautismo = forms.CharField(
        label="Madrina",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # -----------------------
    # Validaciones personalizadas
    # -----------------------
    def _validate_digits(self, value, field_name):
        if value:
            # Eliminar espacios por si acaso
            value = value.strip()
            if not value.isdigit():
                raise forms.ValidationError(f"{field_name} debe contener solo números.")
            if len(value) != 10:
                raise forms.ValidationError(f"{field_name} debe tener 10 dígitos. Valor actual: {len(value)}")
        return value

    def clean_cedula(self):
        return self._validate_digits(self.cleaned_data.get('cedula'), "La cédula")

    def clean_telefono(self):
        return self._validate_digits(self.cleaned_data.get('telefono'), "El teléfono")

    def clean_telefonomadre(self):
        return self._validate_digits(self.cleaned_data.get('telefonomadre'), "El teléfono de la madre")

# ==========================================
# 4. Formularios para GRUPOS
# ==========================================

class GrupoForm(forms.Form):
    nivelcatequesis = forms.ModelChoiceField(
        queryset=Nivel.objects.all(),
        label="Nivel",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ciclo = forms.ModelChoiceField(
        queryset=Ciclo.objects.all().order_by('-fecha_inicio'),
        label="Ciclo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    nombregrupo = forms.CharField(
        max_length=50,
        label="Nombre del Grupo",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    catequista_nombre = forms.CharField(
        max_length=100,
        label="Catequista Titular",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Completo'})
    )
    estado = forms.ChoiceField(
        choices=ESTADO_GRUPO,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class GrupoUpdateForm(forms.Form):
    nombregrupo = forms.CharField(
        max_length=50, 
        label="Nombre del Grupo", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    catequista_nombre = forms.CharField(
        max_length=100,
        label="Catequista Titular",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    estado = forms.ChoiceField(
        choices=ESTADO_GRUPO,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

# ==========================================
# 5. Formularios para INSCRIPCIONES
# ==========================================

class InscripcionCreateForm(forms.Form):
    catequizando = forms.ModelChoiceField(
        queryset=Catequizando.objects.all(),
        label="Catequizando",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.filter(estado='ACTIVO'), # Changed to 'ACTIVO' matching model
        label="Grupo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    estadopago = forms.ChoiceField(
        choices=ESTADO_PAGO,
        label="Estado de Pago",
        initial='PAGADO', # Changed to match model choice
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    # esexcepcion: Not present in new schema, but keeping in form for now in case logic uses it, 
    # but we will likely ignore it in saving.
    esexcepcion = forms.BooleanField(
        required=False,
        label="Es Excepción",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class InscripcionUpdateForm(forms.Form):
    estadoinscripcion = forms.ChoiceField(
        choices=ESTADO_INSCRIPCION,
        label="Estado de la Inscripcion",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    estadopago = forms.ChoiceField(
        choices=ESTADO_PAGO,
        label="Estado del Pago",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    esexcepcion = forms.BooleanField(
        required=False,
        label="Es Excepción",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class AsistenciaForm(forms.Form):
    sesion_id = forms.IntegerField(
        label="Número de Sesión",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    estado = forms.ChoiceField(
        choices=ESTADO_ASISTENCIA,
        label="Estado",
        initial='PRESENTE',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class CalificacionForm(forms.Form):
    descripcion = forms.CharField(
        label="Descripción",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Examen Parcial 1'})
    )
    valor = forms.FloatField(
        label="Nota",
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )

class SesionForm(forms.Form):
    sesion_id = forms.IntegerField(
        label="Número de Sesión",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )
    tema = forms.CharField(
        label="Tema de la Sesión",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha = forms.DateField(
        label="Fecha Programada",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

# ==========================================
# 6. Formularios para CICLOS
# ==========================================

class CicloForm(forms.Form):
    nombreciclo = forms.CharField(
        max_length=100,
        label="Nombre del Ciclo",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fechainicio = forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fechafin = forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    estado = forms.ChoiceField(
        choices=ESTADO_GENERAL,
        label="Estado",
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class CicloUpdateForm(forms.Form):
    nombreciclo = forms.CharField(
        max_length=100,
        label="Nombre del Ciclo",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fechainicio = forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fechafin = forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    estado = forms.ChoiceField(
        choices=ESTADO_GENERAL,
        label="Estado",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
