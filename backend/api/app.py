"""
backend/api/app.py - Aplicación Flask y rutas principales
Define los endpoints de la API conversacional
"""

import os
from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
from backend.agent.copago_agent import CopagoAgent
import traceback

def create_app():
    """Factory pattern para crear la aplicación Flask"""
    # Definir rutas para frontend
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend')
    
    app = Flask(__name__, static_folder=frontend_path, static_url_path='')
    CORS(app)  # Habilitar CORS para frontend
    
    # Inicializar agente
    agent = CopagoAgent()
    
    # Rutas
    @app.route('/', methods=['GET'])
    def index():
        """Servir frontend principal"""
        return send_from_directory(frontend_path, 'index.html')
    
    @app.route('/<path:filename>', methods=['GET'])
    def serve_static(filename):
        """Servir archivos estáticos (CSS, JS, etc)"""
        return send_from_directory(frontend_path, filename)
    
    @app.route('/health', methods=['GET'])
    def health():
        """Verificar que el servidor está activo"""
        return jsonify({"status": "ok", "message": "Servidor activo"}), 200
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        """
        Endpoint principal: recibe mensaje del usuario
        Body: {"message": "Mi síntoma..."}
        """
        try:
            data = request.json
            user_message = data.get('message', '')
            
            if not user_message:
                return jsonify({"error": "Mensaje vacío"}), 400
            
            # Obtener respuesta del agente
            response = agent.process_message(user_message)
            
            return jsonify({
                "status": "success",
                "message": response
            }), 200
            
        except Exception as e:
            print(f"Error en /api/chat: {str(e)}")
            traceback.print_exc()
            return jsonify({
                "status": "error",
                "message": "Error procesando solicitud",
                "error": str(e)
            }), 500
    
    @app.route('/api/reset', methods=['POST'])
    def reset():
        """Reiniciar conversación"""
        agent.reset_conversation()
        return jsonify({"status": "success", "message": "Conversación reiniciada"}), 200
    
    # Error handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Ruta no encontrada"}), 404
    
    return app