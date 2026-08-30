import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Lugh Perfection Calculator",
    page_icon="✨",
    layout="centered"
)

APP_VERSION = "1.0.0"

ATRIBUTOS = 8


# ============================================================
# TIPOS
# ============================================================

TIPOS = {
    "Lugh Normal": {
        "min": 1,
        "max": 25,
        "min_perfeicao": 4.0,
        "color": "#4CC9F0"
    },

    "Lugh Prismático": {
        "min": 12,
        "max": 25,
        "min_perfeicao": 48.0,
        "color": "#D946EF"
    }
}


# ============================================================
# TRADUÇÕES
# ============================================================

TEXT = {

    "pt": {
        "subtitle": "Descubra o quão raro seu Lugh realmente é.",
        "configuration": "⚙️ Configuração",
        "lugh_type": "Tipo de Lugh",
        "normal": "Lugh Normal",
        "prismatic": "Lugh Prismático",
        "perfection": "Perfection",
        "calculate": "✨ CALCULAR",
        "rarity": "RARIDADE",
        "equivalent": "Equivalent Score",
        "probability": "Exact Probability",
        "combinations": "Possible Combinations",
        "distribution": "📊 Distribuição de Raridade",
        "common": "Common",
        "rare": "Rare",
        "very_rare": "Very Rare",
        "extreme": "Extremely Rare",
        "how": "📖 Como funciona a raridade?",
        "how_text": "A raridade é calculada utilizando a distribuição estatística de todas as combinações possíveis de atributos. Quanto mais próximo um Lugh estiver do centro da distribuição, mais comum ele será. Lughs com pontuações extremamente baixas ou extremamente altas são progressivamente mais raros.",
        "prismatic_title": "✨ Lughs Prismáticos",
        "prismatic_text": "Lughs Prismáticos possuem uma faixa de atributos diferente dos Lughs Normais. Por isso, sua raridade é calculada utilizando sua própria distribuição de atributos.",
        "attributes": "📚 Sobre os Atributos dos Lughs",
        "attributes_text": "Cada Lugh possui 8 atributos. A pontuação total é determinada pela soma desses atributos. A calculadora compara essa pontuação com todas as combinações matematicamente possíveis para aquele tipo de Lugh.",
        "your_lugh": "YOUR LUGH",
        "lower": "Lower tail",
        "upper": "Upper tail",
        "center": "Center",
        "language": "Idioma"
    },

    "en": {
        "subtitle": "Discover how rare your Lugh really is.",
        "configuration": "⚙️ Configuration",
        "lugh_type": "Lugh Type",
        "normal": "Lugh Normal",
        "prismatic": "Lugh Prismatic",
        "perfection": "Perfection",
        "calculate": "✨ CALCULATE",
        "rarity": "RARITY",
        "equivalent": "Equivalent Score",
        "probability": "Exact Probability",
        "combinations": "Possible Combinations",
        "distribution": "📊 Rarity Distribution",
        "common": "Common",
        "rare": "Rare",
        "very_rare": "Very Rare",
        "extreme": "Extremely Rare",
        "how": "📖 How does rarity work?",
        "how_text": "Rarity is calculated using the statistical distribution of all possible attribute combinations. The closer a Lugh is to the center of the distribution, the more common it is. Lughs with extremely low or extremely high scores are progressively rarer.",
        "prismatic_title": "✨ Prismatic Lughs",
        "prismatic_text": "Prismatic Lughs have a different attribute range from Normal Lughs. Their rarity is therefore calculated using their own attribute distribution.",
        "attributes": "📚 About Lugh Attributes",
        "attributes_text": "Each Lugh has 8 attributes. The total score is determined by adding these attributes together. The calculator compares this score against every mathematically possible combination for that type of Lugh.",
        "your_lugh": "YOUR LUGH",
        "lower": "Lower tail",
        "upper": "Upper tail",
        "center": "Center",
        "language": "Language"
    }
}


