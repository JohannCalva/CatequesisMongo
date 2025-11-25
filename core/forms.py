from django import forms
from .models import Catequizando, Parroquia

OPCIONES_ESTADO = [
    ('Activo', 'Activo'),
    ('Inactivo', 'Inactivo'),
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
    correo = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )
    
    estado = forms.ChoiceField(
        choices=OPCIONES_ESTADO,
        widget=forms.Select(attrs={'class': 'form-select'})
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
    cedula = forms.CharField(max_length=10, label="Cédula", widget=forms.TextInput(attrs={'class': 'form-control', 
            'minlength': '10', 
            'maxlength': '10',
            'title': 'La cédula debe tener 10 dígitos numéricos',
            'inputmode': 'numeric'}))
    primernombre = forms.CharField(max_length=50, label="Primer Nombre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    segundonombre = forms.CharField(max_length=50, required=False, label="Segundo Nombre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    primerapellido = forms.CharField(max_length=50, label="Primer Apellido", widget=forms.TextInput(attrs={'class': 'form-control'}))
    segundoapellido = forms.CharField(max_length=50, label="Segundo Apellido", widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    fechanacimiento = forms.DateField(
        label="Fecha Nacimiento Padre", 
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    genero = forms.ChoiceField(
        choices=OPCIONES_GENERO, 
        label="Género",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    telefono = forms.CharField(max_length=10, required=False, label="Teléfono", widget=forms.TextInput(attrs={'class': 'form-control',
            'minlength': '10',
            'maxlength': '10',
            'inputmode': 'numeric'}))
    correo = forms.EmailField(max_length=50, required=False, label="Correo", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    # -----------------------
    # B) Dirección
    # -----------------------
    calleprincipal = forms.CharField(max_length=50, label="Calle Principal", widget=forms.TextInput(attrs={'class': 'form-control'}))
    callesecundaria = forms.CharField(max_length=50, label="Calle Secundaria", widget=forms.TextInput(attrs={'class': 'form-control'}))
    sector = forms.CharField(max_length=50, label="Sector", widget=forms.TextInput(attrs={'class': 'form-control'}))

    # -----------------------
    # C) Catequizando (AQUÍ ESTÁN LOS CAMBIOS PRINCIPALES)
    # -----------------------
    parroquiaid = forms.ModelChoiceField(
        queryset=Parroquia.objects.all(),
        label="Parroquia",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    paisnacimiento = forms.CharField(max_length=25, label="País de Nacimiento", widget=forms.TextInput(attrs={'class': 'form-control'}))
    ciudadnacimiento = forms.CharField(max_length=50, label="Ciudad de Nacimiento", widget=forms.TextInput(attrs={'class': 'form-control'}))
    numerohijo = forms.IntegerField(label="Número de Hijo", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    numerohermanos = forms.IntegerField(label="Número de Hermanos", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    # CAMBIO: Estado ahora es Select
    estado = forms.ChoiceField(
        choices=OPCIONES_ESTADO, 
        label="Estado",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # CAMBIO: Año ahora es Select
    anioencurso = forms.ChoiceField(
        choices=OPCIONES_ANIO, 
        required=False, 
        label="Año en Curso",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # CAMBIO: Tipo Sangre ahora es Select
    tiposangre = forms.ChoiceField(
        choices=OPCIONES_SANGRE,
        label="Tipo de Sangre",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    alergia = forms.CharField(max_length=50, required=False, label="Alergia", widget=forms.TextInput(attrs={'class': 'form-control'}))
    comentario = forms.CharField(
        max_length=100, 
        required=False, 
        label="Comentario",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    
    cedulapadre = forms.CharField(max_length=10, required=False, label="Cédula del Padre", widget=forms.TextInput(attrs={'class': 'form-control',
            'minlength': '10',
            'maxlength': '10',
            'inputmode': 'numeric'}))
    pnombrepadre = forms.CharField(max_length=50, label="Primer Nombre Padre", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    snombrepadre = forms.CharField(max_length=50, required=False, label="Segundo Nombre Padre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    papellidopadre = forms.CharField(max_length=50, required=False, label="Primer Apellido Padre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    sapellidopadre = forms.CharField(max_length=50, required=False, label="Segundo Apellido Padre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    fnacimientopadre = forms.DateField(
        label="Fecha Nacimiento Padre", 
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    telefonopadre = forms.CharField(max_length=10, required=False, label="Teléfono Padre", widget=forms.TextInput(attrs={'class': 'form-control',
            'minlength': '10',
            'maxlength': '10',
            'inputmode': 'numeric'}))
    correopadre = forms.EmailField(max_length=50, required=False, label="Correo Padre", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    ocupacionpadre = forms.CharField(max_length=100, required=False, label="Ocupación Padre", widget=forms.TextInput(attrs={'class': 'form-control'}))

    cedulamadre = forms.CharField(max_length=10, required=False, label="Cédula de la Madre", widget=forms.TextInput(attrs={'class': 'form-control',
            'minlength': '10',
            'maxlength': '10',
            'inputmode': 'numeric'}))
    pnombremadre = forms.CharField(max_length=50, required=False, label="Primer Nombre Madre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    snombremadre = forms.CharField(max_length=50, required=False, label="Segundo Nombre Madre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    papellidomadre = forms.CharField(max_length=50, required=False, label="Primer Apellido Madre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    sapellidomadre = forms.CharField(max_length=50, required=False, label="Segundo Apellido Madre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    fnacimientomadre = forms.DateField(
        label="Fecha Nacimiento Madre",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    telefonomadre = forms.CharField(max_length=10, required=False, label="Teléfono Madre", widget=forms.TextInput(attrs={'class': 'form-control',
            'minlength': '10',
            'maxlength': '10',
            'inputmode': 'numeric'}))
    correomadre = forms.EmailField(max_length=50, required=False, label="Correo Madre", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    ocupacionmadre = forms.CharField(max_length=100, required=False, label="Ocupación Madre", widget=forms.TextInput(attrs={'class': 'form-control'}))