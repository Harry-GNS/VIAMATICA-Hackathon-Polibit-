"""
models/prompts.py - Prompts del agente para Claude/Groq
Define el comportamiento del agente conversacional
"""

def get_system_prompt(context: dict) -> str:
    """
    Generar el prompt del sistema para el agente
    
    Args:
        context: Diccionario con datos de hospitales, planes, especialidades y coberturas
        
    Returns:
        Prompt del sistema completo
    """
    
    hospitales_str = _format_hospitals(context.get('hospitales', []))
    planes_str = _format_plans(context.get('planes', []))
    especialidades_str = _format_specialties(context.get('especialidades', []))
    coberturas_str = _format_coberturas(context.get('coberturas', []))
    
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

## COBERTURAS POR PLAN Y ESPECIALIDAD:
{coberturas_str}

## REGLAS DE CÁLCULO DE COPAGO:
1. El copago del hospital y la especialidad se estiman basándose en la cobertura del plan.
2. Si el plan tiene un "Copago Especialidad" específico para esa especialidad, se usa ese valor.
3. Si no hay un copago específico para la especialidad, se calcula el copago estimado de la consulta como:
   Copago Consulta = Costo Base Especialidad * (1 - Cobertura del Plan / 100).
4. El copago base del hospital se suma si corresponde a cargos administrativos o de red.
5. Explica el cálculo paso a paso al paciente de manera clara y sencilla.

## INSTRUCCIONES DE COMPORTAMIENTO:
- Siempre sé amable y empático con el paciente.
- Si no sabes el plan del paciente, pregúntale cuál de los planes disponibles tiene (Plan Básico, Plan Plus, Plan Premium).
- Haz preguntas clarificadoras sobre sus síntomas si es necesario para sugerir la especialidad adecuada.
- Sugiere la opción de hospital más económica (el de menor copago base en la red correspondiente).
- Nunca hagas diagnósticos médicos definitivos, siempre aclara que es una sugerencia de especialidad y que debe consultar con un profesional de la salud.
- Sé conciso, profesional y directo en tus respuestas.
"""
    return system_prompt

def _format_hospitals(hospitales: list) -> str:
    """Formatear lista de hospitales"""
    if not hospitales:
        return "No hay hospitales disponibles en la base de datos."
    
    result = ""
    for h in hospitales:
        result += f"- {h.get('nombre', 'N/A')}: {h.get('direccion', 'N/A')}, {h.get('ciudad', 'N/A')} (Tel: {h.get('telefono', 'N/A')}) - Copago Base: ${h.get('copago_base', 0)} (Red: {h.get('red', 'N/A')})\n"
    return result

def _format_plans(planes: list) -> str:
    """Formatear lista de planes de seguro"""
    if not planes:
        return "No hay planes disponibles en la base de datos."
    
    result = ""
    for p in planes:
        result += f"- {p.get('nombre', 'N/A')} ({p.get('compania', 'N/A')}): Cobertura General {p.get('cobertura_porcentaje', 'N/A')}% - Deducible: ${p.get('deducible', 0)} - Copago Fijo General: ${p.get('copago_fijo', 0)}\n"
    return result

def _format_specialties(especialidades: list) -> str:
    """Formatear lista de especialidades"""
    if not especialidades:
        return "No hay especialidades disponibles en la base de datos."
    
    result = ""
    for e in especialidades:
        sintomas = ", ".join(e.get('sintomas_clave', [])) if isinstance(e.get('sintomas_clave'), list) else e.get('sintomas_clave', 'N/A')
        result += f"- {e.get('nombre', 'N/A')} (Costo Consulta Base: ${e.get('costo_base', 0)}) - Síntomas Clave: {sintomas} - {e.get('descripcion', '')}\n"
    return result

def _format_coberturas(coberturas: list) -> str:
    """Formatear lista de coberturas detalladas por plan y especialidad"""
    if not coberturas:
        return "No hay coberturas específicas configuradas en la base de datos."
    
    result = ""
    for c in coberturas:
        result += f"- Plan: {c.get('plan_nombre', 'N/A')} | Especialidad: {c.get('especialidad_nombre', 'N/A')} | Cobertura Especialidad: {c.get('cubre_porcentaje', 'N/A')}% | Copago Especialidad: ${c.get('copago_especialidad', 'N/A')}\n"
    return result