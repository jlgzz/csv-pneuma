# 📊 Análisis de Datos de Aire Comprimido

Este proyecto procesa, limpia y analiza datos provenientes de un
datalogger de sistemas de aire comprimido. Genera visualizaciones
avanzadas para identificar patrones de consumo, comportamiento operativo
y oportunidades de optimización.

------------------------------------------------------------------------

## 🚀 Funcionalidades

-   📥 Lectura y limpieza de archivos CSV crudos
-   🔧 Corrección de unidades (flujo, presión, temperatura)
-   📈 Generación de:
    -   Gráficas de tendencia
    -   Histogramas
    -   Mapas de calor (2D y 3D)
    -   Curva de duración de carga
-   📤 Exportación de datos procesados

------------------------------------------------------------------------

## 📁 Estructura del Proyecto

    .
    ├── outputs/
    ├── scr/
    ├── scripts/
    ├── venv/
    ├── funciones.py
    ├── graficas.py
    ├── generador_de_reportes.py
    └── README.md

------------------------------------------------------------------------

## ⚙️ Requisitos

Python 3.8+

    pip install pandas numpy matplotlib seaborn

------------------------------------------------------------------------

## ▶️ Uso

1.  Coloca tu archivo CSV en:

```{=html}
<!-- -->
```
    scr/datalogger_rawData.csv

2.  Ejecuta:

```{=html}
<!-- -->
```
    python generador_de_reportes.py

------------------------------------------------------------------------

## 🔄 Flujo del Proceso

1.  Lectura del totalizador inicial\
2.  Carga de datos crudos\
3.  Preprocesamiento (conversiones y correcciones)\
4.  Generación de dataset limpio\
5.  Análisis y visualización

------------------------------------------------------------------------

## 📊 Visualizaciones Generadas

-   Gráfica de tendencia\
-   Histogramas\
-   Mapas de calor\
-   Curva de duración de carga

------------------------------------------------------------------------

## 📈 Casos de Uso

-   Auditorías energéticas\
-   Identificación de fugas\
-   Optimización de compresores\
-   Análisis de demanda

------------------------------------------------------------------------

## 👨‍💻 Autor

Leonel (LeosNoob)
