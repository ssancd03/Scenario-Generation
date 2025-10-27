import os

upscalingMethod = "0"
mapName = "map"
projectRoot = os.path.dirname(os.path.abspath(__file__))

upscalingOptions = {
    "0": {
        "upscaleModel": "x0",
        "upscaleFactor": 0,
        "modelFile": None,
        "description": "Modo predeterminado",
    },
    "2": {
        "upscaleModel": "x2",
        "upscaleFactor": 2,
        "modelFile": "RealESRGAN_x2plus.pth",
        "description": "Método que duplica la resolución de las imágenes",
    },
    "4": {
        "upscaleModel": "x4",
        "upscaleFactor": 4,
        "modelFile": "RealESRGAN_x4plus.pth",
        "description": "Método que cuadruplica la resolución de las imágenes",
    },
}


def getBlenderPath():
    """Obtiene la ruta de instalación predeterminada de Blender 4.1 en Windows.

    Returns:
        str: Ruta al ejecutable de Blender 4.1.
    """
    return "C:/Program Files/Blender Foundation/Blender 4.1/blender.exe"


def getConfig():
    """Obtiene el diccionario de configuración completo con todas las configuraciones y rutas.

    Returns:
        dict: Configuración completa incluyendo configuraciones de textura y rutas de archivos.
    """
    upscaleConfig = upscalingOptions.get(upscalingMethod, upscalingOptions["2"])

    config = {
        "mapName": mapName,
        "texture": {
            "upscaleModel": upscaleConfig["upscaleModel"],
            "upscaleFactor": upscaleConfig["upscaleFactor"],
            "modelFile": upscaleConfig["modelFile"],
            "useGpu": True,
            "tileSize": 0,
            "halfPrecision": False,
            "description": upscaleConfig["description"],
        },
        "paths": {
            "blenderExe": getBlenderPath(),
            "outputDir": os.path.join(projectRoot, "output"),
            "gltfDir": "C:/modelLib",
            "textureDir": "C:/modelLib/texture",
            "modelsDir": os.path.join(projectRoot, "models"),
            "templatesDir": os.path.join(projectRoot, "templates"),
            "savesDir": os.path.join(projectRoot, "saves"),
        },
    }

    return config


def getUpscalingConfig():
    """Obtiene la configuración de upscaling basada en el método de upscaling actual.

    Returns:
        dict: Diccionario de configuración de upscaling con modelo y configuraciones.

    Raises:
        ValueError: Si el método de upscaling no es válido.
    """
    if upscalingMethod not in upscalingOptions:
        raise ValueError(f"Error: Metodo de upscaling '{upscalingMethod}' no válido.")
    return upscalingOptions[upscalingMethod]


def setMapName(newMapName):
    """Establece la variable global del nombre del mapa.

    Args:
        newMapName (str): El nuevo nombre del mapa a establecer.
    """
    global mapName
    mapName = newMapName
