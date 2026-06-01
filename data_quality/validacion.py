
import pandas as pd
import logging

COLUMNAS_REQUERIDAS = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
    "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
    "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
    "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
    "MonthlyCharges", "TotalCharges", "Churn"
]

VALORES_VALIDOS = {
    "gender":          {"Male", "Female"},
    "SeniorCitizen":   {"No", "Yes"},
    "Partner":         {"No", "Yes"},
    "Dependents":      {"No", "Yes"},
    "PhoneService":    {"No", "Yes"},
    "InternetService": {"DSL", "Fiber optic", "No"},
    "Contract":        {"Month-to-month", "One year", "Two year"},
    "Churn":           {"No", "Yes"},
}


def validar(df: pd.DataFrame) -> bool:
    """Ejecuta validación estructural y semántica completa."""

    logging.info("=" * 60)
    logging.info("INICIO DATA QUALITY: validacion")
    errores = 0

    # ── Validación estructural ─────────────────────────────────────────────────
    logging.info("── Validación estructural")

    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]
    if faltantes:
        logging.error(f"FALLA: Columnas faltantes: {faltantes}")
        errores += 1
    else:
        logging.info("Todas las columnas requeridas presentes")

    nulos = df.isnull().sum().sum()
    if nulos > 0:
        logging.error(f"FALLA: {nulos} valores nulos residuales")
        errores += 1
    else:
        logging.info("Sin valores nulos")

    for col in ["MonthlyCharges", "TotalCharges", "tenure"]:
        if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
            logging.error(f"FALLA: {col} debería ser numérico")
            errores += 1
        else:
            logging.info(f"{col} es numérico")

    # ── Validación semántica ───────────────────────────────────────────────────
    logging.info("── Validación semántica")

    for col, valores in VALORES_VALIDOS.items():
        if col in df.columns:
            invalidos = ~df[col].isin(valores)
            if invalidos.any():
                logging.error(f"FALLA: {col} tiene {invalidos.sum()} valores inválidos")
                errores += 1
            else:
                logging.info(f"{col}: valores válidos")

    # Regla: PhoneService=No → MultipleLines="No phone service"
    r2 = df[(df["PhoneService"] == "No") & (df["MultipleLines"] != "No phone service")]
    if len(r2) > 0:
        logging.error(f"FALLA: {len(r2)} inconsistencias PhoneService/MultipleLines")
        errores += 1
    else:
        logging.info("Regla PhoneService/MultipleLines consistente")

    # Regla: tenure entre 0 y 72
    fuera = df[(df["tenure"] < 0) | (df["tenure"] > 72)]
    if len(fuera) > 0:
        logging.error(f"FALLA: {len(fuera)} registros con tenure fuera de rango")
        errores += 1
    else:
        logging.info("tenure dentro de rango [0, 72]")

    logging.info(f"KPI | Total errores de validación: {errores}")

    if errores == 0:
        logging.info("DATA QUALITY completada  — datos aptos para carga")
        print("Validación: todos los checks pasaron (0 errores)")
    else:
        logging.error(f"DATA QUALITY FALLIDA — {errores} errores detectados")
        print(f" Validación fallida: {errores} errores — revisar logs/pipeline.log")

    return errores == 0
