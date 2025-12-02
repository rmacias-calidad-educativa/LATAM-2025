import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# ---------------------------------------------------
# Configuración de página
# ---------------------------------------------------
st.set_page_config(
    page_title="Resultados LATAM 2024-2025",
    layout="wide"
)

st.title("Resultados LATAM 2024-2025")
st.markdown(
    """
    Dashboard de resultados **LATAM 2024-2025**  
    Integra resultados de:
    - **Prueba Cognitiva**
    - **Prueba HSE (Habilidades socioemocionales)**
    """
)

# ---------------------------------------------------
# Colores estilo Innova Schools
# (aprox. azul, verde, naranja)
# ---------------------------------------------------
INNOVA_BLUE = "#00539B"
INNOVA_GREEN = "#7AB800"
INNOVA_ORANGE = "#FF9300"
INNOVA_PALETTE = [INNOVA_BLUE, INNOVA_GREEN, INNOVA_ORANGE]

# ---------------------------------------------------
# Carga de datos
# ---------------------------------------------------
@st.cache_data
def load_data():
    cog = pd.read_excel("data/Colombia_Latam-Cognitivas (2).xlsx")
    hse = pd.read_excel("data/Colombia_Latam_HSE (1).xlsx")

    cog["FUENTE"] = "Cognitivas"
    hse["FUENTE"] = "HSE"

    df = pd.concat([cog, hse], ignore_index=True)

    # MEDIDA_500 numérica
    df["MEDIDA_500"] = pd.to_numeric(df["MEDIDA_500"], errors="coerce")

    # Sexo: tratar "." como missing
    df["SEXO"] = df["SEXO"].replace(".", np.nan)

    # Mapear grados a texto ordenado
    grado_map = {
        "3": "Tercero", 3: "Tercero",
        "4": "Cuarto", 4: "Cuarto",
        "5": "Quinto", 5: "Quinto",
        "6": "Sexto", 6: "Sexto",
        "7": "Septimo", 7: "Septimo",
        "8": "Octavo", 8: "Octavo",
        "9": "Noveno", 9: "Noveno",
    }
    df["GRADO_LABEL"] = df["GRADO"].map(grado_map)
    df["GRADO_LABEL"] = df["GRADO_LABEL"].fillna(df["GRADO"].astype(str))

    # Orden de grados deseado
    grado_order = [
        "Tercero", "Cuarto", "Quinto",
        "Sexto", "Septimo", "Octavo", "Noveno"
    ]
    # Añadir otros grados si existen
    all_grados = sorted(df["GRADO_LABEL"].dropna().unique().tolist())
    others = [g for g in all_grados if g not in grado_order]
    grado_categories = grado_order + others

    df["GRADO_LABEL"] = pd.Categorical(
        df["GRADO_LABEL"],
        categories=grado_categories,
        ordered=True
    )

    return df, grado_categories

df, GRADO_CATEGORIES = load_data()

