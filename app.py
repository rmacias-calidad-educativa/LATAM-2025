import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import unicodedata

# ---------------------------------------------------
# Configuración de página y estilos (fondo negro, texto blanco)
# ---------------------------------------------------
st.set_page_config(
    page_title="Resultados LATAM 2024-2025",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    h1, h2, h3, h4, h5, h6, label {
        color: #FFFFFF !important;
    }
    p, span, div, li {
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo Innova (base64)
LOGO_BASE64 = "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"

st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
        <img src="data:image/png;base64,{LOGO_BASE64}" width="80">
        <h1 style="margin-bottom:0;">Resultados LATAM 2024-2025</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Colores Innova
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

    df_local = pd.concat([cog, hse], ignore_index=True)

    df_local["MEDIDA_500"] = pd.to_numeric(df_local["MEDIDA_500"], errors="coerce")
    df_local["SEXO"] = df_local["SEXO"].replace(".", np.nan)

    # Grados -> etiquetas ordenadas
    grado_map = {
        "3": "Tercero", 3: "Tercero",
        "4": "Cuarto", 4: "Cuarto",
        "5": "Quinto", 5: "Quinto",
        "6": "Sexto", 6: "Sexto",
        "7": "Séptimo", 7: "Séptimo",
        "8": "Octavo", 8: "Octavo",
        "9": "Noveno", 9: "Noveno",
    }
    df_local["GRADO_LABEL"] = df_local["GRADO"].map(grado_map)
    df_local["GRADO_LABEL"] = df_local["GRADO_LABEL"].fillna(df_local["GRADO"].astype(str))

    grado_order = ["Tercero", "Cuarto", "Quinto", "Sexto", "Séptimo", "Octavo", "Noveno"]
    all_grados = sorted(df_local["GRADO_LABEL"].dropna().unique().tolist())
    others = [g for g in all_grados if g not in grado_order]
    grado_categories = grado_order + others

    df_local["GRADO_LABEL"] = pd.Categorical(
        df_local["GRADO_LABEL"],
        categories=grado_categories,
        ordered=True
    )

    return df_local, grado_categories

df, GRADO_CATEGORIES = load_data()

# ---------------------------------------------------
# MEDIDA_500 por sexo y grado (F = Femenino, M = Masculino)
# ---------------------------------------------------
def plot_medida_por_sexo(df_f, grado_categories):
    st.subheader("MEDIDA_500 por sexo y grado")

    df_sexo = df_f[df_f["SEXO"].isin(["F", "M"])].copy()
    if df_sexo.empty:
        st.info("No hay datos con sexo definido (F/M) para los filtros actuales.")
        return

    # Media por grado y sexo
    resumen = (
        df_sexo.groupby(["GRADO_LABEL", "SEXO"])["MEDIDA_500"]
        .mean()
        .reset_index(name="MEDIDA_500_MEDIA")
    )
    resumen["Sexo"] = resumen["SEXO"].map({"F": "Femenino", "M": "Masculino"})

    st.write("**Media de MEDIDA_500 por grado y sexo (F = Femenino, M = Masculino)**")

    # 1 parte tabla, 3 partes gráfica
    col_tab, col_chart = st.columns([1, 3])

    with col_tab:
        st.dataframe(resumen[["GRADO_LABEL", "Sexo", "MEDIDA_500_MEDIA"]])

    # Base del gráfico: barras agrupadas por sexo dentro de cada grado
    base = alt.Chart(resumen).properties(height=380)

    bar = base.mark_bar().encode(
        x=alt.X("GRADO_LABEL:N", sort=grado_categories, title="Grado"),
        # barras agrupadas: una por sexo dentro de cada grado
        xOffset=alt.XOffset("Sexo:N"),
        y=alt.Y("MEDIDA_500_MEDIA:Q", title="Media MEDIDA_500"),
        color=alt.Color(
            "Sexo:N",
            scale=alt.Scale(
                domain=["Femenino", "Masculino"],
                range=[INNOVA_ORANGE, INNOVA_BLUE],
            ),
            title="Sexo",
        ),
        tooltip=[
            "GRADO_LABEL:N",
            "Sexo:N",
            alt.Tooltip("MEDIDA_500_MEDIA:Q", format=".1f"),
        ],
    )

    # Etiquetas con la media sobre cada barra
    text = base.mark_text(dy=-10, color="white").encode(
        x=alt.X("GRADO_LABEL:N", sort=grado_categories),
        xOffset=alt.XOffset("Sexo:N"),
        y="MEDIDA_500_MEDIA:Q",
        text=alt.Text("MEDIDA_500_MEDIA:Q", format=".1f"),
    )

    chart = alt.layer(bar, text)

    with col_chart:
        st.altair_chart(chart, use_container_width=True)

# ---------------------------------------------------
# Cognitivas: niveles (dona + proporciones por grado)
# ---------------------------------------------------
def plot_niveles_cognitivos(df_f, grado_categories):
    st.subheader("NIVEL_LOGRO_4 – Prueba Cognitiva")

    # Orden fijo de niveles
    niveles_order = ["Inicial", "Básico", "Satisfactorio", "Avanzado"]

    # ------------------ DONA GLOBAL ------------------
    counts = df_f["NIVEL_LOGRO_4"].value_counts().reindex(niveles_order, fill_value=0)
    total = counts.sum()

    niveles = pd.DataFrame({"NIVEL_LOGRO_4": niveles_order, "conteo": counts.values})
    if total > 0:
        niveles["proporcion"] = niveles["conteo"] / total
    else:
        niveles["proporcion"] = 0.0
    niveles["porcentaje"] = niveles["proporcion"] * 100

    col_t1, col_t2 = st.columns([1, 2])

    with col_t1:
        st.write("**Proporción de estudiantes por nivel de logro**")
        tabla = niveles.copy()
        tabla["porcentaje"] = tabla["porcentaje"].round(1).astype(str) + "%"
        st.dataframe(tabla[["NIVEL_LOGRO_4", "conteo", "porcentaje"]])

    # paleta incremental de azules (Inicial → Avanzado)
    palette_cog = ["#BBDEFB", "#64B5F6", "#1E88E5", "#0D47A1"]

    with col_t2:
        chart = (
            alt.Chart(niveles)
            .mark_arc(innerRadius=60)
            .encode(
                theta=alt.Theta("proporcion:Q"),
                color=alt.Color(
                    "NIVEL_LOGRO_4:N",
                    scale=alt.Scale(domain=niveles_order, range=palette_cog),
                    title="Nivel de logro",
                ),
                tooltip=[
                    "NIVEL_LOGRO_4:N",
                    alt.Tooltip("proporcion:Q", format=".1%"),
                    "conteo:Q",
                ],
            )
            .properties(height=300)
        )
        st.altair_chart(chart, use_container_width=True)

    # ------------------ BARRAS POR GRADO ------------------
    st.markdown("### NIVEL_LOGRO_4 por grado (proporción en cada grado)")

    # Conteo por grado y nivel
    tabla_ng = (
        df_f.groupby(["GRADO_LABEL", "NIVEL_LOGRO_4"])
        .size()
        .reset_index(name="conteo")
    )

    if tabla_ng.empty:
        st.info("No hay datos para mostrar NIVEL_LOGRO_4 por grado.")
        return

    # Asegurarnos de tener TODAS las combinaciones grado x nivel
    grados_presentes = (
        df_f["GRADO_LABEL"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    grados_presentes = [g for g in grado_categories if g in grados_presentes]

    grid = pd.MultiIndex.from_product(
        [grados_presentes, niveles_order],
        names=["GRADO_LABEL", "NIVEL_LOGRO_4"]
    ).to_frame(index=False)

    tabla_ng = grid.merge(tabla_ng, on=["GRADO_LABEL", "NIVEL_LOGRO_4"], how="left")
    tabla_ng["conteo"] = tabla_ng["conteo"].fillna(0)

    # Totales por grado
    totales_grado = (
        df_f.groupby("GRADO_LABEL")
        .size()
        .reset_index(name="n_grado")
    )
    tabla_ng = tabla_ng.merge(totales_grado, on="GRADO_LABEL", how="left")

    # Proporción y porcentaje
    tabla_ng["proporcion"] = np.where(
        tabla_ng["n_grado"] > 0,
        tabla_ng["conteo"] / tabla_ng["n_grado"],
        0.0,
    )
    tabla_ng["porcentaje"] = tabla_ng["proporcion"] * 100

    st.write("**Proporción por grado y nivel (en %)**")
    tabla_mostrar = tabla_ng.copy()
    tabla_mostrar["porcentaje"] = tabla_mostrar["porcentaje"].round(1).astype(str) + "%"
    st.dataframe(
        tabla_mostrar[["GRADO_LABEL", "NIVEL_LOGRO_4", "conteo", "porcentaje"]]
    )

    # Base del gráfico (barras DESAGREGADAS, no apiladas)
    base = alt.Chart(tabla_ng).properties(height=320)

    chart_ng = (
        base.mark_bar()
        .encode(
            x=alt.X(
                "GRADO_LABEL:N",
                sort=grado_categories,
                title="Grado",
            ),
            # barras desagregadas por nivel dentro de cada grado (en ORDEN fijo)
            xOffset=alt.XOffset(
                "NIVEL_LOGRO_4:N",
                scale=alt.Scale(domain=niveles_order),
            ),
            y=alt.Y(
                "proporcion:Q",
                title="Proporción de estudiantes",
                axis=alt.Axis(format="%", tickCount=6),
                scale=alt.Scale(domain=[0, 1])  # SIEMPRE 0% a 100%
            ),
            color=alt.Color(
                "NIVEL_LOGRO_4:N",
                scale=alt.Scale(domain=niveles_order, range=palette_cog),
                title="Nivel de logro",
            ),
            tooltip=[
                "GRADO_LABEL:N",
                "NIVEL_LOGRO_4:N",
                alt.Tooltip("proporcion:Q", format=".1%"),
                "conteo:Q",
            ],
        )
    )

    # Etiquetas con % sobre cada barra
    text_ng = (
        base.mark_text(dy=-5, color="white")
        .encode(
            x=alt.X(
                "GRADO_LABEL:N",
                sort=grado_categories,
            ),
            xOffset=alt.XOffset(
                "NIVEL_LOGRO_4:N",
                scale=alt.Scale(domain=niveles_order),
            ),
            y="proporcion:Q",
            text=alt.Text("proporcion:Q", format=".0%"),
            detail="NIVEL_LOGRO_4:N",
        )
    )

    st.altair_chart(chart_ng + text_ng, use_container_width=True)

# ---------------------------------------------------
# HSE: niveles por prueba (proporciones)
# ---------------------------------------------------
def plot_niveles_hse(df_f, area_sel):
    st.subheader("NIVEL_LOGRO_4 – Prueba HSE")

    # --- Normalización básica para evitar problemas de tildes/mayúsculas/espacios ---
    def norm(s):
        if pd.isna(s):
            return None
        s = str(s).strip()
        s = unicodedata.normalize("NFKD", s)
        s = "".join(c for c in s if not unicodedata.combining(c))
        return s.lower()

    df_hse = df_f.copy()
    df_hse["nivel_norm"] = df_hse["NIVEL_LOGRO_4"].apply(norm)
    area_norm = norm(area_sel)

    # Orden y mapa por prueba, tal como definiste
    if area_norm == "conciencia social":
        niveles_order = [
            "Egocéntricos",
            "Normativos",
            "Empáticos",
            "Empáticos Compasivos",
        ]
        # mapeo desde forma normalizada a etiqueta bonita
        map_norm_to_label = {
            "egocentricos": "Egocéntricos",
            "normativos": "Normativos",
            "empaticos": "Empáticos",
            "empaticos compasivos": "Empáticos Compasivos",
            "empaticos_compasivos": "Empáticos Compasivos",
        }
        palette = ["#FFF3E0", "#FFE0B2", "#FFB74D", "#FB8C00"]
    elif area_norm == "relaciones interpersonales":
        niveles_order = [
            "Disruptivo",
            "Condicionado",
            "Funcional",
            "Constructivo",
            "Transformador",
        ]
        map_norm_to_label = {
            "disruptivo": "Disruptivo",
            "condicionado": "Condicionado",
            "funcional": "Funcional",
            "constructivo": "Constructivo",
            "transformador": "Transformador",
        }
        palette = ["#E3F2FD", "#BBDEFB", "#90CAF9", "#42A5F5", "#0D47A1"]
    else:
        # fallback si llegara otra prueba
        niveles_order = sorted(df_hse["NIVEL_LOGRO_4"].dropna().unique().tolist())
        map_norm_to_label = {}
        palette = ["#E0F2F1", "#80CBC4", "#26A69A", "#00897B", "#004D40"][: len(niveles_order)]

    # Canonizar las etiquetas usando el mapa; si no está en el mapa, se deja como viene
    df_hse["NIVEL_CANON"] = df_hse["nivel_norm"].map(map_norm_to_label)
    df_hse["NIVEL_CANON"] = df_hse["NIVEL_CANON"].fillna(df_hse["NIVEL_LOGRO_4"])

    # Conteo por nivel respetando el orden deseado
    counts = df_hse["NIVEL_CANON"].value_counts().reindex(niveles_order, fill_value=0)
    total = counts.sum()

    niveles = pd.DataFrame({"NIVEL_LOGRO_4": niveles_order, "conteo": counts.values})
    if total > 0:
        niveles["proporcion"] = niveles["conteo"] / total
    else:
        niveles["proporcion"] = 0.0
    niveles["porcentaje"] = niveles["proporcion"] * 100

    st.write("**Proporción de estudiantes por nivel (HSE)**")
    tabla = niveles.copy()
    tabla["porcentaje"] = tabla["porcentaje"].round(1).astype(str) + "%"
    st.dataframe(tabla[["NIVEL_LOGRO_4", "conteo", "porcentaje"]])

    base = alt.Chart(niveles).properties(height=320)

    # Barras en orden fijo, Y de 0 a 100%
    chart = (
        base.mark_bar()
        .encode(
            x=alt.X(
                "NIVEL_LOGRO_4:N",
                sort=niveles_order,
                title="Nivel",
            ),
            y=alt.Y(
                "proporcion:Q",
                title="Proporción de estudiantes",
                axis=alt.Axis(format="%", tickCount=6),
                scale=alt.Scale(domain=[0, 1]),  # 0% a 100%
            ),
            color=alt.Color(
                "NIVEL_LOGRO_4:N",
                scale=alt.Scale(domain=niveles_order, range=palette),
                title="Nivel",
            ),
            tooltip=[
                "NIVEL_LOGRO_4:N",
                alt.Tooltip("proporcion:Q", format=".1%"),
                "conteo:Q",
            ],
        )
    )

    # Etiquetas en %
    text = (
        base.mark_text(dy=-10, color="white")
        .encode(
            x=alt.X("NIVEL_LOGRO_4:N", sort=niveles_order),
            y="proporcion:Q",
            text=alt.Text("proporcion:Q", format=".0%"),
        )
    )

    st.altair_chart(chart + text, use_container_width=True)

# ---------------------------------------------------
# Lógica de cada pestaña
# ---------------------------------------------------
def show_tab_for_fuente(df_global, fuente, grado_categories, key_prefix):
    df_src = df_global[df_global["FUENTE"] == fuente].copy()
    is_hse = fuente == "HSE"

    if df_src.empty:
        st.warning(f"No hay datos para la fuente: {fuente}")
        return

    st.markdown("### Prueba HSE (Habilidades socioemocionales)" if is_hse else "### Prueba Cognitiva")
    st.markdown("#### Filtros")

    col1, col2, col3 = st.columns(3)

    # Año
    with col1:
        anos = sorted(df_src["ANHO"].dropna().unique().tolist())
        opciones_ano = ["Todos"] + anos
        index_ano = len(opciones_ano) - 1 if len(opciones_ano) > 1 else 0
        ano_sel = st.radio(
            "Año / periodo",
            options=opciones_ano,
            index=index_ano,
            key=f"{key_prefix}_ano",
            horizontal=True,
        )

    # Sede
    with col2:
        sedes = sorted(df_src["SEDE"].dropna().unique().tolist())
        opciones_sede = ["Todas"] + sedes
        sede_sel = st.radio(
            "Sede",
            options=opciones_sede,
            key=f"{key_prefix}_sede",
            horizontal=True,
        )

    # Área / Prueba
    with col3:
        areas = sorted(df_src["COD_AREA"].dropna().unique().tolist())
        if is_hse:
            label_area = "Prueba"
            opciones_area = areas      # sin "Todas"
            index_area = 0
        else:
            label_area = "Área"
            opciones_area = ["Todas"] + areas
            index_area = 0
        area_sel = st.radio(
            label_area,
            options=opciones_area,
            index=index_area,
            key=f"{key_prefix}_area",
            horizontal=True,
        )

    # Grados condicionados por filtros
    df_for_grado = df_src.copy()
    if ano_sel != "Todos":
        df_for_grado = df_for_grado[df_for_grado["ANHO"] == ano_sel]
    if sede_sel != "Todas":
        df_for_grado = df_for_grado[df_for_grado["SEDE"] == sede_sel]
    if is_hse:
        df_for_grado = df_for_grado[df_for_grado["COD_AREA"] == area_sel]
    else:
        if area_sel != "Todas":
            df_for_grado = df_for_grado[df_for_grado["COD_AREA"] == area_sel]

    grados_presentes = [
        g for g in grado_categories
        if g in df_for_grado["GRADO_LABEL"].astype(str).unique()
    ]
    grado_opts = ["Todos"] + grados_presentes if grados_presentes else ["Todos"]

    grado_sel = st.radio(
        "Grado",
        options=grado_opts,
        key=f"{key_prefix}_grado",
        horizontal=True,
    )

    # Filtros finales
    df_f = df_src.copy()
    if ano_sel != "Todos":
        df_f = df_f[df_f["ANHO"] == ano_sel]
    if sede_sel != "Todas":
        df_f = df_f[df_f["SEDE"] == sede_sel]
    if is_hse:
        df_f = df_f[df_f["COD_AREA"] == area_sel]
    else:
        if area_sel != "Todas":
            df_f = df_f[df_f["COD_AREA"] == area_sel]
    if grado_sel != "Todos":
        df_f = df_f[df_f["GRADO_LABEL"].astype(str) == grado_sel]

    st.markdown(f"**Registros filtrados:** {len(df_f)}")

    if df_f.empty:
        st.warning("No hay datos para la combinación de filtros seleccionada.")
        return

    # KPIs
    colk1, colk2, colk3, colk4 = st.columns(4)
    with colk1:
        n_est = df_f["CORREO"].nunique() if "CORREO" in df_f.columns else len(df_f)
        st.metric("Estudiantes únicos", n_est)
    with colk2:
        st.metric("Sedes", df_f["SEDE"].nunique())
    with colk3:
        st.metric("Media MEDIDA_500", f"{df_f['MEDIDA_500'].mean():,.1f}")
    with colk4:
        desv_medida = df_f["MEDIDA_500"].std()
        st.metric("Desviación MEDIDA_500", f"{desv_medida:,.1f}" if not np.isnan(desv_medida) else "N/A")

    st.markdown("---")

    # Comparación por sexo (incluyendo grados)
    plot_medida_por_sexo(df_f, grado_categories)

    st.markdown("---")

    # Niveles
    if is_hse:
        plot_niveles_hse(df_f, area_sel)
    else:
        plot_niveles_cognitivos(df_f, grado_categories)

    # Tabla detalle
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
                    "NIVEL_LOGRO_4",
                ]
            ]
        )

# ---------------------------------------------------
# Tabs principales
# ---------------------------------------------------
tab_cog, tab_hse = st.tabs(
    ["Prueba Cognitiva", "Prueba HSE (Habilidades socioemocionales)"]
)

with tab_cog:
    show_tab_for_fuente(df, "Cognitivas", GRADO_CATEGORIES, key_prefix="cog")

with tab_hse:
    show_tab_for_fuente(df, "HSE", GRADO_CATEGORIES, key_prefix="hse")







