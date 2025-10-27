# Scenario-Generation

## Descripción

Sistema avanzado de generación de escenarios 3D desarrollado en colaboración entre **ISDEFE** (Ingeniería de Sistemas para la Defensa de España) y la **Universidad de León** a través de la Cátedra ISDEFE-ULE. Este proyecto forma parte de la investigación en tecnologías de simulación y modelado 3D para aplicaciones de defensa y aeronáuticas.

El sistema permite el procesamiento automático de modelos 3D en formato GLTF/GLB, mejora de texturas mediante inteligencia artificial, y exportación de escenarios optimizados para simuladores como Microsoft Flight Simulator y otros entornos de simulación.

## Características Principales

### Procesamiento de Modelos 3D
- **Importación automática** de archivos GLTF/GLB
- **Optimización de geometría** con decimación inteligente
- **Fusión de objetos** y eliminación de vértices duplicados
- **Recálculo de normales** y aplicación de sombreado suave
- **Exportación a formato Collada** (.dae) compatible con simuladores

### Mejora de Texturas con IA
- **Upscaling inteligente** utilizando Real-ESRGAN
- **Múltiples factores de escalado**: x2 y x4
- **Soporte para GPU y CPU** con optimización automática
- **Procesamiento por lotes** con barra de progreso
- **Preservación de calidad** en texturas de alta resolución

### Pipeline Automatizado
- **Configuración flexible** mediante archivos de configuración
- **Verificación de dependencias** automática
- **Estructura de carpetas** auto-generada
- **Plantillas personalizables** para metadatos de modelos
- **Sistema de limpieza** para archivos temporales

## Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/ssancd03/Scenario-Generation.git
cd Scenario-Generation
```

### 2. Configurar Entorno Conda
```bash
# Crear entorno desde archivo de configuración
conda env create -f environment.yml

# Activar el entorno
conda activate scenario-generation
```

### 3. Descargar Modelos Real-ESRGAN
Los modelos de upscaling se encuentran en Google Drive debido a su tamaño:
[Modelos Real-ESRGAN](https://drive.google.com/drive/folders/13qXV8j6BLcAKTlM1bKpDywOL2LnK1CX2?usp=sharing)

Descargar y colocar en la carpeta `models/`:
- `RealESRGAN_x2plus.pth`
- `RealESRGAN_x4plus.pth`

### 4. Configurar Rutas
Editar `settings.py` para ajustar las rutas según tu sistema:
```python
def getBlenderPath():
    return "C:/Program Files/Blender Foundation/Blender 4.1/blender.exe"  # Windows
    # return "/usr/bin/blender"  # Linux
    # return "/Applications/Blender.app/Contents/MacOS/Blender"  # macOS
```

## Estructura del Proyecto

```
Scenario-Generation/
├── README.md                    # Este archivo
├── environment.yml              # Configuración del entorno conda
├── settings.py                  # Configuración global del proyecto
├── bridge.py                    # Interfaz principal y coordinador
├── converter.py                 # Pipeline de procesamiento principal
├── blender.py                   # Scripts para Blender
├── cleanup.py                   # Limpieza de archivos temporales
├── app/                         # Aplicación Windows (Earth2MsfsWPF)
├── models/                      # Modelos Real-ESRGAN (descargar por separado)
├── templates/                   # Plantillas para metadatos
│   ├── modelConfig.txt
│   └── modelSDF.txt
├── output/                      # Salida del procesamiento (auto-generada)
│   ├── model.config
│   ├── model.sdf
│   └── meshes/
└── saves/                       # Copias permanentes (auto-generada)
```

## Uso

### Ejecución Principal
```bash
# Activar entorno
conda activate scenario-generation

# Ejecutar pipeline completo
python bridge.py
```

### Configuración de Upscaling
En `settings.py`, modificar la variable `upscalingMethod`:
```python
upscalingMethod = "0"  # Sin upscaling (por defecto)
upscalingMethod = "2"  # Upscaling x2
upscalingMethod = "4"  # Upscaling x4
```

### Flujo de Trabajo
1. **Preparar modelos GLTF**: Colocar archivos .gltf en la carpeta especificada
2. **Preparar texturas**: Organizar texturas PNG en la carpeta de texturas
3. **Ejecutar bridge.py**: Seguir las instrucciones en pantalla
4. **Introducir nombre del mapa**: Especificar identificador único
5. **Esperar procesamiento**: El sistema procesará automáticamente
6. **Revisar resultados**: Los archivos se generan en `output/`
7. **Crear copia permanente**: Opcional, para preservar el trabajo

### Ejecución por Componentes
```bash
# Solo mejora de texturas y procesamiento
python converter.py nombre_mapa

# Solo limpieza de archivos
python cleanup.py
```

## Configuración Avanzada

### Parámetros de Upscaling
```python
"texture": {
    "useGpu": True,           # Usar GPU si está disponible
    "tileSize": 0,            # Tamaño de tile (0 = automático)
    "halfPrecision": False,   # Usar precisión media (ahorra memoria)
}
```

### Rutas Personalizadas
```python
"paths": {
    "gltfDir": "C:/modelLib",              # Directorio de modelos GLTF
    "textureDir": "C:/modelLib/texture",   # Directorio de texturas
    "outputDir": "./output",               # Salida del procesamiento
    "modelsDir": "./models",               # Modelos Real-ESRGAN
    "templatesDir": "./templates",         # Plantillas de metadatos
    "savesDir": "./saves",                 # Copias permanentes
}
```

## Desarrollado por

### Instituciones
- **ISDEFE** - Ingeniería de Sistemas para la Defensa de España
- **Universidad de León** - Cátedra ISDEFE-ULE

### Autor Principal
**Sergio Sánchez de la Fuente**
- Email: ssand@unileon.es
- Afiliación: Universidad de León

## Tecnologías Utilizadas

### Inteligencia Artificial
- **Real-ESRGAN**: Super-resolución de imágenes basada en redes neuronales
- **RRDB (Residual in Residual Dense Block)**: Arquitectura de red neuronal avanzada
- **PyTorch**: Framework de deep learning para inferencia

### Procesamiento 3D
- **Blender**: Motor de renderizado y procesamiento de modelos 3D
- **GLTF/GLB**: Formato estándar para modelos 3D web
- **Collada (DAE)**: Formato de intercambio para simuladores

### Desarrollo
- **Python**: Lenguaje principal de desarrollo
- **Conda**: Gestión de entornos y dependencias
- **OpenCV**: Procesamiento de imágenes
- **NumPy**: Computación científica

## Contribuciones

Este proyecto forma parte de la investigación académica de la Cátedra ISDEFE-ULE. Las contribuciones están sujetas a las políticas de colaboración entre ambas instituciones.

*Desarrollado con el apoyo de ISDEFE y el Grupo de Robótica de la Universidad de León en el marco de la Cátedra de Innovación Tecnológica.*