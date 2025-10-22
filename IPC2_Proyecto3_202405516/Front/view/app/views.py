from django.shortcuts import render, redirect
from django.contrib import messages
import requests

API_URL = "http://localhost:5000"

# Create your views here.
def home(request):
    return render(request, 'index.html')

def enviar_configuracion(request):
    if request.method == 'POST':
        if 'xml_file_config' not in request.FILES:
            messages.error(request, "No se ha seleccionado ningún archivo.")
            return redirect('home') 
        uploaded = request.FILES['xml_file_config']

        try:
            file_bytes = uploaded.read().decode('utf-8') 
            if not file_bytes.strip().startswith('<?xml'):
                messages.error(request, "El archivo no es un XML válido.")
                return redirect('home')
        except Exception as e:
            messages.error(request, f"Error al leer el archivo: {str(e)}")
            return redirect('home')
        
        try:
            headers = {'Content-Type': 'application/xml'}
            resp = requests.post(f"{API_URL}/api/configuracion", data=file_bytes, headers=headers, timeout=15)
            if resp.status_code == 200:
                messages.success(request, f'XML procesado correctamente: {resp.text}')
            else:
                messages.error(request, f'Error del backend: {resp.status_code} - {resp.text}')
        except requests.RequestException as e:
            messages.error(request, f'Error de conexión con el backend: {e}')

    return render(request, 'index.html')

def enviar_consumos(request):
    if request.method == 'POST':
        if 'xml_file_consumos' not in request.FILES:
            messages.error(request, "No se ha seleccionado ningún archivo.")
            return redirect('home') 
        uploaded = request.FILES['xml_file_consumos']

        try:
            file_bytes = uploaded.read().decode('utf-8') 
            if not file_bytes.strip().startswith('<?xml'):
                messages.error(request, "El archivo no es un XML válido.")
                return redirect('home')
        except Exception as e:
            messages.error(request, f"Error al leer el archivo: {str(e)}")
            return redirect('home')
        
        try:
            headers = {'Content-Type': 'application/xml'}
            resp = requests.post(f"{API_URL}/api/consumos", data=file_bytes, headers=headers, timeout=15)
            if resp.status_code == 200:
                messages.success(request, f'XML de consumos procesado correctamente: {resp.text}')
            else:
                messages.error(request, f'Error del backend: {resp.status_code} - {resp.text}')
        except requests.RequestException as e:
            messages.error(request, f'Error de conexión con el backend: {e}')

    return render(request, 'index.html')
