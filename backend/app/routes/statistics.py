"""Rutas para estadísticas"""
from flask import Blueprint, request, jsonify
from app.services import EstadisticaService
import traceback

statistics_bp = Blueprint('statistics', __name__, url_prefix='/api/statistics')

@statistics_bp.route('/', methods=['POST'])
def crear_estadistica():
    """Crear una nueva estadística"""
    try:
        data = request.json
        hospital_id = data.get('hospital_id')
        fecha = data.get('fecha')
        total_camaras = data.get('total_camaras', 0)
        camaras_ocupadas = data.get('camaras_ocupadas', 0)
        camaras_disponibles = data.get('camaras_disponibles', 0)
        temperatura_promedio = data.get('temperatura_promedio')
        alertas_totales = data.get('alertas_totales', 0)
        
        if not hospital_id or not fecha:
            return jsonify({'error': 'hospital_id y fecha son requeridos'}), 400
        
        stat_id = EstadisticaService.crear_estadistica(
            hospital_id, fecha, total_camaras, camaras_ocupadas,
            camaras_disponibles, temperatura_promedio, alertas_totales
        )
        return jsonify({
            'message': 'Estadística creada exitosamente',
            'id': stat_id
        }), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@statistics_bp.route('/hospital/<int:hospital_id>', methods=['GET'])
def obtener_estadisticas(hospital_id):
    """Obtener estadísticas de un hospital"""
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({'error': 'fecha_inicio y fecha_fin son requeridas'}), 400
        
        estadisticas = EstadisticaService.obtener_estadisticas_hospital(hospital_id, fecha_inicio, fecha_fin)
        return jsonify(estadisticas), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@statistics_bp.route('/hospital/<int:hospital_id>/latest', methods=['GET'])
def obtener_ultima_estadistica(hospital_id):
    """Obtener la última estadística de un hospital"""
    try:
        estadistica = EstadisticaService.obtener_ultima_estadistica(hospital_id)
        if not estadistica:
            return jsonify({'error': 'No hay estadísticas disponibles'}), 404
        return jsonify(estadistica), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
