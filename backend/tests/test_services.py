"""Pruebas unitarias para los servicios"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services import (
    HospitalService, SalaService, CamaraService,
    SensorTemperaturaService, AlertaService, EstadisticaService
)

class TestHospitalService:
    @patch('app.services.db')
    def test_crear_hospital(self, mock_db):
        mock_db.execute_query.return_value = 1
        
        result = HospitalService.crear_hospital(
            "Hospital Test", "Calle 1", "123456", "test@test.com"
        )
        
        assert result == 1
        mock_db.execute_query.assert_called_once()
    
    @patch('app.services.db')
    def test_obtener_hospital(self, mock_db):
        mock_db.fetch_one.return_value = {'id': 1, 'nombre': 'Test Hospital'}
        
        result = HospitalService.obtener_hospital(1)
        
        assert result['nombre'] == 'Test Hospital'
        mock_db.fetch_one.assert_called_once()
    
    @patch('app.services.db')
    def test_obtener_todos_hospitales(self, mock_db):
        mock_db.fetch_query.return_value = [
            {'id': 1, 'nombre': 'Hospital 1'},
            {'id': 2, 'nombre': 'Hospital 2'}
        ]
        
        result = HospitalService.obtener_todos_hospitales()
        
        assert len(result) == 2
        mock_db.fetch_query.assert_called_once()

class TestSalaService:
    @patch('app.services.db')
    def test_crear_sala(self, mock_db):
        mock_db.execute_query.return_value = 1
        
        result = SalaService.crear_sala(1, "Sala UCI", "UCI", 10)
        
        assert result == 1
        mock_db.execute_query.assert_called_once()
    
    @patch('app.services.db')
    def test_obtener_salas_por_hospital(self, mock_db):
        mock_db.fetch_query.return_value = [
            {'id': 1, 'nombre': 'Sala 1'},
            {'id': 2, 'nombre': 'Sala 2'}
        ]
        
        result = SalaService.obtener_salas_por_hospital(1)
        
        assert len(result) == 2

class TestCamaraService:
    @patch('app.services.db')
    def test_crear_camara(self, mock_db):
        mock_db.execute_query.return_value = 1
        
        result = CamaraService.crear_camara(1, "Cámara 101", "Estándar")
        
        assert result == 1
    
    @patch('app.services.db')
    def test_obtener_camaras_disponibles(self, mock_db):
        mock_db.fetch_query.return_value = [
            {'id': 1, 'nombre': 'Cámara 1', 'disponible': True},
        ]
        
        result = CamaraService.obtener_camaras_disponibles(1)
        
        assert len(result) == 1
        assert result[0]['disponible'] == True
    
    @patch('app.services.db')
    def test_ocupar_camara(self, mock_db):
        CamaraService.ocupar_camara(1, 5)
        mock_db.execute_query.assert_called_once()
    
    @patch('app.services.db')
    def test_liberar_camara(self, mock_db):
        CamaraService.liberar_camara(1)
        mock_db.execute_query.assert_called_once()

class TestSensorTemperaturaService:
    @patch('app.services.db')
    def test_crear_sensor(self, mock_db):
        mock_db.execute_query.return_value = 1
        
        result = SensorTemperaturaService.crear_sensor(1, "Sensor 1", "Ubicación", 2, 8)
        
        assert result == 1
    
    @patch('app.services.db')
    def test_obtener_temperatura_actual(self, mock_db):
        mock_db.fetch_one.return_value = {
            'temperatura_actual': 5.5,
            'temperatura_minima': 2,
            'temperatura_maxima': 8
        }
        
        result = SensorTemperaturaService.obtener_temperatura_actual(1)
        
        assert result['temperatura_actual'] == 5.5
    
    @patch('app.services.db')
    def test_actualizar_temperatura(self, mock_db):
        SensorTemperaturaService.actualizar_temperatura(1, 6.5)
        mock_db.execute_query.assert_called_once()

class TestAlertaService:
    @patch('app.services.db')
    def test_crear_alerta(self, mock_db):
        mock_db.execute_query.return_value = 1
        
        result = AlertaService.crear_alerta(1, "TEMPERATURA_ALTA", "Mensaje alerta")
        
        assert result == 1
    
    @patch('app.services.db')
    def test_marcar_alerta_enviada(self, mock_db):
        AlertaService.marcar_alerta_enviada(1)
        mock_db.execute_query.assert_called_once()

class TestEstadisticaService:
    @patch('app.services.db')
    def test_crear_estadistica(self, mock_db):
        mock_db.execute_query.return_value = 1
        
        result = EstadisticaService.crear_estadistica(
            1, '2024-01-15', 50, 35, 15, 5.5, 2
        )
        
        assert result == 1

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
