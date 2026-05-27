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


def ejecutar():
    print("\n" + "=" * 55)
    print("  PIPELINE DATAOPS — TELCO CUSTOMER CHURN")
    print("=" * 55)

    inicio = datetime.now()
    logging.info("★ PIPELINE INICIADO")

    # 1 · Ingestion
    print("\n[1/3] Ingestion...")
    df_raw = leer_csv()

    # 2 · Procesamiento
    print("\n[2/3] Procesamiento...")
    df_procesado = transformar(df_raw)

    # 3 · Data Quality
    print("\n[3/3] Data Quality...")
    ok = validar(df_procesado)

    if not ok:
        logging.error("★ PIPELINE DETENIDO — validación fallida")
        print("\n❌ Pipeline detenido. Revisa IA_Proyecto/logs/pipeline.log")
        sys.exit(1)

    # Carga — guardar CSV limpio
    ruta_salida = "IA_Proyecto/data/telco_limpio.csv"
    df_procesado.to_csv(ruta_salida, index=False)
    logging.info(f"Datos cargados en: {ruta_salida}")

    duracion = (datetime.now() - inicio).total_seconds()
    logging.info(f"★ PIPELINE COMPLETADO en {duracion:.2f}s")

    print("\n" + "=" * 55)
    print(f"  ✅ Pipeline completado en {duracion:.2f} segundos")
    print(f"  📄 Datos limpios : IA_Proyecto/data/telco_limpio.csv")
    print(f"  📋 Logs          : IA_Proyecto/logs/pipeline.log")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    ejecutar()
