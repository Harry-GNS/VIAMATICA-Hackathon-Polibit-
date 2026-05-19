/**
 * VIAMATICA - Script Principal
 * Gestiona la interacción del chat y funcionalidades de la interfaz
 */

class ViamaticaChat {
    constructor() {
        this.chatInput = document.querySelector('.chat-input');
        this.btnSend = document.querySelector('.btn-send');
        this.messagesContainer = document.querySelector('.messages-container');
        this.chatWelcome = document.querySelector('.chat-welcome');
        this.historyItems = document.querySelectorAll('.history-item');
        this.hamburgerBtn = document.getElementById('hamburgerBtn');
        this.sidebarOverlay = document.getElementById('sidebarOverlay');
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

        // Historial rápido
        this.historyItems.forEach((item) => {
            item.addEventListener('click', () => {
                const specialty = item.querySelector('span').textContent;
                this.chatInput.value = `Quisiera consultarme sobre ${specialty.toLowerCase()}`;
                this.sendMessage();
            });
        });

        // Hamburger menu
        if (this.hamburgerBtn) {
            this.hamburgerBtn.addEventListener('click', () => {
                document.documentElement.classList.toggle('sidebar-collapsed');
                document.documentElement.classList.toggle('sidebar-open');
            });
        }

        if (this.sidebarOverlay) {
            this.sidebarOverlay.addEventListener('click', () => {
                document.documentElement.classList.remove('sidebar-open');
                document.documentElement.classList.add('sidebar-collapsed');
            });
        }
    }

    sendMessage() {
        const message = this.chatInput.value.trim();

        if (!message) return;

        // Ocultar zona de bienvenida
        if (this.chatWelcome) {
            this.chatWelcome.style.display = 'none';
        }

        // Agregar mensaje del usuario
        this.addMessage(message, 'user');

        // Limpiar input
        this.chatInput.value = '';
        this.chatInput.focus();

        // Enviar al backend
        this.sendToBackend(message);
    }

    async sendToBackend(message) {
        try {
            // Mostrar indicador de carga
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message bot-message';
            loadingDiv.innerHTML = `
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="loading">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            `;
            this.messagesContainer.appendChild(loadingDiv);
            this.scrollToBottom();

            // Hacer petición al backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            // Remover loading
            loadingDiv.remove();

            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }

            const data = await response.json();

            if (data.status === 'success') {
                this.addMessage(data.message, 'bot');
            } else {
                this.addMessage('Error procesando tu solicitud: ' + (data.message || 'Error desconocido'), 'bot');
            }
        } catch (error) {
            this.addMessage('Error conectando con el servidor: ' + error.message, 'bot');
        }
    }

    addMessage(text, sender = 'bot') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        if (sender === 'bot') {
            messageDiv.innerHTML = `
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="bot-response">${text}</div>
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

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new ViamaticaChat();
});
