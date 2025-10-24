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

        if not uploaded.name.lower().endswith('.xml'):
            messages.error(request, "El archivo debe tener extensión .xml.")
            return redirect('home')
        
        try:
            file_bytes = uploaded.read().decode('utf-8') 
            headers = {'Content-Type': 'application/xml'}
            resp = requests.post(f"{API_URL}/api/configuracion", data=file_bytes, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()

                success_message = f"""
                XML '{uploaded.name}' procesado correctamente:
                {data['data']['recursos']} recursos creados | 
                {data['data']['categorias']} categorías creadas | 
                {data['data']['configuraciones']} configuraciones creadas | 
                {data['data']['clientes']} clientes creados |
                {data['data']['instancias']} instancias creadas """

                if data['data']['errores']:
                    success_message += f"\n Se encontraron {len(data['data']['errores'])} advertencias"
                messages.success(request, success_message)
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

        if not uploaded.name.lower().endswith('.xml'):
            messages.error(request, "El archivo debe tener extensión .xml.")
            return redirect('home')
        
        try:
            file_bytes = uploaded.read().decode('utf-8') 
            headers = {'Content-Type': 'application/xml'}
            resp = requests.post(f"{API_URL}/api/consumos", data=file_bytes, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                
                success_message = f"""
                XML '{uploaded.name}' procesado correctamente:
                {data['data']['consumos']} consumos procesados. """

                if data['data']['errores']:
                    success_message += f"\n Se encontraron {len(data['data']['errores'])} advertencias"
                messages.success(request, success_message)
            else:
                messages.error(request, f'Error del backend: {resp.status_code} - {resp.text}')
        except requests.RequestException as e:
            messages.error(request, f'Error de conexión con el backend: {e}')

    return render(request, 'index.html')

def consultar_datos(request):
    try:
        resp = requests.get(f"{API_URL}/api/sistema/consultar", timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            messages.success(request, "Datos consultados correctamente")
            return render(request, 'consultar.html', {'datos_consultados': data['data']})
    except requests.RequestException as e:
        messages.error(request, f'Error de conexión con el backend: {e}')

    return redirect('home')

def inicializar_sistema(request):
    if request.method == 'POST':
        try:
            resp = requests.post(f"{API_URL}/api/sistema/inicializar", timeout=15)
            if resp.status_code == 200:
                messages.success(request, "Sistema inicializado correctamente")
            else:
                messages.error(request, f'Error del backend: {resp.status_code} - {resp.text}')
        except requests.RequestException as e:
            messages.error(request, f'Error de conexión con el backend: {e}')

    return redirect('home')

def menu_creacion(request):
    return render(request, 'menu_creacion.html')

def crear_categoria(request):
    if request.method == 'POST':
        payload = {
            "tipo": "categoria",
            "id_Categoria": request.POST.get('id'),
            "nombre": request.POST.get('nombre'),
            "descripcion": request.POST.get('descripcion'),
            "carga_trabajo": request.POST.get('carga_trabajo'),
        }
        resp = requests.post(f"{API_URL}/api/sistema/menu_creacion/crear/categoria", json=payload)
        
        if resp.status_code == 200:
            messages.success(request, "Categoría creada correctamente.")
        elif resp.status_code == 409:
            messages.warning(request, "Ya existe una categoría con ese ID.")
        else:
            messages.error(request, "Error al crear categoría.")
    return render(request, 'crear_categoria.html')
