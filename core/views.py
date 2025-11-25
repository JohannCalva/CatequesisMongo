from django.shortcuts import render, redirect
from django.views.generic import DetailView, FormView
from django.urls import reverse
from django.db import connection
from django.views import View
from .models import Catequizando
from .forms import CatequizandoUpdateMiniForm, CatequizandoSPForm


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
        # ----------------------------

        with connection.cursor() as cursor:
            values = [
                data["cedula"],
                data["primernombre"],
                data["segundonombre"], 
                data["primerapellido"],
                data["segundoapellido"],
                fecha_nacimiento_str,       # <--- Usamos la variable convertida
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
                f_padre,                    # <--- Usamos la variable protegida padre
                data["telefonopadre"],
                data["correopadre"],
                data["ocupacionpadre"],
                data["cedulamadre"],
                data["pnombremadre"],
                data["snombremadre"],
                data["papellidomadre"],
                data["sapellidomadre"],
                f_madre,                    # <--- Usamos la variable protegida madre
                data["telefonomadre"],
                data["correomadre"],
                data["ocupacionmadre"]
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
                    @OcupacionMadre=%s
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