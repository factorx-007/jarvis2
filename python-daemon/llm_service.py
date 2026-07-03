import os
from openai import OpenAI
import sys

def load_env():
    # Cargar .env desde el directorio correcto (raíz del exe si está compilado)
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")

class LLMService:
    def __init__(self, api_key=None):
        if not api_key:
            load_env()
            api_key = os.environ.get("OPENROUTER_API_KEY")
            
        self.api_key = api_key
        # Configurar la API de OpenRouter
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        
        # Historial de mensajes para mantener el contexto
        self.messages = []
        
        # Prompt del sistema para darle personalidad a Juan (ITACHI UCHIHA)
        system_prompt = (
            "Eres Juan. Tu personalidad está basada en Itachi Uchiha de los Akatsuki. "
            "Eres sumamente inteligente, analítico, misterioso y calmado. Hablas con propiedad y elegancia. "
            "Por defecto, tus respuestas deben ser CORTAS, muy concisas y directas para no gastar tiempo. "
            "SIN EMBARGO, si el usuario te pide explícitamente contexto, detalles o te dice 'explícame', 'cuéntame más', "
            "tienes permitido explayarte y dar respuestas largas y profundas, llenas de sabiduría ninja. "
            "Evita usar markdown (asteriscos, negritas) porque tu respuesta será leída por un sintetizador de voz."
        )
        self.messages.append({"role": "system", "content": system_prompt})

    def query(self, text):
        try:
            print(f"[LLM] Pensando respuesta para: '{text}'...")
            
            # Agregar el mensaje del usuario al historial
            self.messages.append({"role": "user", "content": text})
            
            # Limitar el historial a los últimos 10 mensajes (para no exceder tokens)
            # Siempre conservamos el primer mensaje (system prompt)
            if len(self.messages) > 11:
                self.messages = [self.messages[0]] + self.messages[-10:]
            
            # Consultar OpenRouter (usamos gpt-3.5-turbo o gemini-flash a través de openrouter)
            completion = self.client.chat.completions.create(
                model="openai/gpt-4o-mini", # Usaremos el modelo más eficiente y popular por defecto
                messages=self.messages
            )
            
            response_text = completion.choices[0].message.content
            
            # Agregar la respuesta del asistente al historial
            self.messages.append({"role": "assistant", "content": response_text})
            
            # Limpiar markdown básico que la IA pueda incluir por error
            clean_text = response_text.replace("*", "").replace("#", "").strip()
            
            print(f"[LLM] Respuesta generada: {clean_text}")
            return clean_text
            
        except Exception as e:
            print(f"[LLM] Error al consultar OpenRouter: {e}")
            return "Lo siento, tuve un problema al procesar esa información con mi nueva API."

if __name__ == "__main__":
    # Test simple
    llm = LLMService()
    print(llm.query("Hola, ¿quién eres y qué puedes hacer?"))
