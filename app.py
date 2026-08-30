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
# TIPOS DE LUGH
# ============================================================

TIPOS = {
    "Lugh Normal": {
        "min": 1,
        "max": 25,
        "min_perfeicao": 4.0,
        "color": "#4CC9F0",
        "gradient_start": "#4CC9F0",
        "gradient_end": "#4361EE"
    },

    "Lugh Prismático": {
        "min": 12,
        "max": 25,
        "min_perfeicao": 48.0,
        "color": "#D946EF",
        "gradient_start": "#D946EF",
        "gradient_end": "#7C3AED"
    }
}


# ============================================================
# TRADUÇÕES
# ============================================================

TEXT = {

    "pt": {

        "subtitle":
            "Descubra o quão raro seu Lugh realmente é.",

        "language":
            "Idioma",

        "configuration":
            "Configuração",

        "lugh_type":
            "Tipo de Lugh",

        "normal":
            "Lugh Normal",

        "prismatic":
            "Lugh Prismático",

        "perfection":
            "Perfection",

        "calculate":
            "CALCULAR",

        "rarity":
            "Raridade",

        "equivalent_score":
            "Pontuação Equivalente",

        "exact_probability":
            "Probabilidade Exata",

        "possible_combinations":
            "Combinações Possíveis",

        "distribution":
            "Distribuição de Raridade",

        "distribution_position":
            "Posição na distribuição",

        "lower_tail":
            "Cauda inferior",

        "upper_tail":
            "Cauda superior",

        "center":
            "Centro",

        "common":
            "Comum",

        "rare":
            "Raro",

        "very_rare":
            "Muito Raro",

        "extremely_rare":
            "Extremamente Raro",

        "how_works":
            "Como funciona a raridade?",

        "how_works_text":
            "A raridade é calculada utilizando a distribuição estatística de todas as combinações possíveis de atributos. Quanto mais próximo um Lugh estiver do centro da distribuição, mais comum ele será. Lughs com pontuações extremamente baixas ou extremamente altas são progressivamente mais raros.",

        "prismatic_title":
            "✨ Lughs Prismáticos",

        "prismatic_text":
            "Lughs Prismáticos possuem uma faixa de atributos diferente dos Lughs Normais. Por isso, sua raridade é calculada utilizando sua própria distribuição de atributos.",

        "attributes":
            "Sobre os Atributos dos Lughs",

        "attributes_text":
            "Cada Lugh possui 8 atributos. A pontuação total é determinada pela soma desses atributos. A calculadora compara essa pontuação com todas as combinações matematicamente possíveis para aquele tipo de Lugh.",

        "your_lugh":
            "SEU LUGH",

        "footer":
            "Lugh Perfection Calculator"
    },


    "en": {

        "subtitle":
            "Discover how rare your Lugh really is.",

        "language":
            "Language",

        "configuration":
            "Configuration",

        "lugh_type":
            "Lugh Type",

        "normal":
            "Lugh Normal",

        "prismatic":
            "Lugh Prismatic",

        "perfection":
            "Perfection",

        "calculate":
            "CALCULATE",

        "rarity":
            "Rarity",

        "equivalent_score":
            "Equivalent Score",

        "exact_probability":
            "Exact Probability",

        "possible_combinations":
            "Possible Combinations",

        "distribution":
            "Rarity Distribution",

        "distribution_position":
            "Distribution position",

        "lower_tail":
            "Lower tail",

        "upper_tail":
            "Upper tail",

        "center":
            "Center",

        "common":
            "Common",

        "rare":
            "Rare",

        "very_rare":
            "Very Rare",

        "extremely_rare":
            "Extremely Rare",

        "how_works":
            "How does rarity work?",

        "how_works_text":
            "Rarity is calculated using the statistical distribution of all possible attribute combinations. The closer a Lugh is to the center of the distribution, the more common it is. Lughs with extremely low or extremely high scores are progressively rarer.",

        "prismatic_title":
            "✨ Prismatic Lughs",

        "prismatic_text":
            "Prismatic Lughs have a different attribute range from Normal Lughs. Their rarity is therefore calculated using their own attribute distribution.",

        "attributes":
            "About Lugh Attributes",

        "attributes_text":
            "Each Lugh has 8 attributes. The total score is determined by adding these attributes together. The calculator compares this score against every mathematically possible combination for that type of Lugh.",

        "your_lugh":
            "YOUR LUGH",

        "footer":
            "Lugh Perfection Calculator"
    }
}


