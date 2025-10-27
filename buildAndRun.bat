@echo off
chcp 65001 >nul
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    INICIANDO PROCESO                         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [1/4] Limpiando directorios
if exist "C:\modelLib" rmdir /s /q "C:\modelLib"
if exist "C:\scene" rmdir /s /q "C:\scene"

echo.
echo [2/4] Ejecutando aplicacion de mapas
echo       - Selecciona la región y descarga los datos
echo       - El proceso esperará hasta que completes la descarga y cierres la aplicación
start /wait "Earth2MsfsWPF" "app\Earth2MsfsWPF.exe"

echo.
echo [3/4] Iniciando pipeline de procesamiento
echo       - Configurando nombre del mapa
echo       - Mejorando texturas con IA
echo       - Optimizando geometría 3D en Blender
echo       - Opción de copia permanente
python bridge.py

echo.
echo [4/4] Procesamiento completado
echo       - Archivos generados en la carpeta output

echo.
if exist "saves" (
echo     Copias permanentes disponibles en: saves/
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    PROCESO COMPLETADO                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause
