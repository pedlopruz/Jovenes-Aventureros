from django.shortcuts import render, HttpResponse, redirect
import csv
from .models import *
from django.http import Http404
from .forms import *
from django.db.models import Q
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import inch
from django.core.paginator import Paginator, PageNotAnInteger
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A6, A4
from django.http import HttpResponse
from datetime import datetime
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, NextPageTemplate, PageBreak, Flowable
import requests
from bs4 import BeautifulSoup
import os
import sys
# Create your views here.

import csv
from datetime import datetime
from django.http import HttpResponse

def cargarSocios(request):
    Socios.objects.all().delete()

    # Determinar la ruta base correcta
    if getattr(sys, 'frozen', False):
        # Ejecutando como .exe
        base_path = sys._MEIPASS
    else:
        # Ejecutando en desarrollo con manage.py
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Construir la ruta completa al archivo CSV
    path = os.path.join(base_path, 'data', 'socios.csv')
    
    # Verificar si el archivo existe
    if not os.path.exists(path):
        return HttpResponse(f"Error: No se encontró el archivo en {path}")

    TALLAS_VALIDAS = ["S", "M", "L", "XL", "XXL"]

    try:
        with open(path, newline='', encoding='utf-8-sig') as csvfile:
            lector_csv = csv.DictReader(csvfile, delimiter=',')

            for numero_fila, fila in enumerate(lector_csv, start=1):
                try:
                    numero_socio = int(fila.get('Número de Socio') or 0)

                    nombre = fila.get('Nombre', '').strip()
                    apellidos = fila.get('Apellidos', '').strip()
                    dni = fila.get('DNI', '').strip()

                    telefono = fila.get('Teléfono', '').strip()
                    if telefono.lower() == "sin especificar":
                        telefono = ""

                    codigo_postal = fila.get('Código Postal', '').strip()
                    if codigo_postal.lower() == "sin especificar":
                        codigo_postal = ""

                    ciudad = fila.get('Ciudad', '').strip()
                    if ciudad.lower() == "sin especificar":
                        ciudad = ""

                    provincia = fila.get('Provincia', '').strip()
                    if provincia.lower() == "sin especificar":
                        provincia = ""

                    # Booleanos
                    socio = fila.get('Socio', '').strip().lower() == "true"
                    regalo = fila.get('Regalo', '').strip().lower() == "true"

                    # Fecha como texto
                    fecha_raw = fila.get('Fecha de Nacimiento', '').strip()

                    if not fecha_raw or fecha_raw.lower() == "sin especificar":
                        fecha_nacimiento = ""
                    else:
                        try:
                            fecha_convertida = datetime.strptime(fecha_raw, "%Y-%m-%d")
                        except ValueError:
                            try:
                                fecha_convertida = datetime.strptime(fecha_raw, "%d/%m/%Y")
                            except ValueError:
                                fecha_convertida = None

                        if fecha_convertida:
                            fecha_nacimiento = fecha_convertida.strftime("%Y-%m-%d")
                        else:
                            fecha_nacimiento = fecha_raw

                    # Talla segura
                    talla_camiseta = fila.get('Talla Camiseta', 'S').strip().upper()
                    if talla_camiseta not in TALLAS_VALIDAS:
                        talla_camiseta = "S"

                    Socios.objects.create(
                        numero_socio=numero_socio,
                        nombre=nombre,
                        apellidos=apellidos,
                        dni=dni,
                        fecha_nacimiento=fecha_nacimiento,
                        telefono=telefono,
                        codigo_postal=codigo_postal,
                        ciudad=ciudad,
                        provincia=provincia,
                        socio=socio,
                        regalo=regalo,
                        talla_camiseta=talla_camiseta
                    )

                except Exception as e:
                    print(f"❌ Error en la fila {numero_fila}: {e}")
                    print(f"📄 Contenido: {fila}")

        return HttpResponse("Carga de socios completada correctamente")
    
    except Exception as e:
        return HttpResponse(f"Error al leer el archivo: {str(e)}")


def obtener_imagen_web_BeautifulSoup():
    try:
        url = "https://jovenesaventureros.blogspot.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Obtenemos todas las imágenes dentro de div.separator
        imagenes = soup.select("div.separator img")

        if len(imagenes) >= 2:  # verificamos que haya al menos 2
            return imagenes[1]["src"]  # la segunda imagen (índice 1)
        
        return None  # si no hay suficientes imágenes

    except Exception as e:
        print("❌ ERROR BeautifulSoup:", type(e).__name__, str(e))
        return None



