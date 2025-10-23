from flask import Blueprint, request, jsonify
from database import XMLDatabase 
from services import XMLParser

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