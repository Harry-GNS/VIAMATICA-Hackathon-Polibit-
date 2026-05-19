"""
backend/integrations/notion_client.py - Cliente para integración con Notion
Maneja lectura de planes de seguro y datos del CRM
"""

import os
import json
from typing import List, Dict

class NotionClient:
    """Cliente para interactuar con Notion API"""
    
    def __init__(self):
        """Inicializar cliente de Notion"""
        self.api_key = os.getenv('NOTION_API_KEY')
        self.database_id = os.getenv('NOTION_DATABASE_ID')
        
        # Por ahora, usar datos de ejemplo
        self.insurance_plans = self._load_sample_plans()
    
    def get_insurance_plans(self) -> List[Dict]:
        """
        Obtener planes de seguro disponibles
        
        En producción, esto consultaría la Notion API
        Ahora retorna datos de ejemplo
        """
        return self.insurance_plans
    
    def _load_sample_plans(self) -> List[Dict]:
        """Cargar planes de ejemplo (reemplazar con Notion API)"""
        return [
            {
                "nombre": "Plan Básico",
                "precio_mensual": 50,
                "copago": 15,
                "deducible": 200,
                "cobertura": "80%"
            },
            {
                "nombre": "Plan Plus",
                "precio_mensual": 100,
                "copago": 10,
                "deducible": 100,
                "cobertura": "90%"
            },
            {
                "nombre": "Plan Premium",
                "precio_mensual": 150,
                "copago": 5,
                "deducible": 0,
                "cobertura": "100%"
            }
        ]
    
    def create_insurance_plan(self, plan_data: Dict) -> Dict:
        """Crear nuevo plan de seguro en Notion"""
        # TODO: Implementar cuando conectes Notion API
        print(f"📝 Creando plan: {plan_data.get('nombre')}")
        return plan_data
    
    def update_discount(self, patient_id: str, discount_amount: float) -> bool:
        """Actualizar descuento del paciente en CRM de Notion"""
        # TODO: Implementar cuando conectes Notion API
        print(f"✅ Descuento de ${discount_amount} aplicado a {patient_id}")
        return True