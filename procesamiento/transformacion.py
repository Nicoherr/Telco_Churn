
import pandas as pd
import logging


def transformar(df: pd.DataFrame) -> pd.DataFrame:

    logging.info("=" * 60)
    logging.info("INICIO PROCESAMIENTO: transformacion")

    df = df.copy()
    registros_modificados = 0

    # ── Transformación 1: Imputar TotalCharges ─────────────────────────────────
    # 11 clientes con tenure=0 tienen TotalCharges vacío
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    nulos = df["TotalCharges"].isna().sum()
    df.loc[df["TotalCharges"].isna(), "TotalCharges"] = \
        df.loc[df["TotalCharges"].isna(), "MonthlyCharges"]
    registros_modificados += nulos
    logging.info(f"T1 | TotalCharges: {nulos} valores imputados con MonthlyCharges")

    # ── Transformación 2: Estandarizar SeniorCitizen ───────────────────────────
    df["SeniorCitizen"] = df["SeniorCitizen"].map({0: "No", 1: "Yes"})
    logging.info("T2 | SeniorCitizen: convertido de 0/1 a No/Yes")

    # ── Transformación 3: Eliminar customerID (anonimización) ──────────────────
    df = df.drop(columns=["customerID"])
    logging.info("T3 | customerID eliminado (anonimización - Ley 21.719)")

    # ── Transformación 4: Eliminar duplicados ──────────────────────────────────
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        df = df.drop_duplicates()
        logging.warning(f"T4 | {duplicados} filas duplicadas eliminadas")
    else:
        logging.info("T4 | Sin duplicados detectados ")

    # ── KPIs de procesamiento ──────────────────────────────────────────────────
    nulos_restantes = df.isnull().sum().sum()
    logging.info(f"KPI | Registros modificados : {registros_modificados}")
    logging.info(f"KPI | Nulos residuales      : {nulos_restantes}")
    logging.info(f"KPI | Shape final           : {df.shape}")
    logging.info("PROCESAMIENTO completado")

    print(f"Transformación: {registros_modificados} cambios | {nulos_restantes} nulos residuales | shape {df.shape}")
    return df


if __name__ == "__main__":
    from ingestion.lectura_csv import leer_csv
    df_raw = leer_csv()
    df_transformado = transformar(df_raw)
    print(df_transformado.head())
