"""Generador de datos simulados para desarrollo"""
import random
from datetime import datetime

class MockDataGenerator:
    """Genera datos simulados de sensores y cámaras"""
    
    @staticmethod
    def generar_hospitales():
        """Genera hospitales simulados"""
        return [
            {
                'id': 1,
                'nombre': 'Hospital Central Metropolitano',
                'direccion': 'Avenida Principal 100',
                'telefono': '+34 91 123 4567',
                'email': 'info@hospitalcentral.es'
            },
            {
                'id': 2,
                'nombre': 'Clínica San Juan',
                'direccion': 'Calle Mayor 45',
                'telefono': '+34 91 234 5678',
                'email': 'contacto@clinicasanjuan.es'
            },
            {
                'id': 3,
                'nombre': 'Hospital de la Esperanza',
                'direccion': 'Plaza del Pueblo 12',
                'telefono': '+34 91 345 6789',
                'email': 'admin@hospitalesperanza.es'
            }
        ]
    
    @staticmethod
    def generar_salas(hospital_id):
        """Genera salas simuladas"""
        salas_data = {
            1: [
                {'id': 1, 'nombre': 'UCI - Piso 4', 'tipo': 'UCI', 'capacidad': 12},
                {'id': 2, 'nombre': 'Cardiología - Piso 3', 'tipo': 'Especializada', 'capacidad': 8},
                {'id': 3, 'nombre': 'Banco de Sangre', 'tipo': 'Laboratorio', 'capacidad': 5},
            ],
            2: [
                {'id': 4, 'nombre': 'Pediatría - Piso 2', 'tipo': 'General', 'capacidad': 10},
                {'id': 5, 'nombre': 'Farmacia Clínica', 'tipo': 'Almacén', 'capacidad': 15},
            ],
            3: [
                {'id': 6, 'nombre': 'Almacén de Vacunas', 'tipo': 'Laboratorio', 'capacidad': 3},
                {'id': 7, 'nombre': 'Quirófano 1', 'tipo': 'Quirófano', 'capacidad': 2},
            ]
        }
        for sala in salas_data.get(hospital_id, []):
            sala['hospital_id'] = hospital_id
            sala['created_at'] = datetime.now().isoformat()
        return salas_data.get(hospital_id, [])
    
    @staticmethod
    def generar_camaras(sala_id):
        """Genera cámaras simuladas"""
        return [
            {
                'id': sala_id * 10 + 1,
                'sala_id': sala_id,
                'nombre': f'Cámara {sala_id}-A',
                'tipo': 'Estándar',
                'disponible': bool(random.randint(0, 1)),
                'ocupada_por': random.randint(101, 150) if not bool(random.randint(0, 1)) else None,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': sala_id * 10 + 2,
                'sala_id': sala_id,
                'nombre': f'Cámara {sala_id}-B',
                'tipo': 'UCI' if sala_id == 1 else 'Estándar',
                'disponible': bool(random.randint(0, 1)),
                'ocupada_por': random.randint(101, 150) if not bool(random.randint(0, 1)) else None,
                'created_at': datetime.now().isoformat()
            }
        ]
    
    @staticmethod
    def generar_sensores(sala_id):
        """Genera sensores de temperatura simulados"""
        tipos_sala = {
            1: ('Refrigerador Vacunas', 2, 8),
            2: ('Congelador Banco de Sangre', -25, -20),
            3: ('Sala Operatoria', 18, 24),
            4: ('Habitación Pediátrica', 20, 25),
            5: ('Almacén Medicamentos', 15, 25),
            6: ('Refrigerador Medicamentos', 2, 8),
            7: ('Congelador Backup', -30, -25),
        }
        
        nombre, temp_min, temp_max = tipos_sala.get(sala_id, ('Sensor General', 15, 25))
        
        sensores = []
        for i in range(1, 3):
            temp_actual = round(random.uniform(temp_min - 2, temp_max + 2), 1)
            
            # Determinar estado
            if temp_actual < temp_min or temp_actual > temp_max:
                estado = 'ALERTA'
                alerta_activa = True
            else:
                estado = 'NORMAL'
                alerta_activa = False
            
            sensores.append({
                'id': sala_id * 100 + i,
                'sala_id': sala_id,
                'nombre': f'{nombre} - Sensor {i}',
                'ubicacion': f'Ubicación {chr(64+i)}',
                'temperatura_actual': temp_actual,
                'temperatura_minima': temp_min,
                'temperatura_maxima': temp_max,
                'alerta_activa': alerta_activa,
                'estado': estado,
                'created_at': datetime.now().isoformat()
            })
        
        return sensores
    
    @staticmethod
    def generar_alertas(hospital_id):
        """Genera alertas simuladas"""
        alertas = []
        sensores_con_problemas = [101, 202, 601]  # Algunos sensores con alertas
        
        for sensor_id in sensores_con_problemas[:random.randint(0, 2)]:
            alertas.append({
                'id': len(alertas) + 1,
                'sensor_id': sensor_id,
                'tipo': random.choice(['TEMPERATURA_ALTA', 'TEMPERATURA_BAJA', 'FALLO_SENSOR']),
                'mensaje': f'Lectura anómala en sensor {sensor_id}',
                'enviada': False,
                'fecha_alerta': datetime.now().isoformat()
            })
        
        return alertas
    
    @staticmethod
    def simular_temperatura():
        """Genera una temperatura simulada aleatoria"""
        return {
            'temperatura': round(random.uniform(-30, 30), 1),
            'timestamp': datetime.now().isoformat()
        }
