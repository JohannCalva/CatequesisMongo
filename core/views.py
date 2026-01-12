from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, FormView
from django.urls import reverse
from django.views import View
from django.db import connection 
from .models import Catequizando, Grupo, Inscripcion, Nivel, Ciclo
from .forms import (
    CatequizandoUpdateMiniForm, 
    CatequizandoSPForm, 
    GrupoForm, 
    GrupoUpdateForm, 
    InscripcionCreateForm, 
    InscripcionUpdateForm,
    CicloForm,
    CicloUpdateForm,
    AsistenciaForm,
    CalificacionForm
)

def home(request):
    return render(request, "home.html")

# ==========================================
# CATEQUIZANDOS
# ==========================================

def catequizando_listar(request):
    catequizandos = Catequizando.objects.all()
    return render(request, "catequizandos/listar.html", {"catequizandos": catequizandos})


class CatequizandoDetailView(DetailView):
    model = Catequizando
    template_name = "catequizandos/detalle.html"
    context_object_name = "catequizando"


class CatequizandoUpdateView(View):
    template_name = "catequizandos/editar.html"
    form_class = CatequizandoUpdateMiniForm

    def get(self, request, pk):
        cateq = get_object_or_404(Catequizando, pk=pk)

        form = self.form_class(initial={
            "telefono": cateq.telefono_casa,
            "estado": "ACTIVO", 
            "anioencurso": cateq.escolaridad.get('anio_en_curso', '') if cateq.escolaridad else '',
            "tiposangre": cateq.informacion_salud.get('tipo_sangre', '') if cateq.informacion_salud else '',
            "alergia": ", ".join(cateq.informacion_salud.get('alergias', [])) if cateq.informacion_salud else '',
            "comentario": cateq.observaciones_generales,
        })

        return render(request, self.template_name, {"form": form, "pk": pk})

    def post(self, request, pk):
        form = self.form_class(request.POST) 
        if form.is_valid():
            cateq = get_object_or_404(Catequizando, pk=pk)
            data = form.cleaned_data

            cateq.telefono_casa = data["telefono"]
            cateq.observaciones_generales = data["comentario"]
            
            if not cateq.escolaridad: cateq.escolaridad = {}
            cateq.escolaridad['anio_en_curso'] = data['anioencurso']
            
            if not cateq.informacion_salud: cateq.informacion_salud = {}
            cateq.informacion_salud['tipo_sangre'] = data['tiposangre']
            cateq.informacion_salud['alergias'] = [data['alergia']] if data['alergia'] else []

            cateq.save()
            return redirect("catequizando_detalle", pk=pk)

        return render(request, self.template_name, {"form": form, "pk": pk})


class CatequizandoCreateView(FormView):
    template_name = "catequizandos/crear.html"
    form_class = CatequizandoSPForm

    def form_valid(self, form):
        data = form.cleaned_data

        padres = []
        if data.get('cedulapadre') or data.get('pnombrepadre'):
            padre = {
                "relacion": "PADRE",
                "nombres": f"{data.get('pnombrepadre', '')} {data.get('snombrepadre', '')}".strip(),
                "apellidos": f"{data.get('papellidopadre', '')} {data.get('sapellidopadre', '')}".strip(),
                "telefono": data.get('telefonopadre', ''),
                "ocupacion": data.get('ocupacionpadre', '')
            }
            padres.append(padre)
        
        if data.get('cedulamadre') or data.get('pnombremadre'):
            madre = {
                "relacion": "MADRE",
                "nombres": f"{data.get('pnombremadre', '')} {data.get('snombremadre', '')}".strip(),
                "apellidos": f"{data.get('papellidomadre', '')} {data.get('sapellidomadre', '')}".strip(),
                "telefono": data.get('telefonomadre', ''),
                "ocupacion": data.get('ocupacionmadre', '')
            }
            padres.append(madre)

        rep_legal = {}
        if padres:
            p = padres[0] 
            rep_legal = {
                "es_uno_de_los_padres": True,
                "nombres": p['nombres'],
                "apellidos": p['apellidos'],
                "telefono": p['telefono'],
                "correo": data.get('correopadre') if p['relacion'] == 'PADRE' else data.get('correomadre', '')
            }
        else:
             rep_legal = {
                "es_uno_de_los_padres": False,
                "nombres": "Desconocido",
                "apellidos": "Desconocido",
                "telefono": "",
                "correo": ""
             }

        fe_bautismo = {
            "fecha": str(data.get('fechabautismo')) if data.get('fechabautismo') else None,
            "parroquia": data.get('parroquiabautismoid', ''),
            "ciudad": "", 
            "tomo": data.get('numerotomo'),
            "pagina": data.get('paginatomo'),
            "sacerdote": "",
            "padrino": "",
            "madrina": ""
        }

        info_salud = {
            "tipo_sangre": data.get('tiposangre'),
            "contacto_emergencia": "", 
            "alergias": [data.get('alergia')] if data.get('alergia') else [],
            "aspectos_a_considerar": ""
        }

        escolaridad = {
            "escuela_colegio": "",
            "anio_en_curso": data.get('anioencurso')
        }

        Catequizando.objects.create(
            id=data['cedula'], 
            cedula=data['cedula'],
            primer_nombre=data['primernombre'],
            segundo_nombre=data['segundonombre'],
            primer_apellido=data['primerapellido'],
            segundo_apellido=data['segundoapellido'],
            genero=data['genero'],
            fecha_nacimiento=data['fechanacimiento'],
            lugar_nacimiento=f"{data['ciudadnacimiento']}, {data['paisnacimiento']}",
            numero_hijo=data['numerohijo'],
            numero_hermanos=data['numerohermanos'],
            telefono_casa=data['telefono'],
            direccion=f"{data['calleprincipal']} y {data['callesecundaria']}, {data['sector']}",
            
            padres=padres,
            representante_legal=rep_legal,
            informacion_salud=info_salud,
            fe_bautismo=fe_bautismo,
            escolaridad=escolaridad,
            observaciones_generales=data['comentario']
        )

        return redirect("catequizando_listar")


