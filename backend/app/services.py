"""Servicios de negocio para hospitales"""
from database import db

class HospitalService:
    @staticmethod
    def crear_hospital(nombre, direccion, telefono, email):
        query = "INSERT INTO hospitales (nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s)"
        result = db.execute_query(query, (nombre, direccion, telefono, email))
        return result

    @staticmethod
    def obtener_hospital(id):
        query = "SELECT * FROM hospitales WHERE id = %s"
        return db.fetch_one(query, (id,))

    @staticmethod
    def obtener_todos_hospitales():
        query = "SELECT * FROM hospitales"
        return db.fetch_query(query)

    @staticmethod
    def actualizar_hospital(id, nombre, direccion, telefono, email):
        query = "UPDATE hospitales SET nombre=%s, direccion=%s, telefono=%s, email=%s WHERE id=%s"
        db.execute_query(query, (nombre, direccion, telefono, email, id))

    @staticmethod
    def eliminar_hospital(id):
        query = "DELETE FROM hospitales WHERE id = %s"
        db.execute_query(query, (id,))

class SalaService:
    @staticmethod
    def crear_sala(hospital_id, nombre, tipo, capacidad):
        query = "INSERT INTO salas (hospital_id, nombre, tipo, capacidad) VALUES (%s, %s, %s, %s)"
        result = db.execute_query(query, (hospital_id, nombre, tipo, capacidad))
        return result

    @staticmethod
    def obtener_salas_por_hospital(hospital_id):
        query = "SELECT * FROM salas WHERE hospital_id = %s"
        return db.fetch_query(query, (hospital_id,))

    @staticmethod
    def obtener_sala(id):
        query = "SELECT * FROM salas WHERE id = %s"
        return db.fetch_one(query, (id,))

    @staticmethod
    def actualizar_sala(id, nombre, tipo, capacidad):
        query = "UPDATE salas SET nombre=%s, tipo=%s, capacidad=%s WHERE id=%s"
        db.execute_query(query, (nombre, tipo, capacidad, id))

    @staticmethod
    def eliminar_sala(id):
        query = "DELETE FROM salas WHERE id = %s"
        db.execute_query(query, (id,))

class CamaraService:
    @staticmethod
    def crear_camara(sala_id, nombre, tipo):
        query = "INSERT INTO camaras (sala_id, nombre, tipo, disponible) VALUES (%s, %s, %s, TRUE)"
        result = db.execute_query(query, (sala_id, nombre, tipo))
        return result

    @staticmethod
    def obtener_camaras_por_sala(sala_id):
        query = "SELECT * FROM camaras WHERE sala_id = %s"
        return db.fetch_query(query, (sala_id,))

    @staticmethod
    def obtener_camaras_disponibles(sala_id):
        query = "SELECT * FROM camaras WHERE sala_id = %s AND disponible = TRUE"
        return db.fetch_query(query, (sala_id,))

    @staticmethod
    def obtener_camara(id):
        query = "SELECT * FROM camaras WHERE id = %s"
        return db.fetch_one(query, (id,))

    @staticmethod
    def ocupar_camara(id, paciente_id):
        query = "UPDATE camaras SET disponible=FALSE, ocupada_por=%s WHERE id=%s"
        db.execute_query(query, (paciente_id, id))

    @staticmethod
    def liberar_camara(id):
        query = "UPDATE camaras SET disponible=TRUE, ocupada_por=NULL WHERE id=%s"
        db.execute_query(query, (id,))

    @staticmethod
    def eliminar_camara(id):
        query = "DELETE FROM camaras WHERE id = %s"
        db.execute_query(query, (id,))

class SensorTemperaturaService:
    @staticmethod
    def crear_sensor(sala_id, nombre, ubicacion, temp_min, temp_max):
        query = "INSERT INTO sensores_temperatura (sala_id, nombre, ubicacion, temperatura_minima, temperatura_maxima) VALUES (%s, %s, %s, %s, %s)"
        result = db.execute_query(query, (sala_id, nombre, ubicacion, temp_min, temp_max))
        return result

    @staticmethod
    def obtener_sensor(id):
        query = "SELECT * FROM sensores_temperatura WHERE id = %s"
        return db.fetch_one(query, (id,))

    @staticmethod
    def obtener_sensores_por_sala(sala_id):
        query = "SELECT * FROM sensores_temperatura WHERE sala_id = %s"
        return db.fetch_query(query, (sala_id,))

    @staticmethod
    def actualizar_temperatura(sensor_id, temperatura):
        query = "UPDATE sensores_temperatura SET temperatura_actual=%s WHERE id=%s"
        db.execute_query(query, (temperatura, sensor_id))

    @staticmethod
    def obtener_temperatura_actual(sensor_id):
        query = "SELECT temperatura_actual, temperatura_minima, temperatura_maxima FROM sensores_temperatura WHERE id = %s"
        return db.fetch_one(query, (sensor_id,))

class AlertaService:
    @staticmethod
    def crear_alerta(sensor_id, tipo, mensaje):
        query = "INSERT INTO alertas (sensor_id, tipo, mensaje) VALUES (%s, %s, %s)"
        result = db.execute_query(query, (sensor_id, tipo, mensaje))
        return result

    @staticmethod
    def obtener_alertas_activas(hospital_id):
        query = """SELECT a.* FROM alertas a
                   JOIN sensores_temperatura st ON a.sensor_id = st.id
                   JOIN salas s ON st.sala_id = s.id
                   WHERE s.hospital_id = %s AND a.enviada = FALSE"""
        return db.fetch_query(query, (hospital_id,))

    @staticmethod
    def marcar_alerta_enviada(alerta_id):
        query = "UPDATE alertas SET enviada=TRUE WHERE id=%s"
        db.execute_query(query, (alerta_id,))

class EstadisticaService:
    @staticmethod
    def crear_estadistica(hospital_id, fecha, total_camaras, camaras_ocupadas, 
                         camaras_disponibles, temperatura_promedio, alertas_totales):
        query = """INSERT INTO estadisticas 
                   (hospital_id, fecha, total_camaras, camaras_ocupadas, camaras_disponibles, 
                    temperatura_promedio, alertas_totales) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        result = db.execute_query(query, (hospital_id, fecha, total_camaras, camaras_ocupadas, 
                                          camaras_disponibles, temperatura_promedio, alertas_totales))
        return result

    @staticmethod
    def obtener_estadisticas_hospital(hospital_id, fecha_inicio, fecha_fin):
        query = """SELECT * FROM estadisticas 
                   WHERE hospital_id = %s AND fecha BETWEEN %s AND %s
                   ORDER BY fecha DESC"""
        return db.fetch_query(query, (hospital_id, fecha_inicio, fecha_fin))

    @staticmethod
    def obtener_ultima_estadistica(hospital_id):
        query = "SELECT * FROM estadisticas WHERE hospital_id = %s ORDER BY fecha DESC LIMIT 1"
        return db.fetch_one(query, (hospital_id,))
