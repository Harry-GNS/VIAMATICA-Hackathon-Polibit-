"""
init_database.py - Script para inicializar la base de datos con datos de ejemplo
Ejecutar: python init_database.py
"""

import os
from dotenv import load_dotenv
from backend.database.db_manager import DatabaseManager

if __name__ == '__main__':
    load_dotenv()
    
    db_path = os.getenv('DATABASE_PATH', 'data/viamatica.db')
    
    print("🔄 Inicializando base de datos...")
    db = DatabaseManager(db_path)
    
    # Limpiar datos anteriores
    print("🧹 Limpiando datos anteriores...")
    db.clear_all()
    
    # Cargar datos de ejemplo
    print("📥 Cargando datos de ejemplo...")
    db.load_sample_data()
    
    # Mostrar resumen
    print("\n✅ Base de datos inicializada exitosamente!")
    print(f"📊 Estadísticas:")
    print(f"   - Hospitales: {len(db.get_hospitales())}")
    print(f"   - Especialidades: {len(db.get_especialidades())}")
    print(f"   - Planes de seguro: {len(db.get_planes_seguro())}")
    print(f"\n📂 Ubicación: {db_path}")