def catequizando_eliminar(request, persona_id):
    cateq = get_object_or_404(Catequizando, pk=persona_id)
    cateq.delete()
    return redirect("catequizando_listar")

def catequizando_buscar(request):
    cedula = request.GET.get("cedula")
    apellido = request.GET.get("apellido")

    qs = Catequizando.objects.all()
    if cedula:
        qs = qs.filter(cedula__icontains=cedula)
    if apellido:
        qs = qs.filter(primer_apellido__icontains=apellido)
    
    return render(request, "catequizandos/listar.html", {
        "catequizandos": qs,
        "filtro_cedula": cedula or "",
        "filtro_apellido": apellido or "",
    })

# ==========================================
# GRUPOS
# ==========================================

def grupo_listar(request):
    grupos = Grupo.objects.all()
    niveles = Nivel.objects.all()
    ciclos = Ciclo.objects.all().order_by('-fecha_inicio')
    
    return render(request, "grupos/listar.html", {
        "grupos": grupos,
        "niveles": niveles,
        "ciclos": ciclos,
    })

def grupo_buscar(request):
    nombre = request.GET.get('nombre')
    nivel_id = request.GET.get('nivel_id')
    ciclo_id = request.GET.get('ciclo_id')
    
    # Extra filters requested
    catequista = request.GET.get('catequista')

    qs = Grupo.objects.all()
    if nombre:
        qs = qs.filter(nombre_grupo__icontains=nombre)
    if nivel_id:
        qs = qs.filter(nivel__id=nivel_id)
    if ciclo_id:
        qs = qs.filter(ciclo__id=ciclo_id)
    
    # Filter by Catequista Name (partial match logic in Python for now if not supported directly in complex list lookup)
    # db.grupos.find({ "catequistas.nombre": ... })
    if catequista:
        # Fetching all matches for other filters first to minimize dataset
        # Then filtering in memory since 'catequistas' is a list of dicts.
        current_qs = list(qs)
        qs = [g for g in current_qs if any(c.get('nombre', '').lower().find(catequista.lower()) != -1 for c in g.catequistas)]

        
    niveles = Nivel.objects.all()
    ciclos = Ciclo.objects.all().order_by('-fecha_inicio')

    return render(request, "grupos/listar.html", {
        "grupos": qs,
        "niveles": niveles,
        "ciclos": ciclos,
        "filtro_nombre": nombre or "",
        "filtro_nivel": nivel_id or "",
        "filtro_ciclo": ciclo_id or "",
        "filtro_catequista": catequista or "" 
    })

class GrupoCreateView(FormView):
    template_name = "grupos/crear.html"
    form_class = GrupoForm

    def form_valid(self, form):
        data = form.cleaned_data
        import uuid
        new_id = str(uuid.uuid4())[:8] 

        Grupo.objects.create(
            id=new_id,
            nombre_grupo=data['nombregrupo'],
            ciclo=data['ciclo'],
            nivel=data['nivelcatequesis'], 
            estado=data['estado']
        )
        return redirect('grupo_listar')

