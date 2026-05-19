"""
main.py - Entry point principal de la aplicación
Inicia el servidor Flask y el agente conversacional
"""

import os
from dotenv import load_dotenv
from backend.api.app import create_app

# Cargar variables de entorno
load_dotenv()

if __name__ == '__main__':
    # Crear aplicación Flask
    app = create_app()
    
    # Configuración
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True') == 'True'
    
    # Iniciar servidor
    print(f"🚀 Iniciando servidor en http://localhost:{port}")
    print(f"📊 Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )