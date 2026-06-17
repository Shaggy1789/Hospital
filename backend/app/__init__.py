from flask import Flask, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    # Configurar rutas a frontend
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    template_folder = os.path.join(base_path, 'frontend', 'templates')
    static_folder = os.path.join(base_path, 'frontend', 'static')
    
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, static_url_path='/static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-this')
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from app.routes import hospitals_bp, cameras_bp, temperature_bp, statistics_bp, sensors_bp, reports_bp
    
    app.register_blueprint(hospitals_bp)
    app.register_blueprint(cameras_bp)
    app.register_blueprint(temperature_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(sensors_bp)
    app.register_blueprint(reports_bp)
    
    return app
