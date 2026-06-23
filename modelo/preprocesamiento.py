"""
preprocesamiento.py — Módulo de preparación de datos para ML
Convierte los datos limpios del pipeline en formato apto para
entrenar un modelo de machine learning.
"""

import pandas as pd
import logging
from sklearn.model_selection import train_test_split


def preprocesar(df: pd.DataFrame):
    """
    Prepara el DataFrame limpio para entrenamiento ML.
    - Aplica encoding a variables categóricas
    - Separa variable objetivo (Churn)
    - Divide en conjunto de entrenamiento y prueba

    Args:
        df (pd.DataFrame): datos limpios desde el pipeline

    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    logging.info("=" * 60)
    logging.info("INICIO PREPROCESAMIENTO: modelo ML")

    df = df.copy()

    # ── Paso 1: Convertir variable objetivo a binario ──────────────
    # Churn: Yes=1, No=0
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    logging.info("P1 | Churn convertido a binario (Yes=1, No=0)")

    # ── Paso 2: Separar X (variables entrada) e y (objetivo) ───────
    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    logging.info(f"P2 | Variables de entrada: {X.shape[1]} columnas")
    logging.info(f"P2 | Distribucion objetivo: {y.value_counts().to_dict()}")

    # ── Paso 3: Encoding de variables categóricas ───────────────────
    # pd.get_dummies convierte texto a columnas binarias 0/1
    X = pd.get_dummies(X, drop_first=True)
    logging.info(f"P3 | Encoding aplicado: {X.shape[1]} columnas resultantes")

    # ── Paso 4: Partición 80% entrenamiento / 20% prueba ───────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y        # mantiene proporcion 73/26% en ambos conjuntos
    )

    logging.info(f"P4 | Train: {len(X_train)} filas | Test: {len(X_test)} filas")
    logging.info(f"P4 | Stratify aplicado: proporcion churn preservada")
    logging.info("PREPROCESAMIENTO completado")

    print(f"[OK] Preprocesamiento: {X.shape[1]} variables | Train {len(X_train)} | Test {len(X_test)}")

    return X_train, X_test, y_train, y_test