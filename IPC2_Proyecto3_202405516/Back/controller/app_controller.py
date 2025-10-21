from flask import Blueprint, request, jsonify

app_bp = Blueprint('app', __name__)

@app_bp.get('/status')
def get_status():
    return jsonify({"status": "Todo funcionando correctamente"}), 200