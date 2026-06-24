# Telco Customer Churn — Pipeline DataOps

Pipeline de datos para el análisis y procesamiento del dataset
Telco Customer Churn, desarrollado como proyecto universitario
para la asignatura ITY1101 Gestión de Datos para IA — DuocUC 2026.

---

## Integrantes

| Nombre

Nicolas Herrera
Rodrigo Villaroel
Ismael Sanchez

---

## Descripción del proyecto

Una compañía de telecomunicaciones enfrenta un alto índice de
abandono (churn) entre sus clientes. Este pipeline implementa
las 4 etapas del ciclo DataOps para procesar, limpiar y cargar
los datos, dejándolos listos para un modelo predictivo.

---

## Requisitos previos

| Herramienta | Versión mínima | Notas |
|---|---|---|
| Python | 3.11 | Incluido en el Codespace |
| GitHub Codespaces | — | Entorno recomendado |
| Docker | Cualquiera | Solo si se ejecuta local |

> **Forma recomendada: GitHub Codespaces.**
> Al abrir el Codespace, el entorno se configura automáticamente y todas las dependencias se instalan solas. No requiere ningún paso adicional.

---

## Cómo ejecutar (GitHub Codespaces)

### 1. Abrir el Codespace

En GitHub, hacer clic en **Code → Codespaces → Create codespace on main**.

El `devcontainer.json` ejecuta automáticamente:
```
pip install -r requirements.txt
```
Esto instala todas las dependencias necesarias. Esperar a que el Codespace termine de configurarse (≈1 minuto).

### 2. Correr el pipeline completo

Abrir la terminal del Codespace y ejecutar:

```bash
python3 pipeline.py
```

> ⚠️ **Importante:** usar `python3` y no el botón ▶ de VS Code ni `/usr/bin/python3`.
> El botón de play puede apuntar a un intérprete distinto que no tiene los paquetes instalados.

### 3. Salida esperada

```
=======================================================
  PIPELINE DATAOPS — TELCO CUSTOMER CHURN
=======================================================

[1/5] Ingestion...
 Ingesta: 7043 filas | 21 columnas

[2/5] Procesamiento...
Transformación: 11 cambios | 0 nulos residuales | shape (7021, 20)

[3/5] Data Quality...
Validación: todos los checks pasaron (0 errores)

[4/5] Carga...
[OK] Carga: 7021 filas insertadas en SQLite

[5/5] Modelo IA...
[OK] Preparacion: 7021 registros | 19 features
     Train: 5616 muestras | Test: 1405 muestras
[OK] Entrenamiento: Random Forest | 5616 muestras
[OK] Metricas del modelo:
   Accuracy  : 0.7616
   Recall    : 0.7366
   Precision : 0.5362
   F1 Score  : 0.6206
   AUC-ROC   : 0.8378
   Gini      : 0.6755
=======================================================
```

---

## Estructura del proyecto

```
Telco_Churn/
│
├── pipeline.py                        # Orquestador principal — punto de entrada
│
├── ingestion/
│   └── lectura_csv.py                 # Etapa 1: carga del CSV raw
│
├── procesamiento/
│   └── transformacion.py              # Etapa 2: limpieza y transformación
│
├── data_quality/
│   └── validacion.py                  # Etapa 3: validación de calidad
│
├── carga/
│   └── carga.py                       # Etapa 4: carga a SQLite y CSV
│
├── modelo/
│   ├── preparacion.py                 # Split train/test + encoding
│   ├── entrenamiento.py               # Entrenamiento Random Forest
│   └── metricas.py                    # Métricas y gráficos del modelo
│
├── IA_Proyecto/
│   ├── data/
│   │   ├── telco_raw.csv              # Dataset original
│   │   ├── telco_limpio.csv           # CSV procesado (generado por el pipeline)
│   │   └── telco.db                   # Base de datos SQLite (generada por el pipeline)
│   ├── modelo/
│   │   ├── modelo_churn.pkl           # Modelo entrenado (generado por el pipeline)
│   │   └── graficos/
│   │       ├── matriz_confusion.png   # Generado por el pipeline
│   │       └── curva_roc.png          # Generado por el pipeline
│   └── logs/
│       └── pipeline.log               # Log completo de ejecución
│
├── analisis_univariado_bivariado.ipynb  # Análisis exploratorio (EDA)
├── metricas_telco.ipynb                 # Análisis de métricas de los 3 modelos
├── requirements.txt                     # Dependencias del proyecto
└── .devcontainer/
    └── devcontainer.json                # Configuración del Codespace
```

