"""
models/prompts.py - Prompts del agente para Claude
Define el comportamiento del agente conversacional
"""

def get_system_prompt(context: dict) -> str:
    """
    Generar el prompt del sistema para el agente
    
    Args:
        context: Diccionario con datos de hospitales, planes y especialidades
        
    Returns:
        Prompt del sistema completo
    """
    
    hospitales_str = _format_hospitals(context.get('hospitales', []))
    planes_str = _format_plans(context.get('planes', []))
    especialidades_str = _format_specialties(context.get('especialidades', []))
    
    system_prompt = f"""Eres un asistente de salud experto en seguros médicos y cálculo de copagos.

Tu función es ayudar a los pacientes a:
1. Entender su cobertura de seguro
2. Identificar la especialidad médica correcta según sus síntomas
3. Calcular exactamente cuánto costarían sus copagos
4. Recomendar el hospital más conveniente económicamente

## INFORMACIÓN DE HOSPITALES Y COSTOS:
{hospitales_str}

## PLANES DE SEGURO DISPONIBLES:
{planes_str}

## ESPECIALIDADES MÉDICAS:
{especialidades_str}

## INSTRUCCIONES:
- Siempre sé amable y empático con el paciente
- Haz preguntas clarificadoras si es necesario
- Proporciona cálculos detallados de copagos
- Sugiere la opción más económica cuando sea posible
- Nunca hagas diagnósticos médicos, solo sugiere especialidades
- Sé conciso y directo en tus respuestas
"""
    return system_prompt

def _format_hospitals(hospitales: list) -> str:
    """Formatear lista de hospitales"""
    if not hospitales:
        return "No hay hospitales disponibles en la base de datos."
    
    result = ""
    for h in hospitales:
        result += f"- {h.get('nombre', 'N/A')}: {h.get('ubicacion', 'N/A')} (Tel: {h.get('telefono', 'N/A')})\n"
    return result

def _format_plans(planes: list) -> str:
    """Formatear lista de planes de seguro"""
    if not planes:
        return "No hay planes disponibles en la base de datos."
    
    result = ""
    for p in planes:
        result += f"- {p.get('nombre', 'N/A')}: Cobertura {p.get('cobertura', 'N/A')}% - Copago: ${p.get('copago', 'N/A')}\n"
    return result

def _format_specialties(especialidades: list) -> str:
    """Formatear lista de especialidades"""
    if not especialidades:
        return "No hay especialidades disponibles en la base de datos."
    
    result = ""
    for e in especialidades:
        result += f"- {e.get('nombre', 'N/A')}: Copago ${e.get('copago', 'N/A')}\n"
    return result