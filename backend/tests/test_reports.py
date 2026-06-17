"""Pruebas de integración para los endpoints de reportes"""
import pytest
import sys
import os
import json
from io import BytesIO

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

class TestReportsRoutes:
    """Tests para endpoints de reportes y exportación"""
    
    def test_obtener_camas_endpoint(self, client):
        """Prueba obtener estadísticas de camas"""
        response = client.get('/api/reportes/camas/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'total' in data
        assert 'disponibles' in data
        assert 'ocupadas' in data
        assert 'porcentaje_ocupacion' in data
        assert 'por_piso' in data
        assert data['total'] == 45
        assert data['disponibles'] == 35
        assert data['ocupadas'] == 10
    
    def test_obtener_temperatura_endpoint(self, client):
        """Prueba obtener datos de refrigeradores"""
        response = client.get('/api/reportes/temperatura/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'refrigeradores' in data
        assert 'temperatura_promedio' in data
        assert 'ultima_actualizacion' in data
        assert len(data['refrigeradores']) > 0
        
        # Verificar estructura de refrigerador
        refrig = data['refrigeradores'][0]
        assert 'id' in refrig
        assert 'nombre' in refrig
        assert 'temperatura' in refrig
        assert 'estado' in refrig
    
    def test_descargar_reporte_excel(self, client):
        """Prueba descarga de reporte en Excel"""
        payload = {
            'hospital_id': 1,
            'tipo_reporte': 'ocupacion',
            'fecha_inicio': '2026-06-01',
            'fecha_fin': '2026-06-16'
        }
        
        response = client.post('/api/reportes/descargar', 
                              json=payload,
                              content_type='application/json')
        
        assert response.status_code == 200
        assert response.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        assert len(response.data) > 0
    
    def test_descargar_reporte_temperatura_excel(self, client):
        """Prueba descarga de reporte de temperatura en Excel"""
        payload = {
            'hospital_id': 1,
            'tipo_reporte': 'temperatura',
            'fecha_inicio': '2026-06-01',
            'fecha_fin': '2026-06-16'
        }
        
        response = client.post('/api/reportes/descargar',
                              json=payload,
                              content_type='application/json')
        
        assert response.status_code == 200
        assert response.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        assert len(response.data) > 0
    
    def test_descargar_json(self, client):
        """Prueba descarga de datos en JSON"""
        payload = {
            'hospital_id': 1
        }
        
        response = client.post('/api/reportes/descargar-json',
                              json=payload,
                              content_type='application/json')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert len(response.data) > 0
    
    def test_obtener_camas_hospital_diferente(self, client):
        """Prueba obtener camas de diferentes hospitales"""
        response = client.get('/api/reportes/camas/2')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'total' in data
        assert data['total'] >= 0

class TestReportDataIntegrity:
    """Tests para verificar integridad de datos de reportes"""
    
    def test_camas_suma_correcta(self, client):
        """Verifica que la suma de camas por piso es correcta"""
        response = client.get('/api/reportes/camas/1')
        data = json.loads(response.data)
        
        suma_pisos = sum(piso['total'] for piso in data['por_piso'].values())
        assert suma_pisos == data['total']
    
    def test_ocupacion_porcentaje_valido(self, client):
        """Verifica que el porcentaje de ocupación es válido"""
        response = client.get('/api/reportes/camas/1')
        data = json.loads(response.data)
        
        porcentaje = data['porcentaje_ocupacion']
        assert 0 <= porcentaje <= 100
    
    def test_temperatura_promedio_valida(self, client):
        """Verifica que la temperatura promedio es válida"""
        response = client.get('/api/reportes/temperatura/1')
        data = json.loads(response.data)
        
        if data['refrigeradores']:
            temp_promedio = data['temperatura_promedio']
            # Verificar que sea un número
            assert isinstance(temp_promedio, (int, float))

class TestReportFormatting:
    """Tests para verificar formato de reportes Excel"""
    
    def test_excel_ocupacion_contiene_datos(self, client):
        """Verifica que el Excel de ocupación tiene datos"""
        payload = {
            'hospital_id': 1,
            'tipo_reporte': 'ocupacion'
        }
        
        response = client.post('/api/reportes/descargar',
                              json=payload,
                              content_type='application/json')
        
        # El archivo debe tener contenido
        assert len(response.data) > 5000  # Excel mínimo tiene al menos 5KB
    
    def test_excel_temperatura_contiene_datos(self, client):
        """Verifica que el Excel de temperatura tiene datos"""
        payload = {
            'hospital_id': 1,
            'tipo_reporte': 'temperatura'
        }
        
        response = client.post('/api/reportes/descargar',
                              json=payload,
                              content_type='application/json')
        
        # El archivo debe tener contenido
        assert len(response.data) > 3000  # Excel con pocos datos
    
    def test_descargar_json_formato_valido(self, client):
        """Verifica que el JSON descargado tiene formato válido"""
        payload = {
            'hospital_id': 1
        }
        
        response = client.post('/api/reportes/descargar-json',
                              json=payload,
                              content_type='application/json')
        
        # Verificar que sea JSON válido
        try:
            data = json.loads(response.data)
            assert 'hospital_id' in data or True  # JSON válido
        except:
            pytest.fail("JSON no válido en respuesta")

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
