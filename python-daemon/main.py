import asyncio
import websockets
import json
import datetime
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from reconocimiento_voz.stt_service import STTService
from sintesis_voz.tts_service import TTSService
from control_sistema.os_controller import OSController
from control_navegador.browser_controller import BrowserController
from llm_service import LLMService

class PythonDaemon:
    def __init__(self, websocket_url="ws://localhost:8080/jarvis-ws"):
        self.websocket_url = websocket_url
        self.tts = TTSService()
        self.os_ctrl = OSController()
        self.browser_ctrl = BrowserController()
        
        # Inicializar IA cargando la clave desde el entorno (.env)
        self.llm = LLMService()

        
        # Call on_voice_command whenever voice is detected
        self.stt = STTService(callback=self.on_voice_command)
        
        self.websocket_conn = None
        self.loop = asyncio.new_event_loop()
        
    def start(self):
        print("[DAEMON] Iniciando Python Daemon...")
        self.tts.speak("Hola, soy Juan. Iniciando sistemas.")
        self.stt.start_listening()
        
        # Run asyncio event loop in main thread
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect_websocket())
        
    async def connect_websocket(self):
        while True:
            try:
                print(f"[WS] Conectando a {self.websocket_url}...")
                async with websockets.connect(self.websocket_url) as ws:
                    print("[WS] Conectado al Cerebro Java.")
                    self.websocket_conn = ws
                    self.tts.speak("Conectado al servidor principal.")
                    await self.listen_websocket(ws)
            except Exception as e:
                print(f"[WS] Error de conexión: {e}. Reintentando en 5 segundos...")
                self.websocket_conn = None
                await asyncio.sleep(5)

    async def listen_websocket(self, ws):
        try:
            async for message in ws:
                print(f"[WS] Mensaje recibido de Java: {message}")
                data = json.loads(message)
                self.handle_java_message(data)
        except websockets.exceptions.ConnectionClosed:
            print("[WS] Conexión cerrada.")
            
    def handle_java_message(self, data):
        intent = data.get("intent")
        target = data.get("target")
        tts_message = data.get("tts_message")
        
        if intent == "OPEN_APP":
            success, msg = self.os_ctrl.open_app(target)
            self.tts.speak(tts_message if tts_message else msg)
                
        elif intent == "CLOSE_APP":
            success, msg = self.os_ctrl.close_app(target)
            self.tts.speak(tts_message if tts_message else msg)

        elif intent == "MINIMIZE_APP":
            success, msg = self.os_ctrl.minimize_app(target)
            self.tts.speak(tts_message if tts_message else msg)

        elif intent == "MAXIMIZE_APP":
            success, msg = self.os_ctrl.maximize_app(target)
            self.tts.speak(tts_message if tts_message else msg)

        elif intent == "BROWSER_SEARCH":
            success, msg = self.browser_ctrl.search_google(target)
            self.tts.speak(tts_message if tts_message else msg)
            
        elif intent == "YOUTUBE_SEARCH":
            success, msg = self.browser_ctrl.search_youtube(target)
            self.tts.speak(tts_message if tts_message else msg)
            
        elif intent == "OPEN_WEBSITE":
            success, msg = self.browser_ctrl.open_website(target)
            self.tts.speak(tts_message if tts_message else msg)

        elif intent == "VOLUME_UP":
            success, msg = self.os_ctrl.volume_up()
            self.tts.speak(tts_message if tts_message else msg)

        elif intent == "VOLUME_DOWN":
            success, msg = self.os_ctrl.volume_down()
            self.tts.speak(tts_message if tts_message else msg)

        elif intent == "VOLUME_MUTE":
            success, msg = self.os_ctrl.volume_mute()
            self.tts.speak(tts_message if tts_message else msg)

        elif intent == "MEDIA_PLAY_PAUSE":
            success, msg = self.os_ctrl.media_play_pause()
            self.tts.speak(tts_message if tts_message else msg)

        elif intent == "MEDIA_NEXT":
            success, msg = self.os_ctrl.media_next()
            self.tts.speak(tts_message if tts_message else msg)

        elif intent == "MEDIA_PREV":
            success, msg = self.os_ctrl.media_prev()
            self.tts.speak(tts_message if tts_message else msg)

        elif intent == "LOCK_SCREEN":
            success, msg = self.os_ctrl.lock_screen()
            self.tts.speak(tts_message if tts_message else msg)

        elif intent == "TAKE_SCREENSHOT":
            success, msg = self.os_ctrl.take_screenshot()
            self.tts.speak(tts_message if tts_message else msg)
            
        elif intent == "SAY_TEXT":
            self.tts.speak(tts_message)
                
        elif intent == "LEARN_ALIAS":
            if tts_message:
                self.tts.speak(tts_message)
        
        elif intent == "CHAT_QUERY":
            # Si no es comando de sistema, le preguntamos a la IA usando el texto original (target)
            respuesta_ia = self.llm.query(target)
            
            # Avisamos a Java que vamos a responder (para que quede en el historial del dashboard)
            if self.websocket_conn:
                payload = {
                    "source": "llm",
                    "raw_text": respuesta_ia
                }
                import asyncio
                asyncio.run_coroutine_threadsafe(
                    self.websocket_conn.send(json.dumps(payload)), 
                    self.loop
                )
                
            self.tts.speak(respuesta_ia)
            
        elif intent == "UNKNOWN_APP":
            if tts_message:
                self.tts.speak(tts_message)
            else:
                self.tts.speak("No sé cómo manejar esa aplicación.")

    def on_voice_command(self, text):
        print(f"[DAEMON] Comando detectado: {text}")
        if self.websocket_conn:
            payload = {
                "source": "voice",
                "timestamp": datetime.datetime.now().isoformat(),
                "raw_text": text
            }
            # Send message to Java server
            asyncio.run_coroutine_threadsafe(
                self.websocket_conn.send(json.dumps(payload)), 
                self.loop
            )
        else:
            print("[DAEMON] Servidor no conectado. No se puede procesar el comando.")
            self.tts.speak("No estoy conectado al servidor.")

if __name__ == "__main__":
    daemon = PythonDaemon()
    daemon.start()
