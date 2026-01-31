import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Configuración de la página (Título y Layout)
st.set_page_config(layout="wide")

# Cargar datos
employee_data = pd.read_csv('employee_data.csv')

# --- Header & Logo ---
img = Image.open("syk.jpg")
st.image(img)

"""
# Dashboard de Análisis de Desempeño

Bienvenido al tablero de análisis de desempeño. Aquí podrá explorar los indicadores clave de los colaboradores, 
identificar fortalezas y áreas de oportunidad para mejorar el rendimiento y la calidad de los servicios.

---
"""

# --- Sidebar: Filtros Globales ---
st.sidebar.header("Filtros de Datos")

# 1. Filtro Género
genders = employee_data['gender'].unique().tolist()
# Agregamos una opción para seleccionar todos si se desea, o default al primero
selected_gender = st.sidebar.selectbox("Seleccionar Género:",
                                        options=genders)

# 2. Filtro Rango de Desempeño
min_score = int(employee_data["performance_score"].min())
max_score = int(employee_data["performance_score"].max())

selected_score_range = st.sidebar.slider(
    "Seleccionar Rango de Desempeño:",
    min_value=min_score,
    max_value=max_score,
    value=(min_score, max_score) # Tupla para rango
)

# 3. Filtro Estado Civil
marital_statuses = employee_data['marital_status'].unique().tolist()
selected_marital_status = st.sidebar.selectbox("Seleccionar Estado Civil:",
                                                options=marital_statuses)
# --- Visualizaciones Principales (Grid 2x2) ---

mask = (
    (employee_data['gender'] == selected_gender) &
    (employee_data['performance_score'] >= selected_score_range[0]) &
    (employee_data['performance_score'] <= selected_score_range[1]) &
    (employee_data['marital_status'] == selected_marital_status)
    )

    # Mostrar Datos en Bruto (Opcional, al final)
# --- Filtrado de Datos ---
# Creamos la máscara lógica
filtered_data = employee_data[mask]

with st.expander("Ver Datos Filtrados"):
    st.dataframe(filtered_data)

st.write("---")

# Primera Fila
c1, c2 = st.columns(2)
    
with c1:
#     st.subheader("Distribución de Puntajes de Desempeño")
    # Histograma de puntajes
    fig_hist = px.histogram(employee_data, x="performance_score", 
                            title="Histograma del Desempeño",
                            color_discrete_sequence=['#636EFA'])
    fig_hist.update_layout(bargap=0.2)
    st.plotly_chart(fig_hist)

with c2:
#     st.subheader("Promedio de Horas por Género")
    # Calculamos el promedio sobre los datos filtrados
    avg_work_hours = employee_data.groupby("gender")["average_work_hours"].mean().reset_index()
    fig_bar = px.bar(avg_work_hours, x="gender", y="average_work_hours", 
                        title="Horas Promedio trabajadas",
                        color="gender", 
                        text_auto='.2f')
    st.plotly_chart(fig_bar)

# Segunda Fila
c3, c4 = st.columns(2)

with c3:
#     st.subheader("Edad vs Salario")
    fig_scatter_age_salary = px.scatter(employee_data, x="age", y="salary", 
                                        color="gender", 
                                        title="Dispersión: Edad vs Salario",
                                        hover_data=['name_employee', 'position'])
    st.plotly_chart(fig_scatter_age_salary)

with c4:
#     st.subheader("Horas vs Desempeño")
    fig_scatter_perf_hours = px.scatter(employee_data, x="average_work_hours", y="performance_score", 
                                        color="gender",
                                        title="Relación: Horas Trabajadas vs Desempeño",
                                        size='salary', # Agregamos dimensión extra visual
                                        hover_data=['name_employee'])
    st.plotly_chart(fig_scatter_perf_hours)

    
# --- Conclusión ---

"""
---

## Conclusión del Análisis

**Observaciones Generales:**
1. La distribución de los puntajes de desempeño permite identificar rápidamente el grueso de la fuerza laboral y los empleados de alto/bajo rendimiento.
2. Al cruzar las horas trabajadas con el desempeño, se puede observar si trabajar más horas correlaciona con mejores calificaciones o si existe un punto de rendimiento decreciente.
3. La dispersión de Edad vs Salario ayuda a visualizar la equidad salarial y la proyección de carrera dentro de la empresa.
"""

        