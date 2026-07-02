import asyncio
import websockets
import json
import datetime
import threading
from stt_service import STTService
from tts_service import TTSService
from os_controller import OSController

class PythonDaemon:
    def __init__(self, websocket_url="ws://localhost:8080/jarvis-ws"):
        self.websocket_url = websocket_url
        self.tts = TTSService()
        self.os_ctrl = OSController()
        
        # Call on_voice_command whenever voice is detected
        self.stt = STTService(callback=self.on_voice_command)
        
        self.websocket_conn = None
        self.loop = asyncio.new_event_loop()
        
    def start(self):
        print("[DAEMON] Iniciando Python Daemon...")
        self.tts.speak("Sistema iniciado. Esperando conexión.")
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
            if tts_message:
                self.tts.speak(tts_message)
            elif success:
                self.tts.speak(f"Abriendo {target}")
            else:
                self.tts.speak(msg)
                
        elif intent == "CLOSE_APP":
            success, msg = self.os_ctrl.close_app(target)
            if tts_message:
                self.tts.speak(tts_message)
            else:
                self.tts.speak(msg)
                
        elif intent == "LEARN_ALIAS":
            if tts_message:
                self.tts.speak(tts_message)
        
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
