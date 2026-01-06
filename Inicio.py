import streamlit as st

st.set_page_config(
    page_title="Sistema 5S",
    layout="centered"
)

# ---------- ENCABEZADO ----------
st.markdown(
    """
    <h1 style='text-align: center;'>📋 Sistema de Evaluación 5S</h1>
    <p style='text-align: center; font-size: 18px;'>
        Mejora continua • Orden • Disciplina
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------- DESCRIPCIÓN ----------
st.markdown(
    """
    ### 🔎 ¿Qué permite este sistema?

    ✔️ Realizar evaluaciones del método **5S** por área  
    ✔️ Calcular puntajes de forma automática  
    ✔️ Consultar evaluaciones registradas  
    ✔️ Administrar indicadores y criterios  

    ---
    """
)

# ---------- GUÍA DE USO ----------
st.markdown(
    """
    ### 🧭 ¿Cómo empezar?

    1️⃣ **Evaluación 5S** → Realiza una nueva evaluación  
    2️⃣ **Resultados** → Consulta evaluaciones anteriores  
    3️⃣ **Mantenimiento** → Administra indicadores y áreas  

    """
)

