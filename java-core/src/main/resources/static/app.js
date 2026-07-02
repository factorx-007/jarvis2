document.addEventListener("DOMContentLoaded", () => {
    const wsStatusText = document.getElementById("ws-text");
    const wsStatusDot = document.querySelector(".status-dot");
    const terminalLog = document.getElementById("terminal-log");
    const chatContainer = document.getElementById("chat-container");
    const mockVoiceInput = document.getElementById("mock-voice");
    const btnSend = document.getElementById("btn-send");

    let socket;

    function connectWebSocket() {
        socket = new WebSocket("ws://localhost:8080/jarvis-ws");

        socket.onopen = () => {
            wsStatusText.textContent = "Conectado al Cerebro (Java + AI)";
            wsStatusDot.style.backgroundColor = "var(--success)";
            wsStatusDot.style.boxShadow = "0 0 8px var(--success)";
            addLog("Sistema", "Conexión WebSocket establecida con éxito.", null, null);
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                
                // Actualizaciones de comandos de sistema y voz
                if (data.type === "HISTORY_UPDATE") {
                    const payload = data.payload;
                    addLog("Voz", payload.raw_text, payload.intent, payload.target);
                    // Agregar burbuja de usuario al chat
                    addChatBubble(payload.raw_text, "user-bubble");
                    
                    // Mostrar respuesta del sistema a menos que sea CHAT_QUERY (eso lo maneja el LLM)
                    if (payload.intent !== "CHAT_QUERY" && payload.intent !== "UNKNOWN_APP") {
                        // En la vida real aquí podríamos mostrar un mensaje de confirmación
                        // addChatBubble("Ejecutando orden: " + payload.intent, "bot-bubble");
                    }
                } 
                // Respuestas generadas por la Inteligencia Artificial (Gemini)
                else if (data.type === "LLM_RESPONSE") {
                    addLog("LLM", "Generó respuesta", "CHAT", null);
                    addChatBubble(data.text, "bot-bubble");
                }
                // Si recibimos directamente la respuesta procesada de comandos estáticos
                else if (data.intent && data.tts_message) {
                    addLog("Cerebro", data.tts_message, data.intent, data.target);
                    if (data.intent !== "UNKNOWN_APP") {
                        addChatBubble(data.tts_message, "bot-bubble");
                    }
                }
            } catch (e) {
                console.error("Error parseando mensaje WS", e);
            }
        };

        socket.onclose = () => {
            wsStatusText.textContent = "Desconectado. Reintentando...";
            wsStatusDot.style.backgroundColor = "var(--error)";
            wsStatusDot.style.boxShadow = "0 0 8px var(--error)";
            setTimeout(connectWebSocket, 3000);
        };

        socket.onerror = (error) => {
            console.error("WebSocket Error:", error);
        };
    }

    function addLog(source, text, intent, target) {
        const entry = document.createElement("div");
        entry.className = "log-entry animate__animated animate__fadeIn";
        const time = new Date().toLocaleTimeString();
        
        let html = `<span class="log-time">[${time}] ${source}</span>`;
        html += `<span class="log-text">"${text}"</span>`;
        if (intent) {
            html += `<span class="log-intent">➜ ${intent} | Target: ${target || 'N/A'}</span>`;
        }
        
        entry.innerHTML = html;
        terminalLog.appendChild(entry);
        terminalLog.scrollTop = terminalLog.scrollHeight;
    }

    function addChatBubble(text, type) {
        const bubble = document.createElement("div");
        bubble.className = `chat-bubble ${type} animate__animated animate__fadeInUp`;
        bubble.textContent = text;
        chatContainer.appendChild(bubble);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    btnSend.addEventListener("click", () => {
        const text = mockVoiceInput.value.trim();
        if (text && socket && socket.readyState === WebSocket.OPEN) {
            const payload = {
                source: "voice",
                timestamp: new Date().toISOString(),
                raw_text: text
            };
            socket.send(JSON.stringify(payload));
            mockVoiceInput.value = "";
        }
    });

    mockVoiceInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            btnSend.click();
        }
    });

    // Quick actions
    const quickBtns = document.querySelectorAll(".quick-btn");
    quickBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const cmd = btn.getAttribute("data-cmd");
            if (cmd && socket && socket.readyState === WebSocket.OPEN) {
                const payload = {
                    source: "voice",
                    timestamp: new Date().toISOString(),
                    raw_text: cmd
                };
                socket.send(JSON.stringify(payload));
            }
        });
    });

    // Iniciar conexión
    connectWebSocket();
});
