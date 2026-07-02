import subprocess
import psutil
import pygetwindow as gw
import os
import pyautogui

class OSController:
    def __init__(self):
        # Mapeo de aplicaciones comunes en Windows
        self.app_map = {
            # Navegadores
            "chrome": "chrome.exe",
            "google": "chrome.exe",
            "google chrome": "chrome.exe",
            "navegador": "chrome.exe",
            "edge": "msedge.exe",
            # Herramientas de Windows
            "bloc de notas": "notepad.exe",
            "notepad": "notepad.exe",
            "calculadora": "calc.exe",
            "calc": "calc.exe",
            "explorador": "explorer.exe",
            "explorador de archivos": "explorer.exe",
            "archivos": "explorer.exe",
            "paint": "mspaint.exe",
            "consola": "cmd.exe",
            "cmd": "cmd.exe",
            "terminal": "cmd.exe",
            "powershell": "powershell.exe",
            "configuracion": "ms-settings:",
            "configuración": "ms-settings:",
            "ajustes": "ms-settings:",
            # Aplicaciones populares
            "spotify": "spotify.exe",
            "discord": "C:\\Users\\Acer\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe",
            # Tienda de Windows (UWP apps)
            "whatsapp": "explorer.exe shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
        }

    def _clean_name(self, name):
        if not name:
            return ""
        name = name.lower().strip()
        # Quitar artículos del español
        for article in ["la ", "el ", "los ", "las ", "un ", "una ", "al "]:
            if name.startswith(article):
                name = name[len(article):].strip()
                break
        return name

    def open_app(self, app_name_or_alias):
        if not app_name_or_alias or app_name_or_alias.strip() == "":
            return False, "No especificaste qué aplicación abrir."
        
        name = self._clean_name(app_name_or_alias)
        target_exe = self.app_map.get(name, name)
        try:
            print(f"[OS] Abriendo '{name}' → {target_exe}")
            if target_exe.startswith("ms-settings:"):
                subprocess.Popen(f"start {target_exe}", shell=True)
            elif target_exe.startswith("explorer.exe shell:"):
                subprocess.Popen(target_exe, shell=True)
            else:
                subprocess.Popen(f'start "" "{target_exe}"', shell=True)
            return True, f"Abriendo {app_name_or_alias}"
        except Exception as e:
            print(f"[OS] Error abriendo {target_exe}: {e}")
            return False, f"Error al abrir {app_name_or_alias}"

    def close_app(self, app_name_or_alias):
        name = self._clean_name(app_name_or_alias)
        target_exe = self.app_map.get(name, name)
        
        # Para apps de configuración, cerrar por título de ventana
        if target_exe.startswith("ms-settings:"):
            target_exe = "SystemSettings.exe"
        
        closed = False
        try:
            print(f"[OS] Cerrando '{name}' → {target_exe}")
            # Intentar cerrar por nombre de proceso
            for proc in psutil.process_iter(['name']):
                proc_name = proc.info['name']
                if proc_name and proc_name.lower() == target_exe.lower():
                    proc.kill()
                    closed = True
            # Si no encontramos por exe, buscar por nombre en el título de ventana
            if not closed:
                for proc in psutil.process_iter(['name']):
                    proc_name = proc.info['name']
                    if proc_name and name.lower() in proc_name.lower():
                        proc.kill()
                        closed = True
            if closed:
                return True, f"{app_name_or_alias} cerrado."
            else:
                return False, f"No encontré {app_name_or_alias} en ejecución."
        except Exception as e:
            print(f"[OS] Error cerrando: {e}")
            return False, f"Error al cerrar {app_name_or_alias}"

    def _find_window_by_name(self, name):
        # Buscar por título parcial
        all_windows = gw.getAllWindows()
        for w in all_windows:
            if w.title and name.lower() in w.title.lower():
                return w
        return None

    def minimize_app(self, app_name_or_alias):
        name = self._clean_name(app_name_or_alias)
        window = self._find_window_by_name(name)
        if window:
            window.minimize()
            return True, f"Minimizando {app_name_or_alias}"
        return False, f"No encontré la ventana de {app_name_or_alias}"

    def maximize_app(self, app_name_or_alias):
        name = self._clean_name(app_name_or_alias)
        window = self._find_window_by_name(name)
        if window:
            window.maximize()
            return True, f"Maximizando {app_name_or_alias}"
        return False, f"No encontré la ventana de {app_name_or_alias}"

    # Control de volumen
    def volume_up(self):
        for _ in range(5):
            pyautogui.press("volumeup")
        return True, "Volumen subido."

    def volume_down(self):
        for _ in range(5):
            pyautogui.press("volumedown")
        return True, "Volumen bajado."

    def volume_mute(self):
        pyautogui.press("volumemute")
        return True, "Volumen silenciado."

    # Control multimedia
    def media_play_pause(self):
        pyautogui.press("playpause")
        return True, "Reproduciendo o pausando."

    def media_next(self):
        pyautogui.press("nexttrack")
        return True, "Siguiente pista."

    def media_prev(self):
        pyautogui.press("prevtrack")
        return True, "Pista anterior."

    # Sistema
    def lock_screen(self):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return True, "Pantalla bloqueada."

    def take_screenshot(self):
        screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "captura_juan.png")
        pyautogui.screenshot(screenshot_path)
        return True, f"Captura guardada."

if __name__ == "__main__":
    import time
    os_ctrl = OSController()
    print("Testing: Abriendo notepad...")
    os_ctrl.open_app("notepad")
    time.sleep(3)
    print("Testing: Minimizando notepad...")
    os_ctrl.minimize_app("notepad")
    time.sleep(2)
    print("Testing: Maximizando notepad...")
    os_ctrl.maximize_app("notepad")
    time.sleep(2)
    print("Testing: Cerrando notepad...")
    os_ctrl.close_app("notepad")
    print("Test completo.")
