"""
backend/integrations/hospital_data.py - Manager de datos de hospitales
Maneja la información de hospitales, especialidades y costos
"""

from typing import List, Dict

class HospitalDataManager:
    """Gestor de datos de hospitales y especialidades"""
    
    def __init__(self):
        """Inicializar manager con datos de ejemplo"""
        self.hospitals = self._load_sample_hospitals()
        self.specialties = self._load_sample_specialties()
    
    def get_hospitals(self) -> List[Dict]:
        """Obtener lista de hospitales disponibles"""
        return self.hospitals
    
    def get_specialties(self) -> List[Dict]:
        """Obtener lista de especialidades médicas"""
        return self.specialties
    
    def get_hospital_by_id(self, hospital_id: str) -> Dict:
        """Obtener hospital específico por ID"""
        for h in self.hospitals:
            if h.get('id') == hospital_id:
                return h
        return {}
    
    def _load_sample_hospitals(self) -> List[Dict]:
        """Cargar datos de ejemplo de hospitales"""
        return [
            {
                "id": "hosp_001",
                "nombre": "Hospital Metropolitano",
                "red": "Red Premium",
                "copago_base": 25,
                "telefono": "+593 2 398-6000",
                "direccion": "Av. Mariana de Jesús, Quito"
            },
            {
                "id": "hosp_002",
                "nombre": "Hospital Voz Andes",
                "red": "Red Plus",
                "copago_base": 20,
                "telefono": "+593 2 226-0142",
                "direccion": "Calle 38 y Avenida América, Quito"
            },
            {
                "id": "hosp_003",
                "nombre": "Clínica Pichincha",
                "red": "Red Básica",
                "copago_base": 15,
                "telefono": "+593 2 299-8000",
                "direccion": "Avenida 10 de Agosto, Quito"
            },
            {
                "id": "hosp_004",
                "nombre": "Hospital Baca Ortiz",
                "red": "Red Pública",
                "copago_base": 5,
                "telefono": "+593 2 250-0666",
                "direccion": "Correo del Pío, Quito"
            }
        ]
    
    def _load_sample_specialties(self) -> List[Dict]:
        """Cargar datos de ejemplo de especialidades"""
        return [
            {
                "nombre": "Medicina General",
                "codigo": "MED_GEN",
                "costo_base": 50,
                "sintomas_clave": ["dolor", "fiebre", "malestar"]
            },
            {
                "nombre": "Cardiología",
                "codigo": "CARD",
                "costo_base": 120,
                "sintomas_clave": ["dolor de pecho", "arritmia", "presión alta"]
            },
            {
                "nombre": "Traumatología",
                "codigo": "TRAUMA",
                "costo_base": 100,
                "sintomas_clave": ["fractura", "esguince", "dolor articular"]
            },
            {
                "nombre": "Gastroenterología",
                "codigo": "GASTRO",
                "costo_base": 90,
                "sintomas_clave": ["dolor abdominal", "gastritis", "diarrea"]
            },
            {
                "nombre": "Oftalmología",
                "codigo": "OFTALMOLOGIA",
                "costo_base": 80,
                "sintomas_clave": ["visión borrosa", "dolor ocular", "conjuntivitis"]
            },
            {
                "nombre": "Dermatología",
                "codigo": "DERMA",
                "costo_base": 75,
                "sintomas_clave": ["erupción", "acné", "prurito"]
            }
        ]
    
    def suggest_specialty(self, symptom: str) -> Dict:
        """Sugerir especialidad basada en síntoma (lógica simple)"""
        symptom_lower = symptom.lower()
        
        for specialty in self.specialties:
            for key_symptom in specialty.get('sintomas_clave', []):
                if key_symptom in symptom_lower:
                    return specialty
        
        # Por defecto, medicina general
        return self.specialties[0]
    
    def get_cheapest_hospital(self) -> Dict:
        """Obtener hospital más económico"""
        return min(self.hospitals, key=lambda x: x.get('copago_base', 0))