@echo off
echo Creando entorno virtual venv_clean...
python -m venv venv_clean
call venv_clean\Scripts\activate.bat
echo Instalando dependencias en el entorno virtual...
pip install -r requirements.txt pyinstaller > build_log.txt 2>&1
echo Empaquetando con PyInstaller...
pyinstaller -y --noconsole --name Jarvis --collect-all audioop --hidden-import=pygame jarvis_app.py >> build_log.txt 2>&1
echo Copiando archivos adicionales a la carpeta del ejecutable...
mkdir dist\Jarvis\jre 2>nul
xcopy /E /I /Q /Y ..\jre dist\Jarvis\jre >nul
mkdir dist\Jarvis\java-core\target 2>nul
copy /Y ..\java-core\target\core-0.0.1-SNAPSHOT.jar dist\Jarvis\java-core\target\ >nul
xcopy /E /I /Q /Y ..\4-dashboard-rostro dist\Jarvis\4-dashboard-rostro >nul
if exist .env copy /Y .env dist\Jarvis\ >nul
copy /Y Jarvis.exe.config dist\Jarvis\ >nul
echo Empaquetando todo en Jarvis_Portable.zip (esto puede tardar unos segundos)...
powershell -Command "if (Test-Path 'dist\Jarvis_Portable.zip') { Remove-Item 'dist\Jarvis_Portable.zip' }; Compress-Archive -Path 'dist\Jarvis\*' -DestinationPath 'dist\Jarvis_Portable.zip' -Force"
echo [OK] Proceso completado. 
echo La carpeta extraida esta en: dist\Jarvis\
echo El archivo comprimido final esta en: dist\Jarvis_Portable.zip
