import streamlit as st
import pandas as pd
import numpy as np

# -------------------------
# Configuración de página
# -------------------------
st.set_page_config(
    page_title="Dashboard MEDIDA_500 & NIVEL_LOGRO_4",
    layout="wide"
)

st.title("Dashboard MEDIDA_500 & NIVEL_LOGRO_4")
st.markdown(
    """
    Visualizador integrado de resultados **Cognitivos** y **HSE**  
    Filtra por **año, sede, grado y área** y analiza:
    - **MEDIDA_500** segmentado por **sexo**  
    - Distribución de **NIVEL_LOGRO_4**
    """
)

# -------------------------
# Carga de datos
# -------------------------
@st.cache_data
def load_data():
    # Ajusta rutas/nombres si cambian
    cog = pd.read_excel("data/Colombia_Latam-Cognitivas (2).xlsx")
    hse = pd.read_excel("data/Colombia_Latam_HSE (1).xlsx")

    cog["FUENTE"] = "Cognitivas"
    hse["FUENTE"] = "HSE"

    df = pd.concat([cog, hse], ignore_index=True)

    # Asegurar tipo numérico
    df["MEDIDA_500"] = pd.to_numeric(df["MEDIDA_500"], errors="coerce")

    # Tratar '.' en SEXO como missing
    df["SEXO"] = df["SEXO"].replace(".", np.nan)

    return df

df = load_data()

# -------------------------
# Filtros en barra lateral
# -------------------------
st.sidebar.header("Filtros")

fuentes = st.sidebar.multiselect(
    "Tipo de prueba",
    options=sorted(df["FUENTE"].dropna().unique()),
    default=sorted(df["FUENTE"].dropna().unique())
)

anhos = st.sidebar.multiselect(
    "Año / Periodo (ANHO)",
    options=sorted(df["ANHO"].dropna().unique()),
    default=sorted(df["ANHO"].dropna().unique())
)

sedes = st.sidebar.multiselect(
    "Sede",
    options=sorted(df["SEDE"].dropna().unique()),
    default=sorted(df["SEDE"].dropna().unique())
)

grados = st.sidebar.multiselect(
    "Grado",
    options=sorted(df["GRADO"].dropna().unique()),
    default=sorted(df["GRADO"].dropna().unique())
)

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

st.markdown(f"### Datos filtrados ({len(df_f)} registros)")

if df_f.empty:
    st.warning("No hay datos para la combinación de filtros seleccionada.")
    st.stop()

# -------------------------
# KPIs básicos
# -------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    n_est = df_f["CORREO"].nunique() if "CORREO" in df_f.columns else len(df_f)
    st.metric("Estudiantes únicos", n_est)

with col2:
    n_sedes = df_f["SEDE"].nunique()
    st.metric("Sedes", n_sedes)

with col3:
    media_medida = df_f["MEDIDA_500"].mean()
    st.metric("Media MEDIDA_500", f"{media_medida:,.1f}")

with col4:
    desv_medida = df_f["MEDIDA_500"].std()
    st.metric("Desviación MEDIDA_500",
              f"{desv_medida:,.1f}" if not np.isnan(desv_medida) else "N/A")

st.markdown("---")

# -------------------------
# MEDIDA_500 segmentado por sexo
# -------------------------
st.subheader("MEDIDA_500 segmentado por sexo")

df_sexo = df_f[df_f["SEXO"].isin(["F", "M"])].copy()

if df_sexo.empty:
    st.info("No hay datos con sexo definido (F/M) para los filtros actuales.")
else:
    medida_sexo = (
        df_sexo
        .groupby("SEXO")["MEDIDA_500"]
        .agg(media="mean", n="count")
        .sort_index()
    )

    col_a, col_b = st.columns([1, 2])

    with col_a:
        st.write("**Media de MEDIDA_500 por sexo**")
        st.dataframe(medida_sexo)

    with col_b:
        st.write("**Gráfica de MEDIDA_500 por sexo**")
        st.bar_chart(medida_sexo["media"])

st.markdown("---")

# -------------------------
# Distribución de NIVEL_LOGRO_4 (global)
# -------------------------
st.subheader("Distribución de NIVEL_LOGRO_4 (global)")

niveles = (
    df_f["NIVEL_LOGRO_4"]
    .value_counts(dropna=False)
    .rename_axis("NIVEL_LOGRO_4")
    .to_frame("conteo")
)

niveles["porcentaje"] = (niveles["conteo"] / niveles["conteo"].sum()) * 100

col_t1, col_t2 = st.columns([1, 2])

with col_t1:
    st.write("**Tabla de niveles de logro**")
    st.dataframe(niveles)

with col_t2:
    st.write("**Conteos por NIVEL_LOGRO_4**")
    st.bar_chart(niveles["conteo"])

st.markdown("---")

# -------------------------
# NIVEL_LOGRO_4 por grado (para más detalle)
# -------------------------
st.subheader("NIVEL_LOGRO_4 por grado")

tabla_ng = (
    df_f
    .groupby(["GRADO", "NIVEL_LOGRO_4"])
    .size()
    .reset_index(name="conteo")
)

if tabla_ng.empty:
    st.info("No hay datos para mostrar NIVEL_LOGRO_4 por grado.")
else:
    # Pivotear a formato ancho para gráfica
    pivot_ng = tabla_ng.pivot(
        index="GRADO",
        columns="NIVEL_LOGRO_4",
        values="conteo"
    ).fillna(0)

    st.write("**Tabla (GRADO x NIVEL_LOGRO_4)**")
    st.dataframe(pivot_ng)

    st.write("**Gráfica (barras por grado)** – cada barra es el total de estudiantes por nivel de logro en ese grado")
    st.bar_chart(pivot_ng)

# -------------------------
# Tabla de detalle
# -------------------------
with st.expander("Ver tabla de detalle"):
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