def listar_Socios(request):

    imagen_url = obtener_imagen_web_BeautifulSoup()
    print(imagen_url)
    return render(request, "socios/mostrarSocios.html", {"imagen_url": imagen_url})


def actualizar_Socio(request, socioid):
    socio = Socios.objects.filter(id = socioid).first()
    socio_b = socio.socio
    num = socio.numero_socio
    if socio.socio is True:
        if request.method == 'POST':
            socio_form = SocioForm(request.POST, instance=socio)

            if socio_form.is_valid():
                socio_form.save(commit=False)
                socio.nombre = socio.nombre.upper()
                socio.apellidos = socio.apellidos.upper()
                socio.save()
                if not socio.socio:
                    socio.regalo = False
                    socio.numero_socio = 0
                socio.save()

                if socio.socio is True:
                    return redirect('Mostrar Usuarios Socios')
                else:
                    return redirect('Listar Socios')
            else:
                print(socio_form.errors)  # Para ver en la consola qué está fallando

        else:
            
            socio_form = SocioForm(instance=socio)

        return render(request, 'socios/actualizarSocio.html', {'formulario': socio_form, 'errores': socio_form.errors})
    else:
        if request.method == 'POST':
            socio_form = NoSocioForm(request.POST, instance=socio)

            if socio_form.is_valid():
                if socio_form.cleaned_data["socio"] is False and socio_b is False:
                    socio.numero_socio = 0
                    socio.save()
                elif socio_form.cleaned_data["socio"] is False and socio_b is True:
                    socio.numero_socio = 0
                    socio.regalo = False
                    socio.save()
                elif socio_form.cleaned_data["socio"] is True and socio_b is False:
                    total = 0
                    for i in range(1,300):
                        aparece_socio = Socios.objects.filter(socio = True, numero_socio= i)
                        if aparece_socio:
                            pass
                        else:
                            total = i
                            break


                    socio.numero_socio = total
                    socio.save()
                else:
                    socio.numero_socio = num
                    socio.save()

                socio_form.save()
                socio.nombre = socio.nombre.upper()
                socio.apellidos = socio.apellidos.upper()
                socio.save()

                if socio.socio is True:
                    return redirect('Mostrar Usuarios Socios')
                else:
                    return redirect('Listar Socios')

        else:
            socio_form = NoSocioForm(instance=socio)

        return render(request, 'socios/actualizarNoSocio.html', {'formulario': socio_form})

        

def crear_Socio(request):

    if request.method == 'POST':
        socio_form = NoSocioForm(request.POST)

        if socio_form.is_valid():
            nombre = socio_form.cleaned_data['nombre']
            apellidos = socio_form.cleaned_data['apellidos']
            dni = socio_form.cleaned_data['dni']
            fecha_nacimiento = socio_form.cleaned_data['fecha_nacimiento']
            telefono = socio_form.cleaned_data['telefono']
            codigo_postal = socio_form.cleaned_data['codigo_postal']
            ciudad = socio_form.cleaned_data['ciudad']
            provincia = socio_form.cleaned_data['provincia']
            socio = socio_form.cleaned_data['socio']
            talla_camiseta = socio_form.cleaned_data['talla_camiseta']
            if socio is True:
                total = 0
                for i in range(1,300):
                    aparece_socio = Socios.objects.filter(socio = True, numero_socio= i)
                    if aparece_socio:
                        pass
                    else:
                        total = i
                        break
                numero_socio = total
            else:
                numero_socio = 0
            Socios.objects.create(numero_socio = numero_socio,
                                    nombre = nombre.upper(), 
                                    apellidos=apellidos.upper(), 
                                    dni = dni, 
                                    fecha_nacimiento = fecha_nacimiento, 
                                    telefono=telefono, 
                                    codigo_postal = codigo_postal, 
                                    ciudad = ciudad, 
                                    provincia = provincia,
                                    socio = socio)
            

            return redirect('Listar Socios')

    else:
        socio_form = NoSocioForm()

        return render(request, 'socios/añadirSocios.html', {'formulario': socio_form})
    

