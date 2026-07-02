# 🤖 Juan — Asistente Virtual Híbrido (Java + Python)

Juan es un asistente virtual avanzado con arquitectura de microservicios. Utiliza **Java (Spring Boot)** como cerebro lógico e Inteligencia Artificial (NLP), y **Python** como sistema nervioso para controlar el micrófono, escuchar, hablar (TTS neuronal) y controlar tu PC Windows.

---

## 📥 Requisitos Previos (Instalación)

Si acabas de descargar este repositorio de GitHub, necesitas tener instalados estos **3 programas base** en tu computadora para que todo funcione:

### 1. Python (3.10 o superior)
- Descárgalo desde [python.org](https://www.python.org/downloads/).
- **MUY IMPORTANTE:** Durante la instalación en Windows, asegúrate de marcar la casilla **"Add Python to PATH"** en la primera pantalla.

### 2. Java JDK (17 o superior)
- Descárgalo e instálalo (puedes usar el instalador de [Oracle](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html) o [Adoptium Eclipse Temurin](https://adoptium.net/es/temurin/releases/?version=17)).
- **Nota:** Es necesario instalar el "JDK", no solo el JRE, ya que el sistema necesita compilar el código.

### 3. Navegador basado en Chromium (Edge o Chrome)
- El asistente utiliza Microsoft Edge TTS para hablar con una voz neuronal súper realista y requiere de un navegador instalado para las funciones de búsqueda web.

---

## 🚀 Cómo Iniciar el Proyecto (Primer Uso)

Una vez que tengas Python y Java instalados, iniciar a Juan es muy fácil gracias a los scripts de inicio rápido:

### Paso 1: Iniciar el Cerebro (Java)
1. Ve a la carpeta principal del proyecto.
2. Haz doble clic en el archivo **`INICIAR_JUAN.bat`**.
3. *La primera vez que lo ejecutes tardará un poco porque descargará automáticamente todas las librerías de Spring Boot.*
4. Cuando veas el mensaje `Started JarvisApplication`, la ventana negra está lista. ¡No la cierres!

### Paso 2: Iniciar el Sistema Nervioso (Python)
1. Ve a la carpeta principal del proyecto.
2. Haz doble clic en el archivo **`INICIAR_PYTHON.bat`**.
3. *La primera vez que lo ejecutes descargará las librerías de Python (`speechrecognition`, `playwright`, etc).*
4. Escucharás a Juan presentarse ("Hola, soy Juan").

### Paso 3: Usar el Dashboard (Opcional pero recomendado)
- Abre el archivo `4-dashboard-rostro/index.html` en tu navegador favorito.
- Desde ahí podrás ver todos los logs, enviar comandos de texto, y usar botones de macros rápidas.

---

## 🗣️ ¿Cómo hablar con Juan?

Juan siempre está escuchando, pero solo presta atención si inicias tu frase con su nombre.

**Ejemplos de comandos de voz:**
- *"Juan, abre chrome"*
- *"Juan, busca en youtube música"*
- *"Juan, qué hora es"*
- *"Juan, bloquea la pantalla"*
- *"Juan, reproduce la música"*

> 📖 **Para ver la lista de TODOS los comandos que Juan entiende, lee el archivo `JUAN_GUIA_COMPLETA.md` incluido en este repositorio.**