class GrupoDetailView(DetailView):
    model = Grupo
    template_name = "grupos/detalle.html"
    context_object_name = "grupo"

class GrupoUpdateView(View):
    template_name = "grupos/editar.html"
    form_class = GrupoUpdateForm

    def get(self, request, pk):
        grupo = get_object_or_404(Grupo, pk=pk)
        form = self.form_class(initial={
            'nombregrupo': grupo.nombre_grupo,
            'estado': grupo.estado
        })
        return render(request, self.template_name, {'form': form, 'grupo': grupo})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            grupo = get_object_or_404(Grupo, pk=pk)
            data = form.cleaned_data
            grupo.nombre_grupo = data['nombregrupo']
            grupo.estado = data['estado']
            grupo.save()
            return redirect('grupo_detail', pk=pk)
        return render(request, self.template_name, {'form': form, 'pk': pk})

def grupo_eliminar(request, pk):
    grupo = get_object_or_404(Grupo, pk=pk)
    grupo.delete()
    return redirect('grupo_listar')


# ==========================================
# INSCRIPCIONES
# ==========================================

def inscripcion_listar(request):
    inscripciones = Inscripcion.objects.all()
    return render(request, "inscripciones/listar.html", {
        "inscripciones": inscripciones,
        "grupos": Grupo.objects.all()
    })

def inscripcion_buscar(request):
    cedula = request.GET.get('cedula')
    grupo_id = request.GET.get('grupo_id')
    estado_pago = request.GET.get('estado_pago')

    qs = Inscripcion.objects.all()
    if cedula:
        qs = qs.filter(catequizando__cedula__icontains=cedula)
    if grupo_id:
        qs = qs.filter(grupo__id=grupo_id)
    if estado_pago:
        qs = qs.filter(estado_pago=estado_pago)

    return render(request, "inscripciones/listar.html", {
        "inscripciones": qs,
        "grupos": Grupo.objects.all(),
        "filtro_cedula": cedula or "",
        "filtro_grupo_id": grupo_id or "",
        "filtro_pago": estado_pago or ""
    })

class InscripcionCreateView(FormView):
    template_name = "inscripciones/crear.html"
    form_class = InscripcionCreateForm

    def form_valid(self, form):
        data = form.cleaned_data
        
        count = Inscripcion.objects.filter(catequizando=data['catequizando'], grupo=data['grupo']).count()
        if count > 0:
            return redirect('inscripcion_listar') 

        import datetime
        Inscripcion.objects.create(
            catequizando=data['catequizando'],
            grupo=data['grupo'],
            estado_pago=data['estadopago'],
            fecha_inscripcion=datetime.datetime.now().strftime("%Y-%m-%d"),
            estado_inscripcion='CURSANDO'
        )
        return redirect('inscripcion_listar')

class InscripcionDetailView(DetailView):
    model = Inscripcion
    template_name = "inscripciones/detalle.html"
    context_object_name = "inscripcion"
    
    def get_object(self, queryset=None):
        c_id = self.kwargs.get('catequizando_id')
        g_id = self.kwargs.get('grupo_id')
        return get_object_or_404(Inscripcion, catequizando__id=c_id, grupo__id=g_id)

