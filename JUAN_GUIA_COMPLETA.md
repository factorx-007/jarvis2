# 🤖 Juan — Asistente Virtual Personal: Guía Completa

> Soy **Juan**, tu asistente virtual creado desde cero con tecnología híbrida (Java + Python). Puedo escucharte, hablarte, controlar tu PC, navegar por internet y aprender de ti.

---

## 📖 Historia del Proyecto

Este asistente fue diseñado con una arquitectura de **microservicios**: tres módulos completamente independientes que se comunican en tiempo real entre sí a través de WebSockets (protocolo de mensajes en formato JSON).

El objetivo desde el inicio fue crear algo más que un simple script: una plataforma viva que pueda crecer, aprender y responder de manera natural como si fuera una persona real.

---

## 🏗️ Arquitectura: Los 3 Pilares de Juan

```
[TU VOZ] 🎙️
    ↓
[Python Daemon] → STT (Voz a Texto) → Envía texto a Java vía WebSocket
    ↑
[Java Core] → NLP (Identifica qué quieres) → Envía orden de vuelta a Python
    ↑
[Python Daemon] → Ejecuta la acción (abre app, navega, sube volumen...)
                → TTS (responde en voz natural)
    ↑
[Dashboard Web] → Muestra todo en tiempo real (puedes también escribir comandos)
```

### 🐍 Pilar 1: Python Daemon (`/python-daemon`)
Es el **sistema nervioso** de Juan. Se encarga de todo lo físico:
- **`reconocimiento_voz/stt_service.py`** — Escucha el micrófono 24/7 y activa a Juan cuando dices su nombre.
- **`sintesis_voz/tts_service.py`** — Le da voz humana y natural usando Microsoft Edge Neural TTS.
- **`control_sistema/os_controller.py`** — Controla Windows: abre, cierra, minimiza y maximiza apps.
- **`control_navegador/browser_controller.py`** — Toma el control del navegador Chromium para buscar y navegar.
- **`main.py`** — El director de orquesta: conecta todos los módulos y gestiona el WebSocket con Java.

### ☕ Pilar 2: Java Core (`/java-core`)
Es el **cerebro** de Juan. Piensa y decide:
- **`procesamiento_nlp/ProcesamientoLenguajeService.java`** — Analiza lo que dices, identifica tu intención y genera la respuesta en voz que Juan usará.
- **`memoria_personalizacion/LearningService.java`** — Guarda en base de datos todo lo que Juan aprende: alias, historial de comandos, preferencias.
- **`websocket/JarvisWebSocketHandler.java`** — Recibe mensajes de Python y del Dashboard y los enruta al lugar correcto.
- **Base de datos H2** — Embebida en el mismo Java, guarda historial e inteligencia aprendida en `data/jarvisdb`.

### 🌐 Pilar 3: Dashboard Web (`/4-dashboard-rostro`)
Es el **rostro** de Juan. Una interfaz visual estilo cyberpunk donde puedes:
- Ver la consola en tiempo real de todo lo que pasa.
- Enviar comandos escritos sin usar la voz.
- Usar botones de acción rápida con un solo clic.

---

## 🎙️ Cómo Activar a Juan (Wake Word)
Juan escucha **todo el tiempo** en silencio. Solo reacciona cuando dices su nombre primero.

**Palabra mágica: `juan`**

| Forma de hablarle | Ejemplo completo |
| :--- | :--- |
| `"Juan, [comando]"` | *"Juan, abre la calculadora"* |
| `"Juan"` (pausa) + comando | *"Juan" → espera → "abre notepad"* |

---

## ⚡ Todo lo que Juan Puede Hacer

### 🪟 1. Control de Aplicaciones Windows

Juan puede abrir, cerrar, minimizar o maximizar cualquier programa.

**Verbos que entiende:** `abre`, `abrir`, `inicia`, `lanza`, `ejecuta` / `cierra`, `termina`, `mata` / `minimiza`, `oculta` / `maximiza`, `restaura`, `muestra`

