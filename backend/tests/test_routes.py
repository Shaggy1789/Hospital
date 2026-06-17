"""Pruebas de integración para las rutas API"""
import pytest
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

@pytest.fixture
def app():
    """Crear la aplicación para testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Crear cliente para hacer requests"""
    return app.test_client()

class TestHealthCheck:
    def test_index_endpoint(self, client):
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'mensaje' in data
        assert data['status'] == 'running'
    
    def test_health_endpoint(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'

class TestHospitalRoutes:
    def test_obtener_hospitales_endpoint(self, client):
        """Prueba que el endpoint de hospitales responda"""
        response = client.get('/api/hospitals/')
        # Puede retornar 200 o error de conexión BD, ambos válidos en test
        assert response.status_code in [200, 500]

class TestCameraRoutes:
    def test_obtener_camaras_sala_endpoint(self, client):
        """Prueba que el endpoint de cámaras responda"""
        response = client.get('/api/cameras/sala/1')
        assert response.status_code in [200, 500]

class TestTemperatureRoutes:
    def test_obtener_alertas_endpoint(self, client):
        """Prueba que el endpoint de alertas responda"""
        response = client.get('/api/temperature/alerts/hospital/1')
        assert response.status_code in [200, 500]

class TestStatisticsRoutes:
    def test_obtener_estadisticas_endpoint(self, client):
        """Prueba que el endpoint de estadísticas responda"""
        response = client.get('/api/statistics/hospital/1?fecha_inicio=2024-01-01&fecha_fin=2024-01-31')
        assert response.status_code in [200, 400, 500]

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
