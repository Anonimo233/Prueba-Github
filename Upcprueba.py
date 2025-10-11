import streamlit as st
import pandas as pd
import random

# Configuración de la página
st.set_page_config(page_title="Seguridad en Lima Metropolitana", page_icon="🛡️", layout="centered")

st.title("🛡️ Nivel de Seguridad en Lima Metropolitana")

# Lista de distritos
distritos = [
    "Lima Cercado", "Miraflores", "San Isidro", "La Molina", "Comas",
    "San Juan de Lurigancho", "San Martín de Porres", "Villa El Salvador",
    "Ate", "Santiago de Surco", "Callao", "Los Olivos"
]

# Generar datos simulados
seguridad_2024 = [random.randint(40, 80) for _ in distritos]
seguridad_2025 = [random.randint(50, 95) for _ in distritos]

# Crear DataFrame
df = pd.DataFrame({
    "Distrito": distritos,
    "Seguridad_2024": seguridad_2024,
    "Seguridad_2025": seguridad_2025
})

# Calcular incremento porcentual
df["Incremento (%)"] = ((df["Seguridad_2025"] - df["Seguridad_2024"]) / df["Seguridad_2024"] * 100).round(1)

# Selector de distrito
distrito_sel = st.selectbox("Selecciona un distrito:", df["Distrito"])

# Fila seleccionada
fila = df[df["Distrito"] == distrito_sel].iloc[0]

# Mostrar métrica
st.metric(
    label=f"Índice de seguridad 2025 en {distrito_sel}",
    value=f"{fila['Seguridad_2025']}/100",
    delta=f"{fila['Incremento (%)']}%"
)

# --- Gráfico general (sin color_continuous_scale para máxima compatibilidad) ---
fig = px.bar(
    df,
    x="Distrito",
    y="Incremento (%)",
    color="Incremento (%)",
    title="Incremento del nivel de seguridad por distrito (2024 → 2025)"
)

# Mejorar diseño visual
fig.update_layout(
    xaxis_title="Distrito",
    yaxis_title="Incremento (%)",
    title_x=0.5,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.caption("📊 Datos simulados — versión demostrativa")
