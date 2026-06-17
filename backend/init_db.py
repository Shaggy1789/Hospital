"""Script para inicializar la base de datos"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Crear la base de datos y las tablas necesarias"""
    
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'hospital_db')
    port = os.getenv('DB_PORT', 3306)
    
    try:
        # Conectar sin especificar BD
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        cursor = conn.cursor()
        
        # Crear BD
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        print(f"✓ Base de datos '{database}' creada/verificada")
        
        # Seleccionar BD
        cursor.execute(f"USE {database}")
        
        # Crear tabla hospitales
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospitales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                direccion VARCHAR(200),
                telefono VARCHAR(20),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Tabla 'hospitales' creada")
        
        # Crear tabla salas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS salas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hospital_id INT NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                tipo VARCHAR(50),
                capacidad INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (hospital_id) REFERENCES hospitales(id)
            )
        """)
        print("✓ Tabla 'salas' creada")
        
        # Crear tabla camaras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS camaras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sala_id INT NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                tipo VARCHAR(50),
                disponible BOOLEAN DEFAULT TRUE,
                ocupada_por INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sala_id) REFERENCES salas(id)
            )
        """)
        print("✓ Tabla 'camaras' creada")
        
        # Crear tabla sensores_temperatura
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensores_temperatura (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sala_id INT NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                ubicacion VARCHAR(200),
                temperatura_actual DECIMAL(5, 2),
                temperatura_minima DECIMAL(5, 2),
                temperatura_maxima DECIMAL(5, 2),
                alerta_activa BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (sala_id) REFERENCES salas(id)
            )
        """)
        print("✓ Tabla 'sensores_temperatura' creada")
        
        # Crear tabla registros_temperatura
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros_temperatura (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sensor_id INT NOT NULL,
                temperatura DECIMAL(5, 2) NOT NULL,
                estado VARCHAR(50),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sensor_id) REFERENCES sensores_temperatura(id)
            )
        """)
        print("✓ Tabla 'registros_temperatura' creada")
        
        # Crear tabla usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hospital_id INT NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                rol VARCHAR(50) NOT NULL,
                activo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (hospital_id) REFERENCES hospitales(id)
            )
        """)
        print("✓ Tabla 'usuarios' creada")
        
        # Crear tabla alertas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alertas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sensor_id INT NOT NULL,
                tipo VARCHAR(50) NOT NULL,
                mensaje VARCHAR(500),
                enviada BOOLEAN DEFAULT FALSE,
                fecha_alerta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sensor_id) REFERENCES sensores_temperatura(id)
            )
        """)
        print("✓ Tabla 'alertas' creada")
        
        # Crear tabla estadisticas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estadisticas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hospital_id INT NOT NULL,
                fecha DATE NOT NULL,
                total_camaras INT,
                camaras_ocupadas INT,
                camaras_disponibles INT,
                temperatura_promedio DECIMAL(5, 2),
                alertas_totales INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (hospital_id) REFERENCES hospitales(id),
                UNIQUE KEY unique_hospital_date (hospital_id, fecha)
            )
        """)
        print("✓ Tabla 'estadisticas' creada")
        
        conn.commit()
        print("\n✅ Base de datos inicializada correctamente")
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    create_database()
