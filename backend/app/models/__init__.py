"""Modelos de datos para el sistema hospitalario"""
from datetime import datetime

class Hospital:
    def __init__(self, nombre, direccion=None, telefono=None, email=None, id=None):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Sala:
    def __init__(self, hospital_id, nombre, tipo=None, capacidad=None, id=None):
        self.id = id
        self.hospital_id = hospital_id
        self.nombre = nombre
        self.tipo = tipo
        self.capacidad = capacidad
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'capacidad': self.capacidad,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Camara:
    def __init__(self, sala_id, nombre, tipo=None, disponible=True, ocupada_por=None, id=None):
        self.id = id
        self.sala_id = sala_id
        self.nombre = nombre
        self.tipo = tipo
        self.disponible = disponible
        self.ocupada_por = ocupada_por
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'sala_id': self.sala_id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'disponible': self.disponible,
            'ocupada_por': self.ocupada_por,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SensorTemperatura:
    def __init__(self, sala_id, nombre, ubicacion=None, temp_min=None, temp_max=None, id=None):
        self.id = id
        self.sala_id = sala_id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.temperatura_actual = None
        self.temperatura_minima = temp_min
        self.temperatura_maxima = temp_max
        self.alerta_activa = False
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'sala_id': self.sala_id,
            'nombre': self.nombre,
            'ubicacion': self.ubicacion,
            'temperatura_actual': self.temperatura_actual,
            'temperatura_minima': self.temperatura_minima,
            'temperatura_maxima': self.temperatura_maxima,
            'alerta_activa': self.alerta_activa,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class RegistroTemperatura:
    def __init__(self, sensor_id, temperatura, estado=None, id=None):
        self.id = id
        self.sensor_id = sensor_id
        self.temperatura = temperatura
        self.estado = estado
        self.timestamp = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'temperatura': self.temperatura,
            'estado': self.estado,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class Usuario:
    def __init__(self, hospital_id, nombre, email, rol, activo=True, id=None):
        self.id = id
        self.hospital_id = hospital_id
        self.nombre = nombre
        self.email = email
        self.rol = rol  # 'medico', 'enfermero', 'administrador'
        self.activo = activo
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Alerta:
    def __init__(self, sensor_id, tipo, mensaje=None, id=None):
        self.id = id
        self.sensor_id = sensor_id
        self.tipo = tipo
        self.mensaje = mensaje
        self.enviada = False
        self.fecha_alerta = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'tipo': self.tipo,
            'mensaje': self.mensaje,
            'enviada': self.enviada,
            'fecha_alerta': self.fecha_alerta.isoformat() if self.fecha_alerta else None
        }

class Estadistica:
    def __init__(self, hospital_id, fecha, total_camaras=0, camaras_ocupadas=0, 
                 camaras_disponibles=0, temperatura_promedio=None, alertas_totales=0, id=None):
        self.id = id
        self.hospital_id = hospital_id
        self.fecha = fecha
        self.total_camaras = total_camaras
        self.camaras_ocupadas = camaras_ocupadas
        self.camaras_disponibles = camaras_disponibles
        self.temperatura_promedio = temperatura_promedio
        self.alertas_totales = alertas_totales
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'fecha': self.fecha.isoformat() if hasattr(self.fecha, 'isoformat') else str(self.fecha),
            'total_camaras': self.total_camaras,
            'camaras_ocupadas': self.camaras_ocupadas,
            'camaras_disponibles': self.camaras_disponibles,
            'temperatura_promedio': self.temperatura_promedio,
            'alertas_totales': self.alertas_totales,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
