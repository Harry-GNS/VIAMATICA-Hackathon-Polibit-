/**
 * VIAMATICA - Script Principal
 * Gestiona la interacción del chat y funcionalidades de la interfaz
 */

class ViamaticaChat {
    constructor() {
        this.chatInput = document.querySelector('.chat-input');
        this.btnSend = document.querySelector('.btn-send');
        this.messagesContainer = document.querySelector('.messages-container');
        this.quickButtons = document.querySelectorAll('.quick-btn');
        this.historyItems = document.querySelectorAll('.history-item');
        this.init();
    }

    init() {
        this.attachEventListeners();
        this.focusInput();
    }

    attachEventListeners() {
        // Enviar mensaje al hacer click en botón
        this.btnSend.addEventListener('click', () => this.sendMessage());

        // Enviar mensaje al presionar Enter
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Preguntas rápidas
        this.quickButtons.forEach((btn) => {
            btn.addEventListener('click', () => {
                const question = btn.querySelector('span').textContent;
                this.chatInput.value = question;
                this.focusInput();
            });
        });

        // Historial rápido
        this.historyItems.forEach((item) => {
            item.addEventListener('click', () => {
                const specialty = item.querySelector('span').textContent;
                this.chatInput.value = `Quisiera consultarme sobre ${specialty.toLowerCase()}`;
                this.focusInput();
            });
        });
    }

    sendMessage() {
        const message = this.chatInput.value.trim();

        if (!message) return;

        // Agregar mensaje del usuario
        this.addMessage(message, 'user');

        // Limpiar input
        this.chatInput.value = '';
        this.chatInput.focus();

        // Simular respuesta del bot (en producción, enviaría al backend)
        setTimeout(() => {
            this.simulateBotResponse(message);
        }, 800);
    }

    addMessage(text, sender = 'bot') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const now = new Date();
        const time = now.toLocaleTimeString('es-ES', {
            hour: '2-digit',
            minute: '2-digit',
        });

        if (sender === 'bot') {
            messageDiv.innerHTML = `
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>${this.escapeHtml(text)}</p>
                    <small>hace un momento</small>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <p>${this.escapeHtml(text)}</p>
                    <small>hace un momento</small>
                </div>
            `;
        }

        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    simulateBotResponse(userMessage) {
        const lowerMessage = userMessage.toLowerCase();
        let response = '';

        // Respuestas básicas según palabras clave
        if (
            lowerMessage.includes('dolor') ||
            lowerMessage.includes('síntoma') ||
            lowerMessage.includes('duele')
        ) {
            response = this.generateMedicalResponse(userMessage);
        } else if (
            lowerMessage.includes('costo') ||
            lowerMessage.includes('precio') ||
            lowerMessage.includes('copago')
        ) {
            response = this.generateCostResponse();
        } else if (
            lowerMessage.includes('hospital') ||
            lowerMessage.includes('clínica')
        ) {
            response = this.generateHospitalResponse();
        } else if (
            lowerMessage.includes('cobertura') ||
            lowerMessage.includes('aseguradora') ||
            lowerMessage.includes('plan')
        ) {
            response = this.generateCoverageResponse();
        } else {
            response = this.generateGenericResponse();
        }

        this.addMessage(response, 'bot');
    }

    generateMedicalResponse(symptom) {
        return `<div class="bot-response">
            <p><strong>Análisis de síntomas:</strong> Entiendo que mencionas síntomas relacionados con tu consulta. Basándome en esto, te recomiendo:

            <div class="response-card" style="margin-top: 8px;">
                <h4>Especialidad Recomendada</h4>
                <p class="specialty">Medicina General</p>
                <div class="cost-info">
                    <span class="copago">Copago: <strong>$35</strong></span>
                    <span class="coverage">Cobertura: <strong>92%</strong></span>
                </div>
            </div>

            <div class="response-card">
                <h4>Próximos Pasos</h4>
                <div style="font-size: 13px; line-height: 1.6;">
                    <p>1. Agenda una cita en cualquiera de nuestros hospitales asociados</p>
                    <p>2. Lleva tu documento de identidad y carnet de aseguradora</p>
                    <p>3. Prepara una lista de tus síntomas</p>
                </div>
            </div>
        </div>`;
    }

