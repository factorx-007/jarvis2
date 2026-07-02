import os
import ctypes
import time
import asyncio
import edge_tts

class TTSService:
    def __init__(self, voice="es-ES-AlvaroNeural"):
        self.voice = voice
        
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
            
            # Reproducir el audio usando la API de Windows MCI (Media Control Interface)
            # Esto evita la necesidad de usar dependencias pesadas que requieren compilación como pygame.
            abs_path = os.path.abspath(output_file)
            mci = ctypes.windll.winmm.mciSendStringW
            alias = f"tts_{int(time.time() * 1000)}"
            
            # Abrir archivo
            open_res = mci(f'open "{abs_path}" type mpegvideo alias {alias}', None, 0, 0)
            if open_res != 0:
                # Fallback sin tipo mpegvideo
                open_res = mci(f'open "{abs_path}" alias {alias}', None, 0, 0)
                
            if open_res == 0:
                try:
                    # Reproducir
                    mci(f'play {alias}', None, 0, 0)
                    
                    # Esperar a que termine de reproducirse
                    status_buffer = ctypes.create_unicode_buffer(128)
                    while True:
                        mci(f'status {alias} mode', status_buffer, 128, 0)
                        if status_buffer.value != 'playing':
                            break
                        time.sleep(0.05)
                finally:
                    # Cerrar archivo para liberarlo
                    mci(f'close {alias}', None, 0, 0)
            else:
                print(f"[TTS] [ERROR] No se pudo abrir el archivo de audio con MCI (Codigo: {open_res})")
                
            # Eliminar archivos temporales para que no se acumulen
            if os.path.exists(output_file):
                try: os.remove(output_file)
                except: pass
                
        except Exception as e:
            print(f"[TTS] Error al generar/reproducir voz: {e}")

if __name__ == "__main__":
    tts = TTSService()
    tts.speak("Hola, soy Juan. Inicializando módulo de voz neuronal.")