| Aplicación | Cómo pedirlo |
| :--- | :--- |
| Google Chrome | *"Juan, abre chrome"* o *"abre el navegador"* |
| Notepad / Bloc de notas | *"Juan, abre notepad"* |
| Calculadora | *"Juan, abre la calculadora"* |
| Explorador de archivos | *"Juan, abre el explorador"* o *"abre archivos"* |
| Spotify | *"Juan, abre spotify"* |
| Microsoft Word | *"Juan, abre word"* |
| Microsoft Excel | *"Juan, abre excel"* |
| PowerPoint | *"Juan, abre powerpoint"* |
| Paint | *"Juan, abre paint"* |
| Terminal / CMD | *"Juan, abre la consola"* o *"abre la terminal"* |
| Microsoft Edge | *"Juan, abre edge"* |
| Configuración de Windows | *"Juan, abre la configuración"* |
| Discord | *"Juan, abre discord"* |

### 🌐 2. Navegación Web y Búsquedas

Juan toma el control del navegador por ti.

| Comando | Ejemplo | Resultado |
| :--- | :--- | :--- |
| Buscar en Google | *"Juan, busca en google recetas de pasta"* | Abre Chrome, va a Google, escribe y presiona Enter |
| Buscar en YouTube | *"Juan, busca en youtube música lo-fi"* | Abre YouTube y busca el video |
| Abrir una página | *"Juan, abre youtube"* o *"abre facebook"* | Va directo a `youtube.com` o `facebook.com` |

**Sitios web directos que reconoce:** YouTube, Facebook, Netflix, WhatsApp, Instagram, Twitter, Twitch.

### 🔊 3. Control de Volumen

| Comando | Sinónimos válidos |
| :--- | :--- |
| Subir volumen | *"sube el volumen"*, *"más volumen"*, *"sube el audio"*, *"aumenta el volumen"* |
| Bajar volumen | *"baja el volumen"*, *"menos volumen"*, *"baja el audio"*, *"reduce el volumen"* |
| Silenciar | *"silencia"*, *"mute"*, *"quitar volumen"*, *"modo silencio"*, *"sin sonido"* |

### 🎵 4. Control Multimedia (Spotify, YouTube, etc.)

Controla cualquier reproductor que esté activo en Windows.

| Acción | Cómo pedirlo |
| :--- | :--- |
| Play / Pausa | *"Juan, reproduce"*, *"pausa"*, *"pon la música"*, *"play"* |
| Siguiente canción | *"Juan, siguiente"*, *"otra canción"*, *"salta"*, *"skip"* |
| Canción anterior | *"Juan, anterior"*, *"la anterior"*, *"regresa la canción"* |

### 🛡️ 5. Seguridad y Pantalla

| Acción | Cómo pedirlo |
| :--- | :--- |
| Bloquear pantalla | *"Juan, bloquea la pantalla"*, *"bloquea el equipo"*, *"bloquea el PC"* |
| Captura de pantalla | *"Juan, captura de pantalla"*, *"toma una captura"*, *"screenshot"* |

> La captura se guarda como `captura_jarvis.png` en la carpeta `python-daemon`.

### ⏰ 6. Información del Sistema

| Acción | Cómo pedirlo |
| :--- | :--- |
| Saber la hora | *"Juan, qué hora es"*, *"dime la hora"*, *"qué horas son"* |
| Saber la fecha | *"Juan, qué día es"*, *"la fecha"*, *"qué fecha es hoy"* |

Juan responderá con frases variadas y naturales, no siempre la misma.

### 🧠 7. Aprendizaje y Memoria (Alias)

Juan puede aprender palabras nuevas que tú le enseñes:

```
"Juan, aprende [tu_alias] como [nombre_real]"
```

| Ejemplo | Resultado |
| :--- | :--- |
| *"Juan, aprende mi navegador como chrome"* | La próxima vez que digas *"abre mi navegador"*, Juan abre Chrome |
| *"Juan, aprende el trabajo como word"* | *"abre el trabajo"* → Abre Word |

Todo queda guardado en la base de datos y persiste aunque apagues el PC.

---

## 💻 El Nuevo Dashboard (Mangekyou / Tema Akatsuki)

El archivo `d:/skinet/4-dashboard-rostro/index.html` ha sido rediseñado completamente con temática de Itachi Uchiha.

**Qué puedes hacer desde ahí:**
- **Chat Conversacional Ninja:** Tus comandos y las respuestas de Juan aparecen como burbujas de texto animadas, con transiciones fluidas.
- **Micro-Animaciones:** Incluye un *Sharingan* rotatorio puro CSS en la cabecera.
- **Panel Lateral (Registros Ocultos):** A la derecha, el registro técnico donde verás qué intención ejecutó el sistema.
- **Jutsus (Macros):** Botones listos para ejecutar comandos de un solo clic.

