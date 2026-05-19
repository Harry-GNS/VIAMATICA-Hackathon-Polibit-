"""
backend/agent/copago_agent.py - Agente conversacional principal
Lógica del agente que interpreta síntomas, sugiere especialidades y calcula copagos
"""

import os
from anthropic import Anthropic
from backend.agent.prompts import get_system_prompt
from backend.integrations.notion_client import NotionClient
from backend.integrations.hospital_data import HospitalDataManager

class CopagoAgent:
    """Agente conversacional para estimación de copago y cobertura"""
    
    def __init__(self):
        """Inicializar el agente con API key y datos"""
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("❌ ANTHROPIC_API_KEY no configurado en .env")
        
        self.client = Anthropic()
        self.conversation_history = []
        
        # Inicializar datos
        self.notion_client = NotionClient()
        self.hospital_manager = HospitalDataManager()
        
        print("✅ Agente inicializado correctamente")
    
    def process_message(self, user_message: str) -> str:
        """
        Procesar mensaje del usuario y generar respuesta del agente
        
        Args:
            user_message: Mensaje del paciente
            
        Returns:
            Respuesta del agente
        """
        # Agregar mensaje del usuario al historial
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Contexto con datos de hospitales y planes
        context = self._build_context()
        
        # Llamar a Claude
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system=get_system_prompt(context),
            messages=self.conversation_history
        )
        
        # Extraer respuesta
        assistant_message = response.content[0].text
        
        # Agregar al historial
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def _build_context(self) -> dict:
        """Construir contexto con datos de hospitales y planes de seguro"""
        return {
            "hospitales": self.hospital_manager.get_hospitals(),
            "planes": self.notion_client.get_insurance_plans(),
            "especialidades": self.hospital_manager.get_specialties()
        }
    
    def reset_conversation(self):
        """Reiniciar conversación"""
        self.conversation_history = []
        print("Conversación reiniciada")