def buscar(request):
    if "usern" in request.GET:
        user = request.GET["usern"]
        if user is None or user == "":
            return redirect('Listar Socios')
        elif len(user) > 100:
            return render(request, 'Listar Socios')
        else:
            total_inscripcion = Inscripciones.objects.filter(finalizada = False).count()
            user = user.upper()
            usuario = Socios.objects.filter(Q(apellidos__icontains=user)| Q(numero_socio__icontains=user)).order_by("numero_socio")
            return render(request, "socios/busquedaSocio.html", {"entity": usuario, "num_inscripcion":total_inscripcion, "user":user})
    else:
        return redirect('Listar Socios')
    
def calcular_suma(request):
    total_socios = 0
    recaudacion_banco = 0
    recaudacion_metalico = 0
    total_no_socios = 0
    total_metalico = 0
    total_banco = 0
    numero_socios = 0
    numero_no_socios = 0
    total_guia = 0
    inscripciones = Inscripciones.objects.filter(finalizada = False)
    if inscripciones:
        for ins in inscripciones:
            inscripciones_socio = Inscripcion_Socio.objects.filter(inscripcion = ins)
            for inso in inscripciones_socio:
                if inso.socios.socio is True:
                    total_socios += inso.precio
                else:
                    total_no_socios += inso.precio

                if inso.pago is True:
                    total_metalico += 1
                    recaudacion_metalico += inso.precio
                else:
                    total_banco += 1
                    recaudacion_banco += inso.precio

                if inso.socios.socio is True:
                    numero_socios +=1
                else:
                    numero_no_socios +=1
                if inso.guia is True:
                    total_guia +=1
                



            ins.total_guias = total_guia
            ins.recaudacion_total = total_socios + total_no_socios
            ins.recaudacion_banco = recaudacion_banco
            ins.recaudacion_metalico = recaudacion_metalico
            ins.pago_metalico = total_metalico - total_guia
            ins.pago_banco = total_banco
            ins.total_socios = numero_socios - total_guia
            ins.total_no_socios = numero_no_socios
            ins.save()

    return print("Todo correcto")
    
def listar_incripciones_abiertas(request):
    inscripciones = Inscripciones.objects.filter(finalizada = False)
    if inscripciones:
        calcular_suma(request)
    total = inscripciones.count()
    page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
    try:
        paginator = Paginator(inscripciones, 12)  # 6 usuarios por página
        inscripciones = paginator.page(page)
    except PageNotAnInteger:
            raise Http404

    return render(request, 'socios/mostrarInscripcionAbierta.html', {"entity":inscripciones, "paginator":paginator, "total":total})

def listar_incripciones_cerradas(request):
    calcular_suma(request)
    inscripciones = Inscripciones.objects.filter(finalizada = True)
    page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
    try:
        paginator = Paginator(inscripciones, 12)  # 6 usuarios por página
        inscripciones = paginator.page(page)
        
    except PageNotAnInteger:
            raise Http404

    return render(request, 'socios/mostrarInscripcionCerrada.html', {"entity":inscripciones, "paginator":paginator})

def actualizar_inscripcion(request, inscripcionid):
    inscripcion = Inscripciones.objects.filter(id = inscripcionid).first()

    if request.method == 'POST':
        inscripcion_form = InscripcionForm(request.POST, instance=inscripcion)

        if inscripcion_form.is_valid():

            inscripcion_form.save()
        
        inscripciones_socios = Inscripcion_Socio.objects.filter(inscripcion = inscripcion)
        for inscripcion_socio in inscripciones_socios:
            if inscripcion_socio.socios.socio is True:
                inscripcion_socio.precio = inscripcion.precio_socio
                inscripcion_socio.save()
            else:
                inscripcion_socio.precio = inscripcion.precio_no_socio
                inscripcion_socio.save()
        


        return redirect('Incripciones Abiertas')

    else:
        inscripcion_form = InscripcionForm(instance=inscripcion)

        return render(request, 'socios/actualizarInscripcion.html', {'formulario': inscripcion_form})
    

def crear_inscripcion(request):

    if request.method == 'POST':
        inscripcion_form = InscripcionForm(request.POST)

        if inscripcion_form.is_valid():
            nombre = inscripcion_form.cleaned_data['nombre']
            destino = inscripcion_form.cleaned_data['destino']
            fecha = inscripcion_form.cleaned_data['fecha']
            distancia = inscripcion_form.cleaned_data['distancia']
            dificultad = inscripcion_form.cleaned_data['dificultad']
            precio_socio = inscripcion_form.cleaned_data['precio_socio']
            precio_no_socio = inscripcion_form.cleaned_data['precio_no_socio']
            Inscripciones.objects.create(nombre = nombre, 
                                    destino=destino, 
                                    fecha = fecha, 
                                    distancia = distancia, 
                                    dificultad=dificultad, 
                                    precio_socio = precio_socio, 
                                    precio_no_socio = precio_no_socio)
            

            return redirect('Incripciones Abiertas')
    else:
        inscripcion_form = InscripcionForm()

        return render(request, 'socios/crearInscripcion.html', {'formulario': inscripcion_form})
    
