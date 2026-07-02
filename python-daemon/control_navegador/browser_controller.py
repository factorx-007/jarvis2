import threading
import time
from playwright.sync_api import sync_playwright

class BrowserController:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
    def _run_in_thread(self, target, *args):
        # Run a function in a separate thread and wait for it
        import queue
        q = queue.Queue()
        def wrapper():
            try:
                res = target(*args)
                q.put(("OK", res))
            except Exception as e:
                q.put(("ERROR", e))
        t = threading.Thread(target=wrapper)
        t.start()
        t.join()
        status, res = q.get()
        if status == "ERROR":
            raise res
        return res

    def _start_browser_internal(self):
        if self.playwright is None:
            self.playwright = sync_playwright().start()
        if self.browser is None:
            self.browser = self.playwright.chromium.launch(headless=False)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()

    def ensure_browser_open(self):
        if not self.browser:
            print("[BROWSER] Iniciando navegador Playwright...")
            self._run_in_thread(self._start_browser_internal)
            return "Navegador abierto."
        return "El navegador ya está abierto."

    def search_google(self, query):
        def _task():
            self.ensure_browser_open()
            print(f"[BROWSER] Buscando en Google: {query}")
            self.page.goto("https://www.google.com")
            search_input = self.page.locator('textarea[name="q"], input[name="q"]')
            search_input.fill(query)
            search_input.press("Enter")
            self.page.wait_for_load_state("networkidle")
            return True, f"Buscando {query} en Google."
        
        try:
            return self._run_in_thread(_task)
        except Exception as e:
            print(f"[BROWSER] Error al buscar: {e}")
            return False, f"Error al buscar en Google."

    def search_youtube(self, query):
        def _task():
            self.ensure_browser_open()
            print(f"[BROWSER] Buscando en YouTube: {query}")
            self.page.goto(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
            self.page.wait_for_load_state("domcontentloaded")
            return True, f"Buscando {query} en YouTube."
        try:
            return self._run_in_thread(_task)
        except Exception as e:
            print(f"[BROWSER] Error al buscar en YouTube: {e}")
            return False, f"Error al buscar en YouTube."

    def open_website(self, domain):
        def _task():
            self.ensure_browser_open()
            print(f"[BROWSER] Abriendo web: {domain}")
            dom = domain
            if not dom.endswith(".com") and not dom.endswith(".org") and not dom.endswith(".es"):
                dom += ".com"
            self.page.goto(f"https://www.{dom}")
            self.page.wait_for_load_state("domcontentloaded")
            return True, f"Abriendo la página de {domain}."
        try:
            return self._run_in_thread(_task)
        except Exception as e:
            print(f"[BROWSER] Error al abrir {domain}: {e}")
            return False, f"Error al abrir la web."

    def close_browser(self):
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
        return True, "Navegador cerrado."

if __name__ == "__main__":
    bc = BrowserController()
    bc.search_google("noticias de tecnología")
    time.sleep(5)
    bc.close_browser()
