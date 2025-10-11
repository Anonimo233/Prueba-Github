import streamlit as st
import pandas as pd
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Tecnología en Lima Metropolitana", page_icon="💻", layout="wide")

st.title("💻 Monitoreo del Uso de Tecnología en Lima Metropolitana")

st.markdown(
    """
    Esta aplicación muestra un **análisis simulado** del nivel de uso de tecnología
    en los distritos de **Lima Metropolitana**.  
    Se compara el uso entre **2024 y 2025**, mostrando el incremento relativo
    en acceso a internet, digitalización y adopción de herramientas tecnológicas.
    """
)

# --- DATOS SIMULADOS ---
distritos = [
    "Lima Cercado", "Miraflores", "San Isidro", "La Molina", "Comas",
    "San Juan de Lurigancho", "San Martín de Porres", "Villa El Salvador",
    "Ate", "Santiago de Surco", "Callao", "Los Olivos"
]

tec_2024 = [random.randint(30, 80) for _ in distritos]
tec_2025 = [min(t + random.randint(5, 25), 100) for t in tec_2024]

df = pd.DataFrame({
    "Distrito": distritos,
    "Tecnología 2024": tec_2024,
    "Tecnología 2025": tec_2025
})

df["Incremento (%)"] = ((df["Tecnología 2025"] - df["Tecnología 2024"]) / df["Tecnología 2024"] * 100).round(1)

# --- MÉTRICAS GLOBALES ---
col1, col2, col3 = st.columns(3)
col1.metric("Promedio 2024", f"{df['Tecnología 2024'].mean():.1f}/100")
col2.metric("Promedio 2025", f"{df['Tecnología 2025'].mean():.1f}/100")
col3.metric("Incremento promedio", f"{df['Incremento (%)'].mean():.1f}%", delta_color="normal")

# --- SELECCIÓN DE DISTRITO ---
st.subheader("📍 Análisis por distrito")
distrito_sel = st.selectbox("Selecciona un distrito:", df["Distrito"])
fila = df[df["Distrito"] == distrito_sel].iloc[0]

st.metric(
    label=f"Nivel tecnológico en {distrito_sel} (2025)",
    value=f"{fila['Tecnología 2025']}/100",
    delta=f"{fila['Incremento (%)']}%"
)


# --- VISUALIZACIÓN GENERAL (versión estable sin errores) ---
import numpy as np
import pandas as pd

st.subheader("📊 Visualización general")

# Verificar tipos numéricos
df["Tecnología 2024"] = pd.to_numeric(df["Tecnología 2024"], errors="coerce").fillna(0)
df["Tecnología 2025"] = pd.to_numeric(df["Tecnología 2025"], errors="coerce").fillna(0)

# Crear posiciones numéricas para las barras
x = np.arange(len(df))
width = 0.35

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(10, 5))

# Dibujar las barras
ax.bar(x - width/2, df["Tecnología 2024"], width, label="2024", color="#1f77b4")
ax.bar(x + width/2, df["Tecnología 2025"], width, label="2025", color="#2ca02c")

# Etiquetas y formato
ax.set_xticks(x)
ax.set_xticklabels(df["Distrito"], rotation=45, ha="right", fontsize=9)
ax.set_ylabel("Nivel tecnológico (0 - 100)")
ax.set_title("Nivel tecnológico en distritos de Lima Metropolitana (2024 vs 2025)")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)

# Ajuste visual y render en Streamlit
plt.tight_layout()
st.pyplot(fig)

# Promedios e incremento
prom_2024 = df["Tecnología 2024"].mean()
prom_2025 = df["Tecnología 2025"].mean()
incremento = ((prom_2025 - prom_2024) / prom_2024) * 100 if prom_2024 != 0 else 0

# Texto debajo del gráfico
st.markdown(f"📈 **Incremento promedio general:** {incremento:.1f}% entre 2024 y 2025.")
st.markdown(f"💡 En promedio, los distritos mejoraron de **{prom_2024:.1f}/100** a **{prom_2025:.1f}/100**.")