def cerrar_inscripcion(request):
    inscripcion = Inscripciones.objects.filter(finalizada = False).first()
    inscripcion.finalizada = True
    inscripcion.save()
    return redirect('Incripciones Abiertas')

def buscar_inscripciones(request):
    if "usern" in request.GET:
        user = request.GET["usern"]
        if user is None or user == "":
            return redirect('Incripciones Cerradas')
        elif len(user) > 100:
            return redirect('Incripciones Cerradas')
        else:
            user = user.upper()
            ins = Inscripciones.objects.filter(Q(nombre__icontains=user))
            page = request.GET.get('page', 1)
            try:
                paginator = Paginator(ins, 12)  # 6 usuarios por página
                ins = paginator.page(page)
            except PageNotAnInteger:
                raise Http404

            return render(request, "socios/busquedaInscripcion.html", {"entity": ins, "paginator":paginator})
    else:
        return redirect('Incripciones Cerradas')
    


def crear_inscripcion_socio(request, socioid):

    mensaje = None
    precio = 0

    socio = Socios.objects.filter(id=socioid).first()
    inscripcion = Inscripciones.objects.filter(finalizada=False).first()

    # ⚠️ SIEMPRE DEFINIDA
    asientos_ocupados = list(
        Inscripcion_Socio.objects
        .filter(inscripcion=inscripcion)
        .values_list('asiento_bus', flat=True)
    )

    # Listas de asientos
    asientos_bus_1 = list(range(1, 56))     # 1 - 55
    asientos_bus_2 = list(range(56, 111))   # 56 - 110

    primer_bus_lleno = len(
        [a for a in asientos_ocupados if a <= 55]
    ) >= 55

    # 💰 Precio inicial (GET)
    if socio.socio:
        precio = inscripcion.precio_socio
    else:
        precio = inscripcion.precio_no_socio

    if request.method == 'POST':
        inscripcion_form = Inscripcion_SocioForm(request.POST)

        if inscripcion_form.is_valid():

            es_guia = inscripcion_form.cleaned_data['guia']

            # 🔥 PRECIO DEFINITIVO
            if es_guia:
                precio = 0
            elif socio.socio:
                precio = inscripcion.precio_socio
            else:
                precio = inscripcion.precio_no_socio

            asiento_bus = inscripcion_form.cleaned_data['asiento_bus']

            # VALIDACIONES
            if asiento_bus in asientos_ocupados:
                mensaje = "Asiento ocupado"

            elif Inscripcion_Socio.objects.filter(
                inscripcion=inscripcion,
                socios=socio
            ).exists():
                mensaje = "Usuario ya inscrito en la ruta"

            else:
                numero_bus = 1 if asiento_bus <= 55 else 2

                Inscripcion_Socio.objects.create(
                    inscripcion=inscripcion,
                    socios=socio,
                    precio=precio,
                    numero_bus=numero_bus,
                    asiento_bus=asiento_bus,
                    pago=True,
                    guia=es_guia
                )

                return redirect('Usuarios Inscritos', inscripcion.id)

    else:
        inscripcion_form = Inscripcion_SocioForm()

    # 👇 UN SOLO RENDER, VARIABLES GARANTIZADAS
    return render(request, 'socios/crearInscripcionSocio.html', {
        "formulario": inscripcion_form,
        "socio": socio,
        "inscripcion": inscripcion,
        "precio": precio,
        "mensaje": mensaje,
        "asientos_ocupados": asientos_ocupados,
        "asientos_bus_1": asientos_bus_1,
        "asientos_bus_2": asientos_bus_2,
        "primer_bus_lleno": primer_bus_lleno,
    })



