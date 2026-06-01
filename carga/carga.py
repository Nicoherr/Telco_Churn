"""
carga.py — Etapa 4 del Pipeline DataOps
Carga los datos limpios en una base de datos SQLite
y genera un CSV de respaldo.
"""

import sqlite3
import logging
import os
from datetime import datetime


def cargar(df):
    """
    Carga el DataFrame limpio en SQLite (tabla: clientes)
    y guarda un CSV de respaldo.

    Args:
        df (pd.DataFrame): datos validados listos para carga

    Returns:
        bool: True si la carga fue exitosa
    """
    logging.info("=" * 60)
    logging.info("INICIO CARGA: SQLite + CSV respaldo")

    print("   Conectando a base de datos SQLite...")  # ← agregar

    try:
        # ── Rutas de salida
        os.makedirs("IA_Proyecto/data", exist_ok=True)
        ruta_db = "IA_Proyecto/data/telco.db"
        ruta_csv = "IA_Proyecto/data/telco_limpio.csv"

        inicio = datetime.now()

        # ── Carga en SQLite
        conn = sqlite3.connect(ruta_db)
        df.to_sql("clientes", conn, if_exists="replace", index=False)

        # ── Verificación: contar filas cargadas
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes")
        filas_cargadas = cursor.fetchone()[0]
        conn.close()

        logging.info(
            f"C1 | SQLite: {filas_cargadas} filas insertadas en tabla 'clientes'")
        logging.info(f"C2 | Base de datos: {ruta_db}")

        # ── CSV de respaldo
        df.to_csv(ruta_csv, index=False)
        logging.info(f"C3 | CSV respaldo guardado en: {ruta_csv}")

        # ── KPI de carga
        duracion = (datetime.now() - inicio).total_seconds()
        completitud = (filas_cargadas / len(df)) * 100

        logging.info(f"KPI | Filas cargadas    : {filas_cargadas}/{len(df)}")
        logging.info(f"KPI | Completitud carga : {completitud:.1f}%")
        logging.info(f"KPI | Tiempo de carga   : {duracion:.3f}s")

        # ── Alerta si algo no cuadra
        if filas_cargadas != len(df):
            logging.warning(
                f"Discrepancia: se esperaban {len(df)} filas, se cargaron {filas_cargadas}")

        # ── Prints de resultado  ← agregar todo esto
        print(f"[OK] Carga: {filas_cargadas} filas insertadas en SQLite")
        print(f"   Base de datos : {ruta_db}")
        print(f"   CSV respaldo  : {ruta_csv}")
        print(f"   Completitud   : {completitud:.1f}%")
        print(f"   Tiempo        : {duracion:.3f}s")

        logging.info("CARGA completada")
        return True

        logging.info("CARGA completada ")
        return True

    except Exception as e:
        logging.error(f"Error en carga: {e}")
        return False
