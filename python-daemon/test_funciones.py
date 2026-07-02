import os
os.environ["PYTHONIOENCODING"] = "utf-8"
"""
Script de Testing Automático para Juan
Envía cada comando vía WebSocket a Java y verifica que devuelva el intent correcto.
Uso: python test_funciones.py (con el servidor Java corriendo en puerto 8080)
"""

import asyncio
import websockets
import json
import sys

TESTS = [
    # (comando, intent_esperado, descripción)
    ("abre chrome",                "OPEN_APP",         "Abrir aplicación"),
    ("abre la calculadora",        "OPEN_APP",         "Abrir con artículo"),
    ("cierra notepad",             "CLOSE_APP",        "Cerrar aplicación"),
    ("minimiza chrome",            "MINIMIZE_APP",     "Minimizar ventana"),
    ("oculta chrome",              "MINIMIZE_APP",     "Minimizar con sinónimo"),
    ("maximiza chrome",            "MAXIMIZE_APP",     "Maximizar ventana"),
    ("restaura chrome",            "MAXIMIZE_APP",     "Maximizar con sinónimo"),
    ("busca en google noticias",   "BROWSER_SEARCH",   "Búsqueda en Google"),
    ("busca en youtube musica",    "YOUTUBE_SEARCH",   "Búsqueda en YouTube"),
    ("abre youtube",               "OPEN_WEBSITE",     "Abrir sitio web"),
    ("abre facebook",              "OPEN_WEBSITE",     "Abrir sitio web 2"),
    ("sube el volumen",            "VOLUME_UP",        "Subir volumen"),
    ("mas volumen",                "VOLUME_UP",        "Subir volumen sinónimo"),
    ("aumenta el volumen",         "VOLUME_UP",        "Subir volumen sinónimo 2"),
    ("baja el volumen",            "VOLUME_DOWN",      "Bajar volumen"),
    ("menos volumen",              "VOLUME_DOWN",      "Bajar volumen sinónimo"),
    ("silencia",                   "VOLUME_MUTE",      "Silenciar"),
    ("mute",                       "VOLUME_MUTE",      "Silenciar sinónimo"),
    ("reproduce",                  "MEDIA_PLAY_PAUSE", "Play/Pausa"),
    ("pausa",                      "MEDIA_PLAY_PAUSE", "Play/Pausa sinónimo"),
    ("pon musica",                 "MEDIA_PLAY_PAUSE", "Play/Pausa sinónimo 2"),
    ("play",                       "MEDIA_PLAY_PAUSE", "Play/Pausa sinónimo 3"),
    ("siguiente",                  "MEDIA_NEXT",       "Siguiente canción"),
    ("skip",                       "MEDIA_NEXT",       "Siguiente sinónimo"),
    ("anterior",                   "MEDIA_PREV",       "Canción anterior"),
    ("bloquea la pantalla",        "LOCK_SCREEN",      "Bloquear pantalla"),
    ("bloquea el equipo",          "LOCK_SCREEN",      "Bloquear sinónimo"),
    ("captura de pantalla",        "TAKE_SCREENSHOT",   "Captura de pantalla"),
    ("screenshot",                 "TAKE_SCREENSHOT",   "Captura sinónimo"),
    ("que hora es",                "SAY_TEXT",         "Decir la hora"),
    ("que dia es",                 "SAY_TEXT",         "Decir la fecha"),
    ("aprende editor como notepad","LEARN_ALIAS",      "Aprender alias"),
    ("inicia chrome",              "OPEN_APP",         "Abrir con 'inicia'"),
    ("ejecuta calculadora",        "OPEN_APP",         "Abrir con 'ejecuta'"),
    ("mata notepad",               "CLOSE_APP",        "Cerrar con 'mata'"),
]

async def run_tests():
    url = "ws://localhost:8080/jarvis-ws"
    
    print("=" * 60)
    print("  TEST AUTOMATICO DE FUNCIONES DE JUAN")
    print("=" * 60)
    print()
    
    try:
        async with websockets.connect(url) as ws:
            print(f"[OK] Conectado a {url}\n")
            
            passed = 0
            failed = 0
            
            for cmd, expected_intent, desc in TESTS:
                payload = {
                    "source": "voice",
                    "timestamp": "2026-07-01T00:00:00",
                    "raw_text": cmd
                }
                await ws.send(json.dumps(payload))
                
                # Leer la respuesta del intent (ignorar HISTORY_UPDATE)
                intent_received = None
                for _ in range(5):  # máximo 5 mensajes antes de rendirse
                    response = await asyncio.wait_for(ws.recv(), timeout=3)
                    data = json.loads(response)
                    if data.get("intent"):
                        intent_received = data["intent"]
                        break
                
                if intent_received == expected_intent:
                    print(f"  [PASS] | {desc:<30} | '{cmd}' -> {intent_received}")
                    passed += 1
                else:
                    print(f"  [FAIL] | {desc:<30} | '{cmd}' -> {intent_received} (esperado: {expected_intent})")
                    failed += 1
                
                await asyncio.sleep(0.1)
            
            print()
            print("=" * 60)
            print(f"  RESULTADOS: {passed} pasaron  |  {failed} fallaron  |  Total: {len(TESTS)}")
            print("=" * 60)
            
            return failed == 0
            
    except ConnectionRefusedError:
        print("[ERROR] No se pudo conectar al servidor Java en puerto 8080.")
        print("   Asegurate de que el Cerebro Java esta corriendo.")
        print("   Ejecuta: INICIAR_JUAN.bat")
        return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
