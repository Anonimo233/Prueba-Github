import streamlit as st
import pandas as pd
import random

# Configuración general
st.set_page_config(page_title="Tecnología en Lima Metropolitana", page_icon="💻", layout="centered")

st.title("💻 Nivel de uso de tecnología en Lima Metropolitana")

st.markdown(
    """
    Esta aplicación muestra un análisis **simulado** del incremento en el uso de tecnología
    (por ejemplo: internet, dispositivos inteligentes, servicios digitales, etc.)
    en los distintos distritos de **Lima Metropolitana** entre 2024 y 2025.
    """
)

# Lista de distritos
distritos = [
    "Lima Cercado", "Miraflores", "San Isidro", "La Molina", "Comas",
    "San Juan de Lurigancho", "San Martín de Porres", "Villa El Salvador",
    "Ate", "Santiago de Surco", "Callao", "Los Olivos"
]

# Generar datos simulados
tec_2024 = [random.randint(30, 80) for _ in distritos]
tec_2025 = [min(t + random.randint(0, 20), 100) for t in tec_2024]  # no pasar de 100

# Crear DataFrame
df = pd.DataFrame({
    "Distrito": distritos,
    "Tecnología_2024": tec_2024,
    "Tecnología_2025": tec_2025
})

# Calcular incremento porcentual
df["Incremento (%)"] = ((df["Tecnología_2025"] - df["Tecnología_2024"]) / df["Tecnología_2024"] * 100).round(1)

# Selector de distrito
distrito_sel = st.selectbox("Selecciona un distrito para analizar:", df["Distrito"])

# Fila seleccionada
fila = df[df["Distrito"] == distrito_sel].iloc[0]

# Mostrar métrica
st.metric(
    label=f"Nivel tecnológico 2025 en {distrito_sel}",
    value=f"{fila['Tecnología_2025']}/100",
    delta=f"{fila['Incremento (%)']}%"
)

# --- Gráfico general ---
fig = px.bar(
    df,
    x="Distrito",
    y="Incremento (%)",
    color="Incremento (%)",
    title="Incremento del uso de tecnología por distrito (2024 → 2025)"
)

# Estilo del gráfico
fig.update_layout(
    xaxis_title="Distrito",
    yaxis_title="Incremento (%)",
    title_x=0.5,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Mostrar tabla con datos simulados
with st.expander("📋 Ver datos detallados por distrito"):
    st.dataframe(df, use_container_width=True)

st.caption("📊 Datos simulados — versión demostrativa para fines educativos")

