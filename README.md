# Sistema de Monitoreo Hospitalario

Sistema web para monitoreo y gestión de hospitales, cámaras, sensores de temperatura y alertas.

## 📋 Características

- ✅ Gestión de hospitales
- ✅ Control de cámaras disponibles
- ✅ Monitoreo de temperatura con alertas automáticas
- ✅ Estadísticas por hospital
- ✅ Panel de control intuitivo
- ✅ API REST completa

## 🏗️ Estructura del Proyecto

```
Proyecto hospital/
├── backend/                 # Aplicación Flask
│   ├── app/
│   │   ├── __init__.py     # Configuración de Flask
│   │   ├── config.py       # Configuración de la aplicación
│   │   ├── models/         # Modelos de datos
│   │   ├── routes/         # Rutas de la API
│   │   ├── services.py     # Lógica de negocio
│   │   └── utils/
│   ├── tests/              # Pruebas unitarias
│   ├── requirements.txt    # Dependencias Python
│   ├── .env.example        # Ejemplo de variables de entorno
│   ├── database.py         # Conexión a MySQL
│   ├── init_db.py          # Inicialización de BD
│   └── run.py              # Punto de entrada
│
├── frontend/               # Interfaz de usuario
│   ├── templates/
│   │   └── index.html      # Página principal
│   └── static/
│       ├── css/
│       │   └── style.css   # Estilos
│       └── js/
│           └── app.js      # JavaScript de la app
│
└── README.md               # Este archivo
```

## 🚀 Instalación y Setup

### Requisitos Previos
- Python 3.8+
- MySQL 5.7+ o MariaDB
- pip (gestor de paquetes Python)

### 1. Clonar el repositorio
```bash
git clone <url-repositorio>
cd "Proyecto hospital"
```

### 2. Configurar el entorno virtual
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
cd backend
pip install -r requirements.txt
```

### 4. Configurar base de datos
Copia el archivo `.env.example` a `.env` y actualiza los valores:
```bash
copy .env.example .env
```

Edita `.env` con tus credenciales de MySQL:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=hospital_db
```

### 5. Inicializar la base de datos
```bash
python init_db.py
```

### 6. Ejecutar tests
```bash
pytest tests/ -v
```

### 7. Iniciar la aplicación
```bash
python run.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📡 API Endpoints

### Hospitales
- `GET /api/hospitals/` - Obtener todos los hospitales
- `POST /api/hospitals/` - Crear nuevo hospital
- `GET /api/hospitals/<id>` - Obtener hospital específico
- `PUT /api/hospitals/<id>` - Actualizar hospital
- `DELETE /api/hospitals/<id>` - Eliminar hospital

### Cámaras
- `POST /api/cameras/` - Crear cámara
- `GET /api/cameras/sala/<id>` - Obtener cámaras por sala
- `GET /api/cameras/disponibles/<id>` - Cámaras disponibles
- `POST /api/cameras/<id>/ocupar` - Ocupar cámara
- `POST /api/cameras/<id>/liberar` - Liberar cámara

### Temperatura
- `POST /api/temperature/sensors` - Crear sensor
- `GET /api/temperature/sensors/<id>` - Obtener sensores
- `POST /api/temperature/sensors/<id>/update` - Actualizar temperatura
- `GET /api/temperature/alerts/hospital/<id>` - Obtener alertas

### Estadísticas
- `POST /api/statistics/` - Crear estadística
- `GET /api/statistics/hospital/<id>` - Obtener estadísticas
- `GET /api/statistics/hospital/<id>/latest` - Última estadística

## 🧪 Pruebas

Ejecutar todas las pruebas:
```bash
pytest tests/ -v
```

Pruebas con coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## 📚 Modelos de Datos

- **Hospital**: Información de hospitales
- **Sala**: Salas dentro de hospitales
- **Cámara**: Cámaras en salas
- **SensorTemperatura**: Sensores para monitorear temperatura
- **Usuario**: Personal hospitalario
- **Alerta**: Alertas del sistema
- **Estadística**: Métricas diarias

## 🔧 Variables de Entorno

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu-clave-secreta

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=contraseña
DB_NAME=hospital_db
DB_PORT=3306

SERVER_HOST=0.0.0.0
SERVER_PORT=5000
```

## 📝 Historias de Usuario Implementadas

✅ Configurar alertas automáticas de temperatura
✅ Integrar sensor de temperatura en el sistema
✅ Diseñar API REST de cámaras disponibles
✅ Implementar componente frontend de cámaras
✅ Alertas para refrigeradores de vacunas
✅ Dashboard de estadísticas por hospital

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autores

- Tu Nombre

## 📞 Contacto

Para más información o soporte, contacta a: support@hospital.com
