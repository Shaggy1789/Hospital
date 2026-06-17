"""Rutas para gestión de temperatura y alertas"""
from flask import Blueprint, request, jsonify
from app.services import SensorTemperaturaService, AlertaService
from datetime import datetime
import traceback

temperature_bp = Blueprint('temperature', __name__, url_prefix='/api/temperature')

@temperature_bp.route('/sensors', methods=['POST'])
def crear_sensor():
    """Crear un nuevo sensor de temperatura"""
    try:
        data = request.json
        sala_id = data.get('sala_id')
        nombre = data.get('nombre')
        ubicacion = data.get('ubicacion')
        temp_min = data.get('temperatura_minima')
        temp_max = data.get('temperatura_maxima')
        
        if not sala_id or not nombre:
            return jsonify({'error': 'sala_id y nombre son requeridos'}), 400
        
        sensor_id = SensorTemperaturaService.crear_sensor(sala_id, nombre, ubicacion, temp_min, temp_max)
        return jsonify({
            'message': 'Sensor creado exitosamente',
            'id': sensor_id
        }), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@temperature_bp.route('/sensors/<int:sala_id>', methods=['GET'])
def obtener_sensores_sala(sala_id):
    """Obtener todos los sensores de una sala"""
    try:
        sensores = SensorTemperaturaService.obtener_sensores_por_sala(sala_id)
        return jsonify(sensores), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@temperature_bp.route('/sensors/<int:sensor_id>/current', methods=['GET'])
def obtener_temperatura_actual(sensor_id):
    """Obtener temperatura actual de un sensor"""
    try:
        temp = SensorTemperaturaService.obtener_temperatura_actual(sensor_id)
        if not temp:
            return jsonify({'error': 'Sensor no encontrado'}), 404
        return jsonify(temp), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@temperature_bp.route('/sensors/<int:sensor_id>/update', methods=['POST'])
def actualizar_temperatura(sensor_id):
    """Actualizar temperatura de un sensor"""
    try:
        data = request.json
        temperatura = data.get('temperatura')
        
        if temperatura is None:
            return jsonify({'error': 'temperatura es requerida'}), 400
        
        # Obtener rango de temperatura del sensor
        sensor = SensorTemperaturaService.obtener_sensor(sensor_id)
        if not sensor:
            return jsonify({'error': 'Sensor no encontrado'}), 404
        
        SensorTemperaturaService.actualizar_temperatura(sensor_id, temperatura)
        
        # Verificar si está fuera de rango
        if temperatura < sensor['temperatura_minima'] or temperatura > sensor['temperatura_maxima']:
            AlertaService.crear_alerta(
                sensor_id,
                'TEMPERATURA_FUERA_DE_RANGO',
                f'Temperatura {temperatura}°C fuera del rango permitido ({sensor["temperatura_minima"]}°C - {sensor["temperatura_maxima"]}°C)'
            )
        
        return jsonify({'message': 'Temperatura actualizada exitosamente'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@temperature_bp.route('/alerts/hospital/<int:hospital_id>', methods=['GET'])
def obtener_alertas_activas(hospital_id):
    """Obtener alertas activas de un hospital"""
    try:
        alertas = AlertaService.obtener_alertas_activas(hospital_id)
        return jsonify(alertas), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@temperature_bp.route('/alerts/<int:alerta_id>/mark-sent', methods=['POST'])
def marcar_alerta_enviada(alerta_id):
    """Marcar una alerta como enviada"""
    try:
        AlertaService.marcar_alerta_enviada(alerta_id)
        return jsonify({'message': 'Alerta marcada como enviada'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
