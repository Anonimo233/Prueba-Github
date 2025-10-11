import streamlit as st
import pandas as pd
import random
import plotly.express as px

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

# --- VISUALIZACIONES ---
st.subheader("📊 Visualización general")

# Gráfico de barras comparativo
fig_bar = px.bar(
    df.melt(id_vars="Distrito", value_vars=["Tecnología 2024", "Tecnología 2025"], var_name="Año", value_name="Nivel"),
    x="Distrito",
    y="Nivel",
    color="Año",
    barmode="group",
    title="Comparativa del nivel tecnológico 2024 vs 2025 por distrito"
)
fig_bar.update_layout(title_x=0.5, template="plotly_white")

# Gráfico circular (promedios)
fig_pie = px.pie(
    names=["Tecnología 2024", "Tecnología 2025"],
    values=[df["Tecnología 2024"].mean(), df["Tecnología 2025"].mean()],
    title="Promedio general de tecnología (2024 vs 2025)",
    color_discrete_sequence=px.colors.sequential.Teal
)
fig_pie.update_traces(textinfo="label+percent", pull=[0, 0.1])

# Mostrar gráficos lado a lado
col_g1, col_g2 = st.columns(2)
col_g1.plotly_chart(fig_bar, use_container_width=True)
col_g2.plotly_chart(fig_pie, use_container_width=True)

# --- DATOS DETALLADOS ---
with st.expander("📋 Ver tabla de datos simulados"):
    st.dataframe(df, use_container_width=True)

st.caption("📊 Datos simulados — versión demostrativa educativa")

