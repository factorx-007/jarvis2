# 🤖 Jarvis / Juan — Asistente Virtual: Guía Completa (Versión Standalone)

> Soy **Juan**, tu asistente virtual creado con tecnología híbrida (Java + Python). Ahora empaquetado en un único ejecutable portátil que funciona sin consolas negras ni instalaciones de código complejas.

---

## 🚀 ¿Qué hace Jarvis ahora mismo?

Jarvis ha evolucionado a una arquitectura Standalone (Todo en Uno). Al ejecutar `Jarvis.exe`, ocurren tres cosas simultáneamente de forma transparente e invisible:

1. **Orquestación Dual**: Inicia silenciosamente un servidor Java (Spring Boot) en el puerto `8080` (que maneja la base de datos H2 y lógica interna) y un Daemon de Python (que procesa la Inteligencia Artificial y la voz neuronal).
2. **Interfaz Gráfica Integrada (Mangekyou)**: Despliega una interfaz moderna estilo Akatsuki conectada por WebSockets en tiempo real que te permite ver el historial de conversaciones y ejecutar comandos.
3. **Escucha Activa Automática**: La voz neuronal de Juan te saluda al iniciar y el micrófono queda escuchando de fondo. Puedes darle comandos verbales si pronuncias su palabra clave.

---

## 🛠️ Cómo Iniciar y Configurar Jarvis

¡Olvídate de los scripts `.bat`! Iniciar a Juan ahora es cuestión de dos clics.

### Pasos de Ejecución (Para cualquier PC)
1. **Descomprimir**: Si acabas de descargar a Jarvis, asegúrate de **extraer** todo el contenido del archivo `Jarvis_Portable.zip` en una carpeta. (¡No lo ejecutes desde dentro del ZIP!).
2. Haz doble clic en el archivo **`Jarvis.exe`**.
3. **Pantalla de Configuración Nativa**: Si es la primera vez que lo abres (o si borraste tu llave), aparecerá de inmediato una ventanita clásica de Windows pidiéndote tu API Key de OpenRouter.
4. **Ingresar la Clave**: Pega tu API Key (por ejemplo, `sk-or-v1-...`) y pulsa Aceptar.
5. **Arranque Inmediato**: Jarvis guardará automáticamente tu llave en un archivo oculto `.env` y encenderá todos los motores sin que tengas que reiniciar nada.
6. ¡Listo! Verás el panel de control y escucharás la voz de Juan diciendo: *"Hola, soy Juan. Iniciando sistemas"*.

---

## 🐞 Herramientas de Depuración (Sharingan Debugger)

Si en algún momento notas que Jarvis no te escucha o la IA parece fallar, hemos integrado herramientas profesionales para diagnosticar problemas en tiempo real:

- **La Consola Secreta**: Haz clic directamente sobre el **Ojo Sharingan** rojo (arriba a la derecha) o presiona el botón **Configurar API Key** en la barra lateral.
- **¿Qué muestra?**: Al abrirse, verás los logs internos exactos tanto de **Python** (Inteligencia, Voz, Micrófono) como de **Java** (Base de datos, WebSockets, Spring Boot).
- **Botón "Copiar Logs"**: Un botón rápido para copiar todo el error al portapapeles y pegarlo si requieres soporte.

---

## 🎙️ Cómo Activar a Juan (Wake Word)

Juan escucha **todo el tiempo** en silencio. Solo reacciona cuando dices su nombre primero.

**Palabra mágica: `juan`**

| Forma de hablarle | Ejemplo completo |
| :--- | :--- |
| `"Juan, [comando]"` | *"Juan, abre la calculadora"* |
| `"Juan"` (pausa) + comando | *"Juan" → espera → "busca en google recetas de cocina"* |

---

## ⚡ Todo lo que Juan Puede Hacer

### 🪟 1. Control de Aplicaciones Windows
Juan puede abrir, cerrar, minimizar o maximizar cualquier programa local.

- **Abrir**: *"Juan, abre chrome"*, *"Juan, abre spotify"*, *"Juan, abre excel"*
- **Cerrar**: *"Juan, cierra notepad"*, *"Juan, termina el explorador"*
- **Minimizar/Maximizar**: *"Juan, minimiza chrome"*, *"Juan, maximiza discord"*

### 🌐 2. Navegación Web y Búsquedas
Juan toma el control del navegador Chromium (invisible o visible) por ti.

- **Búsquedas**: *"Juan, busca en youtube cómo hacer pan"*, *"Juan, busca en google programación en java"*
- **Páginas directas**: *"Juan, abre facebook"*, *"Juan, abre twitch"*

### 🔊 3. Control Multimedia y Sistema
- **Volumen**: *"Juan, sube el volumen"*, *"Juan, silencia el equipo"*
- **Reproducción**: *"Juan, pausa"*, *"Juan, siguiente canción"*, *"Juan, reproduce"*
- **Seguridad**: *"Juan, bloquea la pantalla"*
- **Utilidades**: *"Juan, toma una captura de pantalla"*, *"Juan, qué hora es"*

### 🧠 4. Inteligencia Artificial Extrema (Itachi Uchiha)
Juan ahora tiene el intelecto y personalidad de Itachi Uchiha, integrado mediante la API de OpenRouter (`gpt-4o-mini`).

- **Memoria de corto plazo**: Recuerda de qué estaban hablando en los últimos mensajes.
- **Consultas complejas**: Puedes hacerle cualquier pregunta del mundo real.
- **Control de Longitud**: 
  - **Por defecto:** Las respuestas son MUY cortas y directas para que la voz no tarde y no agote tokens.
  - **Contexto Extenso:** Si quieres una explicación magistral y detallada, **díselo explícitamente**: *"Juan, explícame a detalle por qué ocurrió la segunda guerra mundial"*. Él dejará su concisión a un lado y te dará una respuesta masiva y sabia.

---

## 🏗️ Mapa Interno (Por si eres desarrollador)

Todo está dentro de `dist/Jarvis/`. 
- **El Motor**: `Jarvis.exe` coordina todo.
- **El Cerebro Java**: Corre desde `java-core/target/core-0.0.1-SNAPSHOT.jar`.
- **El Rostro (HTML/JS)**: Se encuentra en la carpeta `4-dashboard-rostro`.
- **La Llave Maestra**: Se guarda automáticamente en un archivo oculto `.env` dentro de esa misma carpeta.
