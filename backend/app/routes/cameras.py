"""Rutas para gestión de salas y cámaras"""
from flask import Blueprint, request, jsonify
from app.services import SalaService, CamaraService
import traceback

cameras_bp = Blueprint('cameras', __name__, url_prefix='/api/cameras')

# RUTAS DE SALAS
@cameras_bp.route('/salas', methods=['POST'])
def crear_sala():
    """Crear una nueva sala"""
    try:
        data = request.json
        hospital_id = data.get('hospital_id')
        nombre = data.get('nombre')
        tipo = data.get('tipo')
        capacidad = data.get('capacidad')
        
        if not hospital_id or not nombre:
            return jsonify({'error': 'hospital_id y nombre son requeridos'}), 400
        
        sala_id = SalaService.crear_sala(hospital_id, nombre, tipo, capacidad)
        return jsonify({
            'message': 'Sala creada exitosamente',
            'id': sala_id
        }), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@cameras_bp.route('/salas/hospital/<int:hospital_id>', methods=['GET'])
def obtener_salas_hospital(hospital_id):
    """Obtener todas las salas de un hospital"""
    try:
        salas = SalaService.obtener_salas_por_hospital(hospital_id)
        return jsonify(salas), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@cameras_bp.route('/salas/<int:sala_id>', methods=['GET'])
def obtener_sala(sala_id):
    """Obtener una sala específica"""
    try:
        sala = SalaService.obtener_sala(sala_id)
        if not sala:
            return jsonify({'error': 'Sala no encontrada'}), 404
        return jsonify(sala), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# RUTAS DE CÁMARAS
@cameras_bp.route('/', methods=['POST'])
def crear_camara():
    """Crear una nueva cámara"""
    try:
        data = request.json
        sala_id = data.get('sala_id')
        nombre = data.get('nombre')
        tipo = data.get('tipo')
        
        if not sala_id or not nombre:
            return jsonify({'error': 'sala_id y nombre son requeridos'}), 400
        
        camara_id = CamaraService.crear_camara(sala_id, nombre, tipo)
        return jsonify({
            'message': 'Cámara creada exitosamente',
            'id': camara_id
        }), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@cameras_bp.route('/sala/<int:sala_id>', methods=['GET'])
def obtener_camaras_sala(sala_id):
    """Obtener todas las cámaras de una sala"""
    try:
        camaras = CamaraService.obtener_camaras_por_sala(sala_id)
        return jsonify(camaras), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@cameras_bp.route('/disponibles/<int:sala_id>', methods=['GET'])
def obtener_camaras_disponibles(sala_id):
    """Obtener cámaras disponibles de una sala"""
    try:
        camaras = CamaraService.obtener_camaras_disponibles(sala_id)
        return jsonify(camaras), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@cameras_bp.route('/<int:camara_id>/ocupar', methods=['POST'])
def ocupar_camara(camara_id):
    """Ocupar una cámara"""
    try:
        data = request.json
        paciente_id = data.get('paciente_id')
        CamaraService.ocupar_camara(camara_id, paciente_id)
        return jsonify({'message': 'Cámara ocupada exitosamente'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@cameras_bp.route('/<int:camara_id>/liberar', methods=['POST'])
def liberar_camara(camara_id):
    """Liberar una cámara"""
    try:
        CamaraService.liberar_camara(camara_id)
        return jsonify({'message': 'Cámara liberada exitosamente'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
