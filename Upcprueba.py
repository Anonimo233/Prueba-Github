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
st.write("---") # Separador visual

# --- DATOS SIMULADOS ---
distritos = [
    "Lima Cercado", "Miraflores", "San Isidro", "La Molina", "Comas",
    "San Juan de Lurigancho", "San Martín de Porres", "Villa El Salvador",
    "Ate", "Santiago de Surco", "Callao", "Los Olivos", "Chorrillos",
    "Surquillo", "Barranco", "Magdalena del Mar", "Pueblo Libre", "Jesús María"
]
# Aseguramos que los valores no superen 100 y haya un incremento razonable
tec_2024 = [random.randint(30, 80) for _ in distritos]
tec_2025 = [min(t + random.randint(5, 25), 100) for t in tec_2024]

df = pd.DataFrame({
    "Distrito": distritos,
    "Nivel Tecnológico 2024": tec_2024,
    "Nivel Tecnológico 2025": tec_2025
})

df["Incremento Absoluto"] = df["Nivel Tecnológico 2025"] - df["Nivel Tecnológico 2024"]
df["Incremento Relativo (%)"] = ((df["Incremento Absoluto"] / df["Nivel Tecnológico 2024"]) * 100).round(1)

# --- MÉTRICAS GLOBALES ---
st.header("📊 Resumen General")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Promedio 2024", f"{df['Nivel Tecnológico 2024'].mean():.1f}/100")
    st.progress(df['Nivel Tecnológico 2024'].mean() / 100)
with col2:
    st.metric("Promedio 2025", f"{df['Nivel Tecnológico 2025'].mean():.1f}/100")
    st.progress(df['Nivel Tecnológico 2025'].mean() / 100)
with col3:
    st.metric("Incremento Promedio", f"{df['Incremento Relativo (%)'].mean():.1f}%",
              delta=f"{df['Incremento Relativo (%)'].mean():.1f}%", delta_color="normal")

st.write("---")

# --- VISUALIZACIÓN DE DATOS ---
st.header("📈 Comparativa Tecnológica por Distrito")

# Gráfico de barras interactivo
fig = px.bar(
    df.sort_values(by="Nivel Tecnológico 2025", ascending=False), # Ordenar para mejor visualización
    x="Distrito",
    y=["Nivel Tecnológico 2024", "Nivel Tecnológico 2025"],
    title="Nivel de Uso de Tecnología (2024 vs 2025)",
    labels={"value": "Nivel Tecnológico (/100)", "variable": "Año"},
    barmode="group",
    height=500,
    color_discrete_map={"Nivel Tecnológico 2024": "#636EFA", "Nivel Tecnológico 2025": "#EF553B"}
)
st.plotly_chart(fig, use_container_width=True)

st.write("---")

# --- ANÁLISIS POR DISTRITO ---
st.header("🔍 Análisis Detallado por Distrito")
distrito_sel = st.selectbox("Selecciona un distrito para ver su evolución:", df["Distrito"])

if distrito_sel:
    fila = df[df["Distrito"] == distrito_sel].iloc[0]

    st.subheader(f"Datos para {distrito_sel}")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.metric(
            label="Nivel Tecnológico 2024",
            value=f"{fila['Nivel Tecnológico 2024']}/100"
        )
    with col_d2:
        st.metric(
            label="Nivel Tecnológico 2025",
            value=f"{fila['Nivel Tecnológico 2025']}/100",
            delta=f"{fila['Incremento Absoluto']}" # Mostrar el incremento absoluto en el delta
        )
    with col_d3:
        st.metric(
            label="Incremento Relativo",
            value=f"{fila['Incremento Relativo (%)']}%",
            delta=f"{fila['Incremento Relativo (%)']}%", delta_color="normal"
        )

    # Gráfico de progreso para el distrito seleccionado
    st.subheader(f"Progreso Tecnológico en {distrito_sel}")
    st.progress(int(fila['Nivel Tecnológico 2025'])) # El progress bar va de 0 a 100 por defecto
    st.caption(f"El nivel tecnológico de {distrito_sel} ha alcanzado un {fila['Nivel Tecnológico 2025']}% en 2025.")

st.write("---")

# --- TABLA DE DATOS COMPLETA ---
st.header("📋 Datos Completos")
st.write("Explora la tabla interactiva de todos los distritos.")

# Opciones de ordenamiento
sort_column = st.selectbox(
    "Ordenar por:",
    df.columns[1:], # Excluir "Distrito" del ordenamiento inicial si quieres
    index=df.columns.get_loc("Incremento Relativo (%)")
)
sort_order = st.radio("Orden:", ("Ascendente", "Descendente"))

sorted_df = df.sort_values(by=sort_column, ascending=(sort_order == "Ascendente"))

st.dataframe(sorted_df, use_container_width=True)

# Puedes añadir una imagen o un pie de página
st.write("---")
st.markdown("Desarrollado con ❤️ en Python y Streamlit")

# Para que el modelo de imagen no falle
