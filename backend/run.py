"""Archivo principal de la aplicación Flask"""
import os
from app import create_app
from config import ServerConfig
from flask import render_template

# Crear la aplicación Flask
app = create_app()

@app.route('/')
def index():
    """Servir la página principal"""
    return render_template('index.html')

@app.route('/api')
def api_info():
    """Información de la API"""
    return {
        'mensaje': 'Sistema de Monitoreo Hospitalario',
        'version': '1.0.0',
        'status': 'running'
    }

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    # Crear tabla de base de datos si no existe
    print("Iniciando aplicación Flask...")
    print(f"Servidor en http://{ServerConfig.HOST}:{ServerConfig.PORT}")
    
    app.run(
        host=ServerConfig.HOST,
        port=ServerConfig.PORT,
        debug=True
    )