---

## 🧠 Inteligencia Artificial (Mente de Itachi)

Juan ahora tiene el intelecto y personalidad de Itachi Uchiha, integrado mediante OpenRouter (`gpt-4o-mini`).

**Capacidades de su Cerebro Neuronal:**
- **Memoria de corto plazo:** Recuerda los últimos 10 mensajes (Ej: *"¿Quién inventó el teléfono?"* -> *"¿Y en qué año nació?"*).
- **Control de Longitud (Genjutsu Flexible):** 
  - **Por defecto:** Las respuestas de Juan son MUY cortas y directas (para maximizar la velocidad de la voz).
  - **Contexto Extenso:** Si quieres una respuesta detallada y sabia, **díselo explícitamente**. Ejemplos: *"Juan, explícame a detalle por qué el cielo es azul"* o *"Juan, dame todo el contexto sobre la Revolución Industrial"*. Él se explayará sin límites.

*Ejemplos de cosas que puedes preguntarle:*
- `Juan, dame una idea para cenar hoy con ingredientes baratos.`
- `Juan, explícame la mecánica cuántica a detalle como si fuera un estudiante de la academia.`

---

## 🚀 Cómo Encender Todo (Nuevo Método Súper Rápido)

Olvídate de abrir Eclipse o lidiar con comandos manuales. Ahora iniciar a Juan es cosa de hacer dos clics.

### Paso 1: Iniciar el Cerebro (Java)
1. Ve a la carpeta `D:\skinet\`.
2. Haz doble clic en el archivo **`INICIAR_JUAN.bat`**.
3. Se abrirá una pequeña ventana negra. Espera a que diga `Started JarvisApplication`. (No cierres esta ventana).

### Paso 2: Iniciar el Sistema Nervioso (Python)
1. Ve a la carpeta `D:\skinet\`.
2. Haz doble clic en el archivo **`INICIAR_PYTHON.bat`**.
3. *Si es tu primera vez, instalará la librería de OpenRouter (`openai`) de forma automática.*
4. Juan hablará por los altavoces diciendo: *"Hola, soy Juan. Iniciando sistemas"*.

### Paso 3: Abrir el Dashboard
- Abre el archivo `D:\skinet\4-dashboard-rostro\index.html` en tu navegador y empieza a charlar.

### ✅ ¡Sistema listo! Dile "Juan, cuéntame algo interesante" para probar su nueva inteligencia.

---

## 🗺️ Mapa de Archivos del Proyecto

```
D:\skinet\
│
├── java-core\                          → Cerebro (Spring Boot + Java 17)
│   └── src\main\java\com\jarvis\core\
│       ├── JarvisApplication.java      → Punto de entrada del servidor
│       ├── procesamiento_nlp\          → Inteligencia y comprensión del lenguaje
│       ├── memoria_personalizacion\    → Base de datos y aprendizaje
│       └── websocket\                  → Canal de comunicación con Python y Dashboard
│
├── python-daemon\                      → Sistema Nervioso (Python 3.13)
│   ├── main.py                         → Director de orquesta
│   ├── reconocimiento_voz\             → Escucha el micrófono
│   ├── sintesis_voz\                   → Habla con voz neural
│   ├── control_sistema\                → Controla Windows
│   └── control_navegador\             → Controla el navegador web
│
├── 4-dashboard-rostro\                 → Cara visual (HTML + CSS + JS)
│   ├── index.html                      → Dashboard principal
│   └── style.css                       → Estilos cyberpunk
│
└── comandos_juan.md                    → Referencia rápida de comandos
```

---

## 🔮 Funciones Futuras Planificadas

| Función | Descripción |
| :--- | :--- |
| 🌤️ Clima | *"Juan, cómo está el clima"* → Consulta API de clima en tiempo real |
| ⏰ Recordatorios | *"Juan, recuérdame en 20 minutos apagar el horno"* |
| 🎵 Spotify directo | Control de Spotify vía API oficial (buscar canción, artista) |
| 💡 Domótica | Control de luces inteligentes vía WiFi (HTTP/MQTT) |
| 📰 Noticias | *"Juan, cuáles son las noticias de hoy"* → Scrapeo en tiempo real |
| 👤 Perfil de usuario | Juan aprende tu nombre y personaliza todas sus respuestas |