def crear_inscripcion_socio_b(request, socioid):

    mensaje = None
    precio = 0

    socio = Socios.objects.filter(id=socioid).first()
    inscripcion = Inscripciones.objects.filter(finalizada=False).first()

    # ⚠️ SIEMPRE DEFINIDA
    asientos_ocupados = list(
        Inscripcion_Socio.objects
        .filter(inscripcion=inscripcion)
        .values_list('asiento_bus', flat=True)
    )

    # Listas de asientos
    asientos_bus_1 = list(range(1, 56))     # 1 - 55
    asientos_bus_2 = list(range(56, 111))   # 56 - 110

    primer_bus_lleno = len(
        [a for a in asientos_ocupados if a <= 55]
    ) >= 55

    # 💰 Precio inicial (GET)
    if socio.socio:
        precio = inscripcion.precio_socio
    else:
        precio = inscripcion.precio_no_socio

    if request.method == 'POST':
        inscripcion_form = Inscripcion_SocioForm(request.POST)

        if inscripcion_form.is_valid():

            es_guia = inscripcion_form.cleaned_data['guia']

            # 🔥 PRECIO DEFINITIVO
            if es_guia:
                precio = 0
            elif socio.socio:
                precio = inscripcion.precio_socio
            else:
                precio = inscripcion.precio_no_socio

            asiento_bus = inscripcion_form.cleaned_data['asiento_bus']

            # VALIDACIONES
            if asiento_bus in asientos_ocupados:
                mensaje = "Asiento ocupado"

            elif Inscripcion_Socio.objects.filter(
                inscripcion=inscripcion,
                socios=socio
            ).exists():
                mensaje = "Usuario ya inscrito en la ruta"

            else:
                numero_bus = 1 if asiento_bus <= 55 else 2

                Inscripcion_Socio.objects.create(
                    inscripcion=inscripcion,
                    socios=socio,
                    precio=precio,
                    numero_bus=numero_bus,
                    asiento_bus=asiento_bus,
                    pago=False,
                    guia=es_guia
                )

                return redirect('Usuarios Inscritos', inscripcion.id)

    else:
        inscripcion_form = Inscripcion_SocioForm()

    # 👇 UN SOLO RENDER, VARIABLES GARANTIZADAS
    return render(request, 'socios/crearInscripcionSocio.html', {
        "formulario": inscripcion_form,
        "socio": socio,
        "inscripcion": inscripcion,
        "precio": precio,
        "mensaje": mensaje,
        "asientos_ocupados": asientos_ocupados,
        "asientos_bus_1": asientos_bus_1,
        "asientos_bus_2": asientos_bus_2,
        "primer_bus_lleno": primer_bus_lleno,
    })

def listar_inscritos(request, insid):

    inscripcion = Inscripciones.objects.filter(id = insid).first()
    nombre = inscripcion.nombre
    inscripcion_socio = Inscripcion_Socio.objects.filter(inscripcion = inscripcion).order_by("-asiento_bus")
    return render(request, 'socios/mostrarInscripcionSocio.html', {'entity': inscripcion_socio, "nombre":nombre})


def buscar_inscripciones_socios(request, insid):
    if "usern" in request.GET:
        user = request.GET["usern"]
        if user is None or user == "":
            return redirect('Usuarios Inscritos', insid)
        elif len(user) > 100:
            return redirect('Usuarios Inscritos', insid)
        else:
            user = user.upper()
            inscripcion = Inscripciones.objects.filter(id = insid).first()
            nombre = inscripcion.nombre
            inscripcion_socio = Inscripcion_Socio.objects.filter(inscripcion = inscripcion).order_by("asiento_bus")
            ins = inscripcion_socio.filter(Q(socios__apellidos__icontains=user)|Q(socios__numero_socio__icontains=user))
            page = request.GET.get('page', 1)
            try:
                paginator = Paginator(ins, 12)  # 6 usuarios por página
                ins = paginator.page(page)
            except PageNotAnInteger:
                raise Http404

            return render(request, "socios/busquedaInscripcionSocio.html", {"entity": ins, "paginator":paginator, "nombre":nombre})
    else:
        return redirect('Incripciones Abiertas')
    


