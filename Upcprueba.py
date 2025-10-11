import streamlit as st
import pandas as pd
import random
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Seguridad en Lima Metropolitana", page_icon="🛡️", layout="centered")

st.title("🛡️ Nivel de Seguridad en Lima Metropolitana")

# Lista de distritos
distritos = [
    "Lima Cercado", "Miraflores", "San Isidro", "La Molina", "Comas",
    "San Juan de Lurigancho", "San Martín de Porres", "Villa El Salvador",
    "Ate", "Santiago de Surco", "Callao", "Los Olivos"
]

# 🔹 Generar datos aleatorios
seg_2024 = [random.randint(40, 80) for _ in distritos]
seg_2025 = [random.randint(50, 95) for _ in distritos]

# Crear DataFrame
df = pd.DataFrame({
    "Distrito": distritos,
    "Seguridad_2024": seg_2024,
    "Seguridad_2025": seg_2025
})

# Calcular incremento (%)
df["Incremento (%)"] = ((df["Seguridad_2025"] - df["Seguridad_2024"]) / df["Seguridad_2024"] * 100).round(1)

# 🔹 Selector de distrito
distrito_sel = st.selectbox("Selecciona un distrito:", df["Distrito"])

# Buscar fila correspondiente
fila = df[df["Distrito"] == distrito_sel].iloc[0]

# Mostrar métrica
st.metric(
    label=f"Índice de seguridad 2025 en {distrito_sel}",
    value=f"{fila['Seguridad_2025']}/100",
    delta=f"{fila['Incremento (%)']}%"
)

# 🔹 Gráfico de barras
fig = px.bar(
    df,
    x="Distrito",
    y="Incremento (%)",
    color="Incremento (%)",
    color_continuous_scale="Blues",
    title="Incremento del nivel de seguridad por distrito (2024 → 2025)"
)
st.plotly_chart(fig, use_container_width=True)

# ✅ Línea corregida
st.caption("📊 Datos simulados — versión demostrativa")
