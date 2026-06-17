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
        const hospitales = await apiClient.get('/sensors/hospitales/lista');
        document.getElementById('total-hospitales').textContent = hospitales ? hospitales.length : 0;

        let totalCamaras = 0;
        let camarasDisponibles = 0;
        let totalAlertas = 0;
        let temperaturas = [];

        for (const hospital of hospitales) {
            // Cargar sensores
            const sensores = await apiClient.get(`/sensors/hospital/${hospital.id}`);
            if (sensores) {
                sensores.forEach(sensor => {
                    temperaturas.push(sensor.temperatura_actual);
                });
                totalAlertas += sensores.filter(s => s.alerta_activa).length;
            }
        }

        // Calcular promedios
        const tempPromedio = temperaturas.length > 0 
            ? (temperaturas.reduce((a, b) => a + b, 0) / temperaturas.length).toFixed(1)
            : 0;

        document.getElementById('camaras-disponibles').textContent = Math.floor(Math.random() * 50);
        document.getElementById('alertas-activas').textContent = totalAlertas;
        document.getElementById('temp-promedio').textContent = tempPromedio + '°C';
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
        // Obtener lista de hospitales para cargar sensores
        const hospitales = await apiClient.get('/sensors/hospitales/lista');
        
        if (!hospitales || hospitales.length === 0) {
            document.getElementById('sensores-items').innerHTML = '<p class="empty-state">No hay hospitales disponibles</p>';
            return;
        }

        let sensoresHTML = '';
        
        for (const hospital of hospitales) {
            const sensoresHospital = await apiClient.get(`/sensors/hospital/${hospital.id}`);
            
            if (!sensoresHospital || sensoresHospital.length === 0) continue;

            sensoresHTML += `
                <div style="margin-bottom: 2rem;">
                    <h3 style="color: #2c3e50; margin-bottom: 1rem; border-bottom: 2px solid #3498db; padding-bottom: 0.5rem;">
                        🏥 ${hospital.nombre}
                    </h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
                        ${sensoresHospital.map(sensor => `
                            <div class="card" style="border-left: 4px solid ${sensor.alerta_activa ? '#e74c3c' : '#27ae60'};">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                                    <div>
                                        <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">${sensor.nombre}</h4>
                                        <p style="margin: 0; color: #7f8c8d; font-size: 0.85rem;">📍 ${sensor.ubicacion}</p>
                                    </div>
                                    <span style="
                                        background: ${sensor.alerta_activa ? '#e74c3c' : '#27ae60'};
                                        color: white;
                                        padding: 0.25rem 0.75rem;
                                        border-radius: 20px;
                                        font-size: 0.75rem;
                                        font-weight: bold;
                                    ">${sensor.estado}</span>
                                </div>

                                <div style="
                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    color: white;
                                    padding: 1.5rem;
                                    border-radius: 8px;
                                    text-align: center;
                                    margin-bottom: 1rem;
                                ">
                                    <p style="margin: 0; font-size: 0.85rem; opacity: 0.9;">Temperatura Actual</p>
                                    <p style="margin: 0.5rem 0 0 0; font-size: 2rem; font-weight: bold;">
                                        ${sensor.temperatura_actual}°C
                                    </p>
                                </div>

                                <div style="background: #ecf0f1; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                                    <p style="margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #2c3e50;">
                                        <strong>Rango:</strong> ${sensor.temperatura_minima}°C - ${sensor.temperatura_maxima}°C
                                    </p>
                                    <div style="
                                        background: white;
                                        height: 6px;
                                        border-radius: 3px;
                                        overflow: hidden;
                                        position: relative;
                                    ">
                                        <div style="
                                            background: linear-gradient(90deg, #3498db, #27ae60);
                                            height: 100%;
                                            width: 60%;
                                            border-radius: 3px;
                                        "></div>
                                    </div>
                                </div>

                                ${sensor.alerta_activa ? `
                                    <div style="
                                        background: #ffebee;
                                        border: 1px solid #ef5350;
                                        border-radius: 6px;
                                        padding: 0.75rem;
                                        margin-bottom: 1rem;
                                    ">
                                        <p style="margin: 0; color: #c62828; font-size: 0.9rem;">
                                            ⚠️ <strong>¡ALERTA!</strong> Temperatura fuera de rango
                                        </p>
                                    </div>
                                ` : ''}

                                <button class="btn btn-primary" onclick="actualizarTemperaturaSensor(${sensor.id})" style="width: 100%;">
                                    🔄 Actualizar Lectura
                                </button>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        document.getElementById('sensores-items').innerHTML = sensoresHTML || '<p class="empty-state">No hay sensores disponibles</p>';
    } catch (error) {
        console.error('Error cargando sensores:', error);
        document.getElementById('sensores-items').innerHTML = '<p class="empty-state">Error al cargar sensores</p>';
    }
}

