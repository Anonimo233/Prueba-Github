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
    "Surquillo", "Barranco", "Magdalena del Mar", "Pueblo Libre", "Jesús María",
    "Lince", "San Borja", "Breña", "San Miguel"
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
# Asegurarse de que el cálculo no divida por cero si Nivel Tecnológico 2024 es 0 (poco probable aquí)
df["Incremento Relativo (%)"] = ((df["Incremento Absoluto"] / df["Nivel Tecnológico 2024"]) * 100).round(1)
df.loc[df["Nivel Tecnológico 2024"] == 0, "Incremento Relativo (%)"] = 0 # Manejar división por cero

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
              delta=f"{df['Incremento Relativo (%)'].mean():.1f}%")

st.write("---")

# --- VISUALIZACIÓN DE DATOS con st.bar_chart ---
st.header("📈 Comparativa Tecnológica por Distrito")

# st.bar_chart es más simple y toma directamente el DataFrame.
# Para comparar 2024 y 2025 por distrito, necesitamos configurar el DataFrame adecuadamente.
# Primero, ordenamos el DataFrame para que el gráfico tenga un orden lógico
df_chart = df.set_index("Distrito").sort_values(by="Nivel Tecnológico 2025", ascending=False)

# st.bar_chart tomará las columnas especificadas como barras para cada índice (Distrito)
st.bar_chart(df_chart[["Nivel Tecnológico 2024", "Nivel Tecnológico 2025"]], use_container_width=True)

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
            delta=f"{fila['Incremento Absoluto']}"
        )
    with col_d3:
        st.metric(
            label="Incremento Relativo",
            value=f"{fila['Incremento Relativo (%)']}%",
            delta=f"{fila['Incremento Relativo (%)']}%"
        )

    # Gráfico de progreso para el distrito seleccionado
    st.subheader(f"Progreso Tecnológico en {distrito_sel}")
    st.progress(int(fila['Nivel Tecnológico 2025']))
    st.caption(f"El nivel tecnológico de {distrito_sel} ha alcanzado un {fila['Nivel Tecnológico 2025']}% en 2025.")

st.write("---")

# --- TABLA DE DATOS COMPLETA ---
st.header("📋 Datos Completos")
st.write("Explora la tabla interactiva de todos los distritos.")

# Opciones de ordenamiento: queremos todas las columnas excepto "Distrito"
# Crear una lista con los nombres de las columnas que queremos permitir para ordenar
sortable_columns_options = [col for col in df.columns if col != "Distrito"]

# Determinar el índice predeterminado.
# Buscamos la posición de "Incremento Relativo (%)" en nuestra lista `sortable_columns_options`
try:
    default_sort_index = sortable_columns_options.index("Incremento Relativo (%)")
except ValueError:
    # Si por alguna razón no se encuentra, usamos la primera opción disponible
    default_sort_index = 0

sort_column = st.selectbox(
    "Ordenar por:",
    options=sortable_columns_options, # Aquí pasamos la lista de opciones para el selectbox
    index=default_sort_index         # Y aquí su índice predeterminado
)
sort_order = st.radio("Orden:", ("Ascendente", "Descendente"))

sorted_df = df.sort_values(by=sort_column, ascending=(sort_order == "Ascendente"))

st.dataframe(sorted_df, use_container_width=True)

# Puedes añadir un pie de página
st.write("---")
st.markdown("Desarrollado con ❤️ en Python y Streamlit")
