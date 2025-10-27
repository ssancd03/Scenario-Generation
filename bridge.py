import os
import shutil
import subprocess
import time
from datetime import datetime
from settings import getUpscalingConfig, setMapName


def loadUpscaleConfig():
    """Carga la configuración de upscaling desde las configuraciones.

    Returns:
        dict: Diccionario de configuración de upscaling o None si ocurre un error.
    """
    try:
        config = getUpscalingConfig()
        return config
    except Exception as e:
        print(f"Error cargando configuración de upscaling: {e}")
        return None


def checkDependencies():
    """Verifica si todos los archivos y las dependencias son correctas.

    Returns:
        bool: True si las dependencias son correctas, False en caso contrario.
    """
    print("Comprobando archivos")
    requiredFiles = ["converter.py", "blender.py", "settings.py"]

    missingFiles = []
    for filePath in requiredFiles:
        if not os.path.exists(filePath):
            missingFiles.append(filePath)

    if missingFiles:
        print(f"Archivos no encontrados: {', '.join(missingFiles)}")
        return False

    config = loadUpscaleConfig()
    if config and config.get("upscaleFactor", 0) > 0:
        modelsExist = os.path.exists("models/RealESRGAN_x2plus.pth") and os.path.exists("models/RealESRGAN_x4plus.pth")

        if not modelsExist:
            print("Modelos de upscaling no encontrados")
    else:
        print("Modo sin upscaling seleccionado")

    print("Dependencias verificadas")
    return True


def createOutputStructure():
    """Crea la estructura de directorios de salida necesaria para el procesamiento."""
    print("Preparando estructura de carpetas")

    directories = ["output", "output/meshes"]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print("Estructura de carpetas preparada")


def runProcessingPipeline(mapName):
    """Ejecuta el pipeline principal de procesamiento con el nombre de mapa especificado.

    Args:
        mapName (str): Nombre del mapa a procesar.

    Returns:
        bool: True si la ejecución del pipeline es exitosa.
    """
    pipelinePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "converter.py")

    subprocess.run(["python", pipelinePath, mapName], shell=True)
    return True


def getMapName():
    """Obtiene el nombre del mapa desde la entrada del usuario.

    Returns:
        str: Nombre del mapa introducido por el usuario.
    """

    while True:
        mapName = input("Introduce el nombre del mapa (por defecto: map): ").strip()
        if not mapName:
            mapName = "map"

        if mapName.replace("_", "").replace("-", "").isalnum():
            break
        else:
            print("El nombre del mapa solo puede contener letras, números, guiones y guiones bajos.")

    setMapName(mapName)
    print(f"Nombre del mapa configurado: {mapName}")
    return mapName


def askForPermanentCopy():
    """Pregunta al usuario si desea crear una copia permanente del mapa.

    Returns:
        bool: True si el usuario quiere crear una copia permanente, False en caso contrario.
    """
    print("¿Deseas crear una copia permanente de este mapa?, se guardará en una carpeta separada que no se sobrescribirá.")

    while True:
        response = input("Crear copia permanente? (s/n): ").strip().lower()
        if response in ["s", "si"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Por favor, responde 's' para sí o 'n' para no.")


def createPermanentCopy(mapName):
    """Crea una copia permanente del mapa procesado.

    Args:
        mapName (str): Nombre del mapa para crear la copia permanente.
    """
    from settings import getConfig

    config = getConfig()
    outputDir = config["paths"]["outputDir"]
    savesDir = config["paths"]["savesDir"]

    os.makedirs(savesDir, exist_ok=True)

    finalMapName = mapName
    counter = 1
    permanentDir = os.path.join(savesDir, finalMapName)

    while os.path.exists(permanentDir):
        finalMapName = f"{mapName}({counter})"
        permanentDir = os.path.join(savesDir, finalMapName)
        counter += 1

    try:
        shutil.copytree(outputDir, permanentDir)
        if finalMapName != mapName:
            print(f"Copia permanente creada en: {permanentDir}")
            print(f"(Renombrado a '{finalMapName}' para evitar duplicados)")
        else:
            print(f"Copia permanente creada en: {permanentDir}")
    except Exception as e:
        print(f"Error al crear la copia permanente: {e}")


def main():
    """Funcion principal que se encarga de organizar el sistema de procesado general."""
    startTime = time.time()

    print(f"\nNueva sesión registrada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")

    if not checkDependencies():
        print("Error en las verificaciones iniciales")
        input("Presiona Enter para salir")
        return

    mapName = getMapName()

    upscaleConfig = loadUpscaleConfig()
    if upscaleConfig:
        print(f"Configuración de upscaling: {upscaleConfig['description']}")
        if upscaleConfig["modelFile"] is not None:
            print(f"Modelo: {upscaleConfig['modelFile']}")
        print("")

    createOutputStructure()

    input("\n--- Pulsa Enter para iniciar el procesamiento (Puede llevar un tiempo) ---")

    runProcessingPipeline(mapName)

    endTime = time.time()

    print(f"\nTiempo total de la sesión: {(endTime - startTime):.1f} segundos")

    if askForPermanentCopy():
        createPermanentCopy(mapName)

    try:
        from cleanup import main as cleanupMain

        cleanupMain()
    except Exception:
        pass

    print("\n¡Procesamiento completado!")


if __name__ == "__main__":
    main()
