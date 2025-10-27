import os
import shutil
import subprocess
import sys
import numpy as np
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from PIL import Image
from realesrgan import RealESRGANer
from tqdm import tqdm
from settings import getConfig, setMapName


def createFolder():
    """Crea la estructura de carpetas de salida y prepara los archivos de plantilla."""
    config = getConfig()
    outputDir = config["paths"]["outputDir"]
    templatesDir = config["paths"]["templatesDir"]
    meshDir = os.path.join(outputDir, "meshes")

    if os.path.isdir(outputDir):
        shutil.rmtree(outputDir)
    os.makedirs(outputDir)
    os.makedirs(meshDir)

    with open(os.path.join(templatesDir, "modelConfig.txt"), "r") as f:
        configContent = f.read()
    configContent = configContent.replace("{{MAP_NAME}}", config["mapName"])
    with open(os.path.join(outputDir, "model.config"), "w") as f:
        f.write(configContent)

    with open(os.path.join(templatesDir, "modelSDF.txt"), "r") as f:
        sdfContent = f.read()
    sdfContent = sdfContent.replace("{{MAP_NAME}}", config["mapName"])
    with open(os.path.join(outputDir, "model.sdf"), "w") as f:
        f.write(sdfContent)


def enhanceTextures():
    """Mejora las texturas usando upscaling Real-ESRGAN si está configurado."""
    config = getConfig()
    textureDir = config["paths"]["textureDir"]

    imageFiles = []
    for f in os.listdir(textureDir):
        if f.lower().endswith(".png"):
            imageFiles.append(f)

    device = ("cuda" if torch.cuda.is_available() and config["texture"]["useGpu"] else "cpu")
    print(f"\nDispositivo utilizado: {device}")

    upscaleFactor = config["texture"]["upscaleFactor"]
    modelFile = config["texture"]["modelFile"]

    if upscaleFactor == 0:
        print("Modo sin upscaling seleccionado, utilizando texturas originales")
        print("Procesando modelos 3D en Blender")
        return

    print(f"Iniciando upscaling con factor x{upscaleFactor}")

    if not modelFile:
        print("No se especificó archivo de modelo")
        print("Procesando modelos 3D en Blender")
        return

    modelPath = os.path.join("models", modelFile)
    if not os.path.exists(modelPath):
        print(f"Modelo no encontrado: {modelPath}")
        print("Procesando modelos 3D en Blender")
        return

    stateDict = torch.load(modelPath, map_location = "cpu")["params_ema"]

    model = RRDBNet(
        num_in_ch = 3,
        num_out_ch = 3,
        num_feat = 64,
        num_block = 23,
        num_grow_ch = 32,
        scale = upscaleFactor,
    )

    model.load_state_dict(stateDict, strict=True)
    model = model.to(device)

    upsampler = RealESRGANer(
        scale = upscaleFactor,
        model_path = modelPath,
        model = model,
        tile = config["texture"]["tileSize"],
        tile_pad = 10,
        pre_pad = 0,
        half = config["texture"]["halfPrecision"],
    )

    for fileName in tqdm(imageFiles, desc="Upscaling", unit="texturas"):
        imagePath = os.path.join(textureDir, fileName)
        try:
            img = Image.open(imagePath).convert("RGB")
            imgArray = np.array(img)
            output, _ = upsampler.enhance(imgArray, outscale = upscaleFactor)
            outputImg = Image.fromarray(output)
            outputImg.save(imagePath)
        except Exception as e:
            print(f"Error procesando {fileName}: {str(e)}")

    print("Procesando modelos 3D en Blender")


if __name__ == "__main__":
    """Bloque de ejecución principal para el procesamiento de texturas y modelos de mapas."""
    if len(sys.argv) > 1:
        mapName = sys.argv[1]
        setMapName(mapName)

    try:
        createFolder()
        enhanceTextures()

        config = getConfig()
        blenderDir = config["paths"]["blenderExe"]
        blenderFileDir = os.path.abspath("blender.py")
        gltfDir = config["paths"]["gltfDir"]
        textureDir = config["paths"]["textureDir"]
        outputDir = config["paths"]["outputDir"]
        meshDir = os.path.join(outputDir, "meshes")

        with open(os.devnull, "w") as devnull:
            result = subprocess.run(
                [
                    blenderDir,
                    "--background",
                    "--python",
                    blenderFileDir,
                    "--",
                    gltfDir,
                    textureDir,
                    meshDir,
                    config["mapName"],
                ],
                stdout = devnull,
                stderr = devnull,
            )

        if result.returncode == 0:
            print("Procesamiento de Blender completado")
        else:
            print(f"Error en Blender: código de salida {result.returncode}")

    except Exception as e:
        print(f"Error en el pipeline: {str(e)}")
        sys.exit(1)
