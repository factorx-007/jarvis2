import pyttsx3

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Set speech rate
        self.engine.setProperty('rate', 170)
        
        # Try to find a Spanish voice if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'es' in voice.languages:
                self.engine.setProperty('voice', voice.id)
                break
                
    def speak(self, text):
        print(f"[TTS] Diciendo: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    tts = TTSService()
    tts.speak("Hola Sistema. Inicializando módulos de voz.")
