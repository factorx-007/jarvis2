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

    // Iniciar conexión WebSocket con reintentos automáticos
    connectWebSocket();
    
    // Elementos del DOM
    const sharinganIcon = document.querySelector(".sharingan-icon");
    const debugModal = document.getElementById("debug-modal");
    const setupModal = document.getElementById("setup-modal");
    const closeBtn = document.querySelector(".close-btn");
    const debugLogs = document.getElementById("debug-logs");
    const refreshLogsBtn = document.getElementById("refresh-logs");
    const copyLogsBtn = document.getElementById("copy-logs");
    const saveApiKeyBtn = document.getElementById("save-api-key");
    const apiKeyInput = document.getElementById("api-key-input");
    
    // Simulador de pywebview usando llamadas HTTP al backend Python
    window.pywebview = {
        api: {
            get_logs: async () => {
                try {
                    let res = await fetch("http://localhost:8081/api/logs");
                    let data = await res.json();
                    return data.logs;
                } catch(e) { return "Error obteniendo logs: " + e; }
            },
            has_api_key: async () => {
                try {
                    let res = await fetch("http://localhost:8081/api/has_key");
                    let data = await res.json();
                    return data.has_key;
                } catch(e) { return false; }
            },
            save_api_key: async (key) => {
                try {
                    let res = await fetch("http://localhost:8081/api/save_key", {
                        method: 'POST',
                        body: JSON.stringify({key: key}),
                        headers: {'Content-Type': 'application/json'}
                    });
                    let data = await res.json();
                    return data.success;
                } catch(e) { return false; }
            },
            start_python: async () => {
                try {
                    let res = await fetch("http://localhost:8081/api/start_python", {method: 'POST', body: "{}"});
                    return "Started";
                } catch(e) { return "Error"; }
            }
        }
    };

    function loadLogs() {
        window.pywebview.api.get_logs().then(logs => {
            debugLogs.textContent = logs;
        });
    }
    
    // Al hacer clic en el Sharingan
    sharinganIcon.addEventListener("click", () => {
        debugModal.classList.remove("hidden");
        loadLogs();
    });
    
    closeBtn.addEventListener("click", () => {
        debugModal.classList.add("hidden");
    });
    
    refreshLogsBtn.addEventListener("click", () => {
        loadLogs();
    });

    copyLogsBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(debugLogs.textContent).then(() => {
            alert("Logs copiados al portapapeles.");
        });
    });

    // Lógica para pedir API Key cuando la app inicia o al hacer clic
    const btnConfigApi = document.getElementById("btn-config-api");
    if (btnConfigApi) {
        btnConfigApi.addEventListener("click", () => {
            setupModal.classList.remove("hidden");
        });
    }

    // Inicializar comprobación de API KEY después de un breve delay
    setTimeout(() => {
        window.pywebview.api.has_api_key().then(hasKey => {
            if (!hasKey) {
                setupModal.classList.remove("hidden");
            }
        });
    }, 1000);

    saveApiKeyBtn.addEventListener("click", () => {
        const key = apiKeyInput.value.trim();
        if (key) {
            saveApiKeyBtn.textContent = "Guardando...";
            window.pywebview.api.save_api_key(key).then(success => {
                if (success) {
                    setupModal.classList.add("hidden");
                    alert("¡API Key guardada exitosamente!\n\nPor favor, CIERRA la ventana de Jarvis Activo y vuelve a ABRIR el ejecutable para que el cerebro de IA se conecte con tu nueva clave.");
                    saveApiKeyBtn.textContent = "Guardar e Iniciar";
                    window.pywebview.api.start_python().then(res => {
                        console.log("Python Daemon Result:", res);
                    });
                } else {
                    alert("Error al guardar la API Key.");
                    saveApiKeyBtn.textContent = "Guardar e Iniciar";
                }
            });
        } else {
            alert("Por favor ingresa una API Key válida.");
        }
    });
});
