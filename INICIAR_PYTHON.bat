@echo off
title Juan - Sistema Nervioso (Python)
echo.
echo  =============================================
echo    JUAN - Asistente Virtual Personal
echo    Iniciando el Sistema Nervioso (Python)...
echo  =============================================
echo.
cd /d "%~dp0\python-daemon"
:: 1. Verificar si Python está instalado
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [ERROR] No se encontro Python instalado en el sistema o no esta en el PATH.
    echo  El Sistema Nervioso de Juan requiere Python 3.10 o superior.
    echo.
    echo  Solucion:
    echo   1. Descarga e instala Python desde: https://www.python.org/
    echo   2. ¡IMPORTANTE! Durante la instalacion marca la casilla:
    echo      "Add Python to PATH" antes de dar clic en Install Now.
    echo =======================================================================
    echo.
    pause
    exit /b 1
)
:: 2. Crear el archivo .env si no existe
if not exist .env (
    echo =======================================================================
    echo  [!] No se encontro el archivo de configuracion .env
    echo  Por favor, introduce tu API Key de OpenRouter para la IA
    echo =======================================================================
    echo.
    set /p USER_API_KEY="API Key (comienza con sk-or-): "
    
    :: Escribir en el archivo .env
    echo OPENROUTER_API_KEY=%USER_API_KEY%> .env
    echo.
    echo [OK] Archivo .env creado con exito.
    echo.
)
:: 3. Instalar dependencias usando python -m pip (más seguro que pip solo)
echo [1/3] Verificando e instalando dependencias (puede tardar la primera vez)...
python -m pip install -r requirements.txt -q
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [ERROR] Hubo un problema al instalar las dependencias de Python.
    echo  Intentaremos instalarlas de nuevo mostrando los detalles del error.
    echo =======================================================================
    echo.
    python -m pip install -r requirements.txt
    pause
    exit /b 1
)
:: 4. Instalar los navegadores de Playwright necesarios
echo [2/3] Instalando binarios de Playwright (Navegador)...
python -m playwright install chromium
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [WARNING] Hubo un problema al instalar los binarios de Playwright.
    echo  El control del navegador (abrir webs, YouTube) podria no funcionar.
    echo  Revisa tu conexion a Internet o intenta ejecutar manualmente:
    echo  python -m playwright install chromium
    echo =======================================================================
    echo.
    pause
)
echo.
echo [3/3] Arrancando reconocimiento de voz y automatizacion...
echo.
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [ERROR] El demonio de Python se detuvo de forma inesperada (Codigo: %ERRORLEVEL%).
    echo.
    echo  Soluciones rapidas para problemas comunes:
    echo   1. Error de Microfono: Verifica que tu microfono este conectado y
    echo      configurado como dispositivo de grabacion predeterminado.
    echo   2. Error PyAudio: Si da fallas al compilar PyAudio, asegurate de tener
    echo      las herramientas de desarrollo de C++ instaladas o usa un paquete precompilado.
    echo   3. Error de Conexión: Verifica tu conexion a Internet.
    echo =======================================================================
    echo.
    pause
)
