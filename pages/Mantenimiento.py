import streamlit as st
import pandas as pd
import os

st.title("⚙️ Mantenimiento de Indicadores 5S")

ARCHIVO = "indicadores_5s.csv"

S_OPCIONES = ["Seiri", "Seiton", "Seiso", "Seiketsu", "Shitsuke"]

# ---------- CARGAR ----------
if os.path.exists(ARCHIVO):
    df = pd.read_csv(ARCHIVO)
else:
    df = pd.DataFrame(columns=["id", "area", "s", "descripcion", "activo"])

# ---------- FORM NUEVO ----------
st.subheader("➕ Nuevo indicador")

with st.form("nuevo"):
    area = st.text_input("Área")
    s = st.selectbox("S", S_OPCIONES)
    descripcion = st.text_area("Descripción")
    guardar = st.form_submit_button("Guardar")

    if guardar:
        # AUTOINCREMENTO
        nuevo_id = int(df["id"].max() + 1) if not df.empty else 1

        df = pd.concat([
            df,
            pd.DataFrame([{
                "id": nuevo_id,
                "area": area,
                "s": s,
                "descripcion": descripcion,
                "activo": 1
            }])
        ], ignore_index=True)

        df.to_csv(ARCHIVO, index=False)
        st.success("Indicador guardado")
        st.rerun()

# ---------- SOLO ACTIVOS ----------
st.subheader("📋 Indicadores activos")
df_activos = df[df["activo"] == 1]

# ---------- SELECCIONAR ----------
id_sel = st.selectbox(
    "Seleccionar indicador (ID)",
    df_activos["id"] if not df_activos.empty else []
)

if id_sel:
    fila = df[df["id"] == id_sel].iloc[0]

    st.subheader("✏️ Editar / 🗑 Eliminar")

    area_e = st.text_input("Área", fila["area"])
    s_e = st.selectbox("S", S_OPCIONES, index=S_OPCIONES.index(fila["s"]))
    desc_e = st.text_area("Descripción", fila["descripcion"])

    col1, col2 = st.columns(2)

    # ---------- EDITAR ----------
    if col1.button("💾 Guardar cambios"):
        df.loc[df["id"] == id_sel, ["area", "s", "descripcion"]] = [
            area_e, s_e, desc_e
        ]
        df.to_csv(ARCHIVO, index=False)
        st.success("Indicador actualizado")
        st.rerun()

    # ---------- ELIMINAR LÓGICO ----------
    if col2.button("🗑 Eliminar"):
        df.loc[df["id"] == id_sel, "activo"] = 0
        df.to_csv(ARCHIVO, index=False)
        st.warning("Indicador desactivado")
        st.rerun()

# ---------- TABLA ----------
st.subheader("📊 Tabla visible (solo activos)")
st.dataframe(df_activos,hide_index=True)
