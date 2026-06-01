# Telco Customer Churn — Pipeline DataOps

Pipeline de datos para el análisis y procesamiento del dataset
Telco Customer Churn, desarrollado como proyecto universitario
para la asignatura ITY1101 Gestión de Datos para IA — DuocUC 2025.

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

## Estructura del proyecto

```
Telco_Churn/
├── ingestion/
│   └── lectura_csv.py       # Etapa 1: carga y validación del CSV
├── procesamiento/
│   └── transformacion.py    # Etapa 2: limpieza y transformación
├── data_quality/
│   └── validacion.py        # Etapa 3: validación estructural y semántica
├── carga/
│   └── carga.py             # Etapa 4: carga en SQLite + CSV respaldo
├── IA_Proyecto/
│   ├── data/
│   │   ├── telco_raw.csv    # Dataset original
│   │   ├── telco_limpio.csv # Dataset procesado
│   │   └── telco.db         # Base de datos SQLite
│   └── logs/
│       └── pipeline.log     # Logs de ejecución
├── pipeline.py              # Orquestador principal
├── Dockerfile               # Contenedor Docker
├── requirements.txt         # Dependencias Python
└── .env.example             # Variables de entorno
```

---

## Pipeline DataOps

### Etapa 1 — Ingesta
Lee el CSV original y valida que tenga las 7.043 filas
y 21 columnas esperadas. Genera KPIs de tiempo y volumen.

### Etapa 2 — Limpieza y Transformación
- Imputa 11 valores vacíos en TotalCharges con MonthlyCharges
- Estandariza SeniorCitizen de 0/1 a No/Yes
- Elimina customerID (anonimización — Ley 21.719)
- Elimina filas duplicadas

### Etapa 3 — Validación Estructural y Semántica
- Verifica columnas requeridas
- Valida tipos de datos numéricos
- Valida valores permitidos en variables categóricas
- Verifica reglas de negocio (PhoneService/MultipleLines)
- Verifica rangos numéricos (tenure 0-72)

### Etapa 4 — Carga
- Inserta los datos limpios en base de datos SQLite
- Verifica completitud con SELECT COUNT(*)
- Genera CSV de respaldo
- Registra KPIs de carga

---

## Requisitos

- Docker instalado
- El archivo telco_raw.csv debe estar en IA_Proyecto/data/

---

## Ejecución con Docker

```bash
# 1. Clonar el repositorio
git clone https://github.com/Nicoherr/Telco_Churn.git
cd Telco_Churn

# 2. Construir la imagen
docker build -t telco-pipeline .

# 3. Ejecutar el pipeline
docker run telco-pipeline
```

## Ejecución sin Docker

```bash
pip install -r requirements.txt
python pipeline.py
```

---

## Resultado esperado

```
=======================================================
  PIPELINE DATAOPS — TELCO CUSTOMER CHURN
=======================================================

[1/4] Ingestion...
[OK] Ingesta: 7043 filas | 21 columnas | 0.02s

[2/4] Procesamiento...
[OK] Transformacion: 11 cambios | 0 nulos residuales | shape (7021, 20)

[3/4] Data Quality...
[OK] Validacion: todos los checks pasaron (0 errores)

[4/4] Carga...
   Conectando a base de datos SQLite...
[OK] Carga: 7021 filas insertadas en SQLite
   Completitud : 100.0%

=======================================================
  Pipeline completado en 0.14 segundos
=======================================================
```

---

## Seguridad

- customerID eliminado en etapa de transformación (Ley 21.719)
- Variables de entorno en .env (nunca subir al repositorio)
- Base de datos local sin exposición externa

---

## Tecnologías

| Herramienta | Uso |
|---|---|
| Python 3.11  | Lenguaje principal          |
| Pandas       | Limpieza y transformación   |
| SQLite       | Base de datos de carga      |
| Docker       | Contenedorización           |
| GitHub       | Control de versiones        |
