from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.

def home(request):
    imagen_url = obtener_imagen_web_BeautifulSoup()
    print(imagen_url)
    return render(request, "socios/mostrarSocios.html", {"imagen_url": imagen_url})

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