def exportar_socios_a_Pdf(request, insid):
    actualDate = datetime.now().date()
    inscripcion = Inscripciones.objects.filter(id=insid).first()
    nombre = inscripcion.nombre
    queryset = Inscripcion_Socio.objects.filter(inscripcion=inscripcion).order_by("socios__apellidos")
    filename = f"Lista Bus {nombre}"

    # Unpack values
    # Response Object
    response_pdf = HttpResponse(content_type="application/pdf")
    response_pdf["Content-Disposition"] = f"attachment; filename={filename}.pdf"
    styles = getSampleStyleSheet()

    # Reduce the top margin in the document
    doc = SimpleDocTemplate(
        response_pdf,
        pagesize=letter,
        topMargin=20,  # Ajustar este valor para reducir el margen superior
        leftMargin=30,
        rightMargin=30,
        bottomMargin=20,
    )

    # Create a Story list to hold elements
    Story = []

    # Add cover page elements
    title = f"Usuarios Inscritos {nombre}"
    actualDateText = f"Fecha actual: {actualDate}"

    cover_elements = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 12),  # Ajustar el espacio vertical si es necesario
        Paragraph(actualDateText, styles["Normal"]),
        Spacer(1, 6),
    ]
    # Add cover elements to the Story
    Story.extend(cover_elements)
    # Separation for the table
    Story.append(Spacer(1, 10))
    table_data = [
        [
            "Apellidos",
            "Nombre",
            "Teléfono",
            "Bus-Asiento",
            "Regalo",
            "Observaciones",
        ]
    ]

    for socio in queryset:
        table_row = [
            socio.socios.apellidos,
            socio.socios.nombre,
            socio.socios.telefono,
            f"BUS {socio.numero_bus}-{socio.asiento_bus}",
            socio.socios.regalo,
            socio.socios.socio,
        ]

        table_data.append(table_row)

    # Create a table
    table = Table(table_data, colWidths=[100, 84, 50, 50, 84])  # Adjust the column width as needed

    # Table style
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTSIZE", (0, 0), (-1, -1), 8),  # Adjust the font size as needed
            ("WORDWRAP", (0, 0), (-1, -1), True),  # Allow word wrapping
            ("TEXTCOLOR", (-1, 0), (-1, -1), colors.white),  # Hacer que la última columna sea invisible
        ]
    )

    # Apply colors to the "Regalo" column based on its value
    for i, row in enumerate(table_data[1:], start=1):  # Comenzar desde la segunda fila (índice 1)
        if row[4] is  False and row[5] is False:  
            bg_color = colors.white
            text_color = colors.white
        elif row[4] is  False and row[5] is True:  
            bg_color = colors.red
            text_color = colors.red
        else:  
            bg_color = colors.green
            text_color = colors.green
        table_style.add("BACKGROUND", (4, i), (4, i), bg_color)  # Cambia el índice a 4
        table_style.add("TEXTCOLOR", (4, i), (4, i), text_color)  # Cambia el índice a 4

    table.setStyle(table_style)

    # Table to Story
    Story.append(table)
    doc.build(Story)

    return response_pdf




def exportar_socios_a_Pdf_v2(request, insid):
    actualDate = datetime.now().date()
    inscripcion = Inscripciones.objects.filter(id = insid).first()
    nombre = inscripcion.nombre
    queryset = Inscripcion_Socio.objects.filter(inscripcion = inscripcion).order_by("socios__apellidos")
    filename = f"Lista Seguro {nombre}"
    

    # Unpack values
    # Response Object
    response_pdf = HttpResponse(content_type="application/pdf")
    response_pdf["Content-Disposition"] = f"attachment; filename={filename}.pdf"
    styles = getSampleStyleSheet()

    # This is the PDF document
    doc = SimpleDocTemplate(response_pdf, pagesize=letter)

    # Create a Story list to hold elements
    Story = []

    # Add cover page elements
    title = f"Usuarios Inscritos {nombre}"
    actualDateText = f"Fecha actual: {actualDate}"

    cover_elements = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 12),
        Paragraph(actualDateText, styles["Normal"]),
        Spacer(1, 6),
    ]
    # Add cover elements to the Story
    Story.extend(cover_elements)
    # Separation for the table
    Story.append(Spacer(1, 10))
    table_data = [
        [       
            "Apellidos",
            "Nombre",
            "DNI"
        ]
    ]

    for socio in queryset:
        table_row = [
            (
                socio.socios.apellidos
            ),
            (
                socio.socios.nombre

            ),
            (
                socio.socios.dni
            ),
        ]
        table_data.append(table_row)

    # Create a table
    table = Table(
        table_data, colWidths=[100, 100, 100, 100]
    )  # Adjust the column width as needed

    # Table style
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 8),  # Adjust the font size as needed
                ("WORDWRAP", (0, 0), (-1, -1), True),  # Allow word wrapping
            ]
        )
    )

    # Table to Story
    Story.append(table)
    doc.build(Story)

    return response_pdf

