from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path("cargarSocios/", cargarSocios, name="Cargar Socios"),
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
    path('exportarPDFSocio/<int:insid>', exportar_socios_a_Pdf, name="Exportar a PDF"),
    path('exportarPDFSocioV2/<int:insid>', exportar_socios_a_Pdf_v2, name="Exportar a PDF V2"),
    path('exportarTicketV2/<int:insid>/<int:socioid>', exportar_tiket_socios_a_Pdf_v2, name="Exportar Ticket V2"),
    path('eliminarInscrito/<int:insid>/<int:socioid>', eliminar_de_inscripcion, name="Eliminar Socio Inscripcion"),
    path('mostrarUsuariosSocios', mostrar_socios_socios, name="Mostrar Usuarios Socios"),
    path('mostrarUsuariosSocios/buscar/', buscar_socios_socios),
    path('reestablecerUsuarios/', reestablecer_usuarios, name = "Reestablecer Usuario"),
    path('confirmacion/', confirmacion, name = "Confirmacion"),
    path('eliminarUsuario/<int:socioid>', eliminar_usuario, name = "Eliminar Usuario"),

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)