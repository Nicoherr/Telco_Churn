"""
pipeline.py — Orquestador principal
Pipeline DataOps: Telco Customer Churn
Ejecuta: Ingestion → Procesamiento → Data Quality → Carga → Modelo IA
Uso: python pipeline.py
"""

from modelo.metricas import evaluar
from modelo.entrenamiento import entrenar
from modelo.preparacion import preparar_datos
from carga.carga import cargar
from data_quality.validacion import validar
from procesamiento.transformacion import transformar
from ingestion.lectura_csv import leer_csv
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


def ejecutar():
    print("\n" + "=" * 55)
    print("  PIPELINE DATAOPS — TELCO CUSTOMER CHURN")
    print("=" * 55)

    inicio = datetime.now()
    logging.info("PIPELINE INICIADO")
    logging.info("=" * 60)

    # ── 1 · Ingestion ────────────────────────────────────────────────
    print("\n[1/5] Ingestion...")
    df_raw = leer_csv()

    # ── 2 · Procesamiento ────────────────────────────────────────────
    print("\n[2/5] Procesamiento...")
    df_procesado = transformar(df_raw)

    # ── 3 · Data Quality ─────────────────────────────────────────────
    print("\n[3/5] Data Quality...")
    ok = validar(df_procesado)

    if not ok:
        logging.error("PIPELINE DETENIDO — validacion fallida")
        print("\nPipeline detenido. Revisa IA_Proyecto/logs/pipeline.log")
        sys.exit(1)

    # ── 4 · Carga ────────────────────────────────────────────────────
    print("\n[4/5] Carga...")
    ok_carga = cargar(df_procesado)

    if not ok_carga:
        logging.error("PIPELINE DETENIDO — carga fallida")
        print("\nError en carga. Revisa IA_Proyecto/logs/pipeline.log")
        sys.exit(1)

    # ── 5 · Modelo IA ────────────────────────────────────────────────
    print("\n[5/5] Modelo IA...")

    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("IA_Proyecto/data/telco.db")
    df_modelo = pd.read_sql("SELECT * FROM clientes", conn)
    conn.close()
    logging.info("MODELO | Datos cargados desde telco.db")

    X_train, X_test, y_train, y_test = preparar_datos(df_modelo)
    modelo = entrenar(X_train, y_train)
    metricas = evaluar(modelo, X_test, y_test)

    logging.info(
        f"MODELO | Accuracy={metricas['accuracy']:.4f} | "
        f"Recall={metricas['recall']:.4f} | "
        f"Precision={metricas['precision']:.4f} | "
        f"F1={metricas['f1']:.4f} | "
        f"AUC={metricas['auc']:.4f} | "
        f"Gini={metricas['gini']:.4f}"
    )

    # ── Resumen final ─────────────────────────────────────────────────
    duracion = (datetime.now() - inicio).total_seconds()
    logging.info(f"PIPELINE COMPLETADO en {duracion:.2f}s")

    print("\n" + "=" * 55)
    print(f"  Pipeline completado en {duracion:.2f} segundos")
    print(f"  Base de datos : IA_Proyecto/data/telco.db")
    print(f"  CSV respaldo  : IA_Proyecto/data/telco_limpio.csv")
    print(f"  Modelo        : IA_Proyecto/modelo/modelo_churn.pkl")
    print(f"  Logs          : IA_Proyecto/logs/pipeline.log")
    print(f"  ─────────────────────────────────────────────")
    print(f"  Accuracy      : {metricas['accuracy']:.4f}")
    print(f"  Recall        : {metricas['recall']:.4f}")
    print(f"  Precision     : {metricas['precision']:.4f}")
    print(f"  F1 Score      : {metricas['f1']:.4f}")
    print(f"  AUC-ROC       : {metricas['auc']:.4f}")
    print(f"  Gini          : {metricas['gini']:.4f}")
    print(f"  Gráficos      : IA_Proyecto/modelo/graficos/")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    ejecutar()
