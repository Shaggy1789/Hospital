"""Rutas para gestión de hospitales"""
from flask import Blueprint, request, jsonify
from app.services import HospitalService
import traceback

hospitals_bp = Blueprint('hospitals', __name__, url_prefix='/api/hospitals')

@hospitals_bp.route('/', methods=['POST'])
def crear_hospital():
    """Crear un nuevo hospital"""
    try:
        data = request.json
        nombre = data.get('nombre')
        direccion = data.get('direccion')
        telefono = data.get('telefono')
        email = data.get('email')
        
        if not nombre:
            return jsonify({'error': 'El nombre del hospital es requerido'}), 400
        
        hospital_id = HospitalService.crear_hospital(nombre, direccion, telefono, email)
        return jsonify({
            'message': 'Hospital creado exitosamente',
            'id': hospital_id
        }), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@hospitals_bp.route('/', methods=['GET'])
def obtener_hospitales():
    """Obtener todos los hospitales"""
    try:
        hospitales = HospitalService.obtener_todos_hospitales()
        return jsonify(hospitales), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@hospitals_bp.route('/<int:hospital_id>', methods=['GET'])
def obtener_hospital(hospital_id):
    """Obtener un hospital específico"""
    try:
        hospital = HospitalService.obtener_hospital(hospital_id)
        if not hospital:
            return jsonify({'error': 'Hospital no encontrado'}), 404
        return jsonify(hospital), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@hospitals_bp.route('/<int:hospital_id>', methods=['PUT'])
def actualizar_hospital(hospital_id):
    """Actualizar un hospital"""
    try:
        data = request.json
        HospitalService.actualizar_hospital(
            hospital_id,
            data.get('nombre'),
            data.get('direccion'),
            data.get('telefono'),
            data.get('email')
        )
        return jsonify({'message': 'Hospital actualizado exitosamente'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@hospitals_bp.route('/<int:hospital_id>', methods=['DELETE'])
def eliminar_hospital(hospital_id):
    """Eliminar un hospital"""
    try:
        HospitalService.eliminar_hospital(hospital_id)
        return jsonify({'message': 'Hospital eliminado exitosamente'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
