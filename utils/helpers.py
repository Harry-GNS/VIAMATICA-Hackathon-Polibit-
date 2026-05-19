"""
utils/helpers.py - Funciones auxiliares y utilidades
Funciones compartidas para cálculos y formateo
"""

def calculate_copago(base_copago: float, deducible: float, cost: float) -> float:
    """
    Calcular copago final
    
    Args:
        base_copago: Copago base del plan
        deducible: Deducible del plan
        cost: Costo total del servicio
        
    Returns:
        Copago a pagar por el paciente
    """
    # Si el costo es menor al deducible, paga el costo completo
    if cost < deducible:
        return cost
    
    # Si supera el deducible, suma el copago
    total = deducible + base_copago
    return min(total, cost)  # No pagar más del costo real


def format_currency(amount: float, currency: str = "USD") -> str:
    """Formatear número como moneda"""
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EC":
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def extract_symptom(user_message: str) -> str:
    """
    Extraer síntoma del mensaje del usuario
    
    Args:
        user_message: Mensaje del paciente
        
    Returns:
        Síntoma identificado
    """
    # Palabras clave comunes
    keywords = {
        "dolor": "dolor",
        "duele": "dolor",
        "fiebre": "fiebre",
        "tos": "tos",
        "alergia": "alergia",
        "visión": "problemas visuales",
        "cansancio": "cansancio",
        "inflamación": "inflamación"
    }
    
    message_lower = user_message.lower()
    for keyword, symptom in keywords.items():
        if keyword in message_lower:
            return symptom
    
    return "síntoma general"


def format_hospital_recommendation(hospital: dict, copago: float) -> str:
    """Formatear recomendación de hospital"""
    return f"""
🏥 **{hospital.get('nombre', 'Hospital')}**
   Red: {hospital.get('red', 'N/A')}
   Copago: {format_currency(copago)}
   Teléfono: {hospital.get('telefono', 'N/A')}
   Dirección: {hospital.get('direccion', 'N/A')}
"""


def validate_api_key(api_key: str) -> bool:
    """Validar que la API key tenga formato válido"""
    if not api_key:
        return False
    if len(api_key) < 10:
        return False
    return True


def safe_divide(numerator: float, denominator: float, default: float = 0) -> float:
    """División segura evitando división por cero"""
    try:
        return numerator / denominator if denominator != 0 else default
    except (ZeroDivisionError, TypeError):
        return default