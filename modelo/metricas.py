"""
metricas.py — Módulo de evaluación del modelo ML
Calcula y guarda todas las métricas requeridas por la pauta:
matriz de confusión, accuracy, recall, precisión, F1, ROC y Gini.
"""

import logging
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    recall_score,
    precision_score,
    f1_score,
    roc_curve,
    roc_auc_score,
    classification_report
)


def evaluar(modelo, X_test, y_test):
    """
    Evalúa el modelo entrenado y genera todas las métricas.
    Guarda gráficos en IA_Proyecto/modelo/graficos/

    Args:
        modelo: modelo entrenado (RandomForestClassifier)
        X_test: variables de entrada para prueba
        y_test: variable objetivo real

    Returns:
        dict: diccionario con todas las métricas calculadas
    """
    logging.info("=" * 60)
    logging.info("INICIO METRICAS: evaluacion del modelo")

    os.makedirs("IA_Proyecto/modelo/graficos", exist_ok=True)

    # ── Predicciones ────────────────────────────────────────────────
    y_pred = modelo.predict(X_test)
    y_prob = modelo.predict_proba(X_test)[:, 1]

    # ── Métricas base ───────────────────────────────────────────────
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    gini = 2 * auc - 1

    logging.info(f"M1 | Accuracy  : {accuracy:.4f}")
    logging.info(f"M2 | Recall    : {recall:.4f}")
    logging.info(f"M3 | Precision : {precision:.4f}")
    logging.info(f"M4 | F1 Score  : {f1:.4f}")
    logging.info(f"M5 | AUC-ROC   : {auc:.4f}")
    logging.info(f"M6 | Gini      : {gini:.4f}")

    print(f"[OK] Metricas del modelo:")
    print(f"   Accuracy  : {accuracy:.4f}")
    print(f"   Recall    : {recall:.4f}")
    print(f"   Precision : {precision:.4f}")
    print(f"   F1 Score  : {f1:.4f}")
    print(f"   AUC-ROC   : {auc:.4f}")
    print(f"   Gini      : {gini:.4f}")

    # ── Gráfico 1: Matriz de confusión ──────────────────────────────
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["No Churn", "Churn"],
                yticklabels=["No Churn", "Churn"])
    plt.title("Matriz de Confusion")
    plt.ylabel("Real")
    plt.xlabel("Predicho")
    plt.tight_layout()
    plt.savefig("IA_Proyecto/modelo/graficos/matriz_confusion.png")
    plt.close()
    logging.info("G1 | Matriz de confusion guardada")

    # ── Gráfico 2: Curva ROC ────────────────────────────────────────
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    plt.figure(figsize=(6, 4))
    plt.plot(fpr, tpr, color="blue", label=f"AUC = {auc:.4f}")
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
    plt.title("Curva ROC")
    plt.xlabel("Tasa Falsos Positivos")
    plt.ylabel("Tasa Verdaderos Positivos")
    plt.legend()
    plt.tight_layout()
    plt.savefig("IA_Proyecto/modelo/graficos/curva_roc.png")
    plt.close()
    logging.info("G2 | Curva ROC guardada")

    logging.info("METRICAS completadas")

    return {
        "accuracy":  accuracy,
        "recall":    recall,
        "precision": precision,
        "f1":        f1,
        "auc":       auc,
        "gini":      gini
    }
