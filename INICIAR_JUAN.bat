@echo off
setlocal enabledelayedexpansion
title Juan - Asistente Virtual (Cerebro Java)

echo.
echo  =============================================
echo    JUAN - Asistente Virtual Personal
echo    Iniciando el Cerebro (Java Spring Boot)...
echo  =============================================
echo.

:: Guardar el directorio raíz del script de forma absoluta y robusta
set "ROOT_DIR=%~dp0"
:: Remover comillas y espacios extras si los hay
set "ROOT_DIR=%ROOT_DIR:"=%"
set "JAVA_DIR=%ROOT_DIR%java-core"

cd /d "%JAVA_DIR%"

:: 1. Verificar si Java está instalado
echo [1/3] Verificando instalacion de Java...
where java >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [ERROR] No se encontro Java instalado en el sistema o no esta en el PATH.
    echo  El Cerebro de Juan - Java Spring Boot - requiere Java JDK 17 o superior.
    echo.
    echo  Solucion:
    echo   1. Descarga e instala JDK 17 o superior desde: https://adoptium.net/
    echo   2. Asegurate de marcar la opcion para agregarlo a las variables de entorno.
    echo =======================================================================
    echo.
    pause
    exit /b 1
)

:: Mostrar versión de Java encontrada
echo.
echo Version de Java detectada:
java -version
echo.

:: 2. Detección y resolución de puerto 8080 en uso
echo [2/3] Verificando disponibilidad del puerto 8080...
netstat -ano | findstr :8080 | findstr LISTENING >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo.
    echo =======================================================================
    echo  [WARNING] El puerto 8080 ya esta siendo utilizado por otra aplicacion.
    echo  El Cerebro de Juan necesita el puerto 8080 para arrancar.
    echo.
    
    :: Mostrar los procesos que usan el puerto
    echo  Detalle del proceso bloqueando el puerto 8080:
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do (
        set "CONFLICT_PID=%%a"
        tasklist /FI "PID eq %%a" 2>nul
    )
    
    echo.
    echo  [Opcion 1] Intentar cerrar el proceso conflictivo automaticamente.
    echo  [Opcion 2] Omitir y continuar de todas formas.
    echo  [Opcion 3] Salir.
    echo.
    set /p CHOICE="Selecciona una opcion [1, 2 o 3]: "
    
    if "!CHOICE!"=="1" (
        echo Intentando detener proceso con PID !CONFLICT_PID!...
        taskkill /PID !CONFLICT_PID! /F
        if !ERRORLEVEL! equ 0 (
            echo [OK] Puerto 8080 liberado con exito.
        ) else (
            echo [ERROR] No se pudo detener el proceso automaticamente.
            echo Por favor ejecuta la consola como Administrador o cierra el programa manualmente.
            pause
            exit /b 1
        )
    ) else if "!CHOICE!"=="3" (
        echo Cancelando inicio por conflicto de puerto.
        pause
        exit /b 1
    )
    echo =======================================================================
    echo.
) else (
    echo [OK] Puerto 8080 libre.
)

:: 3. Configurar Maven portable local
if exist "%JAVA_DIR%\apache-maven-3.9.5\bin\mvn.cmd" (
    set "MAVEN_CMD=%JAVA_DIR%\apache-maven-3.9.5\bin\mvn.cmd"
    echo Usando Maven portable local: !MAVEN_CMD!
) else (
    where mvn >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "MAVEN_CMD=mvn"
        echo Usando Maven del sistema global.
    ) else (
        echo.
        echo =======================================================================
        echo  [ERROR] No se encontro Maven portable local ni global en el sistema.
        echo  No se puede compilar ni arrancar la aplicacion Java.
        echo  Falta la carpeta: %JAVA_DIR%\apache-maven-3.9.5\bin
        echo =======================================================================
        echo.
        pause
        exit /b 1
    )
)

echo.
echo [3/3] Compilando e iniciando el servidor...
echo Compilando el proyecto (esto puede tardar unos segundos)...
call "%MAVEN_CMD%" compile
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [ERROR] Fallo la compilacion del proyecto Java.
    echo  Revisa detalladamente los errores de compilacion listados arriba.
    echo =======================================================================
    echo.
    pause
    exit /b 1
)

echo.
echo Iniciando Spring Boot en puerto 8080...
echo Cuando veas "Started JarvisApplication", el Cerebro estara listo.
echo Para detenerlo, cierra esta ventana o presiona Ctrl+C.
echo.

call "%MAVEN_CMD%" spring-boot:run
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================================
    echo  [ERROR] El servidor Spring Boot se detuvo con codigo de error %ERRORLEVEL%.
    echo  Revisa la traza de errores detallada arriba para diagnosticar.
    echo =======================================================================
    echo.
)
pause
