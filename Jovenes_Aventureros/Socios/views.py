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
)
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import inch
from django.core.paginator import Paginator, PageNotAnInteger
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
# Create your views here.

def cargarSocios(request):
    Socios.objects.all().delete()
    path3 = "data/socios.csv"
    with open(path3, newline='', encoding='utf-8-sig') as csvfile:
        lector_csv = csv.DictReader(csvfile, delimiter=';')
        for numero_fila, fila in enumerate(lector_csv, start=1):
            try:
                apellido = fila['Apellido']
                nombre = fila['Nombre']
                dni = fila['DNI']
                fecha = fila['Fecha']
                telefono = fila['Telefono']
                codigo_postal = fila['CP']
                ciudad = fila['Ciudad']
                provincia = fila['Provincia']
                Socios.objects.create(nombre = nombre, 
                                      apellido=apellido, 
                                      dni = dni, 
                                      fecha_nacimiento = fecha, 
                                      telefono=telefono, 
                                      codigo_postal = codigo_postal, 
                                      ciudad = ciudad, 
                                      provincia = provincia)
                    
                    
            except Exception as e:
                print(f"Error en la fila {numero_fila}: {e}")
                print(f"Contenido de la fila {numero_fila}: {fila}")

    return HttpResponse("Todo Ok")


def listar_Socios(request):

    inscripcion = Inscripciones.objects.filter(finalizada = False)
    inscripcion_total = inscripcion.count()
    socios = Socios.objects.all().order_by("apellido")
    page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
    try:
        paginator = Paginator(socios, 10)  # 6 usuarios por página
        socios = paginator.page(page)
    except PageNotAnInteger:
            raise Http404

    return render(request, 'socios/mostrarSocios.html', {"entity":socios, "paginator":paginator, "num_inscripcion":inscripcion_total})

def actualizar_Socio(request, socioid):
    socio = Socios.objects.filter(id = socioid).first()
    if socio.socio is True:
        if request.method == 'POST':
            socio_form = SocioForm(request.POST, instance=socio)

            if socio_form.is_valid():
                user = socio_form.save(commit=False)
                user.save()
                if socio_form.cleaned_data["socio"] is True:
                    total = Socios.objects.filter(socio = True).count()
                    socio.numero_socio = total
                    socio.save()
                else:
                    socio.numero_socio = 0
                    socio.save()

                return redirect('Listar Socios')

        else:
            socio_form = SocioForm(instance=socio)

        return render(request, 'socios/actualizarSocio.html', {'formulario': socio_form})
    else:
        if request.method == 'POST':
            socio_form = NoSocioForm(request.POST, instance=socio)

            if socio_form.is_valid():
                user = socio_form.save(commit=False)
                user.save()
                if socio_form.cleaned_data["socio"] is True:
                    total = Socios.objects.filter(socio = True).count()
                    socio.numero_socio = total
                    socio.save()
                else:
                    socio.numero_socio = 0
                    socio.save()

                return redirect('Listar Socios')

        else:
            socio_form = NoSocioForm(instance=socio)

        return render(request, 'socios/actualizarNoSocio.html', {'formulario': socio_form})

        

def crear_Socio(request):

    if request.method == 'POST':
        socio_form = SocioForm(request.POST)

        if socio_form.is_valid():
            nombre = socio_form.cleaned_data['nombre']
            apellido = socio_form.cleaned_data['apellido']
            dni = socio_form.cleaned_data['dni']
            fecha_nacimiento = socio_form.cleaned_data['fecha_nacimiento']
            telefono = socio_form.cleaned_data['telefono']
            codigo_postal = socio_form.cleaned_data['codigo_postal']
            ciudad = socio_form.cleaned_data['ciudad']
            provincia = socio_form.cleaned_data['provincia']
            socio = socio_form.cleaned_data['socio']
            talla_camiseta = socio_form.cleaned_data['talla_camiseta']
            regalo = socio_form.cleaned_data['regalo']
            total = Socios.objects.filter(socio = True).count()
            if socio is True:
                numero_socio = total+1
            else:
                numero_socio = 0
            Socios.objects.create(numero_socio = numero_socio,
                                    nombre = nombre.upper(), 
                                    apellido=apellido.upper(), 
                                    dni = dni, 
                                    fecha_nacimiento = fecha_nacimiento, 
                                    telefono=telefono, 
                                    codigo_postal = codigo_postal, 
                                    ciudad = ciudad, 
                                    provincia = provincia,
                                    socio = socio,
                                    regalo = regalo)
            

            return redirect('Listar Socios')

    else:
        socio_form = SocioForm()

        return render(request, 'socios/añadirSocios.html', {'formulario': socio_form})
    

