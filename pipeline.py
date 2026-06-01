"""
pipeline.py — Orquestador principal
Pipeline DataOps: Telco Customer Churn
Ejecuta: Ingestion → Procesamiento → Data Quality → Carga
Uso: python pipeline.py
"""

import logging
import os
import sys
from datetime import datetime

os.makedirs("IA_Proyecto/logs", exist_ok=True)

logging.basicConfig(
    filename="IA_Proyecto/logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

from ingestion.lectura_csv       import leer_csv
from procesamiento.transformacion import transformar
from data_quality.validacion      import validar
from carga.carga                  import cargar          # ← nuevo


def ejecutar():
    print("\n" + "=" * 55)
    print("  PIPELINE DATAOPS — TELCO CUSTOMER CHURN")
    print("=" * 55)

    inicio = datetime.now()
    logging.info("PIPELINE INICIADO")
    logging.info("=" * 60)

    # 1 · Ingestion
    print("\n[1/4] Ingestion...")
    df_raw = leer_csv()

    # 2 · Procesamiento
    print("\n[2/4] Procesamiento...")
    df_procesado = transformar(df_raw)

    # 3 · Data Quality
    print("\n[3/4] Data Quality...")
    ok = validar(df_procesado)

    if not ok:
        logging.error("PIPELINE DETENIDO — validación fallida")
        print("\nPipeline detenido. Revisa IA_Proyecto/logs/pipeline.log")
        sys.exit(1)

    # 4 · Carga
    print("\n[4/4] Carga...")
    ok_carga = cargar(df_procesado)

    if not ok_carga:
        logging.error("PIPELINE DETENIDO — carga fallida")
        print("\nError en carga. Revisa IA_Proyecto/logs/pipeline.log")
        sys.exit(1)

    duracion = (datetime.now() - inicio).total_seconds()
    logging.info(f"PIPELINE COMPLETADO en {duracion:.2f}s")

    print("\n" + "=" * 55)
    print(f"  pipeline completado en {duracion:.2f} segundos")
    print(f"  Base de datos : IA_Proyecto/data/telco.db")
    print(f"  CSV respaldo  : IA_Proyecto/data/telco_limpio.csv")
    print(f"  Logs          : IA_Proyecto/logs/pipeline.log")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    ejecutar()