class AlignedImage(Flowable):
    def __init__(self, img_path, width, height, hAlign='LEFT'):
        Flowable.__init__(self)
        self.img_path = img_path
        self.width = width
        self.height = height
        self.hAlign = hAlign

    def draw(self):
        img = Image(self.img_path, width=self.width, height=self.height)
        img.drawOn(self.canv, 0, 0)

def exportar_tiket_socios_html(request, insid, socioid):
    actualDate = datetime.now().date()
    inscripcion = Inscripciones.objects.filter(id=insid).first()
    socios = Inscripcion_Socio.objects.filter(inscripcion=inscripcion, socios__id=socioid)

    tickets = []
    for socio in socios:
        num = socio.socios.numero_socio if socio.socios.socio else ""
        asiento = socio.asiento_bus if socio.numero_bus == 1 else socio.asiento_bus - 55
        tickets.append({
            "ruta": inscripcion.nombre,
            "fecha": inscripcion.fecha,
            "bus": socio.numero_bus,
            "asiento": asiento,
            "precio": socio.precio,
            "num_socio": num,
            "nombre": socio.socios.nombre,
            "apellidos": socio.socios.apellidos,
            "telefono": socio.socios.telefono,
            "dni": socio.socios.dni,
        })

    return render(request, "socios/ticket_termico.html", {"tickets": tickets})

def eliminar_de_inscripcion(request, insid, socioid):
    entity = Inscripcion_Socio.objects.filter(inscripcion__id = insid, socios__id= socioid).first()
    entity.delete()
    return redirect('Usuarios Inscritos', insid)

def eliminar_usuario(request, socioid):
    entity = Socios.objects.filter(id= socioid).first()
    entity.delete()
    return redirect('Listar Socios')

def mostrar_socios_socios(request):
    entity = Socios.objects.filter(socio = True).order_by("numero_socio")
    inscripcion = Inscripciones.objects.filter(finalizada = False)
    inscripcion_total = inscripcion.count()
    return render(request, "socios/mostrarSocioSocio.html", {"entity":entity,"num_inscripcion":inscripcion_total})

def buscar_socios_socios(request):
    if "usern" in request.GET:
        user = request.GET["usern"]
        if user is None or user == "":
            return redirect('Mostrar Usuarios Socios')
        elif len(user) > 100:
            return render(request, 'Mostrar Usuarios Socios')
        else:
            user = user.upper()
            usuario = Socios.objects.filter(Q(apellidos__icontains=user)| Q(numero_socio__icontains=user),socio = True).order_by("numero_socio")
            return render(request, "socios/busquedaSocioSocio.html", {"entity": usuario, "user":user})
    else:
        return redirect('Mostrar Usuarios Socios')

def reestablecer_usuarios(request):
    entity = Socios.objects.all()
    for i in entity:
        i.numero_socio = 0
        i.socio = False
        i.regalo = False
        i.save()

    return redirect("Listar Socios")

def confirmacion(request):
    return render(request, "socios/confirmacion.html")

def generar_csv_socios(request):
    socios = Socios.objects.all().order_by("apellidos")

    # Crear la respuesta HTTP con el tipo de contenido adecuado
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="socios.csv"'

    writer = csv.writer(response)
    # Escribir la cabecera del CSV
    writer.writerow(['Número de Socio', 'Nombre', 'Apellidos', 'DNI', 'Fecha de Nacimiento', 'Teléfono', 'Código Postal', 'Ciudad', 'Provincia', 'Socio', 'Regalo', 'Talla Camiseta'])

    # Escribir los datos de los socios
    for socio in socios:
        writer.writerow([socio.numero_socio, socio.nombre, socio.apellidos, socio.dni, socio.fecha_nacimiento, socio.telefono, socio.codigo_postal, socio.ciudad, socio.provincia, socio.socio, socio.regalo, socio.talla_camiseta])

    return response

def reabrir_inscripcion(request, insid):
    inscripciones_abiertas = Inscripciones.objects.filter(finalizada=False)
    if inscripciones_abiertas.exists():
        return redirect('Incripciones Abiertas')

    inscripcion = Inscripciones.objects.filter(id=insid).first()
    if inscripcion:
        inscripcion.finalizada = False
        inscripcion.save()

    return redirect('Incripciones Abiertas')

