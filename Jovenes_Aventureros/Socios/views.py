from django.shortcuts import render, HttpResponse, redirect
import csv
from .models import *
from django.http import Http404
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger
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
    socios = Socios.objects.all().order_by("apellido")
    page = request.GET.get('page', 1)  # Obtener el número de página de la solicitud GET
    try:
        paginator = Paginator(socios, 12)  # 6 usuarios por página
        socios = paginator.page(page)
    except PageNotAnInteger:
            raise Http404

    return render(request, 'socios/mostrarSocios.html', {"entity":socios, "paginator":paginator})

def actualizar_Socio(request, socioid):
    socio = Socios.objects.filter(id = socioid).first()

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
                total = Socios.objects.filter(socio = True).count()
                socio.numero_socio = total
                socio.save()

            return redirect('Listar Socios')

    else:
        socio_form = SocioForm(instance=socio)

        return render(request, 'socios/actualizarDatos.html', {'formulario': socio_form})
    

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
            total = Socios.objects.filter(socio = True).count()
            if socio is True:
                numero_socio = total+1
            else:
                numero_socio = 0
            Socios.objects.create(numero_socio = numero_socio,
                                    nombre = nombre, 
                                    apellido=apellido, 
                                    dni = dni, 
                                    fecha_nacimiento = fecha_nacimiento, 
                                    telefono=telefono, 
                                    codigo_postal = codigo_postal, 
                                    ciudad = ciudad, 
                                    provincia = provincia,
                                    socio = socio,
                                    talla_camiseta = talla_camiseta)
            

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
            usuario = Socios.objects.filter(Q(apellido__icontains=user)| Q(numero_socio = user))
            return render(request, "socios/busquedaSocio.html", {"entity": usuario})
    else:
        return redirect('Listar Socios')