class InscripcionUpdateView(View):
    template_name = "inscripciones/editar.html"
    form_class = InscripcionUpdateForm

    def get(self, request, catequizando_id, grupo_id):
        inscripcion = get_object_or_404(Inscripcion, catequizando__id=catequizando_id, grupo__id=grupo_id)
        form = self.form_class(initial={
            'estadoinscripcion': inscripcion.estado_inscripcion,
            'estadopago': inscripcion.estado_pago,
        })
        return render(request, self.template_name, {
            'form': form, 
            'catequizando_id': catequizando_id, 
            'grupo_id': grupo_id,
            'item': inscripcion
        })

    def post(self, request, catequizando_id, grupo_id):
        inscripcion = get_object_or_404(Inscripcion, catequizando__id=catequizando_id, grupo__id=grupo_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            inscripcion.estado_inscripcion = data['estadoinscripcion']
            inscripcion.estado_pago = data['estadopago']
            inscripcion.save()
            return redirect('inscripcion_detail', catequizando_id=catequizando_id, grupo_id=grupo_id)
        return render(request, self.template_name, {'form': form, 'catequizando_id': catequizando_id, 'grupo_id': grupo_id})

def inscripcion_eliminar(request, catequizando_id, grupo_id):
    inscripcion = get_object_or_404(Inscripcion, catequizando__id=catequizando_id, grupo__id=grupo_id)
    inscripcion.delete()
    return redirect('inscripcion_listar')


# NEW VIEWS FOR SPECIFIC REQUESTS

class InscripcionTomarAsistenciaView(View):
    template_name = "inscripciones/asistencia.html"
    form_class = AsistenciaForm

    def get(self, request, catequizando_id, grupo_id):
        inscripcion = get_object_or_404(Inscripcion, catequizando__id=catequizando_id, grupo__id=grupo_id)
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form, 'inscripcion': inscripcion
        })

    def post(self, request, catequizando_id, grupo_id):
        inscripcion = get_object_or_404(Inscripcion, catequizando__id=catequizando_id, grupo__id=grupo_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # $push operation simulation
            nuevo_registro = {
                "sesion_id": data['sesion_id'],
                "estado": data['estado']
            }
            if not inscripcion.registro_asistencia:
                inscripcion.registro_asistencia = []
            
            inscripcion.registro_asistencia.append(nuevo_registro)
            inscripcion.save()
            return redirect('inscripcion_detail', catequizando_id=catequizando_id, grupo_id=grupo_id)
        return render(request, self.template_name, {'form': form, 'inscripcion': inscripcion})


class InscripcionAgregarNotaView(View):
    template_name = "inscripciones/calificacion.html"
    form_class = CalificacionForm

    def get(self, request, catequizando_id, grupo_id):
        inscripcion = get_object_or_404(Inscripcion, catequizando__id=catequizando_id, grupo__id=grupo_id)
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form, 'inscripcion': inscripcion
        })

    def post(self, request, catequizando_id, grupo_id):
        inscripcion = get_object_or_404(Inscripcion, catequizando__id=catequizando_id, grupo__id=grupo_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            import datetime
            # $push operation simulation
            nueva_nota = {
                "descripcion": data['descripcion'],
                "valor": data['valor'],
                "fecha": str(datetime.date.today())
            }
            if not inscripcion.calificaciones:
                inscripcion.calificaciones = []
            
            inscripcion.calificaciones.append(nueva_nota)
            inscripcion.save()
            return redirect('inscripcion_detail', catequizando_id=catequizando_id, grupo_id=grupo_id)
        return render(request, self.template_name, {'form': form, 'inscripcion': inscripcion})


# ==========================================
# CICLOS
# ==========================================

def ciclo_listar(request):
    ciclos = Ciclo.objects.all()
    return render(request, "ciclos/listar.html", {"ciclos": ciclos})

class CicloDetailView(DetailView):
    model = Ciclo
    template_name = "ciclos/detalle.html"
    context_object_name = "ciclo"

class CicloCreateView(FormView):
    template_name = "ciclos/crear.html"
    form_class = CicloForm

    def form_valid(self, form):
        data = form.cleaned_data
        import uuid
        new_id = str(uuid.uuid4())[:8]

        Ciclo.objects.create(
            id=new_id,
            nombre=data['nombreciclo'],
            fecha_inicio=data['fechainicio'],
            fecha_fin=data['fechafin'],
            estado=data['estado']
        )
        return redirect('ciclo_listar')

class CicloUpdateView(View):
    template_name = "ciclos/editar.html"
    form_class = CicloUpdateForm

    def get(self, request, pk):
        ciclo = get_object_or_404(Ciclo, pk=pk)
        form = self.form_class(initial={
            'nombreciclo': ciclo.nombre,
            'fechainicio': ciclo.fecha_inicio,
            'fechafin': ciclo.fecha_fin,
            'estado': ciclo.estado
        })
        return render(request, self.template_name, {'form': form, 'ciclo': ciclo})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            ciclo = get_object_or_404(Ciclo, pk=pk)
            data = form.cleaned_data
            ciclo.nombre = data['nombreciclo']
            ciclo.fecha_inicio = data['fechainicio']
            ciclo.fecha_fin = data['fechafin']
            ciclo.estado = data['estado']
            ciclo.save()
            return redirect('ciclo_listar')
        return render(request, self.template_name, {'form': form, 'pk': pk})

def ciclo_eliminar(request, pk):
    ciclo = get_object_or_404(Ciclo, pk=pk)
    ciclo.delete()
    return redirect('ciclo_listar')
