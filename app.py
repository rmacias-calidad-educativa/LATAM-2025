import streamlit as st
import pandas as pd
import numpy as np

# -------------------------
# Configuración de página
# -------------------------
st.set_page_config(
    page_title="Dashboard Cognitivas & HSE",
    layout="wide"
)

st.title("Dashboard Cognitivas & HSE")
st.markdown(
    "Este visualizador integra resultados de **pruebas cognitivas** y **HSE** "
    "por **año, sede, grado y área**, con foco en **MEDIDA_500** y **NIVEL_LOGRO_4**."
)

# -------------------------
# Carga de datos
# -------------------------
@st.cache_data
def load_data():
    # Ajusta los nombres si cambiaron en tu repo
    cog = pd.read_excel("data/Colombia_Latam-Cognitivas (2).xlsx")
    hse = pd.read_excel("data/Colombia_Latam_HSE (1).xlsx")

    # Origen de la prueba
    cog["FUENTE"] = "Cognitivas"
    hse["FUENTE"] = "HSE"

    # Unificar columnas (ambas tienen misma estructura base)
    df = pd.concat([cog, hse], ignore_index=True)

    # Asegurarnos de que MEDIDA_500 sea numérica
    df["MEDIDA_500"] = pd.to_numeric(df["MEDIDA_500"], errors="coerce")

    # Limpiar el sexo (quedarnos con F/M y tratar '.' como NaN)
    df["SEXO"] = df["SEXO"].replace(".", np.nan)

    return df

df = load_data()

# -------------------------
# Barra lateral: filtros
# -------------------------
st.sidebar.header("Filtros")

# Fuente (Cognitivas / HSE)
fuentes = st.sidebar.multiselect(
    "Tipo de prueba (fuente)",
    options=sorted(df["FUENTE"].dropna().unique()),
    default=sorted(df["FUENTE"].dropna().unique())
)

# Año (ANHO)
anhos = st.sidebar.multiselect(
    "Año / Periodo (ANHO)",
    options=sorted(df["ANHO"].dropna().unique()),
    default=sorted(df["ANHO"].dropna().unique())
)

# Sede
sedes = st.sidebar.multiselect(
    "Sede",
    options=sorted(df["SEDE"].dropna().unique()),
    default=sorted(df["SEDE"].dropna().unique())
)

# Grado
grados = st.sidebar.multiselect(
    "Grado",
    options=sorted(df["GRADO"].dropna().unique()),
    default=sorted(df["GRADO"].dropna().unique())
)

# Área
areas = st.sidebar.multiselect(
    "Área (COD_AREA)",
    options=sorted(df["COD_AREA"].dropna().unique()),
    default=sorted(df["COD_AREA"].dropna().unique())
)

# -------------------------
# Aplicar filtros
# -------------------------
mask = (
    df["FUENTE"].isin(fuentes) &
    df["ANHO"].isin(anhos) &
    df["SEDE"].isin(sedes) &
    df["GRADO"].isin(grados) &
    df["COD_AREA"].isin(areas)
)

df_f = df[mask].copy()

st.markdown(f"### Resultados filtrados ({len(df_f)} registros)")

if df_f.empty:
    st.warning("No hay datos para la combinación de filtros seleccionada.")
    st.stop()

# -------------------------
# Indicadores generales
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    n_students = df_f["CORREO"].nunique() if "CORREO" in df_f.columns else len(df_f)
    st.metric("Estudiantes (únicos)", n_students)

with col2:
    media_medida = df_f["MEDIDA_500"].mean()
    st.metric("Media MEDIDA_500", f"{media_medida:,.1f}")

with col3:
    desv_medida = df_f["MEDIDA_500"].std()
    if not np.isnan(desv_medida):
        st.metric("Desviación MEDIDA_500", f"{desv_medida:,.1f}")
    else:
        st.metric("Desviación MEDIDA_500", "N/A")

st.markdown("---")

# -------------------------
# MEDIDA_500 segmentado por sexo
# -------------------------
st.subheader("MEDIDA_500 segmentado por sexo")

df_sexo = df_f[df_f["SEXO"].isin(["F", "M"])].copy()

if df_sexo.empty:
    st.info("No hay datos con sexo definido (F/M) para los filtros actuales.")
else:
    # Agregar media y conteo por sexo
    medida_sexo = (
        df_sexo.groupby("SEXO")["MEDIDA_500"]
        .agg(media="mean", n="count")
        .sort_index()
    )

    st.write("**Media de MEDIDA_500 por sexo**")
    st.dataframe(medida_sexo)

    # Gráfica sencilla de barras
    st.bar_chart(medida_sexo["media"])

st.markdown("---")

# -------------------------
# Distribución de NIVEL_LOGRO_4
# -------------------------
st.subheader("Distribución de NIVEL_LOGRO_4")

niveles = (
    df_f["NIVEL_LOGRO_4"]
    .value_counts(dropna=False)
    .rename_axis("NIVEL_LOGRO_4")
    .to_frame("conteo")
)

niveles["porcentaje"] = (niveles["conteo"] / niveles["conteo"].sum()) * 100

st.write("**Tabla de niveles de logro (4 niveles / categorías HSE)**")
st.dataframe(niveles)

st.write("**Gráfica de conteos por NIVEL_LOGRO_4**")
st.bar_chart(niveles["conteo"])

# -------------------------
# Tabla detallada opcional
# -------------------------
with st.expander("Ver datos detallados (tabla)"):
    st.dataframe(
        df_f[
            [
                "FUENTE",
                "ANHO",
                "SEDE",
                "GRADO",
                "COD_AREA",
                "SEXO",
                "MEDIDA_500",
                "NIVEL_LOGRO_4"
            ]
        ]
    )