# ============================================================
# ESTADO
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "en"


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       BODY
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 50% -10%,
                rgba(100, 70, 255, 0.16),
                transparent 42%
            ),
            #080A0F;
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 1rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       HEADER
       ===================================================== */

    .logo-center {
        width: 100%;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 10px;
    }

    .logo-center img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #FFFFFF;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #8992A3;
        font-size: 16px;
        margin-bottom: 35px;
    }


    /* =====================================================
       CARDS
       ===================================================== */

    .section-card {
        background: rgba(20, 23, 32, 0.88);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 24px;
        margin-top: 15px;
        margin-bottom: 20px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.22);
    }

    .section-title {
        font-size: 18px;
        font-weight: 750;
        color: #FFFFFF;
        margin-bottom: 5px;
    }


    /* =====================================================
       RESULT
       ===================================================== */

    .result-card {
        border-radius: 25px;
        padding: 38px 20px;
        text-align: center;
        margin-top: 28px;
        margin-bottom: 22px;

        background:
            radial-gradient(
                circle at 50% 0%,
                var(--glow),
                transparent 62%
            ),
            #11141D;

        border: 1px solid var(--border);

        box-shadow:
            0 18px 55px rgba(0,0,0,0.30);
    }

    .result-type {
        color: #8A93A3;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 12px;
        margin-bottom: 10px;
    }

    .result-perfection {
        color: #FFFFFF;
        font-size: 58px;
        font-weight: 900;
        line-height: 1;
    }

    .result-label {
        color: #737D8D;
        font-size: 13px;
        margin-top: 7px;
    }

    .rarity-label {
        color: #737D8D;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 30px;
    }

    .rarity-value {
        font-size: 44px;
        font-weight: 900;
        line-height: 1.1;
        margin-top: 5px;
    }

    .rarity-tier {
        display: inline-block;
        margin-top: 13px;
        padding: 7px 17px;
        border-radius: 30px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        color: #E5E8EF;
        font-size: 13px;
        font-weight: 700;
    }


    /* =====================================================
       METRICS
       ===================================================== */

    .metric {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 17px;
        padding: 18px 10px;
        text-align: center;
        min-height: 90px;
    }

    .metric-label {
        color: #737D8D;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        color: #FFFFFF;
        font-size: 17px;
        font-weight: 750;
        margin-top: 9px;
    }


    /* =====================================================
       TIER
       ===================================================== */

    .tier-bar {
        height: 8px;
        border-radius: 20px;

        background:
            linear-gradient(
                90deg,
                #414754 0%,
                #69717E 30%,
                #A68A55 55%,
                #A84E9C 75%,
                #E74C65 100%
            );

        margin-top: 18px;
    }

    .tier-labels {
        display: flex;
        justify-content: space-between;
        color: #697383;
        font-size: 10px;
        margin-top: 8px;
    }


    /* =====================================================
       INFO
       ===================================================== */

    .info-card {
        background: rgba(20,23,32,0.75);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 25px;
        margin-top: 20px;
    }

    .info-card h3 {
        color: #FFFFFF;
        margin-bottom: 12px;
    }

    .info-card p {
        color: #9AA3B2;
        line-height: 1.75;
        font-size: 14px;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;
        color: #505866;
        font-size: 12px;
        margin-top: 45px;
        padding-top: 22px;
        border-top: 1px solid rgba(255,255,255,0.05);
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 600px) {

        .main .block-container {
            padding-left: 15px;
            padding-right: 15px;
        }

        .main-title {
            font-size: 30px;
        }

        .result-perfection {
            font-size: 46px;
        }

        .rarity-value {
            font-size: 32px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGO
# ============================================================

try:

    logo = Image.open("logo.png")

    logo_col1, logo_col2, logo_col3 = st.columns(
        [1, 2, 1]
    )

    with logo_col2:

        st.image(
            logo,
            use_container_width=True
        )

except Exception:
    pass


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Lugh Perfection Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{t if False else TEXT[st.session_state.language]["subtitle"]}</div>',
    unsafe_allow_html=True
)


# ============================================================
# IDIOMA
# ============================================================

lang_col1, lang_col2, lang_col3 = st.columns(
    [1, 2, 1]
)

with lang_col2:

    idioma = st.radio(
        "Language",
        [
            "🇺🇸 English",
            "🇧🇷 Português"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    if idioma == "🇧🇷 Português":

        st.session_state.language = "pt"

    else:

        st.session_state.language = "en"


t = TEXT[st.session_state.language]


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.markdown(
    f"""
    <div class="section-card">
        <div class="section-title">
            ⚙️ {t["configuration"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


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


# ============================================================
# PONTUAÇÃO
# ============================================================

min_pontos = ATRIBUTOS * min_valor
max_pontos = ATRIBUTOS * max_valor

quantidade_valores = (
    max_valor - min_valor + 1
)

combinacoes_totais = (
    quantidade_valores ** ATRIBUTOS
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
# INPUT
# ============================================================

perfeicao = st.number_input(
    t["perfection"],
    min_value=min_perfeicao,
    max_value=100.0,
    value=min_perfeicao,
    step=0.01,
    format="%.2f"
)


# ============================================================
# CALCULAR
# ============================================================

if st.button(
    f"✨ {t['calculate']}",
    use_container_width=True
):

    # ========================================================
    # PERFECTION → SCORE
    # ========================================================

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


    # ========================================================
    # CENTRO
    # ========================================================

    centro_pontos = (
        min_pontos + max_pontos
    ) / 2


    # ========================================================
    # CAUDA
    # ========================================================

    if pontos < centro_pontos:

        combinacoes_favoraveis = sum(
            quantidade
            for score, quantidade in dp.items()
            if score <= pontos
        )

        lado_curva = t["lower_tail"]

    elif pontos > centro_pontos:

        combinacoes_favoraveis = sum(
            quantidade
            for score, quantidade in dp.items()
            if score >= pontos
        )

        lado_curva = t["upper_tail"]

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


    # ========================================================
    # PROBABILIDADE
    # ========================================================

    porcentagem_real = (
        combinacoes_favoraveis
        / combinacoes_totais
    ) * 100


    # ========================================================
    # RARIDADE
    # ========================================================

    chance = (
        combinacoes_totais
        / combinacoes_favoraveis
    )


    # ========================================================
    # CLASSIFICAÇÃO
    # ========================================================

    if chance < 10:

        tier = t["common"]

    elif chance < 100:

        tier = t["rare"]

    elif chance < 1000:

        tier = t["very_rare"]

    else:

        tier = t["extremely_rare"]


    # ========================================================
    # RESULTADO
    # ========================================================

    st.markdown(
        f"""
        <div
            class="result-card"
            style="
                --glow: {TIPOS[tipo]["color"]}25;
                --border: {TIPOS[tipo]["color"]}50;
            "
        >

            <div class="result-type">
                {tipo_visual}
            </div>

            <div class="result-perfection">
                {perfeicao:.2f}%
            </div>

            <div class="result-label">
                Perfection
            </div>

            <div class="rarity-label">
                {t["rarity"]}
            </div>

            <div
                class="rarity-value"
                style="color:{cor};"
            >
                1 in {chance:,.0f}
            </div>

            <div class="rarity-tier">
                {tier}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # MÉTRICAS
    # ========================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            f"""
            <div class="metric">

                <div class="metric-label">
                    {t["equivalent_score"]}
                </div>

                <div class="metric-value">
                    {pontos} / {max_pontos}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="metric">

                <div class="metric-label">
                    {t["exact_probability"]}
                </div>

                <div class="metric-value">
                    {porcentagem_real:.9f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="metric">

                <div class="metric-label">
                    {t["possible_combinations"]}
                </div>

                <div class="metric-value">
                    {combinacoes_totais:,}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # GRÁFICO
    # ========================================================

    st.markdown(
        f"""
        <div class="section-card">

            <div class="section-title">
                📊 {t["distribution"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


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


    chart_data = pd.DataFrame(
        {
            "Score": scores,
            "Probability": probabilities
        }
    )


    # ========================================================
    # PONTO DO LUGH
    # ========================================================

    probabilidade_score = (
        dp[pontos]
        / combinacoes_totais
    ) * 100


    # ========================================================
    # PLOTLY
    # ========================================================

    fig = go.Figure()


    # Curva

    fig.add_trace(
        go.Scatter(
            x=chart_data["Score"],
            y=chart_data["Probability"],
            mode="lines",
            line=dict(
                color=cor,
                width=4,
                shape="spline"
            ),
            fill="tozeroy",
            fillcolor=(
                "rgba(76,201,240,0.10)"
                if tipo == "Lugh Normal"
                else "rgba(217,70,239,0.10)"
            ),
            hovertemplate=(
                "Score: %{x}"
                "<br>Probability: %{y:.8f}%"
                "<extra></extra>"
            ),
            name="Distribution"
        )
    )


    # Linha vertical

    fig.add_vline(
        x=pontos,
        line_width=2,
        line_dash="dash",
        line_color=cor
    )


    # Marcador

    fig.add_trace(
        go.Scatter(
            x=[pontos],
            y=[probabilidade_score],
            mode="markers",
            marker=dict(
                size=15,
                color=cor,
                line=dict(
                    color="white",
                    width=3
                )
            ),
            hovertemplate=(
                f"Score: {pontos}"
                f"<br>Perfection: {perfeicao:.2f}%"
                f"<br>Probability: {porcentagem_real:.9f}%"
                "<extra></extra>"
            ),
            name=t["your_lugh"]
        )
    )


    # ========================================================
    # LAYOUT
    # ========================================================

    fig.update_layout(

        height=440,

        margin=dict(
            l=10,
            r=10,
            t=30,
            b=45
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#8992A3"
        ),

        xaxis=dict(
            title="Score",
            gridcolor="rgba(255,255,255,0.05)",
            zeroline=False
        ),

        yaxis=dict(
            title="Probability (%)",
            gridcolor="rgba(255,255,255,0.05)",
            zeroline=False
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#8992A3"
            )
        ),

        hoverlabel=dict(
            bgcolor="#151923",
            bordercolor=cor,
            font_color="white"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


    # ========================================================
    # INDICADOR
    # ========================================================

    st.markdown(
        f"""
        <div style="
            text-align:center;
            margin-top:5px;
            margin-bottom:20px;
        ">

            <span style="
                display:inline-block;
                padding:8px 16px;
                border-radius:30px;
                background:{cor}18;
                border:1px solid {cor}45;
                color:{cor};
                font-size:12px;
                font-weight:750;
            ">

                ✦ {t["your_lugh"]}: {pontos}

            </span>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # BARRA DE RARIDADE
    # ========================================================

    st.markdown(
        f"""
        <div class="tier-bar"></div>

        <div class="tier-labels">

            <span>{t["common"]}</span>

            <span>{t["rare"]}</span>

            <span>{t["very_rare"]}</span>

            <span>{t["extremely_rare"]}</span>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    f"""
    <div class="info-card">

        <h3>📖 {t["how_works"]}</h3>

        <p>
            {t["how_works_text"]}
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PRISMÁTICOS
# ============================================================

st.markdown(
    f"""
    <div class="info-card">

        <h3>{t["prismatic_title"]}</h3>

        <p>
            {t["prismatic_text"]}
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ATRIBUTOS
# ============================================================

st.markdown(
    f"""
    <div class="info-card">

        <h3>📚 {t["attributes"]}</h3>

        <p>
            {t["attributes_text"]}
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f"""
    <div class="footer">

        ✨ {t["footer"]}<br>

        Version {APP_VERSION}

    </div>
    """,
    unsafe_allow_html=True
)
