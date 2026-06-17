"""Pruebas unitarias para los modelos"""
import pytest
import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import (
    Hospital, Sala, Camara, SensorTemperatura, 
    RegistroTemperatura, Usuario, Alerta, Estadistica
)
from datetime import datetime, date

class TestHospitalModel:
    def test_hospital_creation(self):
        hospital = Hospital(
            nombre="Hospital General",
            direccion="Calle Principal 123",
            telefono="1234567890",
            email="hospital@example.com"
        )
        
        assert hospital.nombre == "Hospital General"
        assert hospital.direccion == "Calle Principal 123"
        assert hospital.telefono == "1234567890"
        assert hospital.email == "hospital@example.com"
    
    def test_hospital_to_dict(self):
        hospital = Hospital("Test Hospital")
        result = hospital.to_dict()
        
        assert result['nombre'] == "Test Hospital"
        assert 'created_at' in result

class TestSalaModel:
    def test_sala_creation(self):
        sala = Sala(
            hospital_id=1,
            nombre="Sala de Cuidados Intensivos",
            tipo="UCI",
            capacidad=10
        )
        
        assert sala.hospital_id == 1
        assert sala.nombre == "Sala de Cuidados Intensivos"
        assert sala.tipo == "UCI"
        assert sala.capacidad == 10
    
    def test_sala_to_dict(self):
        sala = Sala(1, "Test Sala")
        result = sala.to_dict()
        
        assert result['hospital_id'] == 1
        assert result['nombre'] == "Test Sala"

class TestCamaraModel:
    def test_camara_creation(self):
        camara = Camara(
            sala_id=1,
            nombre="Cámara 101",
            tipo="Estándar"
        )
        
        assert camara.sala_id == 1
        assert camara.nombre == "Cámara 101"
        assert camara.disponible == True
    
    def test_camara_ocupada(self):
        camara = Camara(1, "Cámara 101", disponible=False, ocupada_por=5)
        assert camara.disponible == False
        assert camara.ocupada_por == 5

class TestSensorTemperaturaModel:
    def test_sensor_creation(self):
        sensor = SensorTemperatura(
            sala_id=1,
            nombre="Sensor Refrigerador",
            ubicacion="Esquina norte",
            temp_min=2,
            temp_max=8
        )
        
        assert sensor.sala_id == 1
        assert sensor.nombre == "Sensor Refrigerador"
        assert sensor.temperatura_minima == 2
        assert sensor.temperatura_maxima == 8
        assert sensor.alerta_activa == False
    
    def test_sensor_to_dict(self):
        sensor = SensorTemperatura(1, "Test Sensor", temp_min=0, temp_max=25)
        result = sensor.to_dict()
        
        assert result['nombre'] == "Test Sensor"
        assert result['alerta_activa'] == False

class TestRegistroTemperaturaModel:
    def test_registro_creation(self):
        registro = RegistroTemperatura(
            sensor_id=1,
            temperatura=5.5,
            estado="NORMAL"
        )
        
        assert registro.sensor_id == 1
        assert registro.temperatura == 5.5
        assert registro.estado == "NORMAL"
    
    def test_registro_to_dict(self):
        registro = RegistroTemperatura(1, 10.0)
        result = registro.to_dict()
        
        assert result['sensor_id'] == 1
        assert result['temperatura'] == 10.0

class TestUsuarioModel:
    def test_usuario_creation(self):
        usuario = Usuario(
            hospital_id=1,
            nombre="Dr. Juan Pérez",
            email="juan@hospital.com",
            rol="medico"
        )
        
        assert usuario.hospital_id == 1
        assert usuario.nombre == "Dr. Juan Pérez"
        assert usuario.email == "juan@hospital.com"
        assert usuario.rol == "medico"
        assert usuario.activo == True
    
    def test_usuario_diferentes_roles(self):
        roles = ["medico", "enfermero", "administrador"]
        for rol in roles:
            usuario = Usuario(1, "Test", "test@test.com", rol)
            assert usuario.rol == rol

class TestAlertaModel:
    def test_alerta_creation(self):
        alerta = Alerta(
            sensor_id=1,
            tipo="TEMPERATURA_FUERA_DE_RANGO",
            mensaje="Temperatura muy alta"
        )
        
        assert alerta.sensor_id == 1
        assert alerta.tipo == "TEMPERATURA_FUERA_DE_RANGO"
        assert alerta.enviada == False
    
    def test_alerta_to_dict(self):
        alerta = Alerta(1, "TEST_ALERT")
        result = alerta.to_dict()
        
        assert result['enviada'] == False
        assert result['tipo'] == "TEST_ALERT"

class TestEstadisticaModel:
    def test_estadistica_creation(self):
        estadistica = Estadistica(
            hospital_id=1,
            fecha=date(2024, 1, 15),
            total_camaras=50,
            camaras_ocupadas=35,
            camaras_disponibles=15,
            temperatura_promedio=5.5,
            alertas_totales=2
        )
        
        assert estadistica.hospital_id == 1
        assert estadistica.total_camaras == 50
        assert estadistica.camaras_ocupadas == 35
        assert estadistica.camaras_disponibles == 15
    
    def test_estadistica_to_dict(self):
        estadistica = Estadistica(1, date(2024, 1, 1), 10, 5, 5, 4.5, 1)
        result = estadistica.to_dict()
        
        assert result['hospital_id'] == 1
        assert result['total_camaras'] == 10

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
