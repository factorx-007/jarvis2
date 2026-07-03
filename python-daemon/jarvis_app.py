import os
import sys
import subprocess
import threading
import time
import webview
from main import PythonDaemon

# Paths are relative to the executable (when compiled) or this script
if getattr(sys, 'frozen', False):
    # If compiled with PyInstaller
    base_dir = sys._MEIPASS
    project_root = os.path.dirname(sys.executable)
else:
    # If running as script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)

# Redirigir salidas para depuración
py_log_path = os.path.join(project_root, "jarvis_debug.log")
java_log_path = os.path.join(project_root, "java_debug.log")

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")
    def write(self, message):
        self.log.write(message)
        self.log.flush()
    def flush(self):
        pass

sys.stdout = Logger(py_log_path)
sys.stderr = sys.stdout

# Variable global para el thread del daemon
daemon_thread = None

class Api:
    def get_logs(self):
        try:
            with open(py_log_path, "r", encoding="utf-8", errors="replace") as f:
                py_logs = f.read()[-3000:]
        except Exception as e:
            py_logs = f"Error: {e}"
        try:
            with open(java_log_path, "r", encoding="utf-8", errors="replace") as f:
                java_logs = f.read()[-3000:]
        except Exception as e:
            java_logs = f"Error: {e}"
        return f"=== PYTHON LOGS ===\n{py_logs}\n\n=== JAVA LOGS ===\n{java_logs}"

    def has_api_key(self):
        env_path = os.path.join(project_root, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()
                if "OPENROUTER_API_KEY=" in content:
                    return True
        return False

    def save_api_key(self, key):
        env_path = os.path.join(project_root, ".env")
        try:
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(f'OPENROUTER_API_KEY="{key.strip()}"\n')
            return True
        except Exception as e:
            print(f"Error guardando API key: {e}")
            return False

    def start_python(self):
        global daemon_thread
        if daemon_thread and daemon_thread.is_alive():
            return "Ya está corriendo"
        daemon_thread = threading.Thread(target=run_python_daemon, daemon=True)
        daemon_thread.start()
        return "Iniciado"

def start_java_backend():
    print("[Jarvis App] Iniciando Cerebro Java...")
    java_exe = os.path.join(project_root, "jre", "bin", "java.exe")
    jar_path = os.path.join(project_root, "java-core", "target", "core-0.0.1-SNAPSHOT.jar")
    
    if not os.path.exists(java_exe):
        print(f"[Jarvis App] No se encontró JRE local en {java_exe}, intentando con java del sistema...")
        java_exe = "java"
        
    try:
        creationflags = 0
        if getattr(sys, 'frozen', False):
            creationflags = subprocess.CREATE_NO_WINDOW
            
        java_log_file = open(java_log_path, "w", encoding="utf-8")
        process = subprocess.Popen(
            [java_exe, "-jar", jar_path],
            stdout=java_log_file,
            stderr=java_log_file,
            creationflags=creationflags
        )
        return process
    except Exception as e:
        print(f"[Jarvis App] Error iniciando Java: {e}")
        return None

def run_python_daemon():
    print("[Jarvis App] Iniciando Sistema Nervioso (Python)...")
    try:
        daemon = PythonDaemon()
        daemon.start()
    except Exception as e:
        import traceback
        print(f"[Jarvis App] Error crítico en el daemon de Python:\n{traceback.format_exc()}")

def main():
    java_proc = start_java_backend()
    time.sleep(3)
    
    print("[Jarvis App] Abriendo ventana del Dashboard...")
    dashboard_path = os.path.join(project_root, "4-dashboard-rostro", "index.html")
    
    api_instance = Api()
    
    # Iniciar daemon automáticamente si ya tiene la llave
    if api_instance.has_api_key():
        api_instance.start_python()
    
    webview.create_window(
        title="Jarvis - Asistente Virtual",
        url=f"file:///{dashboard_path.replace(chr(92), '/')}",
        width=1000,
        height=800,
        min_size=(800, 600),
        text_select=False,
        js_api=api_instance
    )
    
    webview.start()
    
    print("[Jarvis App] Cerrando aplicación...")
    if java_proc:
        java_proc.terminate()
        try:
            java_proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            java_proc.kill()
    
    sys.exit(0)

if __name__ == "__main__":
    main()
