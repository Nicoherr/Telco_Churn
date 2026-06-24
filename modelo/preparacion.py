"""
preparacion.py — Partición y preparación de datos para el modelo ML
Limpia columnas problemáticas, encodea categóricas y hace split train/test.
"""

import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def preparar_datos(df):
    """
    Prepara X e y desde el DataFrame limpio y hace split 80/20.

    Pasos:
        1. Drop de customerID (no aporta al modelo)
        2. TotalCharges → float (viene como string en el raw)
        3. Encode de columnas categóricas con LabelEncoder
        4. Encode de Churn: Yes=1, No=0
        5. Train/test split estratificado (80/20)

    Args:
        df: DataFrame cargado desde telco.db o desde el CSV limpio

    Returns:
        X_train, X_test, y_train, y_test
    """
    logging.info("=" * 60)
    logging.info("INICIO PREPARACION: limpieza y particion train/test")

    df = df.copy()

    # ── 1. Drop columnas no útiles ───────────────────────────────────
    if "customerID" in df.columns:
        df.drop(columns=["customerID"], inplace=True)
        logging.info("P1 | customerID eliminado")

    # ── 2. TotalCharges → float (espacios vacíos → NaN → media) ─────
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    nulos_tc = df["TotalCharges"].isna().sum()
    if nulos_tc > 0:
        media_tc = df["TotalCharges"].mean()
        df["TotalCharges"].fillna(media_tc, inplace=True)
        logging.info(
            f"P2 | TotalCharges: {nulos_tc} nulos imputados con media ({media_tc:.2f})")
    else:
        logging.info("P2 | TotalCharges: sin nulos, conversión a float OK")

    # ── 3. Encode target: Churn Yes=1, No=0 ─────────────────────────
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    logging.info("P3 | Churn encodado: Yes=1, No=0")

    # ── 4. Encode columnas categóricas restantes ─────────────────────
    columnas_cat = df.select_dtypes(include=["object"]).columns.tolist()
    columnas_cat = [c for c in columnas_cat if c != "Churn"]

    le = LabelEncoder()
    for col in columnas_cat:
        df[col] = le.fit_transform(df[col].astype(str))

    logging.info(
        f"P4 | Columnas encodadas ({len(columnas_cat)}): {columnas_cat}")

    # ── 5. Separar X e y ────────────────────────────────────────────
    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    # ── 6. Split estratificado 80/20 ────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y      # conserva proporción 73%/26% en train y test
    )

    logging.info(f"P5 | Total muestras : {len(df)}")
    logging.info(
        f"P6 | Train          : {len(X_train)} ({len(X_train)/len(df)*100:.1f}%)")
    logging.info(
        f"P7 | Test           : {len(X_test)} ({len(X_test)/len(df)*100:.1f}%)")
    logging.info(f"P8 | Features       : {X.shape[1]} variables")
    logging.info("PREPARACION completada")

    print(f"[OK] Preparacion: {len(df)} registros | {X.shape[1]} features")
    print(
        f"     Train: {len(X_train)} muestras | Test: {len(X_test)} muestras")

    return X_train, X_test, y_train, y_test