# ============================================================
# ESTADO DO IDIOMA
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "en"


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 50% -15%,
                rgba(100, 70, 255, 0.16),
                transparent 45%
            ),
            #080A0F;
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1 {
        text-align: center;
        font-weight: 800;
    }

    .subtitle {
        text-align: center;
        color: #8992A3;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .logo {
        display: flex;
        justify-content: center;
    }

    div.stButton > button {
        height: 50px;
        border-radius: 12px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 15px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 22px;
    }

    .footer {
        text-align: center;
        color: #505866;
        font-size: 12px;
        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGO
# ============================================================

logo_left, logo_center, logo_right = st.columns([1, 2, 1])

with logo_center:

    try:

        logo = Image.open("logo.png")

        st.image(
            logo,
            width=180
        )

    except FileNotFoundError:

        st.warning("Logo file not found: logo.png")


# ============================================================
# TÍTULO
# ============================================================

st.title("✨ Lugh Perfection Calculator")

st.markdown(
    f'<p class="subtitle">{TEXT[st.session_state.language]["subtitle"]}</p>',
    unsafe_allow_html=True
)


# ============================================================
# IDIOMA
# ============================================================

language_left, language_center, language_right = st.columns(
    [1, 2, 1]
)

with language_center:

    idioma = st.radio(
        TEXT[st.session_state.language]["language"],
        [
            "🇺🇸 English",
            "🇧🇷 Português"
        ],
        horizontal=True
    )

    novo_idioma = (
        "pt"
        if idioma == "🇧🇷 Português"
        else "en"
    )

    if novo_idioma != st.session_state.language:

        st.session_state.language = novo_idioma

        st.rerun()


t = TEXT[st.session_state.language]


# ============================================================
# CONFIGURAÇÃO
# ============================================================

with st.container(border=True):

    st.subheader(t["configuration"])

    tipo_visual = st.radio(
        t["lugh_type"],
        [
            t["normal"],
            t["prismatic"]
        ],
        horizontal=True
    )

    if tipo_visual == t["normal"]:

        tipo = "Lugh Normal"

    else:

        tipo = "Lugh Prismático"


    min_valor = TIPOS[tipo]["min"]
    max_valor = TIPOS[tipo]["max"]
    min_perfeicao = TIPOS[tipo]["min_perfeicao"]

    cor = TIPOS[tipo]["color"]


    perfeicao = st.number_input(
        t["perfection"],
        min_value=min_perfeicao,
        max_value=100.0,
        value=min_perfeicao,
        step=0.01,
        format="%.2f"
    )


    calcular = st.button(
        t["calculate"],
        use_container_width=True
    )


# ============================================================
# DISTRIBUIÇÃO
# ============================================================

@st.cache_data
def calcular_distribuicao(
    quantidade_atributos,
    minimo,
    maximo
):

    dp = {0: 1}

    for _ in range(quantidade_atributos):

        proximo_dp = {}

        for soma, quantidade in dp.items():

            for valor in range(
                minimo,
                maximo + 1
            ):

                nova_soma = soma + valor

                proximo_dp[nova_soma] = (
                    proximo_dp.get(
                        nova_soma,
                        0
                    )
                    + quantidade
                )

        dp = proximo_dp

    return dp


dp = calcular_distribuicao(
    ATRIBUTOS,
    min_valor,
    max_valor
)


# ============================================================
# CÁLCULO
# ============================================================

if calcular:

    min_pontos = ATRIBUTOS * min_valor

    max_pontos = ATRIBUTOS * max_valor

    quantidade_valores = (
        max_valor - min_valor + 1
    )

    combinacoes_totais = (
        quantidade_valores ** ATRIBUTOS
    )


    # --------------------------------------------------------
    # PERFECTION → SCORE
    # --------------------------------------------------------

    proporcao = (
        (perfeicao - min_perfeicao)
        / (100.0 - min_perfeicao)
    )

    pontos = round(
        min_pontos
        + proporcao *
        (max_pontos - min_pontos)
    )

    pontos = max(
        min_pontos,
        min(
            pontos,
            max_pontos
        )
    )


    # --------------------------------------------------------
    # CENTRO
    # --------------------------------------------------------

    centro_pontos = (
        min_pontos + max_pontos
    ) / 2


    # --------------------------------------------------------
    # CAUDA
    # --------------------------------------------------------

    if pontos < centro_pontos:

        combinacoes_favoraveis = sum(
            quantidade
            for score, quantidade in dp.items()
            if score <= pontos
        )

        lado_curva = t["lower"]

    elif pontos > centro_pontos:

        combinacoes_favoraveis = sum(
            quantidade
            for score, quantidade in dp.items()
            if score >= pontos
        )

        lado_curva = t["upper"]

    else:

        combinacoes_favoraveis = sum(
            quantidade
            for score, quantidade in dp.items()
            if score <= pontos
        )

        lado_curva = t["center"]


    combinacoes_favoraveis = max(
        1,
        combinacoes_favoraveis
    )


    # --------------------------------------------------------
    # PROBABILIDADE
    # --------------------------------------------------------

    porcentagem_real = (
        combinacoes_favoraveis
        / combinacoes_totais
    ) * 100


    # --------------------------------------------------------
    # RARIDADE
    # --------------------------------------------------------

    chance = (
        combinacoes_totais
        / combinacoes_favoraveis
    )


    # --------------------------------------------------------
    # CLASSIFICAÇÃO
    # --------------------------------------------------------

    if chance < 10:

        tier = t["common"]

    elif chance < 100:

        tier = t["rare"]

    elif chance < 1000:

        tier = t["very_rare"]

    else:

        tier = t["extreme"]


    # ========================================================
    # RESULTADO
    # ========================================================

    st.divider()

    st.subheader(tipo_visual)


    # --------------------------------------------------------
    # PERFECTION
    # --------------------------------------------------------

    st.markdown(
        f"# {perfeicao:.2f}%"
    )

    st.caption("Perfection")


    # --------------------------------------------------------
    # RARIDADE
    # --------------------------------------------------------

    st.markdown(
        f"## {t['rarity']}"
    )

    st.markdown(
        f"# 1 in {chance:,.0f}"
    )

    st.caption(tier)


    # --------------------------------------------------------
    # MÉTRICAS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            t["equivalent"],
            f"{pontos} / {max_pontos}"
        )


    with col2:

        st.metric(
            t["probability"],
            f"{porcentagem_real:.9f}%"
        )


    with col3:

        st.metric(
            t["combinations"],
            f"{combinacoes_totais:,}"
        )


    st.caption(
        f"{t['distribution']}: {lado_curva}"
    )


    # ========================================================
    # GRÁFICO
    # ========================================================

    st.divider()

    st.subheader(t["distribution"])


    scores = list(
        range(
            min_pontos,
            max_pontos + 1
        )
    )


    probabilities = [
        (
            dp[score]
            / combinacoes_totais
        ) * 100
        for score in scores
    ]


    probabilidade_score = (
        dp[pontos]
        / combinacoes_totais
    ) * 100


    # --------------------------------------------------------
    # PLOTLY
    # --------------------------------------------------------

    fig = go.Figure()


    # CURVA

    fig.add_trace(
        go.Scatter(
            x=scores,
            y=probabilities,
            mode="lines",
            name="Distribution",
            line={
                "color": cor,
                "width": 4,
                "shape": "spline"
            },
            fill="tozeroy",
            fillcolor=(
                "rgba(76,201,240,0.12)"
                if tipo == "Lugh Normal"
                else "rgba(217,70,239,0.12)"
            ),
            hovertemplate=(
                "Score: %{x}"
                "<br>Probability: %{y:.8f}%"
                "<extra></extra>"
            )
        )
    )


    # LINHA DO LUGH

    fig.add_vline(
        x=pontos,
        line_width=2,
        line_dash="dash",
        line_color=cor
    )


    # MARCADOR

    fig.add_trace(
        go.Scatter(
            x=[pontos],
            y=[probabilidade_score],
            mode="markers",
            name=t["your_lugh"],
            marker={
                "size": 17,
                "color": cor,
                "line": {
                    "color": "white",
                    "width": 3
                }
            },
            hovertemplate=(
                f"Perfection: {perfeicao:.2f}%"
                f"<br>Score: {pontos}"
                f"<br>Probability: {porcentagem_real:.9f}%"
                "<extra></extra>"
            )
        )
    )


    # --------------------------------------------------------
    # LAYOUT
    # --------------------------------------------------------

    fig.update_layout(

        height=450,

        margin={
            "l": 20,
            "r": 20,
            "t": 25,
            "b": 45
        },

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font={
            "color": "#8992A3"
        },

        xaxis={
            "title": "Score",
            "gridcolor": "rgba(255,255,255,0.05)",
            "zeroline": False
        },

        yaxis={
            "title": "Probability (%)",
            "gridcolor": "rgba(255,255,255,0.05)",
            "zeroline": False
        },

        legend={
            "bgcolor": "rgba(0,0,0,0)"
        },

        hoverlabel={
            "bgcolor": "#151923",
            "bordercolor": cor,
            "font_color": "white"
        }
    )


    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


    # ========================================================
    # ESCALA DE RARIDADE
    # ========================================================

    st.progress(
        min(
            1.0,
            pontos / max_pontos
        )
    )

    scale_col1, scale_col2, scale_col3, scale_col4 = st.columns(4)

    with scale_col1:
        st.caption(t["common"])

    with scale_col2:
        st.caption(t["rare"])

    with scale_col3:
        st.caption(t["very_rare"])

    with scale_col4:
        st.caption(t["extreme"])


# ============================================================
# INFORMAÇÕES
# ============================================================

st.divider()

with st.expander(
    t["how"],
    expanded=True
):

    st.write(
        t["how_text"]
    )


with st.expander(
    t["prismatic_title"]
):

    st.write(
        t["prismatic_text"]
    )


with st.expander(
    t["attributes"]
):

    st.write(
        t["attributes_text"]
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    f"✨ Lugh Perfection Calculator • Version {APP_VERSION}"
)
