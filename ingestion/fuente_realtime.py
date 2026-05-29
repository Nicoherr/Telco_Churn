
import pandas as pd
import logging
from datetime import datetime


def leer_realtime(n_registros: int = 10) -> pd.DataFrame:

    logging.info("INGESTION realtime: simulando llegada de nuevos registros")

    from ingestion.lectura_csv import leer_csv
    df_full = leer_csv()
    df_stream = df_full.tail(n_registros).copy()

    logging.info(f"KPI | Registros recibidos en stream: {len(df_stream)}")
    print(f"✅ Stream simulado: {len(df_stream)} registros nuevos recibidos")
    return df_stream


if __name__ == "__main__":
    df = leer_realtime(5)
    print(df)
