"""Importar y exportar blueprints de rutas"""
from .hospitals import hospitals_bp
from .cameras import cameras_bp
from .temperature import temperature_bp
from .statistics import statistics_bp
from .sensors import sensors_bp
from .reports import reports_bp

__all__ = ['hospitals_bp', 'cameras_bp', 'temperature_bp', 'statistics_bp', 'sensors_bp', 'reports_bp']
