import os
import re
from settings import getConfig


def cleanDaeFile(filePath):
    """Limpia un archivo DAE elimando los componentes iniciales de un proyecto BLender.
    
    Args:
        filePath (str): Ruta al archivo DAE.
        
    Returns:
        bool: True si se realizaron los cambios en el archivo, False en caso contrario.
    """
    if not os.path.exists(filePath):
        return False

    try:
        with open(filePath, "r", encoding = "utf-8") as f:
            content = f.read()

        cubeGeometryPattern = r"<geometry id=\"Cube-mesh\" name=\"Cube\">.*?</geometry>"
        cubeNodePattern = r"<node id=\"Cube\" name=\"Cube\" type=\"NODE\">.*?</node>"

        cameraLibraryPattern = r"<library_cameras>.*?</library_cameras>"
        cameraNodePattern = (r"<node id=\"Camera\" name=\"Camera\" type=\"NODE\">.*?</node>")

        lightLibraryPattern = r"<library_lights>.*?</library_lights>"
        lightNodePattern = r"<node id=\"Light\" name=\"Light\" type=\"NODE\">.*?</node>"

        geometryMatches = re.findall(cubeGeometryPattern, content, re.DOTALL)
        if geometryMatches:
            content = re.sub(cubeGeometryPattern, "", content, flags = re.DOTALL)

        nodeMatches = re.findall(cubeNodePattern, content, re.DOTALL)
        if nodeMatches:
            content = re.sub(cubeNodePattern, "", content, flags = re.DOTALL)

        cameraLibMatches = re.findall(cameraLibraryPattern, content, re.DOTALL)
        if cameraLibMatches:
            content = re.sub(cameraLibraryPattern, "", content, flags = re.DOTALL)

        cameraNodeMatches = re.findall(cameraNodePattern, content, re.DOTALL)
        if cameraNodeMatches:
            content = re.sub(cameraNodePattern, "", content, flags = re.DOTALL)

        lightLibMatches = re.findall(lightLibraryPattern, content, re.DOTALL)
        if lightLibMatches:
            content = re.sub(lightLibraryPattern, "", content, flags = re.DOTALL)

        lightNodeMatches = re.findall(lightNodePattern, content, re.DOTALL)
        if lightNodeMatches:
            content = re.sub(lightNodePattern, "", content, flags = re.DOTALL)

        if (geometryMatches or nodeMatches or cameraLibMatches or cameraNodeMatches or lightLibMatches or lightNodeMatches):
            with open(filePath, "w", encoding = "utf-8") as f:
                f.write(content)
            return True
        else:
            return False

    except Exception:
        return False


def cleanupOutputDae():
    """Limpia el archivo DAE en el directorio de salida."""
    config = getConfig()
    outputDir = config["paths"]["outputDir"]
    meshesDir = os.path.join(outputDir, "meshes")

    if not os.path.exists(meshesDir):
        return

    for f in os.listdir(meshesDir):
        if f.endswith(".dae"):
            daePath = os.path.join(meshesDir, f)
            cleanDaeFile(daePath)
            break


def cleanupSavesDae():
    """Limpia todos los archivos DAE en los directorios de almacenamiento permanente."""
    config = getConfig()
    savesDir = config["paths"]["savesDir"]

    if not os.path.exists(savesDir):
        return

    for saveFolder in os.listdir(savesDir):
        savePath = os.path.join(savesDir, saveFolder)
        if os.path.isdir(savePath):
            meshesPath = os.path.join(savePath, "meshes")
            if os.path.exists(meshesPath):
                daeFiles = []
                for f in os.listdir(meshesPath):
                    if f.endswith(".dae"):
                        daeFiles.append(f)

                if not daeFiles:
                    continue

                for daeFile in daeFiles:
                    daePath = os.path.join(meshesPath, daeFile)
                    cleanDaeFile(daePath)


def main():
    """Función principal que ejecuta la limpieza de archivos DAE."""
    cleanupOutputDae()
    cleanupSavesDae()


if __name__ == "__main__":
    main()
