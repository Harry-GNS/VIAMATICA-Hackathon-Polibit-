"""
backend/database/db_manager.py - Manager de SQLite
Gestiona la base de datos local para planes de seguro, hospitales y especialidades
"""

import sqlite3
import os
from typing import List, Dict
from pathlib import Path

class DatabaseManager:
    """Gestor de base de datos SQLite"""
    
    def __init__(self, db_path: str = "data/viamatica.db"):
        """
        Inicializar conexión a base de datos
        
        Args:
            db_path: Ruta del archivo SQLite
        """
        self.db_path = db_path
        
        # Crear directorio si no existe
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Inicializar base de datos
        self._init_database()
    
    def _get_connection(self):
        """Obtener conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Retornar filas como diccionarios
        return conn
    
    def _init_database(self):
        """Crear tablas si no existen"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Tabla de hospitales
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospitales (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                red TEXT NOT NULL,
                copago_base REAL NOT NULL,
                telefono TEXT,
                direccion TEXT,
                ciudad TEXT
            )
        """)
        
        # Tabla de especialidades
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS especialidades (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                codigo TEXT UNIQUE NOT NULL,
                costo_base REAL NOT NULL,
                sintomas_clave TEXT,
                descripcion TEXT
            )
        """)
        
        # Tabla de planes de seguro
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS planes_seguro (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                compania TEXT NOT NULL,
                cobertura_porcentaje REAL NOT NULL,
                deducible REAL,
                copago_fijo REAL,
                descripcion TEXT
            )
        """)
        
        # Tabla de cobertura por especialidad y plan
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cobertura_especialidad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id TEXT NOT NULL,
                especialidad_id TEXT NOT NULL,
                cubre_porcentaje REAL NOT NULL,
                copago_especialidad REAL,
                FOREIGN KEY (plan_id) REFERENCES planes_seguro(id),
                FOREIGN KEY (especialidad_id) REFERENCES especialidades(id),
                UNIQUE(plan_id, especialidad_id)
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Base de datos inicializada")
    
    # ========== HOSPITALES ==========
    def get_hospitales(self) -> List[Dict]:
        """Obtener todos los hospitales"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hospitales")
        hospitales = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return hospitales
    
    def get_hospital_by_id(self, hospital_id: str) -> Dict:
        """Obtener hospital por ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hospitales WHERE id = ?", (hospital_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else {}
    
    def add_hospital(self, id: str, nombre: str, red: str, copago_base: float, 
                     telefono: str = None, direccion: str = None, ciudad: str = None):
        """Agregar nuevo hospital"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO hospitales 
            (id, nombre, red, copago_base, telefono, direccion, ciudad)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id, nombre, red, copago_base, telefono, direccion, ciudad))
        conn.commit()
        conn.close()
    
    # ========== ESPECIALIDADES ==========
    def get_especialidades(self) -> List[Dict]:
        """Obtener todas las especialidades"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM especialidades")
        especialidades = []
        for row in cursor.fetchall():
            spec = dict(row)
            spec['sintomas_clave'] = spec['sintomas_clave'].split(',') if spec['sintomas_clave'] else []
            especialidades.append(spec)
        conn.close()
        return especialidades
    
    def add_especialidad(self, id: str, nombre: str, codigo: str, costo_base: float,
                        sintomas_clave: List[str] = None, descripcion: str = None):
        """Agregar nueva especialidad"""
        conn = self._get_connection()
        cursor = conn.cursor()
        sintomas_str = ','.join(sintomas_clave) if sintomas_clave else ""
        cursor.execute("""
            INSERT OR REPLACE INTO especialidades 
            (id, nombre, codigo, costo_base, sintomas_clave, descripcion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id, nombre, codigo, costo_base, sintomas_str, descripcion))
        conn.commit()
        conn.close()
    
    # ========== PLANES DE SEGURO ==========
    def get_planes_seguro(self) -> List[Dict]:
        """Obtener todos los planes de seguro"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM planes_seguro")
        planes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return planes
    
    def get_plan_by_id(self, plan_id: str) -> Dict:
        """Obtener plan de seguro por ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM planes_seguro WHERE id = ?", (plan_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else {}
    
    def add_plan_seguro(self, id: str, nombre: str, compania: str, cobertura_porcentaje: float,
                       deducible: float = None, copago_fijo: float = None, descripcion: str = None):
        """Agregar nuevo plan de seguro"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO planes_seguro 
            (id, nombre, compania, cobertura_porcentaje, deducible, copago_fijo, descripcion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id, nombre, compania, cobertura_porcentaje, deducible, copago_fijo, descripcion))
        conn.commit()
        conn.close()
    
    # ========== COBERTURA POR ESPECIALIDAD ==========
    def get_cobertura(self, plan_id: str, especialidad_id: str) -> Dict:
        """Obtener cobertura para un plan y especialidad específicos"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM cobertura_especialidad 
            WHERE plan_id = ? AND especialidad_id = ?
        """, (plan_id, especialidad_id))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else {}
    
    def add_cobertura(self, plan_id: str, especialidad_id: str, cubre_porcentaje: float, 
                     copago_especialidad: float = None):
        """Agregar cobertura para plan y especialidad"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO cobertura_especialidad 
            (plan_id, especialidad_id, cubre_porcentaje, copago_especialidad)
            VALUES (?, ?, ?, ?)
        """, (plan_id, especialidad_id, cubre_porcentaje, copago_especialidad))
        conn.commit()
        conn.close()
    
    # ========== UTILIDADES ==========
    def load_sample_data(self):
        """Cargar datos de ejemplo"""
        # Hospitales
        hospitales = [
            ("hosp_001", "Hospital Metropolitano", "Red Premium", 25, "+593 2 398-6000", "Av. Mariana de Jesús", "Quito"),
            ("hosp_002", "Hospital Voz Andes", "Red Plus", 20, "+593 2 226-0142", "Calle 38 y Avenida América", "Quito"),
            ("hosp_003", "Clínica Pichincha", "Red Básica", 15, "+593 2 299-8000", "Avenida 10 de Agosto", "Quito"),
            ("hosp_004", "Hospital Baca Ortiz", "Red Pública", 5, "+593 2 250-0666", "Correo del Pío", "Quito"),
        ]
        
        for hosp in hospitales:
            self.add_hospital(*hosp)
        
        # Especialidades
        especialidades = [
            ("esp_001", "Medicina General", "MED_GEN", 50, ["dolor", "fiebre", "malestar"], "Consulta general"),
            ("esp_002", "Cardiología", "CARD", 120, ["pecho", "corazón", "presión"], "Especialista del corazón"),
            ("esp_003", "Dermatología", "DERM", 80, ["piel", "acné", "alergia"], "Especialista de la piel"),
            ("esp_004", "Ginecología", "GIN", 100, ["ginecología", "reproductivo"], "Especialista femenino"),
            ("esp_005", "Oftalmología", "OFT", 90, ["ojos", "visión", "vista"], "Especialista de los ojos"),
        ]
        
        for esp in especialidades:
            self.add_especialidad(*esp)
        
        # Planes de seguro
        planes = [
            ("plan_001", "Plan Básico", "Seguros XYZ", 60, 100, 15, "Cobertura básica"),
            ("plan_002", "Plan Plus", "Seguros XYZ", 80, 50, 10, "Cobertura intermedia"),
            ("plan_003", "Plan Premium", "Seguros XYZ", 95, 0, 5, "Cobertura completa"),
        ]
        
        for plan in planes:
            self.add_plan_seguro(*plan)
        
        # Cobertura por especialidad
        coberturas = [
            ("plan_001", "esp_001", 100, 15),
            ("plan_001", "esp_002", 60, 30),
            ("plan_001", "esp_003", 70, 20),
            ("plan_002", "esp_001", 100, 10),
            ("plan_002", "esp_002", 80, 20),
            ("plan_002", "esp_003", 90, 15),
            ("plan_003", "esp_001", 100, 5),
            ("plan_003", "esp_002", 100, 10),
            ("plan_003", "esp_003", 100, 10),
        ]
        
        for cob in coberturas:
            self.add_cobertura(*cob)
        
        print("✅ Datos de ejemplo cargados")
    
    def clear_all(self):
        """Limpiar todas las tablas"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cobertura_especialidad")
        cursor.execute("DELETE FROM planes_seguro")
        cursor.execute("DELETE FROM especialidades")
        cursor.execute("DELETE FROM hospitales")
        conn.commit()
        conn.close()