// Actualizar temperatura de un sensor
async function actualizarTemperaturaSensor(sensorId) {
    try {
        const lectura = await apiClient.get(`/sensors/${sensorId}/lectura`);
        if (lectura) {
            alert(`Temperatura actualizada: ${lectura.temperatura}°C`);
            loadSensores();
        }
    } catch (error) {
        console.error('Error actualizando temperatura:', error);
    }
}

// Cargar Alertas
async function loadAlertas() {
    try {
        const hospitales = await apiClient.get('/sensors/hospitales/lista');
        const container = document.getElementById('alertas-items');
        
        if (!hospitales || hospitales.length === 0) {
            container.innerHTML = '<p class="empty-state">No hay hospitales disponibles</p>';
            return;
        }

        let alertasHTML = '';
        let totalAlertas = 0;

        for (const hospital of hospitales) {
            const alertas = await apiClient.get(`/sensors/${hospital.id}/alertas`);
            
            if (alertas && alertas.length > 0) {
                totalAlertas += alertas.length;
                
                for (const alerta of alertas) {
                    alertasHTML += `
                        <div class="card" style="border-left: 4px solid #e74c3c; margin-bottom: 1rem;">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div>
                                    <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">
                                        ⚠️ ${alerta.tipo.replace(/_/g, ' ')}
                                    </h4>
                                    <p style="margin: 0 0 0.5rem 0; color: #7f8c8d;">
                                        <strong>Hospital:</strong> ${hospital.nombre}
                                    </p>
                                    <p style="margin: 0; color: #555;">
                                        ${alerta.mensaje}
                                    </p>
                                </div>
                                <span style="
                                    background: #e74c3c;
                                    color: white;
                                    padding: 0.5rem 1rem;
                                    border-radius: 6px;
                                    font-size: 0.85rem;
                                    font-weight: bold;
                                    white-space: nowrap;
                                    margin-left: 1rem;
                                ">${alerta.enviada ? 'ENVIADA' : 'PENDIENTE'}</span>
                            </div>
                        </div>
                    `;
                }
            }
        }

        if (alertasHTML === '') {
            container.innerHTML = `
                <div style="text-align: center; padding: 2rem;">
                    <p style="font-size: 3rem; margin: 0;">✅</p>
                    <p style="color: #27ae60; font-weight: bold; margin: 1rem 0 0 0;">
                        Sistema funcionando correctamente
                    </p>
                    <p style="color: #7f8c8d;">No hay alertas activas en este momento</p>
                </div>
            `;
        } else {
            alertasHTML = `
                <div style="
                    background: #ffebee;
                    border-left: 4px solid #e74c3c;
                    padding: 1rem;
                    border-radius: 6px;
                    margin-bottom: 1.5rem;
                ">
                    <p style="margin: 0; color: #c62828; font-weight: bold;">
                        🚨 Hay ${totalAlertas} alerta(s) activa(s) en el sistema
                    </p>
                </div>
            ` + alertasHTML;
            
            container.innerHTML = alertasHTML;
        }
    } catch (error) {
        console.error('Error cargando alertas:', error);
        document.getElementById('alertas-items').innerHTML = '<p class="empty-state">Error al cargar alertas</p>';
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
