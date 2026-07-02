document.addEventListener("DOMContentLoaded", () => {
    const wsStatusText = document.getElementById("ws-text");
    const wsStatusDot = document.querySelector(".status-dot");
    const terminalLog = document.getElementById("terminal-log");
    const mockVoiceInput = document.getElementById("mock-voice");
    const btnSend = document.getElementById("btn-send");

    let socket;

    function connectWebSocket() {
        socket = new WebSocket("ws://localhost:8080/jarvis-ws");

        socket.onopen = () => {
            wsStatusText.textContent = "Conectado al Cerebro (Java)";
            wsStatusDot.style.backgroundColor = "var(--success)";
            wsStatusDot.style.boxShadow = "0 0 8px var(--success)";
            addLog("Sistema", "Conexión WebSocket establecida con éxito.", null, null);
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                
                // Si el evento es un broadcast de actualización de historial
                if (data.type === "HISTORY_UPDATE") {
                    const payload = data.payload;
                    addLog(
                        "Voz", 
                        payload.raw_text, 
                        payload.intent, 
                        payload.target
                    );
                } 
                // Si recibimos directamente la respuesta procesada
                else if (data.intent) {
                    // Solo registramos si tiene tts_message u otra info útil que no venga en el HISTORY_UPDATE
                    if(data.tts_message) {
                        addLog("Cerebro", data.tts_message, data.intent, data.target);
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
        entry.className = "log-entry";
        
        const time = new Date().toLocaleTimeString();
        
        let html = `<span class="log-time">[${time}] ${source}</span>`;
        html += `<span class="log-text">"${text}"</span>`;
        
        if (intent) {
            html += `<span class="log-intent">➜ Intent: ${intent} | Target: ${target || 'N/A'}</span>`;
        }
        
        entry.innerHTML = html;
        terminalLog.appendChild(entry);
        
        // Auto scroll
        terminalLog.scrollTop = terminalLog.scrollHeight;
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

    // Iniciar conexión
    connectWebSocket();
});
