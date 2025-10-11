import streamlit as st
import pandas as pd
import random
import plotly.express as px

st.set_page_config(page_title="Seguridad en Lima Metropolitana", page_icon="🛡️", layout="centered")

st.title("🛡️ Nivel de Seguridad en Lima Metropolitana")

# Distritos simulados
distritos = [
    "Lima Cercado", "Miraflores", "San Isidro", "La Molina", "Comas", "San Juan de Lurigancho",
    "San Martín de Porres", "Villa El Salvador", "Ate", "Surco", "Callao", "Los Olivos"
]

# Simulación de datos
data = {
    "Distrito": distritos,
    "Seguridad_2024": [random.randint(40, 80) for _ in distritos],
    "Seguridad_2025": [random.randint(50, 95) for _ in distritos]
}

df = pd.DataFrame(data)
df["Incremento (%)"] = ((df["Seguridad_2025"] - df["Seguridad_2024"]) / df["Seguridad_2024"] * 100).round(1)

# Selección del distrito
distrito_sel = st.selectbox("Selecciona un distrito:", distritos)

# Mostrar datos del distrito
fila = df[df["Distrito"] == distrito_sel].iloc[0]
st.metric(
    label=f"Índice de seguridad 2025 en {distrito_sel}",
    value=f"{fila['Seguridad_2025']}/100",
    delta=f"{fila['Incremento (%)']}%"
)

# Mostrar gráfico
fig = px.bar(
    df,
    x="Distrito",
    y="Incremento (%)",
    color="Incremento (%)",
    title="Incremento del nivel de seguridad por distrito (2024 → 2025)",
)
st.plotly_chart(fig, use_container_width=True)

st.caption("📊 Datos simulados — versión 