---

## Dependencias

Definidas en `requirements.txt` e instaladas automáticamente por el Codespace:

```
pandas==2.2.2
numpy==2.4.6
scikit-learn==1.4.2
matplotlib==3.9.0
seaborn==0.13.2
joblib==1.4.2
```

Para instalar manualmente (solo si se ejecuta fuera del Codespace):

```bash
pip install -r requirements.txt
```

---

## Archivos generados por el pipeline

Cada ejecución genera o sobreescribe los siguientes archivos:

| Archivo | Descripción |
|---|---|
| `IA_Proyecto/data/telco.db` | Base de datos SQLite con tabla `clientes` |
| `IA_Proyecto/data/telco_limpio.csv` | Dataset procesado en CSV |
| `IA_Proyecto/modelo/modelo_churn.pkl` | Modelo Random Forest serializado |
| `IA_Proyecto/modelo/graficos/matriz_confusion.png` | Gráfico de matriz de confusión |
| `IA_Proyecto/modelo/graficos/curva_roc.png` | Gráfico de curva ROC |
| `IA_Proyecto/logs/pipeline.log` | Log detallado de todas las etapas |

---

## Etapas del pipeline

| Etapa | Módulo | Descripción |
|---|---|---|
| 1 · Ingestion | `ingestion/lectura_csv.py` | Lee `telco_raw.csv` y valida estructura básica |
| 2 · Procesamiento | `procesamiento/transformacion.py` | Limpia nulos, corrige tipos, elimina duplicados |
| 3 · Data Quality | `data_quality/validacion.py` | Verifica integridad y completitud del dataset |
| 4 · Carga | `carga/carga.py` | Persiste en SQLite (`telco.db`) y CSV de respaldo |
| 5 · Modelo IA | `modelo/` | Entrena Random Forest y calcula métricas completas |

---

## Métricas del modelo

El modelo entrenado es un **Random Forest** con `class_weight="balanced"` para compensar el desbalance de clases (73% No Churn / 26% Churn).

| Métrica | Valor |
|---|---|
| Accuracy | 0.7616 |
| Recall | 0.7366 |
| Precision | 0.5362 |
| F1 Score | 0.6206 |
| AUC-ROC | 0.8378 |
| **Gini** | **0.6755** |

> El índice Gini de **0.6755 supera el umbral de 0.60**, lo que indica un modelo con buena capacidad discriminativa para detectar clientes en riesgo de abandono.

---

## Notebooks de análisis

| Notebook | Contenido |
|---|---|
| `analisis_univariado_bivariado.ipynb` | EDA completo: estadísticas descriptivas, distribuciones, tasas de churn por variable, matriz de correlación |
| `metricas_telco.ipynb` | Comparación de 3 modelos (Regresión Logística, Árbol de Decisión, Random Forest) con métricas y curvas ROC/Gini |

Para ejecutarlos, abrir directamente en VS Code o Jupyter dentro del Codespace.

---

## Solución de problemas frecuentes

**Error: `ModuleNotFoundError`**
Asegurarse de usar `python3` y no el botón ▶ de VS Code:
```bash
python3 pipeline.py
```

**Error: `No module named pip`**
Instalar con pip3:
```bash
pip3 install -r requirements.txt
```

**El pipeline se detiene en Data Quality**
Revisar el log para ver qué validación falló:
```bash
cat IA_Proyecto/logs/pipeline.log
```
