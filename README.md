# TFG - Análisis Territorial con Deep Learning

Este repositorio contiene el código y los recursos utilizados en el Trabajo de Fin de Grado (TFG) titulado **"Uso del Deep Learning para la Gestión Territorial: Segmentación y Detección con Sentinel-2"**, realizado por Carlos Romero Matarín en el marco del Grado en Ingeniería Informática (VIU, 2025).

## Objetivo

Desarrollar un sistema inteligente capaz de realizar:
- **Segmentación multiclase** del territorio mediante el modelo U-Net.
- **Detección puntual de estructuras** artificiales con el modelo YOLOv8.
- **Análisis multitemporal** sobre imágenes satelitales Sentinel-2 de la zona de Terrassa y el AMB.

## Modelos empleados

- **U-Net:** Segmentación semántica con etiquetas EUCROPMAP.
- **YOLOv8:** Detección de objetos en imágenes RGB Sentinel-2 (.jpg).

## Estructura del proyecto

```
TFG_VIU_ING_INF/
│
├── importacion/          # Scripts de descarga y preprocesamiento
├── Datos/                # Imágenes Sentinel-2 y etiquetas organizadas por año
├── script.ipynb          # Cuaderno principal con flujo completo del análisis
├── yolov8n.pt            # Modelo YOLOv8 entrenado
├── mejor_modelo.h5       # Mejor modelo U-Net
└── README.md             # Este archivo
```

## 🔗 Repositorio

Repositorio disponible en: [https://github.com/Ifcarlitos/TFG_VIU_ING_INF](https://github.com/Ifcarlitos/TFG_VIU_ING_INF)
