#!/usr/bin/env python
"""Script para ejecutar la aplicación como aplicación de escritorio"""

import os
import sys
import webbrowser
import threading
import time

def main():
    # Obtener el directorio donde está el ejecutable
    if getattr(sys, 'frozen', False):
        # Estamos en un ejecutable de PyInstaller
        project_dir = os.path.dirname(sys.executable)
    else:
        # Estamos en desarrollo
        project_dir = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(project_dir)
    
    # Configurar entorno Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jovenes_Aventureros.settings')
    os.environ['DEBUG'] = 'True'
    
    # Abrir navegador después de un momento
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://127.0.0.1:8000")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Configurar y ejecutar Django
    try:
        import django
        from django.core.management import call_command
        
        django.setup()
        
        print("\n" + "="*50)
        print("Iniciando Jóvenes Aventureros...")
        print("La aplicación se abrirá en su navegador.")
        print("No cierre esta ventana mientras use la aplicación.")
        print("Para cerrar, presione Ctrl+C")
        print("="*50 + "\n")
        
        # Ejecutar migraciones
        call_command("migrate", interactive=False)
        
        # Iniciar servidor
        call_command("runserver", "127.0.0.1:8000", use_reloader=False)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCerrando aplicación...")
        sys.exit(0)