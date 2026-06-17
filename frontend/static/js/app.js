/**
 * Sistema de Monitoreo Hospitalario - API Client
 */

const API_BASE_URL = 'http://localhost:5000/api';

// Utilidades para API
const apiClient = {
    async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`);
            return await response.json();
        } catch (error) {
            console.error('Error en GET:', error);
            return null;
        }
    },

    async post(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('Error en POST:', error);
            return null;
        }
    },

    async put(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('Error en PUT:', error);
            return null;
        }
    },

    async delete(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'DELETE'
            });
            return await response.json();
        } catch (error) {
            console.error('Error en DELETE:', error);
            return null;
        }
    }
};

// Gestión de secciones
function switchSection(sectionId) {
    // Ocultar todas las secciones
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // Mostrar sección seleccionada
    document.getElementById(sectionId).classList.add('active');

    // Actualizar navegación activa
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');

    // Cargar datos según sección
    if (sectionId === 'dashboard') {
        loadDashboard();
    } else if (sectionId === 'hospitales') {
        loadHospitales();
    } else if (sectionId === 'camaras') {
        loadCamaras();
    } else if (sectionId === 'sensores') {
        loadSensores();
    } else if (sectionId === 'alertas') {
        loadAlertas();
    }
}

// Cargar Dashboard
async function loadDashboard() {
    try {
        const hospitales = await apiClient.get('/hospitals/');
        document.getElementById('total-hospitales').textContent = hospitales ? hospitales.length : 0;

        // Por ahora, valores de demostración
        document.getElementById('camaras-disponibles').textContent = Math.floor(Math.random() * 50);
        document.getElementById('alertas-activas').textContent = Math.floor(Math.random() * 10);
        document.getElementById('temp-promedio').textContent = (5 + Math.random() * 3).toFixed(1) + '°C';
    } catch (error) {
        console.error('Error cargando dashboard:', error);
    }
}

// Cargar Hospitales
async function loadHospitales() {
    try {
        const hospitales = await apiClient.get('/hospitals/');
        const container = document.getElementById('hospitales-items');

        if (!hospitales || hospitales.length === 0) {
            container.innerHTML = '<p class="empty-state">No hay hospitales registrados</p>';
            return;
        }

        container.innerHTML = hospitales.map(hospital => `
            <div class="card list-item">
                <div class="item-info">
                    <h4>${hospital.nombre}</h4>
                    <p><strong>Dirección:</strong> ${hospital.direccion || 'N/A'}</p>
                    <p><strong>Teléfono:</strong> ${hospital.telefono || 'N/A'}</p>
                    <p><strong>Email:</strong> ${hospital.email || 'N/A'}</p>
                </div>
                <div class="item-actions">
                    <button class="btn btn-warning">Editar</button>
                    <button class="btn btn-danger" onclick="deleteHospital(${hospital.id})">Eliminar</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error cargando hospitales:', error);
    }
}

// Crear Hospital
document.getElementById('form-hospital')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const hospital = {
        nombre: document.getElementById('hospital-nombre').value,
        direccion: document.getElementById('hospital-direccion').value,
        telefono: document.getElementById('hospital-telefono').value,
        email: document.getElementById('hospital-email').value
    };

    const result = await apiClient.post('/hospitals/', hospital);
    if (result && result.id) {
        alert('Hospital creado exitosamente');
        e.target.reset();
        loadHospitales();
    } else {
        alert('Error al crear hospital');
    }
});

// Eliminar Hospital
async function deleteHospital(id) {
    if (confirm('¿Estás seguro de que deseas eliminar este hospital?')) {
        const result = await apiClient.delete(`/hospitals/${id}`);
        if (result && result.message) {
            alert('Hospital eliminado exitosamente');
            loadHospitales();
        } else {
            alert('Error al eliminar hospital');
        }
    }
}

// Cargar Cámaras
async function loadCamaras() {
    try {
        const hospitales = await apiClient.get('/hospitals/');
        const selectSala = document.getElementById('camara-sala');

        if (hospitales && hospitales.length > 0) {
            selectSala.innerHTML = '<option value="">Seleccionar Sala</option>';
            // En una aplicación real, cargarías las salas del hospital
        }

        // Cargar lista de cámaras
        // En una aplicación real, esto variaría según el hospital/sala seleccionada
        const container = document.getElementById('camaras-items');
        container.innerHTML = '<p class="empty-state">Selecciona una sala para ver las cámaras</p>';
    } catch (error) {
        console.error('Error cargando cámaras:', error);
    }
}

// Crear Cámara
document.getElementById('form-camara')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const camara = {
        sala_id: parseInt(document.getElementById('camara-sala').value),
        nombre: document.getElementById('camara-nombre').value,
        tipo: document.getElementById('camara-tipo').value
    };

    if (!camara.sala_id) {
        alert('Por favor selecciona una sala');
        return;
    }

    const result = await apiClient.post('/cameras/', camara);
    if (result && result.id) {
        alert('Cámara creada exitosamente');
        e.target.reset();
        loadCamaras();
    } else {
        alert('Error al crear cámara');
    }
});

// Cargar Sensores
async function loadSensores() {
    try {
        const container = document.getElementById('sensores-items');
        container.innerHTML = `
            <div class="empty-state">
                <p>No hay sensores configurados</p>
                <p>Los sensores se mostrarán aquí cuando se creen en el sistema</p>
            </div>
        `;
    } catch (error) {
        console.error('Error cargando sensores:', error);
    }
}

// Cargar Alertas
async function loadAlertas() {
    try {
        const container = document.getElementById('alertas-items');
        container.innerHTML = `
            <div class="card alert-badge success">
                ✓ Sistema funcionando correctamente
            </div>
            <p class="empty-state">No hay alertas activas en este momento</p>
        `;
    } catch (error) {
        console.error('Error cargando alertas:', error);
    }
}

// Manejadores de navegación
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const sectionId = e.target.getAttribute('href').substring(1);
        switchSection(sectionId);
    });
});

// Cargar dashboard al iniciar
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});
