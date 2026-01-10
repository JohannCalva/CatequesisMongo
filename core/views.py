from django.shortcuts import render, redirect
from django.views.generic import DetailView, FormView
from django.urls import reverse
from django.db import connection
from django.views import View
from .models import Catequizando, Grupo, Inscripcion, NivelCatequesis, CicloCatequesis
from .forms import (
    CatequizandoUpdateMiniForm, 
    CatequizandoSPForm, 
    GrupoForm, 
    GrupoUpdateForm, 
    InscripcionCreateForm, 
    InscripcionUpdateForm
)


def home(request):
    return render(request, "home.html")

def catequizando_listar(request):
    with connection.cursor() as cursor:
        cursor.execute("EXEC Participante.sp_ListarCatequizandos")

        if cursor.description is None:
            catequizandos = []
        else:
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            catequizandos = [
                dict(zip(columns, row))
                for row in rows
            ]

    return render(request, "catequizandos/listar.html", {"catequizandos": catequizandos})


class CatequizandoDetailView(DetailView):
    model = Catequizando
    template_name = "catequizandos/detalle.html"
    context_object_name = "catequizando"


class CatequizandoUpdateView(View):
    template_name = "catequizandos/editar.html"
    form_class = CatequizandoUpdateMiniForm

    def get(self, request, pk):
        cateq = Catequizando.objects.get(personaid_id=pk)

        form = self.form_class(initial={
            "telefono": cateq.personaid.telefono,
            "correo": cateq.personaid.correo,
            "estado": cateq.estado,
            "anioencurso": cateq.anioencurso,
            "tiposangre": cateq.tiposangre,
            "alergia": cateq.alergia,
            "comentario": cateq.comentario,
        })

        return render(request, self.template_name, {"form": form, "pk": pk})

    def post(self, request, pk):
        form = self.form_class(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            with connection.cursor() as cursor:
                cursor.execute("""
                    EXEC Participante.sp_ActualizarCatequizandoBasico
                        @PersonaID=%s,
                        @Correo=%s,
                        @Telefono=%s,
                        @Estado=%s,
                        @AnioEnCurso=%s,
                        @TipoSangre=%s,
                        @Alergia=%s,
                        @Comentario=%s
                """, [
                    pk,
                    data["correo"],
                    data["telefono"],
                    data["estado"],
                    data["anioencurso"],
                    data["tiposangre"],
                    data["alergia"],
                    data["comentario"],
                ])

            return redirect("catequizando_detalle", pk=pk)

        return render(request, self.template_name, {"form": form, "pk": pk})


class CatequizandoCreateView(FormView):
    template_name = "catequizandos/crear.html"
    form_class = CatequizandoSPForm

    def form_valid(self, form):
        data = form.cleaned_data

        # --- CORRECCIÓN DE FECHAS ---
        # 1. Catequizando: Es obligatorio en el form, solo convertimos a string.
        fecha_nacimiento_str = str(data["fechanacimiento"])

        # 2. Padre: Si viene vacío o None, enviamos '1900-01-01' para evitar error de SQL (NOT NULL).
        if data.get("fnacimientopadre"):
            f_padre = str(data["fnacimientopadre"])
        else:
            f_padre = '1900-01-01'

        # 3. Madre: Misma lógica de protección.
        if data.get("fnacimientomadre"):
            f_madre = str(data["fnacimientomadre"])
        else:
            f_madre = '1900-01-01'
        
        # 4. Fe de Bautismo: Handling Nulls
        parroquia_bautismo = data.get("parroquiabautismoid")
        parroquia_bautismo_id = parroquia_bautismo.pk if parroquia_bautismo else None
        
        fecha_bautismo = data.get("fechabautismo")
        fecha_bautismo_str = str(fecha_bautismo) if fecha_bautismo else None

        # ----------------------------

        with connection.cursor() as cursor:
            values = [
                data["cedula"],
                data["primernombre"],
                data["segundonombre"], 
                data["primerapellido"],
                data["segundoapellido"],
                fecha_nacimiento_str,
                data["genero"],
                data["telefono"],
                data["correo"],
                data["calleprincipal"],
                data["callesecundaria"],
                data["sector"],
                data["parroquiaid"].pk, 
                data["paisnacimiento"],
                data["ciudadnacimiento"],
                data["numerohijo"],
                data["numerohermanos"],
                data["estado"],
                data["anioencurso"],
                data["tiposangre"],
                data["alergia"],
                data["comentario"],
                data["cedulapadre"],
                data["pnombrepadre"],
                data["snombrepadre"],
                data["papellidopadre"],
                data["sapellidopadre"],
                f_padre,
                data["telefonopadre"],
                data["correopadre"],
                data["ocupacionpadre"],
                data["cedulamadre"],
                data["pnombremadre"],
                data["snombremadre"],
                data["papellidomadre"],
                data["sapellidomadre"],
                f_madre,
                data["telefonomadre"],
                data["correomadre"],
                data["ocupacionmadre"],
                # Nuevos parametros Fe de Bautismo
                parroquia_bautismo_id,
                fecha_bautismo_str,
                data.get("numerotomo"),
                data.get("paginatomo")
            ]

            cursor.execute("""
                EXEC Participante.sp_InsertarCatequizando
                    @Cedula=%s,
                    @PrimerNombre=%s,
                    @SegundoNombre=%s,
                    @PrimerApellido=%s,
                    @SegundoApellido=%s,
                    @FechaNacimiento=%s,
                    @Genero=%s,
                    @Telefono=%s,
                    @Correo=%s,
                    @CallePrincipal=%s,
                    @CalleSecundaria=%s,
                    @Sector=%s,
                    @ParroquiaID=%s,
                    @PaisNacimiento=%s,
                    @CiudadNacimiento=%s,
                    @NumeroHijo=%s,
                    @NumeroHermanos=%s,
                    @Estado=%s,
                    @AnioEnCurso=%s,
                    @TipoSangre=%s,
                    @Alergia=%s,
                    @Comentario=%s,
                    @CedulaPadre=%s,
                    @PNombrePadre=%s,
                    @SNombrePadre=%s,
                    @PApellidoPadre=%s,
                    @SApellidoPadre=%s,
                    @FNacimientoPadre=%s,
                    @TelefonoPadre=%s,
                    @CorreoPadre=%s,
                    @OcupacionPadre=%s,
                    @CedulaMadre=%s,
                    @PNombreMadre=%s,
                    @SNombreMadre=%s,
                    @PApellidoMadre=%s,
                    @SApellidoMadre=%s,
                    @FNacimientoMadre=%s,
                    @TelefonoMadre=%s,
                    @CorreoMadre=%s,
                    @OcupacionMadre=%s,
                    @ParroquiaBautismoID=%s,
                    @FechaBautismo=%s,
                    @NumeroTomo=%s,
                    @PaginaTomo=%s
            """, values)

        return redirect("catequizando_listar")


def catequizando_eliminar(request, persona_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            EXEC Participante.sp_EliminarCatequizando @PersonaID=%s
        """, [persona_id])

    return redirect("catequizando_listar")

def catequizando_buscar(request):
    cedula = request.GET.get("cedula") or None
    apellido = request.GET.get("apellido") or None
    estado = request.GET.get("estado") or None

    with connection.cursor() as cursor:
        cursor.execute("""
            EXEC Participante.sp_BuscarCatequizandos
                @Cedula=%s,
                @PrimerApellido=%s,
                @Estado=%s
        """, [cedula, apellido, estado])

        if cursor.description is None:
            catequizandos = []
        else:
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            catequizandos = [dict(zip(columns, row)) for row in rows]

    return render(request, "catequizandos/listar.html", {
        "catequizandos": catequizandos,
        "filtro_cedula": request.GET.get("cedula", ""),
        "filtro_apellido": request.GET.get("apellido", ""),
        "filtro_estado": request.GET.get("estado", ""),
    })

# ==========================================
# VISTAS GRUPOS (CRUD con SP)
# ==========================================

# ==========================================
# VISTAS GRUPOS (CRUD con SP)
# ==========================================

# grupo_listar se ha fusionado con la logica de busqueda abajo

class GrupoCreateView(FormView):
    template_name = "grupos/crear.html"
    form_class = GrupoForm

    def form_valid(self, form):
        data = form.cleaned_data
        with connection.cursor() as cursor:
            cursor.execute("""
                EXEC Catequesis.sp_InsertarGrupo
                    @NivelCatequesisID=%s,
                    @CicloID=%s,
                    @NombreGrupo=%s,
                    @Estado=%s
            """, [
                data['nivelcatequesis'].pk,
                data['ciclo'].pk,
                data['nombregrupo'],
                data['estado']
            ])
        return redirect('grupo_listar')

class GrupoDetailView(DetailView):
    model = Grupo
    template_name = "grupos/detalle.html"
    context_object_name = "grupo"

class GrupoUpdateView(View):
    template_name = "grupos/editar.html"
    form_class = GrupoUpdateForm

    def get(self, request, pk):
        # Intentamos obtener el grupo via ORM para llenar el form
        # O podríamos usar el SP de BuscarGrupo filtrando por nombre/id si tuvieramos uno específico de ID
        grupo = Grupo.objects.get(pk=pk)
        form = self.form_class(initial={
            'nombregrupo': grupo.nombregrupo,
            'estado': grupo.estado
        })
        return render(request, self.template_name, {'form': form, 'grupo': grupo})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("""
                    EXEC Catequesis.sp_ActualizarGrupo
                        @GrupoID=%s,
                        @NombreGrupo=%s,
                        @Estado=%s
                """, [pk, data['nombregrupo'], data['estado']])
            return redirect('grupo_detail', pk=pk)
        return render(request, self.template_name, {'form': form, 'pk': pk})

def grupo_eliminar(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("EXEC Catequesis.sp_EliminarGrupo @GrupoID=%s", [pk])
    return redirect('grupo_listar')


def grupo_listar(request):
    with connection.cursor() as cursor:
        cursor.execute("EXEC Catequesis.sp_ListarGrupos")

        if cursor.description is None:
            grupos = []
        else:
            columns = [col[0] for col in cursor.description]
            grupos = [dict(zip(columns, row)) for row in cursor.fetchall()]

    niveles = NivelCatequesis.objects.all()
    ciclos = CicloCatequesis.objects.all().order_by('-fechainicio')

    return render(request, "grupos/listar.html", {
        "grupos": grupos,
        "niveles": niveles,
        "ciclos": ciclos,
        "filtro_nombre": "",
        "filtro_nivel": "",
        "filtro_ciclo": "",
    })


def grupo_buscar(request):
    nombre = request.GET.get('nombre', '')
    nivel_id = request.GET.get('nivel_id') or None
    ciclo_id = request.GET.get('ciclo_id') or None

    with connection.cursor() as cursor:
        cursor.execute("""
            EXEC Catequesis.sp_BuscarGrupo 
                @NombreGrupo=%s, 
                @NivelID=%s, 
                @CicloID=%s
        """, [nombre if nombre else None, nivel_id, ciclo_id])
        
        if cursor.description is None:
            grupos = []
        else:
            columns = [col[0] for col in cursor.description]
            grupos = [dict(zip(columns, row)) for row in cursor.fetchall()]

    niveles = NivelCatequesis.objects.all()
    ciclos = CicloCatequesis.objects.all().order_by('-fechainicio')

    return render(request, "grupos/listar.html", {
        "grupos": grupos,
        "niveles": niveles,
        "ciclos": ciclos,
        "filtro_nombre": nombre,
        "filtro_nivel": int(nivel_id) if nivel_id else "",
        "filtro_ciclo": int(ciclo_id) if ciclo_id else ""
    })

# ==========================================
# VISTAS INSCRIPCIONES (CRUD con SP)
# ==========================================

def inscripcion_listar(request):
    with connection.cursor() as cursor:
        cursor.execute("EXEC Participante.sp_ListarInscripciones")

        if cursor.description is None:
            inscripciones = []
        else:
            columns = [col[0] for col in cursor.description]
            inscripciones = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, "inscripciones/listar.html", {
        "inscripciones": inscripciones,
        "grupos": Grupo.objects.all(),
        "filtro_cedula": "",
        "filtro_grupo_id": ""
    })


def inscripcion_buscar(request):
    cedula = request.GET.get('cedula') or None
    grupo_id = request.GET.get('grupo_id') or None

    inscripciones = []

    with connection.cursor() as cursor:
        cursor.execute("""
            EXEC Participante.sp_BuscarInscripciones
                @Cedula=%s,
                @GrupoID=%s
        """, [cedula, grupo_id])

        if cursor.description:
            columns = [col[0] for col in cursor.description]
            inscripciones = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, "inscripciones/listar.html", {
        "inscripciones": inscripciones,
        "grupos": Grupo.objects.all(),
        "filtro_cedula": cedula or "",
        "filtro_grupo_id": int(grupo_id) if grupo_id else ""
    })


class InscripcionCreateView(FormView):
    template_name = "inscripciones/crear.html"
    form_class = InscripcionCreateForm

    def form_valid(self, form):
        data = form.cleaned_data
        with connection.cursor() as cursor:
            # Note: The SP might raise an error if already enrolled.
            # We should probably handle try/catch or assume SP handles it gracefully (based on SP definition provided).
            # The SP has PRINT '...' which Django might not capture easily as error without raising exception.
            # However, PyODBC/Django usually doesn't raise exception for PRINTs.
            # We rely on SP validation logic.
            
            cursor.execute("""
                EXEC Participante.sp_InsertarInscripcion
                    @CatequizandoID=%s,
                    @GrupoID=%s,
                    @EstadoPago=%s,
                    @EsExcepcion=%s
            """, [
                data['catequizando'].pk,
                data['grupo'].pk,
                data['estadopago'],
                data['esexcepcion']
            ])
        return redirect('inscripcion_listar')

class InscripcionDetailView(DetailView):
    # This is tricky because it has a composite PK.
    # We can't easily use standard DetailView.get_object.
    # We will override get_object to fetch by (catequizando_id, grupo_id).
    model = Inscripcion
    template_name = "inscripciones/detalle.html"
    context_object_name = "inscripcion"

    def get_object(self, queryset=None):
        c_id = self.kwargs.get('catequizando_id')
        g_id = self.kwargs.get('grupo_id')
        return Inscripcion.objects.get(catequizando_personaid=c_id, grupo=g_id)

class InscripcionUpdateView(View):
    template_name = "inscripciones/editar.html"
    form_class = InscripcionUpdateForm

    def get(self, request, catequizando_id, grupo_id):
        inscripcion = Inscripcion.objects.get(catequizando_personaid=catequizando_id, grupo=grupo_id)
        form = self.form_class(initial={
            'estadoinscripcion': inscripcion.estadoinscripcion,
            'estadopago': inscripcion.estadopago,
            'esexcepcion': inscripcion.esexcepcion
        })
        return render(request, self.template_name, {
            'form': form, 
            'catequizando_id': catequizando_id, 
            'grupo_id': grupo_id,
            'item': inscripcion # To show details like name in template
        })

    def post(self, request, catequizando_id, grupo_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("""
                    EXEC Participante.sp_ActualizarInscripcion
                        @CatequizandoID=%s,
                        @GrupoID=%s,
                        @EstadoInscripcion=%s,
                        @EstadoPago=%s,
                        @EsExcepcion=%s
                """, [
                    catequizando_id, 
                    grupo_id, 
                    data['estadoinscripcion'], 
                    data['estadopago'], 
                    data['esexcepcion']
                ])
            return redirect('inscripcion_detail', catequizando_id=catequizando_id, grupo_id=grupo_id)
        return render(request, self.template_name, {'form': form, 'catequizando_id': catequizando_id, 'grupo_id': grupo_id})

def inscripcion_eliminar(request, catequizando_id, grupo_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            EXEC Participante.sp_EliminarInscripcion 
                @CatequizandoID=%s, 
                @GrupoID=%s
        """, [catequizando_id, grupo_id])
    return redirect('inscripcion_listar')




# ==========================================
# VISTAS CICLOS (CRUD con SP)
# ==========================================

from .forms import CicloForm, CicloUpdateForm

def ciclo_listar(request):
    with connection.cursor() as cursor:
        cursor.execute("EXEC Catequesis.sp_ListarCiclos")
        if cursor.description is None:
            ciclos = []
        else:
            columns = [col[0] for col in cursor.description]
            ciclos = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return render(request, "ciclos/listar.html", {"ciclos": ciclos})

class CicloDetailView(DetailView):
    model = CicloCatequesis
    template_name = "ciclos/detalle.html"
    context_object_name = "ciclo"

class CicloCreateView(FormView):
    template_name = "ciclos/crear.html"
    form_class = CicloForm

    def form_valid(self, form):
        data = form.cleaned_data
        with connection.cursor() as cursor:
            cursor.execute("""
                EXEC Catequesis.sp_InsertarCiclo
                    @NombreCiclo=%s,
                    @FechaInicio=%s,
                    @FechaFin=%s,
                    @Estado=%s
            """, [
                data['nombreciclo'],
                str(data['fechainicio']),
                str(data['fechafin']),
                data['estado']
            ])
        return redirect('ciclo_listar')

class CicloUpdateView(View):
    template_name = "ciclos/editar.html"
    form_class = CicloUpdateForm

    def get(self, request, pk):
        try:
            ciclo = CicloCatequesis.objects.get(pk=pk)
            form = self.form_class(initial={
                'nombreciclo': ciclo.nombreciclo,
                'fechainicio': ciclo.fechainicio,
                'fechafin': ciclo.fechafin,
                'estado': ciclo.estado
            })
            return render(request, self.template_name, {'form': form, 'ciclo': ciclo})
        except CicloCatequesis.DoesNotExist:
             return redirect('ciclo_listar')

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("""
                    EXEC Catequesis.sp_ActualizarCiclo
                        @CicloID=%s,
                        @NombreCiclo=%s,
                        @FechaInicio=%s,
                        @FechaFin=%s,
                        @Estado=%s
                """, [
                    pk,
                    data['nombreciclo'],
                    str(data['fechainicio']),
                    str(data['fechafin']),
                    data['estado']
                ])
            return redirect('ciclo_listar')
        return render(request, self.template_name, {'form': form, 'pk': pk})

def ciclo_eliminar(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("EXEC Catequesis.sp_EliminarCiclo @CicloID=%s", [pk])
    return redirect('ciclo_listar')
