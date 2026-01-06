import streamlit as st
import pandas as pd
import os

st.title("📊 Resultados de Evaluaciones 5S")

ARCH_EVAL = "evaluaciones_5s.csv"

# ---------- VALIDAR ARCHIVO ----------
if not os.path.exists(ARCH_EVAL):
    st.warning("Aún no existen evaluaciones registradas")
    st.stop()

df = pd.read_csv(ARCH_EVAL)

df["codigo_eval"] = df["codigo_eval"].astype(str)


# ---------- FILTROS ----------
st.subheader("🔎 Filtros")

col1, col2, col3 = st.columns(3)

with col1:
    codigo_filtro = st.text_input("Código de evaluación")

with col2:
    areas = ["Todos"] + sorted(df["area"].dropna().unique().tolist())
    area_filtro = st.selectbox("Área", areas)

with col3:
    responsable_filtro = st.text_input("Responsable")

# ---------- APLICAR FILTROS ----------
df_filtrado = df.copy()

if codigo_filtro:
    df_filtrado = df_filtrado[
        df_filtrado["codigo_eval"].str.contains(codigo_filtro, case=False)
    ]

if area_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["area"] == area_filtro]

if responsable_filtro:
    df_filtrado = df_filtrado[
        df_filtrado["responsable"].str.contains(responsable_filtro, case=False)
    ]

# ---------- RESULTADOS ----------
st.divider()
st.subheader("📋 Evaluaciones registradas")

# ---------- LIMPIAR TABLA ----------

if "confirmar_borrado_eval" not in st.session_state:
    st.session_state.confirmar_borrado_eval = False

if st.button("🧹 Limpiar todas las evaluaciones"):
    st.session_state.confirmar_borrado_eval = True

if st.session_state.confirmar_borrado_eval:
    st.warning(
        "⚠️ ¿Estás seguro de eliminar todas las evaluaciones?\n\n"
        "Esta acción no se puede deshacer."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("❌ Cancelar"):
            st.session_state.confirmar_borrado_eval = False
            st.rerun()

    with col2:
        if st.button("✅ Sí, eliminar"):
            df_vacio = df.iloc[0:0]   # mantiene columnas
            df_vacio.to_csv(ARCH_EVAL, index=False)

            st.success("Evaluaciones eliminadas correctamente")
            st.session_state.confirmar_borrado_eval = False
            st.rerun()



st.dataframe(df_filtrado, use_container_width=True,hide_index=True)

st.caption(f"Total de evaluaciones encontradas: {len(df_filtrado)}")
