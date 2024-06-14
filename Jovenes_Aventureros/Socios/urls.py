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


    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)