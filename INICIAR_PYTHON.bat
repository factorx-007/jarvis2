@echo off
setlocal enabledelayedexpansion
title Juan - Sistema Nervioso (Python)

echo.
echo  =============================================
echo    JUAN - Asistente Virtual Personal
echo    Iniciando el Sistema Nervioso (Python)...
echo  =============================================
echo.

:: Guardar el directorio raíz del script de forma absoluta y robusta
set "ROOT_DIR=%~dp0"
:: Remover comillas y espacios extras si los hay
set "ROOT_DIR=%ROOT_DIR:"=%"
set "PYTHON_DIR=%ROOT_DIR%python-daemon"

cd /d "%PYTHON_DIR%"

:: 1. Verificar si Python está instalado
echo [1/5] Verificando instalacion de Python...
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

:: Mostrar versión de Python encontrada
python --version
echo.

:: 2. Crear o verificar el archivo .env
echo [2/5] Verificando archivo de configuracion .env...
set "ENV_EXISTS=0"
if exist .env (
    findstr "OPENROUTER_API_KEY=" .env >nul 2>nul
    if !ERRORLEVEL! equ 0 (
        set "ENV_EXISTS=1"
    )
)

if "!ENV_EXISTS!"=="0" (
    echo.
    echo =======================================================================
    echo  [!] No se encontro la clave API de OpenRouter en .env
    echo  Por favor, introduce tu API Key de OpenRouter para la IA.
    echo  Debe comenzar con sk-or-
    echo =======================================================================
    echo.
    set /p USER_API_KEY="API Key: "
    set "USER_API_KEY=!USER_API_KEY:"=!"
    set "USER_API_KEY=!USER_API_KEY: =!"
    echo OPENROUTER_API_KEY=!USER_API_KEY!> .env
    echo.
    echo [OK] Archivo .env creado con exito.
    echo.
) else (
    echo [OK] Archivo .env configurado correctamente.
)
 
:: 3. Instalar dependencias usando python -m pip
echo.
echo [3/5] Verificando e instalando dependencias (puede tardar la primera vez)...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [!] La instalacion general de dependencias fallo.
    echo  Intentando instalar paquetes individualmente para diagnosticar...
    echo =======================================================================
    echo.
    
    set "FAILED_PACKAGES="
    for /f "usebackq delims=" %%i in ("requirements.txt") do (
        echo Instalando %%i...
        python -m pip install "%%i"
        if !ERRORLEVEL! NEQ 0 (
            set "FAILED_PACKAGES=!FAILED_PACKAGES! %%i"
        )
    )
    
    if not "!FAILED_PACKAGES!"=="" (
        echo.
        echo =======================================================================
        echo  [ERROR] Los siguientes paquetes fallaron al instalarse:
        echo  !FAILED_PACKAGES!
        echo.
        echo  Soluciones recomendadas para problemas comunes:
        
        :: Buscar si pyaudio fallo
        echo !FAILED_PACKAGES! | findstr /i "pyaudio" >nul
        if !ERRORLEVEL! equ 0 (
            echo  * pyaudio: Requiere herramientas de desarrollo de C++ de Visual Studio.
            echo           Como alternativa, puedes descargar e instalar un archivo .whl
            echo           precompilado adecuado para tu version de Python (p. ej. de PyPI
            echo           o repositorios comunitarios).
        )
        
        :: Buscar si pygame fallo
        echo !FAILED_PACKAGES! | findstr /i "pygame" >nul
        if !ERRORLEVEL! equ 0 (
            echo  * pygame: En versiones experimentales de Python como 3.14, no hay wheels 
            echo          precompilados. Se recomienda usar Python 3.10, 3.11 o 3.12.
        )
        
        echo.
        echo  Prueba tambien a actualizar pip ejecutando: python -m pip install --upgrade pip
        echo =======================================================================
        echo.
        pause
        exit /b 1
    ) else (
        echo [OK] Dependencias instaladas individualmente de forma exitosa.
    )
) else (
    echo [OK] Dependencias de Python listas.
)

:: 4. Instalar los navegadores de Playwright necesarios
echo.
echo [4/5] Verificando Playwright Chromium...
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); p.chromium.launch(headless=True); p.stop()" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Playwright Chromium no esta instalado. Instalando navegador...
    python -m playwright install chromium
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo =======================================================================
        echo  [WARNING] Hubo un problema al instalar los binarios de Playwright.
        echo  El control del navegador [abrir webs, YouTube] podria no funcionar.
        echo  Revisa tu conexion a Internet o intenta ejecutar manualmente:
        echo  python -m playwright install chromium
        echo =======================================================================
        echo.
        pause
    )
) else (
    echo [OK] Playwright Chromium esta listo.
)

:: 5. Verificar si hay un micrófono activo en el sistema
echo.
echo [5/5] Verificando dispositivo de microfono...
python -c "import sys, pyaudio; p = pyaudio.PyAudio(); count = p.get_device_count(); p.terminate(); sys.exit(0) if count > 0 else sys.exit(1)" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [WARNING] No se detecto un microfono activo en tu sistema.
    echo  El reconocimiento de voz [STT] de Juan no funcionara.
    echo.
    echo  Soluciones:
    echo   1. Conecta un microfono a tu equipo.
    echo   2. Ve a la Configuracion de Sonido de Windows y asegurate de que 
    echo      este habilitado e introduciendo audio.
    echo =======================================================================
    echo.
    set /p PROCEED_MIC="Deseas iniciar de todas formas? [S/N]: "
    if /i "!PROCEED_MIC!" NEQ "S" (
        exit /b 1
    )
) else (
    echo [OK] Microfono activo detectado.
)

echo.
echo =======================================================================
echo  Arrancando reconocimiento de voz y automatizacion...
echo =======================================================================
echo.
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [ERROR] El demonio de Python se detuvo de forma inesperada (Codigo: %ERRORLEVEL%).
    echo  Revisa los errores detallados arriba.
    echo =======================================================================
    echo.
    pause
)
