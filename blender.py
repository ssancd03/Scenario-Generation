import os
import sys
import bpy


def importGLTF(directory):
    """Importa todos los archivos GLTF del directorio especificado.

    Args:
        directory (str): Ruta al directorio que contiene los archivos GLTF.

    Returns:
        bool: True si la importación se finalizó de manera correcta.
    """
    gltfFiles = []
    for f in os.listdir(directory):
        if f.endswith(".gltf"):
            gltfFiles.append(f)

    for gltfFile in gltfFiles:
        bpy.ops.import_scene.gltf(filepath = os.path.join(directory, gltfFile))
    return True


def findTextures(textureDir):
    """Encuentra y enlaza los archivos de texturas de un directorio especificado.

    Args:
        textureDir (str): Ruta al directorio que contiene los archivos de texturas.
    """
    bpy.ops.file.find_missing_files(directory = textureDir)


def exportCollada(outputDir, mapName):
    """Exporta la escena como un archivo tipo Collada (.dae).

    Args:
        outputDir (str): Directorio de salida para el archivo exportado.
        mapName (str): Nombre del mapa aplicado al archivo de salida.
    """
    outputPath = os.path.join(outputDir, f"{mapName}.dae")
    bpy.ops.wm.collada_export(filepath = outputPath)


def removeDuplicateVertices():
    """Elimina vértices duplicados de todos los objetos de las mallas"""
    meshObjects = []
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            meshObjects.append(obj)

    for obj in meshObjects:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.select_all(action = "DESELECT")
        obj.select_set(True)

        bpy.ops.object.mode_set(mode = "EDIT")
        bpy.ops.mesh.select_all(action = "SELECT")
        bpy.ops.mesh.remove_doubles(threshold = 0.001)
        bpy.ops.object.mode_set(mode = "OBJECT")


def calculateNormals():
    """Recalcula las normales de los objetos de las mallas."""
    meshObjects = []
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            meshObjects.append(obj)

    for obj in meshObjects:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.select_all(action = "DESELECT")
        obj.select_set(True)

        bpy.ops.object.mode_set(mode = "EDIT")
        bpy.ops.mesh.select_all(action = "SELECT")
        bpy.ops.mesh.normals_make_consistent(inside = False)
        bpy.ops.object.mode_set(mode = "OBJECT")


def smoothShade():
    """Aplica sombreado a todos los objetos de las mallas."""
    meshObjects = []
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            meshObjects.append(obj)

    for obj in meshObjects:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.select_all(action = "DESELECT")
        obj.select_set(True)

        bpy.ops.object.shade_smooth()


def mergeObjects():
    """Fusiona todos los objetos de malla en un solo objeto y elimina duplicados."""
    meshObjects = []
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            meshObjects.append(obj)

    if len(meshObjects) > 1:
        for obj in meshObjects:
            obj.select_set(True)

        bpy.context.view_layer.objects.active = meshObjects[0]
        bpy.ops.object.join()

        bpy.ops.object.mode_set(mode = "EDIT")
        bpy.ops.mesh.select_all(action = "SELECT")
        bpy.ops.mesh.remove_doubles(threshold = 0.01)
        bpy.ops.object.mode_set(mode = "OBJECT")


def optimizeGeometry():
    """Optimiza la geometría de la malla aplicando el modificador de decimación."""
    meshObjects = []
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            meshObjects.append(obj)

    for obj in meshObjects:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.select_all(action = "DESELECT")
        obj.select_set(True)

        decimate = obj.modifiers.new(name = "Decimate", type = "DECIMATE")
        decimate.ratio = 0.9
        decimate.use_collapse_triangulate = True

        bpy.ops.object.modifier_apply(modifier = "Decimate")


def main():
    """Función principal que procesa modelos 3D a través del pipeline de Blender."""
    args = sys.argv[sys.argv.index("--") + 1 :]
    gltfDir, textureDir, outputDir, mapName = args

    if importGLTF(gltfDir):
        findTextures(textureDir)
        removeDuplicateVertices()
        calculateNormals()
        smoothShade()
        # mergeObjects
        # optimizeGeometry
        exportCollada(outputDir, mapName)


if __name__ == "__main__":
    main()
