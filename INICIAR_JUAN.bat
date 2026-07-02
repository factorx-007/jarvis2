@echo off
title Juan - Asistente Virtual (Cerebro Java)
echo.
echo  =============================================
echo    JUAN - Asistente Virtual Personal
echo    Iniciando el Cerebro (Java Spring Boot)...
echo  =============================================
echo.

cd /d D:\skinet\java-core

:: Usar el Maven portable que ya está descargado
set PATH=%PATH%;%CD%\apache-maven-3.9.5\bin

echo [1/2] Compilando el proyecto...
call mvn compile -q
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Falló la compilación. Revisa los errores arriba.
    pause
    exit /b 1
)

echo [2/2] Arrancando el servidor en puerto 8080...
echo.
echo  Cuando veas "Started JarvisApplication", el Cerebro está listo.
echo  Para detenerlo, cierra esta ventana o presiona Ctrl+C.
echo.
call mvn spring-boot:run -q
pause
