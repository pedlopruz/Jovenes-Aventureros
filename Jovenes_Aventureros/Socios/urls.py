from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("cargarSocios/", cargarSocios, name="Cargar Socios"),
    path("mostrarSocios/", listar_Socios, name="Listar Socios"),
    path("actualizarSocio/<int:socioid>/", actualizar_Socio, name="Actualizar Socios"),
    path("crearSocio/", crear_Socio, name="Crear Socios"),
    path('mostrarSocios/buscar/', buscar),
    path("mostrarIncripciones/abiertas/", listar_incripciones_abiertas, name="Incripciones Abiertas"),
    path("mostrarIncripciones/cerradas/", listar_incripciones_cerradas, name="Incripciones Cerradas"),
    path("actualizarInscripcion/<int:inscripcionid>/", actualizar_inscripcion, name="Actualizar Inscripcion"),
    path("crearInscripcion/", crear_inscripcion, name="Crear Inscripcion"),
    path("cerrarInscripcion/", cerrar_inscripcion, name="Cerrar Inscripcion"),
    path('mostrarIncripciones/cerradas/buscar/', buscar_inscripciones),
    path("crearInscripcionSocio/<int:socioid>/", crear_inscripcion_socio, name="Inscribir Socios"),
    path("crearInscripcionSocioB/<int:socioid>/", crear_inscripcion_socio_b, name="Inscribir Socios B"),
    path('mostrarInscripcionSocio/<int:insid>/', listar_inscritos, name="Usuarios Inscritos"),
    path('mostrarInscripcionSocio/<int:insid>/buscar/', buscar_inscripciones_socios),


    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)