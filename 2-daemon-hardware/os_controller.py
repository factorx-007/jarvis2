import subprocess
import psutil
import os

class OSController:
    def __init__(self):
        # Mapeo básico de aplicaciones comunes en Windows
        self.app_map = {
            "chrome": "chrome.exe",
            "google": "chrome.exe",
            "google chrome": "chrome.exe",
            "navegador": "chrome.exe",
            "bloc de notas": "notepad.exe",
            "notepad": "notepad.exe",
            "calculadora": "calc.exe",
            "calc": "calc.exe",
            "explorador": "explorer.exe",
            "explorador de archivos": "explorer.exe",
            "archivos": "explorer.exe",
            "spotify": "spotify.exe"
        }

    def open_app(self, app_name_or_alias):
        # Limpieza defensiva de artículos en Python por si Java no recompiló
        name = app_name_or_alias.lower().strip()
        for article in ["la ", "el ", "los ", "las ", "un ", "una "]:
            if name.startswith(article):
                name = name[len(article):].strip()
                break
                
        target_exe = self.app_map.get(name, name)
        try:
            print(f"[OS] Abriendo {target_exe}...")
            # En Windows, usar start para que busque en el PATH
            subprocess.Popen(f"start {target_exe}", shell=True)
            return True, f"Abriendo {app_name_or_alias}"
        except Exception as e:
            print(f"[OS] Error abriendo {target_exe}: {e}")
            return False, f"Error al abrir {app_name_or_alias}"

    def close_app(self, app_name_or_alias):
        # Limpieza defensiva de artículos en Python
        name = app_name_or_alias.lower().strip()
        for article in ["la ", "el ", "los ", "las ", "un ", "una "]:
            if name.startswith(article):
                name = name[len(article):].strip()
                break
                
        target_exe = self.app_map.get(name, name)
        closed = False
        try:
            print(f"[OS] Cerrando {target_exe}...")
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() == target_exe.lower():
                    proc.kill()
                    closed = True
            if closed:
                return True, f"{app_name_or_alias} cerrado."
            else:
                return False, f"No encontré {app_name_or_alias} en ejecución."
        except Exception as e:
            print(f"[OS] Error cerrando {target_exe}: {e}")
            return False, f"Error al cerrar {app_name_or_alias}"

if __name__ == "__main__":
    import time
    os_ctrl = OSController()
    os_ctrl.open_app("notepad")
    time.sleep(3)
    os_ctrl.close_app("notepad")
