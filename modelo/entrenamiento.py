"""
entrenamiento.py — Módulo de entrenamiento del modelo ML
Entrena un modelo Random Forest para predecir churn
y guarda el modelo entrenado en disco.
"""

import logging
import os
import joblib
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier


def entrenar(X_train, y_train):
    """
    Entrena un modelo Random Forest con los datos de entrenamiento.
    Guarda el modelo entrenado en IA_Proyecto/modelo/modelo_churn.pkl

    Args:
        X_train: variables de entrada para entrenamiento
        y_train: variable objetivo para entrenamiento

    Returns:
        RandomForestClassifier: modelo entrenado
    """
    logging.info("=" * 60)
    logging.info("INICIO ENTRENAMIENTO: Random Forest")

    os.makedirs("IA_Proyecto/modelo", exist_ok=True)

    inicio = datetime.now()

    # ── Configuración del modelo ────────────────────────────────────
    # class_weight="balanced" compensa el desbalance 73/26% de churn
    modelo = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight="balanced",
        random_state=42
    )

    # ── Entrenamiento ───────────────────────────────────────────────
    modelo.fit(X_train, y_train)

    duracion = (datetime.now() - inicio).total_seconds()

    logging.info(f"E1 | Algoritmo      : Random Forest")
    logging.info(f"E2 | n_estimators   : 100 arboles")
    logging.info(f"E3 | max_depth      : 10")
    logging.info(f"E4 | class_weight   : balanced (desbalance 73/26%)")
    logging.info(f"E5 | Tiempo entreno : {duracion:.2f}s")

    # ── Guardar modelo entrenado ────────────────────────────────────
    ruta_modelo = "IA_Proyecto/modelo/modelo_churn.pkl"
    joblib.dump(modelo, ruta_modelo)
    logging.info(f"E6 | Modelo guardado en: {ruta_modelo}")
    logging.info("ENTRENAMIENTO completado")

    print(
        f"[OK] Entrenamiento: Random Forest | {len(X_train)} muestras | {duracion:.2f}s")

    return modelo
