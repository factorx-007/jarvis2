import os
import pygame
import time
import asyncio
import edge_tts

class TTSService:
    def __init__(self, voice="es-ES-AlvaroNeural"):
        self.voice = voice
        pygame.mixer.init()
        
    def speak(self, text):
        print(f"[TTS] Diciendo: {text}")
        output_file = "response.mp3"
        
        # Eliminar si existe previo
        if os.path.exists(output_file):
            try: os.remove(output_file)
            except: pass
            
        try:
            # OPTIMIZACION EXTREMA: Usar edge_tts nativo, ejecutándolo en un hilo dedicado 
            # para no chocar con el event loop de websockets.
            def _generate():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                communicate = edge_tts.Communicate(text, self.voice)
                loop.run_until_complete(communicate.save(output_file))
                loop.close()
                
            import threading
            t = threading.Thread(target=_generate)
            t.start()
            t.join()
            
            # Reproducir el audio
            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()
            
            # Esperar a que termine de reproducirse
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Liberar el archivo
            pygame.mixer.music.unload()
            
            # Eliminar archivos temporales para que no se acumulen
            if os.path.exists(output_file):
                try: os.remove(output_file)
                except: pass
                
        except Exception as e:
            print(f"[TTS] Error al generar/reproducir voz: {e}")

if __name__ == "__main__":
    tts = TTSService()
    tts.speak("Hola, soy Juan. Inicializando módulo de voz neuronal.")
