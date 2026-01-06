import streamlit as st
import pandas as pd
from datetime import date
import os

st.title("📝 Evaluación de las 5S")

ARCH_IND = "indicadores_5s.csv"
ARCH_EVAL = "evaluaciones_5s.csv"

# ---------- CARGAR INDICADORES ----------
if not os.path.exists(ARCH_IND):
    st.error("No existe indicadores_5s.csv")
    st.stop()

df_ind = pd.read_csv(ARCH_IND)
df_ind = df_ind[df_ind["activo"] == 1]

# ---------- DATOS GENERALES ----------
st.subheader("📋 Datos de la evaluación")

responsable = st.text_input("Responsable")
codigo = st.text_input("Código evaluación")
fecha = st.date_input("Fecha", date.today())

areas = sorted(df_ind["area"].unique())
area_sel = st.selectbox("Área", areas)

# ---------- FILTRAR POR ÁREA ----------
df_area = df_ind[df_ind["area"] == area_sel]

# ---------- CHECKLIST ----------
st.subheader("✔ Checklist 5S")

puntaje_total = 0
maximo = len(df_area)

puntaje_por_s = {}   # 👈 NUEVO

for s in df_area["s"].unique():
    st.markdown(f"### {s}")
    df_s = df_area[df_area["s"] == s]

    puntaje_por_s[s] = 0   # 👈 inicializar

    for _, fila in df_s.iterrows():
        marcado = st.checkbox(fila["descripcion"], key=f"ind_{fila['id']}")

        if marcado:
            puntaje_por_s[s] += 1
            puntaje_total += 1

# ---------- RESULTADOS ----------
st.divider()
st.subheader("📊 Resultados")

for s, puntos in puntaje_por_s.items():
    st.write(f"**{s}**: {puntos}")

st.metric("Puntaje total", f"{puntaje_total} / {maximo}")

# ---------- GUARDAR ----------
if st.button("💾 Guardar evaluación"):
    if not responsable or not codigo:
        st.error("Complete responsable y código")
    elif puntaje_total == 0:
        st.error("Debe marcar al menos un indicador")
    else:
        fila_eval = {
            "codigo_eval": codigo,
            "fecha": fecha,
            "responsable": responsable,
            "area": area_sel,
            "Seiri": puntaje_por_s.get("Seiri", 0),
            "Seiton": puntaje_por_s.get("Seiton", 0),
            "Seiso": puntaje_por_s.get("Seiso", 0),
            "Seiketsu": puntaje_por_s.get("Seiketsu", 0),
            "Shitsuke": puntaje_por_s.get("Shitsuke", 0),
            "puntaje_total": puntaje_total,
            "maximo": maximo
        }

        df_eval = pd.DataFrame([fila_eval])

        if os.path.exists(ARCH_EVAL):
            df_eval.to_csv(ARCH_EVAL, mode="a", header=False, index=False)
        else:
            df_eval.to_csv(ARCH_EVAL, index=False)

        st.success("✅ Evaluación guardada correctamente")
