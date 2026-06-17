import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    """Clase para manejar conexión a MySQL"""
    
    def __init__(self):
        self.connection = None
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'hospital_db')
        self.port = os.getenv('DB_PORT', 3306)

    def connect(self):
        """Establecer conexión a la BD"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                print(f"Conectado a la BD {self.database}")
                return True
        except Error as e:
            print(f"Error al conectar a la BD: {e}")
            return False

    def get_connection(self):
        """Obtener la conexión actual"""
        if self.connection and self.connection.is_connected():
            return self.connection
        else:
            self.connect()
            return self.connection

    def execute_query(self, query, params=None):
        """Ejecutar una consulta INSERT, UPDATE o DELETE"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return None

    def fetch_query(self, query, params=None):
        """Ejecutar una consulta SELECT"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return None

    def fetch_one(self, query, params=None):
        """Obtener un resultado de SELECT"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return None

    def close(self):
        """Cerrar conexión"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")

db = DatabaseConnection()
