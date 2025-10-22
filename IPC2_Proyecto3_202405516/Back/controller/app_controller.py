from flask import Blueprint, request, jsonify
from database import XMLDatabase 
from services import XMLParser

app_bp = Blueprint('app', __name__)

db = XMLDatabase()
db.initialize_database()
parser = XMLParser()

@app_bp.get('/status')
def get_status():
    return jsonify({"status": "Todo funcionando correctamente"}), 200

@app_bp.post('/api/configuracion')
def recibir_configuracion():
    try:
        xml_content = request.data.decode('utf-8')
        resultados = parser.procesar_configuracion(xml_content)

        data = {
            'recursos': len(resultados['recursos_procesados']),
            'categorias': len(resultados['categorias_procesadas']),
            'clientes': len(resultados['clientes_procesados']),
            'errores': resultados['errores']
        }

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

        return jsonify({"status": "success", "message": "Consumos recibidos", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400