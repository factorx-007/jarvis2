import os
import sys
import subprocess
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import tkinter as tk
from main import PythonDaemon

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    project_root = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)

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

daemon_thread = None

def get_logs_text():
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

def has_api_key_logic():
    env_path = os.path.join(project_root, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            if "OPENROUTER_API_KEY=" in f.read():
                return True
    return False

def save_api_key_logic(key):
    env_path = os.path.join(project_root, ".env")
    try:
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f'OPENROUTER_API_KEY="{key.strip()}"\n')
        return True
    except Exception as e:
        print(f"Error guardando API key: {e}")
        return False

def run_python_daemon():
    print("[Jarvis App] Iniciando Sistema Nervioso (Python)...")
    try:
        daemon = PythonDaemon()
        daemon.start()
    except Exception as e:
        import traceback
        print(f"[Jarvis App] Error crítico en el daemon de Python:\n{traceback.format_exc()}")

def start_python_logic():
    global daemon_thread
    if daemon_thread and daemon_thread.is_alive():
        return "Ya está corriendo"
    daemon_thread = threading.Thread(target=run_python_daemon, daemon=True)
    daemon_thread.start()
    return "Iniciado"

class ApiHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if self.path == '/api/logs':
            self.wfile.write(json.dumps({"logs": get_logs_text()}).encode('utf-8'))
        elif self.path == '/api/has_key':
            self.wfile.write(json.dumps({"has_key": has_api_key_logic()}).encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if self.path == '/api/save_key':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            key = data.get("key", "")
            success = save_api_key_logic(key)
            self.wfile.write(json.dumps({"success": success}).encode('utf-8'))
        elif self.path == '/api/start_python':
            res = start_python_logic()
            self.wfile.write(json.dumps({"status": res}).encode('utf-8'))

def run_server():
    server = HTTPServer(('localhost', 8081), ApiHandler)
    server.serve_forever()

def kill_existing_java():
    java_exe_path = os.path.join(project_root, "jre", "bin", "java.exe").lower()
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                exe = proc.info['exe']
                if exe and exe.lower() == java_exe_path:
                    print(f"[Jarvis App] Matando proceso Java huérfano (PID: {proc.info['pid']}) para liberar puerto...")
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception as e:
        print(f"Error al limpiar procesos Java: {e}")

def start_java_backend():
    kill_existing_java()
    print("[Jarvis App] Iniciando Cerebro Java...")
    java_exe = os.path.join(project_root, "jre", "bin", "java.exe")
    jar_path = os.path.join(project_root, "java-core", "target", "core-0.0.1-SNAPSHOT.jar")
    
    if not os.path.exists(java_exe):
        print(f"[Jarvis App] No se encontró JRE local en {java_exe}, intentando con java del sistema...")
        java_exe = "java"
        
    try:
        creationflags = subprocess.CREATE_NO_WINDOW if getattr(sys, 'frozen', False) else 0
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

def main():
    java_proc = start_java_backend()
    
    # Start API server for frontend
    threading.Thread(target=run_server, daemon=True).start()
    
    if has_api_key_logic():
        start_python_logic()
        
    print("[Jarvis App] Esperando a que Java responda...")
    time.sleep(5)
    
    # Open dashboard in user's default browser!
    print("[Jarvis App] Abriendo Dashboard en el navegador...")
    webbrowser.open("http://localhost:8080")
    
    # Show tiny control window to keep app alive
    root = tk.Tk()
    root.title("Jarvis Activo")
    root.geometry("350x150")
    root.configure(bg="#111111")
    tk.Label(root, text="🔴 El Sistema Jarvis está ejecutándose.\n\nPuedes interactuar desde tu navegador web.\n\nCierra esta ventana para apagar todos los sistemas.", fg="#ff0000", bg="#111111", font=("Segoe UI", 10)).pack(expand=True)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
    
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
