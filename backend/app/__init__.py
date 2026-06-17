from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-this')
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from app.routes import hospitals_bp, cameras_bp, temperature_bp, statistics_bp
    
    app.register_blueprint(hospitals_bp)
    app.register_blueprint(cameras_bp)
    app.register_blueprint(temperature_bp)
    app.register_blueprint(statistics_bp)
    
    return app
