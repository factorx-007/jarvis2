import speech_recognition as sr
import threading
import time

class STTService:
    def __init__(self, wake_words=["juan", "wan", "guan", "juana", "one", "guam", "cuán", "pan"], callback=None):
        self.recognizer = sr.Recognizer()
        self.wake_words = [w.lower() for w in wake_words]
        self.callback = callback
        self.is_listening = False
        try:
            self.microphone = sr.Microphone()
            # Adjust for ambient noise
            with self.microphone as source:
                print("[STT] Calibrando para ruido de fondo...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                # Bajar el umbral de energía para captar mejor la voz
                self.recognizer.energy_threshold = max(self.recognizer.energy_threshold * 0.8, 150)
                self.recognizer.dynamic_energy_threshold = True
                
                # OPTIMIZACION EXTREMA: Reducir el tiempo que espera en silencio para enviar el comando
                self.recognizer.pause_threshold = 0.5
                
                print(f"[STT] Calibración completa. Umbral de energía: {self.recognizer.energy_threshold:.0f}")
        except Exception as e:
            print(f"[STT] [WARNING] No se pudo inicializar o calibrar el micrófono: {e}")
            self.microphone = None

    def start_listening(self):
        self.is_listening = True
        self._listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listen_thread.start()

    def stop_listening(self):
        self.is_listening = False

    def _listen_loop(self):
        if not self.microphone:
            print("[STT] [ERROR] El servicio de reconocimiento de voz (STT) no se iniciará porque no hay un micrófono disponible.")
            self.is_listening = False
            return
            
        print(f"[STT] Escuchando activamente. Wake words: {self.wake_words}")
        print("[STT] Di 'Juan' seguido de tu comando (ej: 'Juan abre la calculadora').")
        while self.is_listening:
            try:
                with self.microphone as source:
                    try:
                        audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=8)
                        
                        text = self.recognizer.recognize_google(audio, language="es-MX").lower()
                        print(f"[STT] 🎙️ Escuchado: '{text}'")
                        
                        detected_word = next((w for w in self.wake_words if w in text), None)
                        if detected_word:
                            # Extraer comando después del wake word
                            command = text.split(detected_word, 1)[-1].strip()
                            if command and self.callback:
                                print(f"[STT] ✅ Comando para Juan: '{command}'")
                                self.callback(command)
                            elif not command and self.callback:
                                print("[STT] Wake word detectado solo. Escuchando comando...")
                                try:
                                    audio_cmd = self.recognizer.listen(source, timeout=4, phrase_time_limit=8)
                                    cmd_text = self.recognizer.recognize_google(audio_cmd, language="es-MX").lower()
                                    print(f"[STT] ✅ Comando para Juan: '{cmd_text}'")
                                    self.callback(cmd_text)
                                except:
                                    print("[STT] No se detectó comando después del wake word.")
                        # No imprimir nada si no contiene wake word (reduce ruido en consola)
                                
                    except sr.WaitTimeoutError:
                        pass
                    except sr.UnknownValueError:
                        pass  # No inundar la consola con estos mensajes
                    except sr.RequestError as e:
                        print(f"[STT] ❌ Error de red con Google: {e}")
                    except Exception as e:
                        print(f"[STT] ❌ Error inesperado: {e}")
            except Exception as e:
                print(f"[STT] ❌ Error al acceder al dispositivo de micrófono: {e}")
                time.sleep(2)
            time.sleep(0.05)

if __name__ == "__main__":
    def on_command(cmd):
        print(f"Comando recibido: {cmd}")
    
    stt = STTService(callback=on_command)
    stt.start_listening()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stt.stop_listening()
