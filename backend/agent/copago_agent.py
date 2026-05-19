"""
backend/agent/copago_agent.py - Agente conversacional principal
Lógica del agente que interpreta síntomas, sugiere especialidades y calcula copagos
Usa Groq API para LLM y SQLite para base de datos
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from groq import Groq
from models.prompts import get_system_prompt
from backend.database.db_manager import DatabaseManager

class CopagoAgent:
    """Agente conversacional para estimación de copago y cobertura"""
    
    def __init__(self):
        """Inicializar el agente con API key y datos"""
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("❌ GROQ_API_KEY no configurado en .env")
        
        self.client = Groq(api_key=self.api_key)
        self.conversation_history = []
        
        # Inicializar base de datos
        self.db = DatabaseManager()
        
        print("✅ Agente inicializado correctamente con Groq + SQLite")
    
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
        
        # Llamar a Groq API
        # Groq client expects the system prompt included in the messages list
        messages = [
            {"role": "system", "content": get_system_prompt(context)}
        ] + self.conversation_history

        try:
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                max_tokens=1000,
                messages=messages
            )

            # Extraer respuesta
            assistant_message = response.choices[0].message.content
        except Exception as e:
            # Mostrar error en consola y devolver mensaje legible al cliente
            print("Error en /api/chat:", e)
            assistant_message = (
                "Lo siento, el servicio de LLM no está disponible en este momento. "
                "Error: " + str(e)
            )
        
        # Agregar al historial
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def _build_context(self) -> dict:
        """Construir contexto con datos de hospitales y planes de seguro desde SQLite"""
        return {
            "hospitales": self.db.get_hospitales(),
            "planes": self.db.get_planes_seguro(),
            "especialidades": self.db.get_especialidades()
        }
    
    def reset_conversation(self):
        """Reiniciar conversación"""
        self.conversation_history = []
        print("Conversación reiniciada")