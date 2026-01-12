from django.urls import path
from .views import (
    CatequizandoDetailView,
    CatequizandoUpdateView,
    CatequizandoCreateView,
    catequizando_buscar,
    catequizando_eliminar,
    catequizando_listar,
    
    # Grupos
    grupo_listar,
    grupo_buscar,
    GrupoCreateView,
    GrupoDetailView,
    GrupoUpdateView,
    grupo_eliminar,


    # Inscripciones
    inscripcion_listar,
    InscripcionCreateView,
    InscripcionDetailView,
    InscripcionUpdateView,
    inscripcion_eliminar,
    inscripcion_buscar,
    InscripcionTomarAsistenciaView,
    InscripcionAgregarNotaView,

    # Ciclos
    ciclo_listar,
    CicloCreateView,
    CicloUpdateView,
    CicloDetailView,
    ciclo_eliminar
)

urlpatterns = [
    # ==========================
    # CATEQUIZANDOS
    # ==========================
    path("catequizandos/", catequizando_listar, name="catequizando_listar"),
    path('catequizandos/<str:pk>/detalle/', CatequizandoDetailView.as_view(), name='catequizando_detalle'),
    path('catequizandos/<str:pk>/editar/', CatequizandoUpdateView.as_view(), name='catequizando_editar'),
    path('catequizandos/crear/', CatequizandoCreateView.as_view(), name='catequizando_crear'),
    path("catequizandos/<str:persona_id>/eliminar/", catequizando_eliminar, name="catequizando_eliminar"),
    path("catequizandos/buscar/", catequizando_buscar, name="catequizando_buscar"),

    # ==========================
    # GRUPOS
    # ==========================
    path("grupos/", grupo_listar, name="grupo_listar"),
    path("grupos/crear/", GrupoCreateView.as_view(), name="grupo_crear"),
    path("grupos/<str:pk>/detalle/", GrupoDetailView.as_view(), name="grupo_detail"),
    path("grupos/<str:pk>/editar/", GrupoUpdateView.as_view(), name="grupo_editar"),
    path("grupos/<str:pk>/eliminar/", grupo_eliminar, name="grupo_eliminar"),
    path("grupos/buscar/", grupo_buscar, name="grupo_buscar"),

    # ==========================
    # INSCRIPCIONES
    # ==========================
    path("inscripciones/", inscripcion_listar, name="inscripcion_listar"),
    path("inscripciones/crear/", InscripcionCreateView.as_view(), name="inscripcion_crear"),
    path("inscripciones/<str:catequizando_id>/<str:grupo_id>/detalle/", InscripcionDetailView.as_view(), name="inscripcion_detail"),
    path("inscripciones/<str:catequizando_id>/<str:grupo_id>/editar/", InscripcionUpdateView.as_view(), name="inscripcion_editar"),
    path("inscripciones/<str:catequizando_id>/<str:grupo_id>/eliminar/", inscripcion_eliminar, name="inscripcion_eliminar"),
    path("inscripciones/buscar/", inscripcion_buscar, name="inscripcion_buscar"),
    
    # Nuevas rutas para Asistencia y Notas
    path("inscripciones/<str:catequizando_id>/<str:grupo_id>/asistencia/", InscripcionTomarAsistenciaView.as_view(), name="inscripcion_asistencia"),
    path("inscripciones/<str:catequizando_id>/<str:grupo_id>/nota/", InscripcionAgregarNotaView.as_view(), name="inscripcion_nota"),


    # ==========================
    # CICLOS
    # ==========================
    path("ciclos/", ciclo_listar, name="ciclo_listar"),
    path("ciclos/crear/", CicloCreateView.as_view(), name="ciclo_crear"),
    path("ciclos/<str:pk>/detalle/", CicloDetailView.as_view(), name="ciclo_detalle"),
    path("ciclos/<str:pk>/editar/", CicloUpdateView.as_view(), name="ciclo_editar"),
    path("ciclos/<str:pk>/eliminar/", ciclo_eliminar, name="ciclo_eliminar"),
]
