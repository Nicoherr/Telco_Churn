
import pandas as pd
import logging
import os
from datetime import datetime

os.makedirs("IA_Proyecto/logs", exist_ok=True)
logging.basicConfig(
    filename="IA_Proyecto/logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

RUTA_CSV = "IA_Proyecto/data/telco_raw.csv"
FILAS_ESPERADAS = 7043
COLUMNAS_ESPERADAS = 21


def leer_csv(ruta: str = RUTA_CSV) -> pd.DataFrame:
    """Carga el CSV y valida volumen y estructura."""

    logging.info("=" * 60)
    logging.info("INICIO INGESTION: lectura_csv")
    logging.info(f"Fuente: {ruta}")

    if not os.path.exists(ruta):
        logging.error(f"Archivo no encontrado: {ruta}")
        raise FileNotFoundError(f"No se encontró: {ruta}")

    inicio = datetime.now()
    df = pd.read_csv(ruta)
    duracion = (datetime.now() - inicio).total_seconds()

    # KPIs de ingesta
    logging.info(
        f"KPI | Filas cargadas   : {len(df)} (esperadas: {FILAS_ESPERADAS})")
    logging.info(
        f"KPI | Columnas cargadas: {len(df.columns)} (esperadas: {COLUMNAS_ESPERADAS})")
    logging.info(f"KPI | Tiempo de carga  : {duracion:.2f}s")

    if len(df) != FILAS_ESPERADAS:
        logging.warning(f"ALERTA: filas inesperadas ({len(df)})")

    logging.info("INGESTION completada ")
    print(
        f" Ingesta: {len(df)} filas | {len(df.columns)} columnas | {duracion:.2f}s")
    return df


if __name__ == "__main__":
    df = leer_csv()
    print(df.head())