def buscar(request):
    if "usern" in request.GET:
        user = request.GET["usern"]
        if user is None or user == "":
            return redirect('Listar Socios')
        elif len(user) > 100:
            return render(request, 'Listar Socios')
        else:
            user = user.upper()
            usuario = Socios.objects.filter(Q(apellido__icontains=user)| Q(numero_socio__icontains=user))
            page = request.GET.get('page', 1)
            try:
                paginator = Paginator(usuario, 12)  # 6 usuarios por página
                usuario = paginator.page(page)
            except PageNotAnInteger:
                raise Http404

            return render(request, "socios/busquedaSocio.html", {"entity": usuario, "paginator":paginator})
    else:
        return redirect('Listar Socios')
    
def calcular_suma(request):
    total_socios = 0
    total_no_socios = 0
    inscripciones = Inscripciones.objects.all()
    for ins in inscripciones:
        inscripciones_socio = Inscripcion_Socio.objects.filter(inscripcion = ins)
        for inso in inscripciones_socio:
            if inso.socios.socio is True:
                total_socios += inso.precio
            else:
                total_no_socios += inso.precio
        
        ins.recaudacion_socios = total_socios
        ins.recaudacion_no_socios = total_no_socios
        ins.save()
    return print("Todo correcto")
    
def listar_incripciones_abiertas(request):
    calcular_suma(request)
    inscripciones = Inscripciones.objects.filter(finalizada = False)
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
            ins = inscripcion_form.save(commit=False)
            ins.save()
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
    socio = Socios.objects.filter(id = socioid).first()
    inscripcion = Inscripciones.objects.filter(finalizada = False).first()
    if socio.socio is True:
        precio = inscripcion.precio_socio
    else:
        precio = inscripcion.precio_no_socio
    if request.method == 'POST':
        inscripcion_form = Inscripcion_SocioForm(request.POST)

        if inscripcion_form.is_valid():
            asiento_bus = inscripcion_form.cleaned_data['asiento_bus']
            inscripcion_socio = Inscripcion_Socio.objects.filter(inscripcion = inscripcion)
            ocupado = any(i.asiento_bus == asiento_bus for i in inscripcion_socio)
            repite = Inscripcion_Socio.objects.filter(inscripcion = inscripcion, socios = socio).count()
            print(repite)
            if repite != 0:
                mensaje = "Usuario ya Inscripto en ruta"
                return render(request, 'socios/crearInscripcionSocio.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":mensaje})
            if ocupado:
                mensaje = "Asiento ocupado"
                return render(request, 'socios/crearInscripcionSocio.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":mensaje})
            else:
                if asiento_bus <= 55:
                    numero_bus = 1
                else:
                    numero_bus = 2
                Inscripcion_Socio.objects.create(inscripcion = inscripcion, 
                                    socios = socio, 
                                    precio = precio, 
                                    numero_bus = numero_bus, 
                                    asiento_bus= asiento_bus)
            

            return redirect('Listar Socios')
    else:
        inscripcion_form = Inscripcion_SocioForm()

    return render(request, 'socios/crearInscripcionSocio.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":mensaje})
    
def crear_inscripcion_socio_b(request, socioid):
    mensaje = None
    socio = Socios.objects.filter(id = socioid).first()
    inscripcion = Inscripciones.objects.filter(finalizada = False).first()
    if socio.socio is True:
        precio = inscripcion.precio_socio
    else:
        precio = inscripcion.precio_no_socio
    if request.method == 'POST':
        inscripcion_form = Inscripcion_Socio_B_Form(request.POST)

        if inscripcion_form.is_valid():
            asiento_bus = inscripcion_form.cleaned_data['asiento_bus']
            inscripcion_socio = Inscripcion_Socio.objects.filter(inscripcion = inscripcion)
            ocupado = any(i.asiento_bus == asiento_bus for i in inscripcion_socio)
            repite = Inscripcion_Socio.objects.filter(inscripcion = inscripcion, socios = socio).count()
            print(repite)
            if repite != 0:
                mensaje = "Usuario ya Inscripto en ruta"
                return render(request, 'socios/crearInscripcionSocio.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":mensaje})
            if ocupado:
                mensaje = "Asiento ocupado"
                return render(request, 'socios/crearInscripcionSocio.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":mensaje})
            elif asiento_bus < 21:
                mensaje = "La incripcion comienza a partir del asiento 21"
                return render(request, 'socios/crearInscripcionSocio.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":mensaje})
            else:
                if asiento_bus <= 55:
                    numero_bus = 1
                else:
                    numero_bus = 2
                Inscripcion_Socio.objects.create(inscripcion = inscripcion, 
                                    socios = socio, 
                                    precio = precio, 
                                    numero_bus = numero_bus, 
                                    asiento_bus= asiento_bus)
            

            return redirect('Listar Socios')
    else:
        inscripcion_form = Inscripcion_Socio_B_Form()

    return render(request, 'socios/crearInscripcionSocioB.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":mensaje})
    

def listar_inscritos(request, insid):

    inscripcion = Inscripciones.objects.filter(id = insid).first()
    nombre = inscripcion.nombre
    inscripcion_socio = Inscripcion_Socio.objects.filter(inscripcion = inscripcion).order_by("asiento_bus")
    page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
    try:
        paginator = Paginator(inscripcion_socio, 12)  # 6 usuarios por página
        inscripcion_socio = paginator.page(page)
        
    except PageNotAnInteger:
            raise Http404

    return render(request, 'socios/mostrarInscripcionSocio.html', {'entity': inscripcion_socio, "paginator":paginator, "nombre":nombre})


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
            ins = inscripcion_socio.filter(Q(socios__apellido__icontains=user)|Q(socios__numero_socio__icontains=user))
            page = request.GET.get('page', 1)
            try:
                paginator = Paginator(ins, 12)  # 6 usuarios por página
                ins = paginator.page(page)
            except PageNotAnInteger:
                raise Http404

            return render(request, "socios/busquedaInscripcionSocio.html", {"entity": ins, "paginator":paginator, "nombre":nombre})
    else:
        return redirect('Incripciones Abiertas')
    

def calcular_suma(request):
    total_socios = 0
    total_no_socios = 0
    inscripciones = Inscripciones.objects.all()
    for ins in inscripciones:
        inscripciones_socio = Inscripcion_Socio.objects.filter(inscripcion = ins)
        for inso in inscripciones_socio:
            if inso.socios.socio is True:
                total_socios += inso.precio
            else:
                total_no_socios += inso.precio
        
        ins.recaudacion_socios = total_socios
        ins.recaudacion_no_socios = total_no_socios
        ins.save()
    return print("Todo correcto")


def exportar_socios_a_Pdf(request, insid):
    actualDate = datetime.now().date()
    inscripcion = Inscripciones.objects.filter(id = insid).first()
    nombre = inscripcion.nombre
    queryset = Inscripcion_Socio.objects.filter(inscripcion = inscripcion).order_by("socios__apellido")
    filename = "Usuarios Inscritos"
    

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
            "Nº Socio",
            "Apellido",
            "Nombre",
            "Teléfono",
            "Regalo",
        ]
    ]

    for socio in queryset:
        table_row = [
            (
                socio.socios.numero_socio
                
            ),
            (
                socio.socios.apellido
            ),
            (
                socio.socios.nombre

            ),
            (
                socio.socios.telefono
            ),
            (
                socio.socios.regalo
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
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
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


def exportar_socios_a_Pdf_v2(request, insid):
    actualDate = datetime.now().date()
    inscripcion = Inscripciones.objects.filter(id = insid).first()
    nombre = inscripcion.nombre
    queryset = Inscripcion_Socio.objects.filter(inscripcion = inscripcion).order_by("-socios__apellido")
    filename = "Usuarios Inscritos"
    

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
            "Apellido",
            "Nombre",
            "DNI"
        ]
    ]

    for socio in queryset:
        table_row = [
            (
                socio.socios.apellido
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
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
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

def exportar_tiket_socios_a_Pdf_v2(request, insid, socioid):
    actualDate = datetime.now().date()
    inscripcion = Inscripciones.objects.filter(id=insid).first()
    nombre = inscripcion.nombre
    socios = Inscripcion_Socio.objects.filter(inscripcion=inscripcion, socios__id = socioid)
    filename = "Tique_Usuarios_Inscritos"
    
    # Response Object
    response_pdf = HttpResponse(content_type="application/pdf")
    response_pdf["Content-Disposition"] = f"attachment; filename={filename}.pdf"
    styles = getSampleStyleSheet()

    # Custom style for subtitles
    subtitle_style = ParagraphStyle(name="Subtitle", parent=styles["Heading2"], fontSize=12, spaceAfter=6)

    # This is the PDF document
    doc = SimpleDocTemplate(response_pdf, pagesize=A6, rightMargin=inch/4, leftMargin=inch/4, topMargin=inch/4, bottomMargin=inch/4)

    # Create a Story list to hold elements
    Story = []

    # Add tique elements with subtitles
    title = f"Usuarios Inscritos"
    actualDateText = f"Fecha: {actualDate}"

    tique_elements = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 12),
        Paragraph("Información General", subtitle_style),
        Paragraph(actualDateText, styles["Normal"]),
        Spacer(1, 12),
        Paragraph("Detalles de Socio", subtitle_style),
        Spacer(1, 6),
    ]
    
    # Add tique elements to the Story
    Story.extend(tique_elements)

    # Add details of each socio
    for socio in socios:
        socio_details = [
            Paragraph(f"Nº Socio: {socio.socios.numero_socio}", styles["Normal"]),
            Paragraph(f"Apellido: {socio.socios.apellido}", styles["Normal"]),
            Paragraph(f"Nombre: {socio.socios.nombre}", styles["Normal"]),
            Paragraph(f"DNI: {socio.socios.dni}", styles["Normal"]),
            Spacer(1, 6),
        ]
        Story.extend(socio_details)

    doc.build(Story)

    return response_pdf

    return response_pdf