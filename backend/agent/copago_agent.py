"""
backend/agent/copago_agent.py - Agente conversacional principal
Lógica del agente que interpreta síntomas, sugiere especialidades y calcula copagos
Usa Groq API para LLM y SQLite para base de datos
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from groq import Groq
from types import SimpleNamespace
from models.prompts import get_system_prompt
from backend.database.db_manager import DatabaseManager

class CopagoAgent:
    """Agente conversacional para estimación de copago y cobertura"""
    
    def __init__(self):
        """Inicializar el agente con API key y datos"""
        self.api_key = os.getenv('GROQ_API_KEY')
        # Si no hay clave, no fallamos: usamos modo simulación para desarrollo local
        if not self.api_key:
            print("[WARN] GROQ_API_KEY no configurado: iniciando en modo simulación (sin LLM)")

        # Intentar crear cliente Groq; si falla, intentaremos usar la API REST como fallback
        self.simulate_mode = False
        self.use_rest_fallback = False
        try:
            if self.api_key:
                self.client = Groq(api_key=self.api_key)
            else:
                raise RuntimeError("API key no provista, forzando modo simulado")
        except Exception as e:
            print("[WARN] No se pudo inicializar Groq client por:", str(e))
            # Verificar si se fuerza el uso de la API REST mediante variable de entorno
            force_rest = os.getenv('USE_GROQ_REST', '0') in ('1', 'true', 'True')
            if force_rest and self.api_key:
                print("[INFO] Uso forzado de REST (USE_GROQ_REST=1)")
                self.client = None
                self.use_rest_fallback = True
            else:
                # Intentar fallback vía REST HTTP si hay clave disponible
                if self.api_key:
                    print("[INFO] Intentando fallback usando la API REST de Groq")
                    self.client = None
                    self.use_rest_fallback = True
                else:
                    print("[WARN] No hay API key: activando modo simulado")
                    self.client = None
                    self.simulate_mode = True
        self.conversation_history = []
        
        # Inicializar base de datos
        self.db = DatabaseManager()
        
        print("[OK] Agente inicializado correctamente (Groq o modo simulación) + SQLite")
    
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

        assistant_message = ""
        if self.simulate_mode:
            assistant_message = self._simulate_response(user_message, context)
        else:
            # Si tenemos cliente oficial, usarlo
            if self.client:
                tried_models = []
                # Construir lista de modelos a probar. Se puede configurar `GROQ_MODEL` en .env
                try_models = []
                primary = os.getenv('GROQ_MODEL')
                if primary:
                    try_models.append(primary.strip())
                # Añadir modelos alternativos configurables
                try_models += os.getenv(
                    'GROQ_MODEL_ALTERNATES',
                    'llama-3.3-70b-versatile,llama-3.1-8b-instant'
                ).split(',')
                success = False
                last_error = None
                for model_name in try_models:
                    model_name = model_name.strip()
                    if not model_name:
                        continue
                    tried_models.append(model_name)
                    try:
                        response = self.client.chat.completions.create(
                            model=model_name,
                            max_tokens=1000,
                            messages=messages
                        )
                        assistant_message = response.choices[0].message.content
                        success = True
                        break
                    except Exception as e:
                        last_error = e
                        err_text = str(e).lower()
                        print(f"Error con modelo {model_name}:", e)
                        # si el error indica modelo decommissioned, intentar siguiente
                        if 'decommission' in err_text or 'decommissioned' in err_text or 'model' in err_text and 'no longer supported' in err_text:
                            continue
                        else:
                            # otros errores: seguir al siguiente intento
                            continue

                if not success:
                    print("No se obtuvo respuesta válida con modelos:", tried_models)
                    # Intentar REST fallback si está habilitado
                    if self.use_rest_fallback and self.api_key:
                        try:
                            assistant_message = self._call_groq_rest(messages)
                        except Exception as e2:
                            print("Error en REST fallback:", e2)
                            assistant_message = self._simulate_response(user_message, context)
                    else:
                        assistant_message = self._simulate_response(user_message, context)
            elif self.use_rest_fallback and self.api_key:
                try:
                    assistant_message = self._call_groq_rest(messages)
                except Exception as e:
                    print("Error en REST fallback:", e)
                    assistant_message = self._simulate_response(user_message, context)
            else:
                assistant_message = self._simulate_response(user_message, context)
        
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

    def _simulate_response(self, user_message: str, context: dict) -> str:
        """Generador simple de respuestas coherentes basadas en reglas y la BD.

        Busca especialidades por palabras clave en `sintomas_clave` y devuelve
        una respuesta con especialidad sugerida, hospitales cercanos y estimación
        de copago basada en `costo_base` y `copago_base` del hospital.
        """
        import random
        msg = user_message.lower()

        # Buscar mejor coincidencia de especialidad
        best = None
        best_score = 0
        for esp in context.get('especialidades', []):
            keywords = [k.strip().lower() for k in (esp.get('sintomas_clave') or [])]
            score = sum(1 for kw in keywords if kw and kw in msg)
            if score > best_score:
                best_score = score
                best = esp
            elif score == best_score and score > 0:
                # Preferir especialidades más específicas frente a Medicina General
                if best and best.get('nombre', '').lower().startswith('medicina') and not esp.get('nombre', '').lower().startswith('medicina'):
                    best = esp

        if not best:
            # Si no hubo coincidencias, sugerir Medicina General
            for esp in context.get('especialidades', []):
                if esp.get('nombre', '').lower().startswith('medicina'):
                    best = esp
                    break

        if not best and context.get('especialidades'):
            best = context['especialidades'][0]

        especialidad_nombre = best.get('nombre', 'Medicina General') if best else 'Medicina General'
        costo_base = float(best.get('costo_base', 0)) if best else 0

        # Seleccionar hospitales: preferir por menor copago_base
        hospitales = list(context.get('hospitales', []))
        if hospitales:
            hospitales_sorted = sorted(hospitales, key=lambda h: float(h.get('copago_base', 0)))
            # recomendar hasta 3, pero variar el orden para no responder siempre igual
            top_hosp = hospitales_sorted[:3]
            random.shuffle(top_hosp)
            hosp_primary = top_hosp[0]
            hosp_list = ', '.join(h.get('nombre') for h in top_hosp)
            copago_hospital = float(hosp_primary.get('copago_base', 0))
        else:
            hosp_list = 'hospitales locales'
            copago_hospital = 0

        estimacion_total = costo_base + copago_hospital

        # Plantillas variadas para evitar respuestas idénticas
        templates = [
            "Basado en lo que indicas, lo más recomendable es consultar con {esp}. En {hosp} suelen atender esta especialidad. Una consulta puede costar alrededor de ${total:.2f} (costo base ${costo:.2f} + copago hospital ${copago:.2f}). ¿Quieres que busque horarios o recomiende un hospital en tu ciudad?",
            "Parece relacionado con {esp}. Te sugiero acudir a {hosp}. Estimación aproximada: ${total:.2f} (costo base ${costo:.2f} + copago ${copago:.2f}). Si me dices tu plan de seguro puedo calcular cobertura.",
            "Recomendación: {esp}. Algunos centros donde te pueden atender: {hosp}. Coste estimado: ${total:.2f}. ¿Quieres que te muestre opciones con menor copago?"
        ]

        template = random.choice(templates)
        respuesta = template.format(
            esp=especialidad_nombre,
            hosp=hosp_list,
            total=estimacion_total,
            costo=costo_base,
            copago=copago_hospital
        )

        return respuesta
    
    def reset_conversation(self):
        """Reiniciar conversación"""
        self.conversation_history = []
        print("Conversación reiniciada")

    def _call_groq_rest(self, messages: list) -> str:
        """Llamada directa a la API REST de Groq como fallback.

        Usa `requests` para postear a /v1/chat/completions y devuelve el contenido.
        """
        import requests
        api_key = self.api_key
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b'),
            "messages": messages,
            "max_tokens": 1000
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"Groq REST error {resp.status_code}: {resp.text}")
        data = resp.json()
        # Intentar extraer estructura similar: choices[0].message.content
        try:
            return data['choices'][0]['message']['content']
        except Exception:
            return str(data)