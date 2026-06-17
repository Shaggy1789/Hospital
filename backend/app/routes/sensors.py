"""Rutas para datos simulados de sensores"""
from flask import Blueprint, jsonify
from app.mock_data import MockDataGenerator

sensors_bp = Blueprint('sensors', __name__, url_prefix='/api/sensors')

@sensors_bp.route('/hospital/<int:hospital_id>', methods=['GET'])
def obtener_sensores_hospital(hospital_id):
    """Obtener sensores simulados de un hospital"""
    try:
        sensores = []
        salas = MockDataGenerator.generar_salas(hospital_id)
        
        for sala in salas:
            sensores.extend(MockDataGenerator.generar_sensores(sala['id']))
        
        return jsonify(sensores), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sensors_bp.route('/sala/<int:sala_id>', methods=['GET'])
def obtener_sensores_sala(sala_id):
    """Obtener sensores simulados de una sala"""
    try:
        sensores = MockDataGenerator.generar_sensores(sala_id)
        return jsonify(sensores), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sensors_bp.route('/<int:sensor_id>/lectura', methods=['GET'])
def obtener_lectura_sensor(sensor_id):
    """Obtener lectura simulada de un sensor"""
    try:
        lectura = MockDataGenerator.simular_temperatura()
        lectura['sensor_id'] = sensor_id
        return jsonify(lectura), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sensors_bp.route('/hospitales/lista', methods=['GET'])
def listar_hospitales():
    """Obtener lista de hospitales simulados"""
    try:
        hospitales = MockDataGenerator.generar_hospitales()
        return jsonify(hospitales), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sensors_bp.route('/<int:hospital_id>/alertas', methods=['GET'])
def obtener_alertas(hospital_id):
    """Obtener alertas simuladas de un hospital"""
    try:
        alertas = MockDataGenerator.generar_alertas(hospital_id)
        return jsonify(alertas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
