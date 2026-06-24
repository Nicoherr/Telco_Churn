"""
Dashboard BI — Telco Customer Churn
ITY1101 — Gestión de Datos para IA | Evaluación Parcial N°3
Herramienta: Streamlit
Uso: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, recall_score, precision_score, f1_score,
    confusion_matrix, roc_curve, roc_auc_score, ConfusionMatrixDisplay
)

import warnings
warnings.filterwarnings('ignore')

# ── Configuración de la página ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Telco Churn",
    page_icon="📊",
    layout="wide"
)

# ── Título principal ───────────────────────────────────────────────────────────
st.title("📊 Dashboard BI — Telco Customer Churn")
st.markdown("**ITY1101 — Gestión de Datos para IA | Evaluación Parcial N°3**")
st.markdown("---")

# ── Cargar datos ───────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    ruta = '/Users/nicolasherrera/Telco_Churn/IA_Proyecto/data/telco_limpio.csv'
    df = pd.read_csv(ruta)
    return df

@st.cache_data
def entrenar_modelos(df):
    df_ml = df.copy()
    le = LabelEncoder()
    for col in df_ml.select_dtypes(include=['object']).columns:
        df_ml[col] = le.fit_transform(df_ml[col])

    X = df_ml.drop('Churn', axis=1)
    y = df_ml['Churn']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    lr = LogisticRegression(max_iter=1000, random_state=42)
    dt = DecisionTreeClassifier(max_depth=5, random_state=42)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)

    lr.fit(X_train_s, y_train)
    dt.fit(X_train, y_train)
    rf.fit(X_train, y_train)

    return {
        'X_test': X_test, 'X_test_s': X_test_s, 'y_test': y_test,
        'modelos': {
            'Regresión Logística': (lr, X_test_s),
            'Árbol de Decisión':   (dt, X_test),
            'Random Forest':       (rf, X_test),
        }
    }

# ── Cargar datos y entrenar ────────────────────────────────────────────────────
try:
    df = cargar_datos()
    datos = entrenar_modelos(df)
    y_test = datos['y_test']
    modelos = datos['modelos']
except Exception as e:
    st.error(f"❌ Error cargando datos: {e}")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — KPIs generales
# ══════════════════════════════════════════════════════════════════════════════
st.header("📋 Resumen del Dataset")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total clientes", f"{len(df):,}")
with col2:
    churn_si = (df['Churn'] == 'Yes').sum()
    st.metric("Clientes con Churn", f"{churn_si:,}")
with col3:
    tasa = churn_si / len(df) * 100
    st.metric("Tasa de Churn", f"{tasa:.1f}%")
with col4:
    st.metric("Variables", f"{df.shape[1]}")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — Distribución de Churn
# ══════════════════════════════════════════════════════════════════════════════
st.header("📊 Análisis Exploratorio")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de Churn")
    fig, ax = plt.subplots(figsize=(5, 4))
    counts = df['Churn'].value_counts()
    colors = ['#2ecc71', '#e74c3c']
    bars = ax.bar(counts.index, counts.values, color=colors, alpha=0.85)
    ax.set_xlabel('Churn')
    ax.set_ylabel('Cantidad de clientes')
    for bar, val in zip(bars, counts.values):
        pct = val / len(df) * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                f'{val}\n({pct:.1f}%)', ha='center', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("Churn por Tipo de Contrato")
    fig, ax = plt.subplots(figsize=(5, 4))
    contrato = df.groupby('Contract')['Churn'].apply(
        lambda x: (x == 'Yes').sum() / len(x) * 100
    )
    bars = ax.bar(contrato.index, contrato.values,
                  color=['#e74c3c', '#f39c12', '#2ecc71'], alpha=0.85)
    ax.set_ylabel('Tasa de Churn (%)')
    for bar, val in zip(bars, contrato.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.1f}%', ha='center', fontweight='bold')
    plt.xticks(rotation=10)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — Métricas de los modelos
# ══════════════════════════════════════════════════════════════════════════════
st.header("🤖 Rendimiento de Modelos de IA")

# Calcular métricas
filas = []
for nombre, (modelo, X) in modelos.items():
    y_pred = modelo.predict(X)
    y_prob = modelo.predict_proba(X)[:, 1]
    auc    = roc_auc_score(y_test, y_prob)
    filas.append({
        'Modelo':     nombre,
        'Accuracy':   f"{accuracy_score(y_test, y_pred):.2%}",
        'Recall':     f"{recall_score(y_test, y_pred):.2%}",
        'Precisión':  f"{precision_score(y_test, y_pred):.2%}",
        'F1 Score':   f"{f1_score(y_test, y_pred):.4f}",
        'AUC':        f"{auc:.4f}",
        'Gini':       f"{2*auc-1:.4f}",
    })

df_metricas = pd.DataFrame(filas)
st.dataframe(df_metricas, use_container_width=True, hide_index=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — Selector de modelo
# ══════════════════════════════════════════════════════════════════════════════
st.header("🔍 Análisis Detallado por Modelo")

modelo_sel = st.selectbox(
    "Selecciona un modelo para ver su análisis:",
    list(modelos.keys())
)

modelo_obj, X_sel = modelos[modelo_sel]
y_pred_sel = modelo_obj.predict(X_sel)
y_prob_sel = modelo_obj.predict_proba(X_sel)[:, 1]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Matriz de Confusión")
    fig, ax = plt.subplots(figsize=(5, 4))
    cm = confusion_matrix(y_test, y_pred_sel)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                   display_labels=['No Churn', 'Churn'])
    disp.plot(ax=ax, colorbar=False, cmap='Blues')
    ax.set_title(f'{modelo_sel}\nAccuracy: {accuracy_score(y_test, y_pred_sel):.2%}',
                 fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("Curva ROC")
    fig, ax = plt.subplots(figsize=(5, 4))
    fpr, tpr, _ = roc_curve(y_test, y_prob_sel)
    auc_val = roc_auc_score(y_test, y_prob_sel)
    gini_val = 2 * auc_val - 1
    ax.plot(fpr, tpr, color='#3498db', linewidth=2,
            label=f'AUC = {auc_val:.3f} | Gini = {gini_val:.3f}')
    ax.plot([0,1],[0,1], 'k--', linewidth=1, label='Modelo aleatorio')
    ax.set_xlabel('Tasa Falsos Positivos')
    ax.set_ylabel('Tasa Verdaderos Positivos')
    ax.set_title('Curva ROC', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# KPIs del modelo seleccionado
st.subheader(f"📊 KPIs — {modelo_sel}")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Accuracy",  f"{accuracy_score(y_test, y_pred_sel):.2%}")
c2.metric("Recall",    f"{recall_score(y_test, y_pred_sel):.2%}")
c3.metric("Precisión", f"{precision_score(y_test, y_pred_sel):.2%}")
c4.metric("F1 Score",  f"{f1_score(y_test, y_pred_sel):.4f}")
c5.metric("Gini",      f"{2*roc_auc_score(y_test, y_prob_sel)-1:.4f}")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5 — Seguridad
# ══════════════════════════════════════════════════════════════════════════════
st.header("🔐 Auditoría de Seguridad")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Datos Sensibles Identificados")
    datos_sensibles = {
        'Campo': ['gender', 'SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'PaymentMethod'],
        'Tipo': ['Dato personal', 'Dato sensible', 'Dato financiero', 'Dato financiero', 'Dato financiero'],
        'Medida': ['Anonimizar', 'Controlar acceso', 'Cifrar', 'Cifrar', 'Cifrar']
    }
    st.dataframe(pd.DataFrame(datos_sensibles), use_container_width=True, hide_index=True)

with col2:
    st.subheader("Medidas de Seguridad Implementadas")
    st.success("✅ customerID eliminado (Ley 21.719 — Minimización)")
    st.success("✅ Credenciales en .env (no versionado en GitHub)")
    st.success("✅ Logs de auditoría en pipeline.log")
    st.info("⚠️ Cifrado AES-256 pendiente (próximo paso)")
    st.info("⚠️ Control de roles pendiente (próximo paso)")

st.markdown("---")
st.caption("Dashboard desarrollado con Streamlit | ITY1101 Gestión de Datos para IA | DuocUC 2025")
