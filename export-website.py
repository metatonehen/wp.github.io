#!/usr/bin/env python
import os
import shutil
import json
from flask import render_template
from main import app
from routes import *

"""
Script para exportar el sitio METATONEHEN como páginas HTML estáticas
"""

# Carpeta donde se guardarán los archivos exportados
EXPORT_DIR = 'website_export'

# Asegurarse de que la carpeta de exportación exista
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

# Crear carpetas necesarias
os.makedirs(os.path.join(EXPORT_DIR, 'css'), exist_ok=True)
os.makedirs(os.path.join(EXPORT_DIR, 'js'), exist_ok=True)
os.makedirs(os.path.join(EXPORT_DIR, 'images'), exist_ok=True)
os.makedirs(os.path.join(EXPORT_DIR, 'uploads'), exist_ok=True)
os.makedirs(os.path.join(EXPORT_DIR, 'fonts'), exist_ok=True)

# Copiar archivos estáticos
def copy_static_files():
    # Copiar CSS
    for file in os.listdir('static/css'):
        if file.endswith('.css'):
            shutil.copy2(os.path.join('static/css', file), 
                         os.path.join(EXPORT_DIR, 'css', file))
    
    # Copiar JS
    for file in os.listdir('static/js'):
        if file.endswith('.js'):
            shutil.copy2(os.path.join('static/js', file), 
                         os.path.join(EXPORT_DIR, 'js', file))
    
    # Copiar imágenes
    for file in os.listdir('static/images'):
        src_path = os.path.join('static/images', file)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, os.path.join(EXPORT_DIR, 'images', file))
    
    # Copiar fuentes si existen
    if os.path.exists('static/fonts'):
        for file in os.listdir('static/fonts'):
            src_path = os.path.join('static/fonts', file)
            if os.path.isfile(src_path):
                shutil.copy2(src_path, os.path.join(EXPORT_DIR, 'fonts', file))

    # Copiar archivos de uploads si existen
    if os.path.exists('static/uploads'):
        for file in os.listdir('static/uploads'):
            src_path = os.path.join('static/uploads', file)
            if os.path.isfile(src_path):
                shutil.copy2(src_path, os.path.join(EXPORT_DIR, 'uploads', file))

# Modificar URLs en archivos CSS para que apunten correctamente
def fix_css_urls():
    for file in os.listdir(os.path.join(EXPORT_DIR, 'css')):
        if file.endswith('.css'):
            css_path = os.path.join(EXPORT_DIR, 'css', file)
            with open(css_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reemplazar referencias a URL Flask por rutas relativas
            content = content.replace("url_for('static', filename='", "../")
            content = content.replace("')", "")
            
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(content)

# Modificar URLs en archivos HTML para que apunten correctamente
def fix_html_urls(html_content):
    # Reemplazar URL Flask por rutas relativas
    html_content = html_content.replace("{{ url_for('static', filename='css/", "css/")
    html_content = html_content.replace("{{ url_for('static', filename='js/", "js/")
    html_content = html_content.replace("{{ url_for('static', filename='images/", "images/")
    html_content = html_content.replace("{{ url_for('static', filename='uploads/", "uploads/")
    html_content = html_content.replace("{{ url_for('static', filename='fonts/", "fonts/")
    
    # Reemplazar enlaces a rutas de Flask
    html_content = html_content.replace("{{ url_for('index') }}", "index.html")
    html_content = html_content.replace("{{ url_for('courses') }}", "courses.html")
    html_content = html_content.replace("{{ url_for('sessions') }}", "sessions.html")
    html_content = html_content.replace("{{ url_for('group_sessions') }}", "group_sessions.html")
    html_content = html_content.replace("{{ url_for('memberships') }}", "memberships.html")
    html_content = html_content.replace("{{ url_for('natal_chart') }}", "natal_chart.html")
    html_content = html_content.replace("{{ url_for('human_design') }}", "human_design.html")
    html_content = html_content.replace("{{ url_for('blog') }}", "blog.html")
    html_content = html_content.replace("{{ url_for('about') }}", "about.html")
    html_content = html_content.replace("{{ url_for('contact') }}", "contact.html")
    
    # Cerrar sintaxis Jinja que quedó abierta
    html_content = html_content.replace("') }}", "")
    html_content = html_content.replace('" %}', "")
    
    return html_content

# Generar las páginas HTML estáticas
def generate_html_pages():
    # Lista de rutas y sus nombres de archivo correspondientes
    pages = [
        ('index', 'index.html', index),
        ('courses', 'courses.html', courses),
        ('sessions', 'sessions.html', sessions),
        ('group_sessions', 'group_sessions.html', group_sessions),
        ('memberships', 'memberships.html', memberships),
        ('natal_chart', 'natal_chart.html', natal_chart),
        ('human_design', 'human_design.html', human_design),
        ('blog', 'blog.html', blog),
        ('about', 'about.html', about),
        ('contact', 'contact.html', contact)
    ]
    
    # Crear una dummy request para usar en las funciones de las rutas
    with app.test_request_context():
        for route_name, filename, view_func in pages:
            print(f"Generando {filename}...")
            try:
                # Llamar a la función de vista para obtener el contenido renderizado
                # Utilizamos un try-except ya que algunas funciones de vista pueden 
                # requerir parámetros o tener lógica específica
                template_name = f"{route_name}.html"
                
                # En lugar de llamar a la función de vista, renderizamos directamente la plantilla
                # con datos de prueba básicos para cada página
                template_data = {
                    'content': {},
                    'session': {'language': 'en'},
                    'featured_courses': [],
                    'testimonials': []
                }
                
                html_content = render_template(template_name, **template_data)
                
                # Arreglar URLs para que funcionen como sitio estático
                html_content = fix_html_urls(html_content)
                
                # Guardar el archivo HTML
                with open(os.path.join(EXPORT_DIR, filename), 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"✓ {filename} generado correctamente")
            except Exception as e:
                print(f"Error generando {filename}: {str(e)}")

# Función principal
def export_website():
    print("Exportando sitio web METATONEHEN...")
    
    # Copiar archivos estáticos
    print("Copiando archivos estáticos...")
    copy_static_files()
    
    # Arreglar URLs en CSS
    print("Arreglando URLs en archivos CSS...")
    fix_css_urls()
    
    # Generar páginas HTML
    print("Generando páginas HTML...")
    generate_html_pages()
    
    print("\nExportación completada!")
    print(f"El sitio web ha sido exportado a la carpeta: {EXPORT_DIR}")
    print("Ahora puedes subir estos archivos a cualquier hosting para publicar tu sitio web.")

if __name__ == "__main__":
    export_website()