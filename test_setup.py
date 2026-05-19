"""
test_setup.py - Script para verificar que todo está configurado correctamente
Ejecutar: python test_setup.py
"""

import os
from dotenv import load_dotenv

print("=" * 60)
print("🔍 VERIFICACIÓN DE SETUP - VIAMATICA")
print("=" * 60)

# Cargar variables de entorno
load_dotenv()

# 1. Verificar API Key
print("\n1️⃣  Verificando GROQ_API_KEY...")
groq_key = os.getenv('GROQ_API_KEY')
if groq_key and groq_key != 'tu_groq_api_key_aqui':
    print("   ✅ GROQ_API_KEY configurado")
else:
    print("   ❌ GROQ_API_KEY NO configurado o valor por defecto")
    print("   📌 Instrucciones:")
    print("      1. Ve a https://console.groq.com")
    print("      2. Copia tu API key")
    print("      3. Pega en .env: GROQ_API_KEY=tu_key")

# 2. Verificar dependencias
print("\n2️⃣  Verificando dependencias...")
try:
    import flask
    print("   ✅ Flask instalado")
except:
    print("   ❌ Flask NO instalado")

try:
    import groq
    print("   ✅ Groq instalado")
except:
    print("   ❌ Groq NO instalado")
    print("   💡 Ejecuta: pip install -r requirements.txt")

# 3. Verificar estructura de carpetas
print("\n3️⃣  Verificando estructura de carpetas...")
folders = ['backend', 'backend/api', 'backend/agent', 'backend/database', 'backend/integrations', 'models']
for folder in folders:
    if os.path.isdir(folder):
        print(f"   ✅ {folder}/")
    else:
        print(f"   ❌ {folder}/ FALTA")

# 4. Verificar base de datos
print("\n4️⃣  Verificando base de datos...")
try:
    from backend.database.db_manager import DatabaseManager
    db = DatabaseManager()
    hospitales = db.get_hospitales()
    print(f"   ✅ Base de datos OK - {len(hospitales)} hospitales cargados")
except Exception as e:
    print(f"   ❌ Error en base de datos: {e}")

# 5. Verificar agente
print("\n5️⃣  Verificando agente...")
try:
    if groq_key and groq_key != 'tu_groq_api_key_aqui':
        from backend.agent.copago_agent import CopagoAgent
        agent = CopagoAgent()
        print("   ✅ Agente inicializado correctamente")
    else:
        print("   ⏭️  Saltando (falta API key)")
except Exception as e:
    print(f"   ❌ Error en agente: {e}")

print("\n" + "=" * 60)
print("🚀 SETUP COMPLETO!")
print("=" * 60)
print("\n📍 Próximos pasos:")
print("   1. pip install -r requirements.txt")
print("   2. Configurar GROQ_API_KEY en .env")
print("   3. python main.py")
print("\n")
