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
# Create your views here.

def cargarSocios(request):
    Socios.objects.all().delete()
    path3 = "data/socios.csv"
    with open(path3, newline='', encoding='utf-8-sig') as csvfile:
        lector_csv = csv.DictReader(csvfile, delimiter=';')
        for numero_fila, fila in enumerate(lector_csv, start=1):
            try:
                apellidos = fila['Apellido']
                nombre = fila['Nombre']
                dni = fila['DNI']
                fecha = fila['Fecha']
                telefono = fila['Telefono']
                codigo_postal = fila['CP']
                ciudad = fila['Ciudad']
                provincia = fila['Provincia']
                Socios.objects.create(nombre = nombre, 
                                      apellidos=apellidos, 
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

    total_inscripcion = Inscripciones.objects.filter(finalizada = False).count()
    inscripcion = Inscripciones.objects.filter(finalizada = False).first()
    if inscripcion is None:
        nombre = "NO CREADA"
    else:
        nombre = inscripcion.nombre
    socios = Socios.objects.all().order_by("apellidos")

    return render(request, 'socios/mostrarSocios.html', {"entity":socios, "nombre":nombre, "num_inscripcion":total_inscripcion})

def actualizar_Socio(request, socioid):
    socio = Socios.objects.filter(id = socioid).first()
    socio_b = socio.socio
    num = socio.numero_socio
    if socio.socio is True:
        if request.method == 'POST':
            socio_form = SocioForm(request.POST, instance=socio)

            if socio_form.is_valid():
                socio_form.save()
                socio.nombre = socio.nombre.upper()
                socio.apellidos = socio.apellidos.upper()
                socio.save()
                if socio.socio is False:
                    socio.regalo = False
                    socio.numero_socio = 0
                    socio.save()

                if socio.socio is True:
                    return redirect('Mostrar Usuarios Socios')
                else:
                    return redirect('Listar Socios')

        else:
            socio_form = SocioForm(instance=socio)

        return render(request, 'socios/actualizarSocio.html', {'formulario': socio_form})
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
            return render(request, "socios/busquedaSocio.html", {"entity": usuario, "num_inscripcion":total_inscripcion})
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
        inscripcion_form = InscripcionFormA(request.POST, instance=inscripcion)

        if inscripcion_form.is_valid():
            inscripcion_form.save()

        return redirect('Incripciones Abiertas')

    else:
        inscripcion_form = InscripcionFormA(instance=inscripcion)

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
    total = 0
    total_intermedio = []
    total_intermedio_dividido = set()
    aparece_socio = Inscripcion_Socio.objects.filter(inscripcion__finalizada = False).order_by("-asiento_bus").first()
    if aparece_socio:
        total = aparece_socio.asiento_bus + 1
    else:
        total = 0

    aparece_socio_intermedio = Inscripcion_Socio.objects.filter(inscripcion__finalizada = False).order_by("asiento_bus")
    j= 1
    if len(aparece_socio_intermedio) > 0:

        for i in aparece_socio_intermedio:
            primero = i.asiento_bus
            for j in range(primero):
                if aparece_socio_intermedio.filter(asiento_bus = j):
                    pass
                else:
                    total_intermedio_dividido.add(j)
        if len(total_intermedio_dividido) > 1:
            total_intermedio_dividido = list(total_intermedio_dividido)
            inicio = total_intermedio_dividido[1]
            for x in range(1, len(total_intermedio_dividido)):
                if total_intermedio_dividido[x] != total_intermedio_dividido[x-1]+1:
                    total_intermedio.append((inicio, total_intermedio_dividido[x-1]))
                    inicio = total_intermedio_dividido[x]

            total_intermedio.append((inicio, total_intermedio_dividido[-1]))


    socio = Socios.objects.filter(id = socioid).first()
    inscripcion = Inscripciones.objects.filter(finalizada = False).first()
    if socio.socio is True:
        precio = inscripcion.precio_socio
    else:
        precio = inscripcion.precio_no_socio
    if request.method == 'POST':
        inscripcion_form = Inscripcion_SocioForm(request.POST)

        if inscripcion_form.is_valid():
            if inscripcion_form.cleaned_data['guia'] is True:
                precio = 0
            elif socio.socio is True:
                precio = inscripcion.precio_socio
            elif socio.socio is False:
                precio = inscripcion.precio_no_socio
            asiento_bus = inscripcion_form.cleaned_data['asiento_bus']
            inscripcion_socio = Inscripcion_Socio.objects.filter(inscripcion = inscripcion)
            ocupado = any(i.asiento_bus == asiento_bus for i in inscripcion_socio)
            repite = Inscripcion_Socio.objects.filter(inscripcion = inscripcion, socios = socio).count()
            print(repite)
            if repite != 0:
                mensaje = "Usuario ya Inscripto en ruta"
                return render(request, 'socios/crearInscripcionSocio.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":mensaje, "total":total, "total_intermedio":total_intermedio})
            if ocupado:
                mensaje = "Asiento ocupado"
                return render(request, 'socios/crearInscripcionSocio.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":mensaje, "total":total, "total_intermedio":total_intermedio})
            else:
                if asiento_bus <= 55:
                    numero_bus = 1
                else:
                    numero_bus = 2
                Inscripcion_Socio.objects.create(inscripcion = inscripcion, 
                                    socios = socio, 
                                    precio = precio, 
                                    numero_bus = numero_bus, 
                                    asiento_bus= asiento_bus,
                                    pago = True,
                                    guia = inscripcion_form.cleaned_data['guia'])
            

            return redirect('Usuarios Inscritos',inscripcion.id)
            
    else:
        inscripcion_form = Inscripcion_SocioForm()

        return render(request, 'socios/crearInscripcionSocio.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":mensaje, "total":total, "total_intermedio":total_intermedio})


def crear_inscripcion_socio_b(request, socioid):
    precio = 0
    mensaje = 0
    total = 0
    total_intermedio = []
    total_intermedio_dividido = set()
    aparece_socio = Inscripcion_Socio.objects.filter(inscripcion__finalizada = False).order_by("-asiento_bus").first()
    if aparece_socio:
        total = aparece_socio.asiento_bus + 1
    else:
        total = 0

    aparece_socio_intermedio = Inscripcion_Socio.objects.filter(inscripcion__finalizada = False).order_by("asiento_bus")
    j= 1
    if len(aparece_socio_intermedio) > 0:

        for i in aparece_socio_intermedio:
            primero = i.asiento_bus
            for j in range(primero):
                if aparece_socio_intermedio.filter(asiento_bus = j):
                    pass
                else:
                    total_intermedio_dividido.add(j)
        if len(total_intermedio_dividido) > 1:
            total_intermedio_dividido = list(total_intermedio_dividido)
            inicio = total_intermedio_dividido[1]
            for x in range(1, len(total_intermedio_dividido)):
                if total_intermedio_dividido[x] != total_intermedio_dividido[x-1]+1:
                    total_intermedio.append((inicio, total_intermedio_dividido[x-1]))
                    inicio = total_intermedio_dividido[x]

            total_intermedio.append((inicio, total_intermedio_dividido[-1]))


    socio = Socios.objects.filter(id = socioid).first()
    inscripcion = Inscripciones.objects.filter(finalizada = False).first()
    if socio.socio is True:
        precio = inscripcion.precio_socio
    else:
        precio = inscripcion.precio_no_socio
    if request.method == 'POST':
        inscripcion_form = Inscripcion_SocioForm(request.POST)

        if inscripcion_form.is_valid():
            if inscripcion_form.cleaned_data['guia'] is True:
                precio = 0

            elif socio.socio is True:
                precio = inscripcion.precio_socio
            elif socio.socio is False:
                precio = inscripcion.precio_no_socio
            asiento_bus = inscripcion_form.cleaned_data['asiento_bus']
            inscripcion_socio = Inscripcion_Socio.objects.filter(inscripcion = inscripcion)
            ocupado = any(i.asiento_bus == asiento_bus for i in inscripcion_socio)
            repite = Inscripcion_Socio.objects.filter(inscripcion = inscripcion, socios = socio).count()
            print(repite)
            if repite != 0:
                return render(request, 'socios/crearInscripcionSociob.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":"Usuario ya Inscripto en ruta", "total":total, "total_intermedio":total_intermedio})
            if ocupado:
                return render(request, 'socios/crearInscripcionSocioB.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":"Asiento ocupado", "total":total, "total_intermedio":total_itermedio})
            #elif asiento_bus < 21:

            #    return render(request, 'socios/crearInscripcionSocioB.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":"La Inscripción comienza a partir del asiento 21", "total":total, "total_itermedio":total_itermedio})
            else:
                if asiento_bus <= 55:
                    numero_bus = 1
                else:
                    numero_bus = 2
                Inscripcion_Socio.objects.create(inscripcion = inscripcion, 
                                    socios = socio, 
                                    precio = precio, 
                                    numero_bus = numero_bus, 
                                    asiento_bus= asiento_bus,
                                    pago = False,
                                    guia = inscripcion_form.cleaned_data['guia'])
            

            return redirect('Usuarios Inscritos',inscripcion.id)
            
    else:
        inscripcion_form = Inscripcion_SocioForm()

        return render(request, 'socios/crearInscripcionSocioB.html', {'formulario': inscripcion_form, "socio":socio, "inscripcion":inscripcion, "precio":precio, "mensaje":mensaje, "total":total, "total_intermedio":total_intermedio})
    

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

def exportar_tiket_socios_a_Pdf_v2(request, insid, socioid):
    actualDate = datetime.now().date()
    inscripcion = Inscripciones.objects.filter(id=insid).first()
    nombre = inscripcion.nombre
    socios = Inscripcion_Socio.objects.filter(inscripcion=inscripcion, socios__id=socioid)
    filename = f"tique {nombre}"

    # Response Object
    response_pdf = HttpResponse(content_type="application/pdf")
    response_pdf["Content-Disposition"] = f"attachment; filename={filename}.pdf"
    styles = getSampleStyleSheet()

    # Custom style for subtitles
    subtitle_style = ParagraphStyle(name="Subtitle", parent=styles["Heading2"], fontSize=12, spaceAfter=-10)
    ubtitle_style = ParagraphStyle(name="Subtitle", fontSize=9)
    

    # This is the PDF document
    doc = SimpleDocTemplate(response_pdf, pagesize=A4, rightMargin=inch/500, leftMargin=inch/500, topMargin=inch/4, bottomMargin=inch/4)

    # Create a Story list to hold elements
    Story = []

    # Add tique elements with subtitles
    logoPath_pdf = "media/img/logo_t.png"
    logo_pdf = AlignedImage(logoPath_pdf, width=190, height=70, hAlign='LEFT')
    actualDateText = f"Fecha: {actualDate}"
    for socio in socios:
        if socio.socios.socio is True:
            num = socio.socios.numero_socio
        else:
            num = ""
        asiento = 0
        if socio.numero_bus == 1:
            asiento = socio.asiento_bus
        else:
            asiento = socio.asiento_bus - 55

        tique_elements = [
            logo_pdf,
            Paragraph(f"Ruta: {inscripcion.nombre}", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Fecha: {inscripcion.fecha}", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Bus: {socio.numero_bus} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Asiento: {asiento}", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Cuota:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{socio.precio}€", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Nº Socio: {num}", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Nombre: {socio.socios.nombre}",styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"apellidos: {socio.socios.apellidos}", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Tfn: {socio.socios.telefono} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DNI: {socio.socios.dni}", styles["Normal"]),
            Spacer(1, 12),
            Paragraph(f"Firma: ", styles["Normal"]),
            Spacer(1, 60),
            Paragraph(f"__________________________________________", styles["Normal"]),
            Spacer(1, 20),
            PageBreak(),
            logo_pdf,
            Paragraph(f"Ruta: {inscripcion.nombre}", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Fecha: {inscripcion.fecha}", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Bus: {socio.numero_bus} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Asiento: {asiento}", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Cuota:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{socio.precio}€", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Nº Socio: {num}", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Nombre: {socio.socios.nombre}",styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"apellidos: {socio.socios.apellidos}", styles["Normal"]),
            Spacer(1, 6),
            Paragraph(f"Tfn: {socio.socios.telefono} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DNI: {socio.socios.dni}", styles["Normal"]),
            Paragraph(f"Advertencia Legal", subtitle_style),
            Paragraph(
                """El senderismo y/o montañismo son deportes<br/>
                   inherentemente con riesgos en mayor o menor<br/> 
                   medida,al desarrollarse en un entorno como<br/>
                   es el medio natural, y dependientes del estado<br/> 
                   físico de cada participante, además de su<br/>
                   equipación, técnicas e inclemencia del tiempo.<br/>
                   Su práctica conlleva la aceptación de este hecho,<br/>
                   recomendando encarecidamente estar<br/>
                   preparados para la actividad.<br/>
                   La presente ruta es una actividad<br/>
                   organizada por lo tanto el participante se<br/> 
                   somete a la reglamentación existente e<br/>
                   indicaciones de la organización.<br/> 
                   Acepto que mi imagen pueda<br/>
                   aparecer en las fotos que se puedan compartir<br/>
                   en los espacios virtuales, cuyo propósito es la<br/> 
                   difusión de las actividades que<br/> 
                   la asociación realice.""",
                ubtitle_style
            ),
        ]

    # Add tique elements to the Story
    Story.extend(tique_elements)

    doc.build(Story)

    return response_pdf

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
            return render(request, "socios/busquedaSocioSocio.html", {"entity": usuario})
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