@echo off
title Juan - Sistema Nervioso (Python)
echo.
echo  =============================================
echo    JUAN - Asistente Virtual Personal
echo    Iniciando el Sistema Nervioso (Python)...
echo  =============================================
echo.

cd /d "%~dp0\python-daemon"

echo [1/2] Verificando e instalando dependencias (puede tardar la primera vez)...
pip install -r requirements.txt -q
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ADVERTENCIA: Hubo un problema al instalar las dependencias. 
    echo Asegurate de tener Python instalado y agregado al PATH.
)

echo.
echo [2/2] Arrancando reconocimiento de voz y automatizacion...
echo.
python main.py

echo.
pause
