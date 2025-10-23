from flask import Blueprint, request, jsonify
from database import XMLDatabase 
from services import XMLParser
import xml.etree.ElementTree as ET

app_bp = Blueprint('app', __name__)

db = XMLDatabase()
parser = XMLParser()

@app_bp.get('/status')
def get_status():
    return jsonify({"status": "Todo funcionando correctamente"}), 200

@app_bp.post('/api/configuracion')
def recibir_configuracion():
    try:
        xml_content = request.data.decode('utf-8')
        resultados = parser.procesar_informacion(xml_content)

        data = {
            'recursos': len(resultados['recursos_procesados']),
            'categorias': len(resultados['categorias_procesadas']),
            'clientes': len(resultados['clientes_procesados']),
            'instancias': len(resultados['instancias_procesadas']),
            'configuraciones': len(resultados['configuraciones_procesadas']),
            'errores': resultados['errores']
        }

        for recurso in resultados['recursos_procesados']:
            db.guardar_recurso(recurso.to_dict())
        
        for cliente in resultados['clientes_procesados']:
            db.guardar_cliente(cliente.to_dict())

        for categoria in resultados['categorias_procesadas']:
            db.guardar_categoria(categoria.to_dict())

        for configuracion in resultados['configuraciones_procesadas']:
            db.guardar_configuracion(configuracion.to_dict())
            for id_recurso, cantidad in configuracion.recursos.items():
                db.guardar_configuracion_recurso(configuracion.id_configuracion, id_recurso, cantidad)
        
        for instancia in resultados['instancias_procesadas']:
            db.guardar_instancia(instancia.to_dict())

        return jsonify({"status": "success", "message": "Configuración recibida", "data": data}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    
@app_bp.post('/api/consumos')    
def recibir_consumos():
    try:
        xml_content = request.data.decode('utf-8')
        resultados = parser.procesar_consumos(xml_content)
        
        data = {
            'consumos': len(resultados['consumos_procesados']),
            'errores': resultados['errores']
        }

        for consumo in resultados['consumos_procesados']:
            db.guardar_consumo(consumo.to_dict())

        return jsonify({"status": "success", "message": "Consumos recibidos", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    
@app_bp.post('/api/sistema/inicializar')
def inicializar_sistema():
    if db.inicializar_sistema():
        return jsonify({"status": "success", "message": "Sistema inicializado correctamente"}), 200
    else:
        return jsonify({"status": "error", "message": "Error al inicializar sistema"}), 500
    
@app_bp.get('/api/sistema/consultar')
def consultar_datos():
    import xml.etree.ElementTree as ET

    try:
        datos = {
            'categorias': [],
            'recursos': [],
            'configuraciones': [],
            'clientes': [],
            'instancias': [],
            'consumos': []
        }

        def safe_text(elem, tag):
            nodo = elem.find(tag)
            return nodo.text if nodo is not None else ""

        # Categorías
        try:
            tree = ET.parse(db.get_file_path('categorias.xml'))
            for elem in tree.getroot().findall('categoria'):
                datos['categorias'].append({
                    'id': elem.get('id'),
                    'nombre': safe_text(elem, 'nombre'),
                    'descripcion': safe_text(elem, 'descripcion'),
                    'cargaTrabajo': safe_text(elem, 'cargaTrabajo')
                })
        except Exception:
            pass

        # Recursos
        try:
            tree = ET.parse(db.get_file_path('recursos.xml'))
            for elem in tree.getroot().findall('recurso'):
                datos['recursos'].append({
                    'id': elem.get('id'),
                    'nombre': safe_text(elem, 'nombre'),
                    'abreviatura': safe_text(elem, 'abreviatura'),
                    'metrica': safe_text(elem, 'metrica'),
                    'tipo': safe_text(elem, 'tipo'),
                    'valorXhora': safe_text(elem, 'valorXhora')
                })
        except Exception:
            pass

        # Configuraciones
        try:
            tree = ET.parse(db.get_file_path('configuraciones.xml'))
            for elem in tree.getroot().findall('configuracion'):
                datos['configuraciones'].append({
                    'id': elem.get('id'),
                    'idCategoria': elem.get('idCategoria', ''),
                    'nombre': safe_text(elem, 'nombre'),
                    'descripcion': safe_text(elem, 'descripcion')
                })
        except Exception:
            pass

        # Clientes
        try:
            tree = ET.parse(db.get_file_path('clientes.xml'))
            for elem in tree.getroot().findall('cliente'):
                datos['clientes'].append({
                    'nit': elem.get('nit'),
                    'nombre': safe_text(elem, 'nombre'),
                    'usuario': safe_text(elem, 'usuario'),
                    'direccion': safe_text(elem, 'direccion'),
                    'correo': safe_text(elem, 'correoElectronico')
                })
        except Exception:
            pass

        # Instancias
        try:
            tree = ET.parse(db.get_file_path('instancias.xml'))
            for elem in tree.getroot().findall('instancia'):
                datos['instancias'].append({
                    'id': elem.get('id'),
                    'nitCliente': elem.get('nitCliente', ''),
                    'idConfiguracion': safe_text(elem, 'idConfiguracion'),
                    'nombre': safe_text(elem, 'nombre'),
                    'fechaInicio': safe_text(elem, 'fechaInicio'),
                    'estado': safe_text(elem, 'estado'),
                    'fechaFinal': safe_text(elem, 'fechaFinal')
                })
        except Exception:
            pass

        # Consumos
        try:
            tree = ET.parse(db.get_file_path('consumos.xml'))
            for elem in tree.getroot().findall('consumo'):
                datos['consumos'].append({
                    'nitCliente': elem.get('nitCliente'),
                    'idInstancia': elem.get('idInstancia'),
                    'tiempo': safe_text(elem, 'tiempo'),
                    'fechaHora': safe_text(elem, 'fechahora')
                })
        except Exception:
            pass

        return jsonify({"status": "success", "data": datos}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