# ---------------------------------------------------
# Función común para cada hoja (Cognitiva / HSE)
# ---------------------------------------------------
def show_tab_for_fuente(df_global, fuente, grado_categories, key_prefix):
    df_src = df_global[df_global["FUENTE"] == fuente].copy()

    if df_src.empty:
        st.warning(f"No hay datos para la fuente: {fuente}")
        return

    st.markdown(f"### { 'Prueba Cognitiva' if fuente=='Cognitivas' else 'Prueba HSE (Habilidades socioemocionales)' }")

    # -------------------------
    # Filtros (selección única con botones)
    # -------------------------
    st.markdown("#### Filtros")

    col1, col2, col3 = st.columns(3)

    # Año
    with col1:
        anos = sorted(df_src["ANHO"].dropna().unique().tolist())
        opciones_ano = ["Todos"] + anos
        ano_sel = st.radio(
            "Año / periodo",
            options=opciones_ano,
            index=len(opciones_ano) - 1 if anos else 0,  # por defecto el último año
            key=f"{key_prefix}_ano",
            horizontal=True
        )

    # Sede
    with col2:
        sedes = sorted(df_src["SEDE"].dropna().unique().tolist())
        opciones_sede = ["Todas"] + sedes
        sede_sel = st.radio(
            "Sede",
            options=opciones_sede,
            key=f"{key_prefix}_sede",
            horizontal=True
        )

    # Área
    with col3:
        areas = sorted(df_src["COD_AREA"].dropna().unique().tolist())
        opciones_area = ["Todas"] + areas
        area_sel = st.radio(
            "Área",
            options=opciones_area,
            key=f"{key_prefix}_area",
            horizontal=True
        )

    # Grado (último filtro, como pediste)
    grado_opts = ["Todos"] + [
        g for g in grado_categories
        if g in df_src["GRADO_LABEL"].astype(str).unique()
    ]
    grado_sel = st.radio(
        "Grado",
        options=grado_opts,
        key=f"{key_prefix}_grado",
        horizontal=True
    )

    # -------------------------
    # Aplicar filtros
    # -------------------------
    df_f = df_src.copy()

    if ano_sel != "Todos":
        df_f = df_f[df_f["ANHO"] == ano_sel]
    if sede_sel != "Todas":
        df_f = df_f[df_f["SEDE"] == sede_sel]
    if area_sel != "Todas":
        df_f = df_f[df_f["COD_AREA"] == area_sel]
    if grado_sel != "Todos":
        df_f = df_f[df_f["GRADO_LABEL"].astype(str) == grado_sel]

    st.markdown(f"**Registros filtrados:** {len(df_f)}")

    if df_f.empty:
        st.warning("No hay datos para la combinación de filtros seleccionada.")
        return

    # -------------------------
    # KPIs
    # -------------------------
    colk1, colk2, colk3, colk4 = st.columns(4)

    with colk1:
        n_est = df_f["CORREO"].nunique() if "CORREO" in df_f.columns else len(df_f)
        st.metric("Estudiantes únicos", n_est)

    with colk2:
        n_sedes = df_f["SEDE"].nunique()
        st.metric("Sedes", n_sedes)

    with colk3:
        media_medida = df_f["MEDIDA_500"].mean()
        st.metric("Media MEDIDA_500", f"{media_medida:,.1f}")

    with colk4:
        desv_medida = df_f["MEDIDA_500"].std()
        st.metric(
            "Desviación MEDIDA_500",
            f"{desv_medida:,.1f}" if not np.isnan(desv_medida) else "N/A"
        )

    st.markdown("---")

    # -------------------------
    # MEDIDA_500 segmentado por sexo y grado
    # -------------------------
    st.subheader("MEDIDA_500 por sexo y grado")

    df_sexo = df_f[df_f["SEXO"].isin(["F", "M"])].copy()

    if df_sexo.empty:
        st.info("No hay datos con sexo definido (F/M) para los filtros actuales.")
    else:
        # Tabla resumen
        resumen_sexo = (
            df_sexo.groupby(["GRADO_LABEL", "SEXO"])["MEDIDA_500"]
            .mean()
            .reset_index(name="MEDIDA_500_MEDIA")
        )

        col_a, col_b = st.columns([1, 2])

        with col_a:
            st.write("**Tabla de medias por grado y sexo**")
            st.dataframe(resumen_sexo)

        # Gráfica Altair
        with col_b:
            chart_sexo = (
                alt.Chart(resumen_sexo)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "GRADO_LABEL:N",
                        sort=grado_categories,
                        title="Grado"
                    ),
                    y=alt.Y(
                        "MEDIDA_500_MEDIA:Q",
                        title="Media MEDIDA_500"
                    ),
                    color=alt.Color(
                        "SEXO:N",
                        title="Sexo",
                        scale=alt.Scale(
                            domain=["F", "M"],
                            range=[INNOVA_ORANGE, INNOVA_BLUE]
                        )
                    ),
                    tooltip=[
                        "GRADO_LABEL:N",
                        "SEXO:N",
                        alt.Tooltip("MEDIDA_500_MEDIA:Q", format=".1f")
                    ]
                )
                .properties(height=300)
            )
            st.altair_chart(chart_sexo, use_container_width=True)

    st.markdown("---")

    # -------------------------
    # Distribución de NIVEL_LOGRO_4 (global)
    # -------------------------
    st.subheader("Distribución de NIVEL_LOGRO_4")

    niveles = (
        df_f["NIVEL_LOGRO_4"]
        .value_counts(dropna=False)
        .reset_index()
    )
    niveles.columns = ["NIVEL_LOGRO_4", "conteo"]
    niveles["porcentaje"] = niveles["conteo"] / niveles["conteo"].sum() * 100

    col_n1, col_n2 = st.columns([1, 2])

    with col_n1:
        st.write("**Tabla de niveles de logro**")
        st.dataframe(niveles)

    with col_n2:
        chart_niveles = (
            alt.Chart(niveles)
            .mark_bar()
            .encode(
                x=alt.X("NIVEL_LOGRO_4:N", title="Nivel de logro"),
                y=alt.Y("conteo:Q", title="Número de estudiantes"),
                color=alt.Color(
                    "NIVEL_LOGRO_4:N",
                    scale=alt.Scale(range=INNOVA_PALETTE),
                    title="Nivel de logro"
                ),
                tooltip=[
                    "NIVEL_LOGRO_4:N",
                    "conteo:Q",
                    alt.Tooltip("porcentaje:Q", format=".1f")
                ]
            )
            .properties(height=300)
        )
        st.altair_chart(chart_niveles, use_container_width=True)

    st.markdown("---")

    # -------------------------
    # NIVEL_LOGRO_4 por grado
    # -------------------------
    st.subheader("NIVEL_LOGRO_4 por grado")

    tabla_ng = (
        df_f
        .groupby(["GRADO_LABEL", "NIVEL_LOGRO_4"])
        .size()
        .reset_index(name="conteo")
    )

    if tabla_ng.empty:
        st.info("No hay datos para mostrar NIVEL_LOGRO_4 por grado.")
    else:
        st.write("**Tabla (GRADO x NIVEL_LOGRO_4)**")
        st.dataframe(tabla_ng)

        chart_ng = (
            alt.Chart(tabla_ng)
            .mark_bar()
            .encode(
                x=alt.X(
                    "GRADO_LABEL:N",
                    sort=grado_categories,
                    title="Grado"
                ),
                y=alt.Y("conteo:Q", title="Número de estudiantes"),
                color=alt.Color(
                    "NIVEL_LOGRO_4:N",
                    scale=alt.Scale(range=INNOVA_PALETTE),
                    title="Nivel de logro"
                ),
                tooltip=[
                    "GRADO_LABEL:N",
                    "NIVEL_LOGRO_4:N",
                    "conteo:Q"
                ]
            )
            .properties(height=320)
        )
        st.altair_chart(chart_ng, use_container_width=True)

    # -------------------------
    # Tabla de detalle (opcional)
    # -------------------------
    with st.expander("Ver tabla de detalle"):
        st.dataframe(
            df_f[
                [
                    "FUENTE",
                    "ANHO",
                    "SEDE",
                    "GRADO_LABEL",
                    "COD_AREA",
                    "SEXO",
                    "MEDIDA_500",
                    "NIVEL_LOGRO_4"
                ]
            ]
        )

# ---------------------------------------------------
# Tabs: una hoja para cada tipo de prueba
# ---------------------------------------------------
tab_cog, tab_hse = st.tabs([
    "Prueba Cognitiva",
    "Prueba HSE (Habilidades socioemocionales)"
])

with tab_cog:
    show_tab_for_fuente(df, "Cognitivas", GRADO_CATEGORIES, key_prefix="cog")

with tab_hse:
    show_tab_for_fuente(df, "HSE", GRADO_CATEGORIES, key_prefix="hse")
