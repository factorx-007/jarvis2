@echo off
title Juan - Asistente Virtual (Cerebro Java)
echo.
echo  =============================================
echo    JUAN - Asistente Virtual Personal
echo    Iniciando el Cerebro (Java Spring Boot)...
echo  =============================================
echo.
cd /d "%~dp0java-core"
:: 1. Verificar si Java está instalado
where java >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [ERROR] No se encontro Java instalado en el sistema o no esta en el PATH.
    echo  El Cerebro de Juan (Java Spring Boot) requiere Java JDK 17 o superior.
    echo.
    echo  Solucion:
    echo   1. Descarga e instala JDK 17 desde: https://adoptium.net/
    echo   2. Asegurate de marcar la opcion para agregarlo a las variables de entorno.
    echo =======================================================================
    echo.
    pause
    exit /b 1
)
:: Usar el Maven portable que ya está descargado
set PATH=%PATH%;%CD%\apache-maven-3.9.5\bin
echo [1/2] Compilando el proyecto...
call mvn compile -q
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [ERROR] Fallo la compilacion del proyecto Java.
    echo  Revisa los errores detallados arriba.
    echo  Causas comunes:
    echo   - Archivos modificados con errores de sintaxis en Java.
    echo   - El JDK instalado es una version antigua (menor a Java 17).
    echo =======================================================================
    echo.
    pause
    exit /b 1
)
echo [2/2] Arrancando el servidor en puerto 8080...
echo.
echo  Cuando veas "Started JarvisApplication", el Cerebro esta listo.
echo  Para detenerlo, cierra esta ventana o presiona Ctrl+C.
echo.
call mvn spring-boot:run -q
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [ERROR] El servidor Spring Boot se detuvo con codigo de error %ERRORLEVEL%.
    echo  Posibles causas:
    echo   - El puerto 8080 ya esta siendo utilizado por otra aplicacion.
    echo     (Prueba a cerrar otras consolas o programas que usen el puerto 8080).
    echo =======================================================================
    echo.
)
pause
