@echo off
echo Creando entorno virtual venv_clean...
python -m venv venv_clean
call venv_clean\Scripts\activate.bat
echo Instalando dependencias en el entorno virtual...
pip install -r requirements.txt pywebview pyinstaller > build_log.txt 2>&1
echo Empaquetando con PyInstaller...
pyinstaller -y --noconsole --name Jarvis jarvis_app.py >> build_log.txt 2>&1
echo Copiando archivos adicionales a la carpeta del ejecutable...
mkdir dist\Jarvis\jre 2>nul
xcopy /E /I /Q /Y ..\jre dist\Jarvis\jre >nul
mkdir dist\Jarvis\java-core\target 2>nul
copy /Y ..\java-core\target\core-0.0.1-SNAPSHOT.jar dist\Jarvis\java-core\target\ >nul
xcopy /E /I /Q /Y ..\4-dashboard-rostro dist\Jarvis\4-dashboard-rostro >nul
if exist .env copy /Y .env dist\Jarvis\ >nul
echo [OK] Proceso completado. El ejecutable está en dist\Jarvis\Jarvis.exe