    generateCostResponse() {
        return `<div class="bot-response">
            <p><strong>Información de Costos:</strong> Aquí está el desglose según tu plan:

            <div class="response-card" style="margin-top: 8px;">
                <h4>Costos Típicos</h4>
                <div style="font-size: 13px; display: flex; flex-direction: column; gap: 8px;">
                    <div><strong>Consulta General:</strong> Copago $35</div>
                    <div><strong>Especialista:</strong> Copago $60</div>
                    <div><strong>Laboratorios:</strong> Copago $25</div>
                    <div><strong>Radiografía:</strong> Copago $40</div>
                </div>
            </div>

            <p style="margin-top: 8px;">Recuerda que ya has utilizado $150 de tu deducible de $500.</p>
        </div>`;
    }

    generateHospitalResponse() {
        return `<div class="bot-response">
            <p><strong>Hospitales Disponibles en tu Red:</strong>

            <div class="response-card">
                <h4>Opciones Cercanas</h4>
                <div class="hospital-list">
                    <div class="hospital-item">
                        <p>Hospital Central Metropolitano</p>
                        <small>A 2.5 km • Disponibilidad: Hoy • Tel: (1) 2345-6789</small>
                    </div>
                    <div class="hospital-item">
                        <p>Clínica Premium Salud</p>
                        <small>A 5.1 km • Disponibilidad: Mañana • Tel: (1) 9876-5432</small>
                    </div>
                    <div class="hospital-item">
                        <p>Centro Médico San Rafael</p>
                        <small>A 7.3 km • Disponibilidad: Mañana • Tel: (1) 1234-5678</small>
                    </div>
                </div>
            </div>
        </div>`;
    }

    generateCoverageResponse() {
        return `<div class="bot-response">
            <p><strong>Detalles de tu Cobertura:</strong>

            <div class="response-card">
                <h4>Plan Gold Plus</h4>
                <div style="font-size: 13px; display: flex; flex-direction: column; gap: 10px;">
                    <div>
                        <strong>Aseguradora:</strong> SeguroPlus<br>
                        <strong>Vigencia:</strong> 12 meses<br>
                        <strong>Cobertura Base:</strong> 92%
                    </div>
                    <div>
                        <strong>Deducible:</strong> $500 (Utilizado: $150)<br>
                        <strong>Copago Máx/Año:</strong> $5,000<br>
                        <strong>Limitaciones:</strong> Ninguna
                    </div>
                </div>
            </div>

            <p style="margin-top: 8px; font-size: 12px;">¿Necesitas ayuda para entender algo específico de tu cobertura?</p>
        </div>`;
    }

    generateGenericResponse() {
        return `Entiendo tu pregunta. Puedo ayudarte con:<br><br>
        • Síntomas y especialidades médicas<br>
        • Costos y copagos<br>
        • Hospitales disponibles<br>
        • Detalles de tu cobertura<br><br>
        ¿Qué información necesitas en este momento?`;
    }

    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 0);
    }

    focusInput() {
        this.chatInput.focus();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new ViamaticaChat();
});

// Agregar efecto visual al enviar
document.addEventListener('DOMContentLoaded', () => {
    const btnSend = document.querySelector('.btn-send');
    const originalHTML = btnSend.innerHTML;

    document.querySelector('.chat-input').addEventListener('input', () => {
        const input = document.querySelector('.chat-input');
        if (input.value.trim()) {
            btnSend.style.opacity = '1';
        } else {
            btnSend.style.opacity = '0.7';
        }
    });
});
