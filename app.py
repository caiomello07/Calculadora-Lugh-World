```python
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Lugh Perfection Calculator",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CONFIGURAÇÕES
# ============================================================

APP_VERSION = "1.0.0"

ATRIBUTOS = 8

TIPOS = {
    "Lugh Normal": {
        "min": 1,
        "max": 25,
        "min_perfeicao": 4.0,
        "color": "#4CC9F0",
        "glow": "rgba(76, 201, 240, 0.25)"
    },

    "Lugh Prismático": {
        "min": 12,
        "max": 25,
        "min_perfeicao": 48.0,
        "color": "#D946EF",
        "glow": "rgba(217, 70, 239, 0.25)"
    }
}


# ============================================================
# TRADUÇÕES
# ============================================================

TRANSLATIONS = {

    "pt": {

        "subtitle":
            "Descubra o quão raro seu Lugh realmente é.",

        "configuration":
            "Configuração",

        "lugh_type":
            "Tipo de Lugh",

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
            "Como funciona?",

        "how_works_text":
            """
            A raridade é calculada utilizando a distribuição estatística
            de todas as combinações possíveis de atributos.

            Quanto mais próximo um Lugh estiver do centro da distribuição,
            mais comum ele será.

            Lughs com pontuações extremamente baixas ou extremamente altas
            aparecem com menor frequência e, portanto, são progressivamente
            mais raros.
            """,

        "prismatic":
            "✨ Lughs Prismáticos",

        "prismatic_text":
            """
            Lughs Prismáticos possuem uma faixa de atributos diferente
            dos Lughs Normais.

            Por isso, sua raridade é calculada utilizando uma distribuição
            própria, levando em consideração exclusivamente as combinações
            possíveis dentro da faixa Prismática.
            """,

        "attributes":
            "Sobre os Atributos dos Lughs",

        "attributes_text":
            """
            Cada Lugh possui 8 atributos.

            A pontuação total é determinada pela soma desses atributos.
            A calculadora compara essa pontuação com todas as combinações
            matematicamente possíveis para aquele tipo de Lugh.

            Isso permite determinar não apenas a Perfection, mas também
            o quão estatisticamente rara é aquela combinação de atributos.
            """,

        "common_desc":
            "Uma combinação bastante comum.",

        "rare_desc":
            "Uma combinação menos frequente.",

        "very_rare_desc":
            "Uma combinação estatisticamente incomum.",

        "extremely_rare_desc":
            "Uma combinação extremamente difícil de encontrar.",

        "your_lugh":
            "SEU LUGH",

        "footer":
            "Lugh Perfection Calculator"
    },


    "en": {

        "subtitle":
            "Discover how rare your Lugh really is.",

        "configuration":
            "Configuration",

        "lugh_type":
            "Lugh Type",

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
            """
            Rarity is calculated using the statistical distribution
            of all possible attribute combinations.

            The closer a Lugh is to the center of the distribution,
            the more common it is.

            Lughs with extremely low or extremely high scores occur
            less frequently and are therefore progressively rarer.
            """,

        "prismatic":
            "✨ Prismatic Lughs",

        "prismatic_text":
            """
            Prismatic Lughs have a different attribute range from
            Normal Lughs.

            Their rarity is therefore calculated using their own
            distribution curve, based exclusively on the possible
            combinations within the Prismatic attribute range.
            """,

        "attributes":
            "About Lugh Attributes",

        "attributes_text":
            """
            Each Lugh has 8 attributes.

            The total score is determined by adding these attributes
            together.

            The calculator compares this score against every mathematically
            possible combination for that type of Lugh.

            This allows us to determine not only the Perfection value,
            but also how statistically rare that particular attribute
            combination is.
            """,

        "common_desc":
            "A very common combination.",

        "rare_desc":
            "A less frequent combination.",

        "very_rare_desc":
            "A statistically uncommon combination.",

        "extremely_rare_desc":
            "An extremely difficult combination to find.",

        "your_lugh":
            "YOUR LUGH",

        "footer":
            "Lugh Perfection Calculator"
    }
}


# ============================================================
# IDIOMA
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "en"


language_col1, language_col2, language_col3 = st.columns(
    [1, 1, 1]
)

with language_col2:

    language = st.radio(
        "Language",
        ["🇺🇸 English", "🇧🇷 Português"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if language == "🇧🇷 Português":
        st.session_state.language = "pt"
    else:
        st.session_state.language = "en"


t = TRANSLATIONS[st.session_state.language]


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 50% -10%,
                rgba(120, 80, 255, 0.12),
                transparent 40%
            ),
            #080A0F;
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.5px;
    }


    /* =====================================================
       HEADER
       ===================================================== */

    .logo-container {
        text-align: center;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    .logo-container img {
        max-width: 180px;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
        background: linear-gradient(
            90deg,
            #ffffff,
            #bfc7d5
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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

    .custom-card {
        background: rgba(20, 23, 32, 0.85);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 25px;
        margin-top: 15px;
        margin-bottom: 20px;
        box-shadow:
            0 10px 40px rgba(0,0,0,0.25);
    }

    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 15px;
    }


    /* =====================================================
       RESULTADO PRINCIPAL
       ===================================================== */

    .result-card {
        background:
            radial-gradient(
                circle at 50% 0%,
                var(--glow),
                transparent 55%
            ),
            #11141D;

        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 35px 25px;
        text-align: center;
        margin-top: 25px;
        margin-bottom: 25px;
    }

    .result-perfection {
        font-size: 54px;
        font-weight: 900;
        color: #ffffff;
        line-height: 1;
        margin-bottom: 8px;
    }

    .result-label {
        color: #8C95A5;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .rarity-label {
        margin-top: 28px;
        color: #8C95A5;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .rarity-value {
        font-size: 42px;
        font-weight: 900;
        color: #ffffff;
        margin-top: 2px;
    }

    .rarity-tier {
        display: inline-block;
        margin-top: 10px;
        padding: 6px 14px;
        border-radius: 20px;
        background: rgba(255,255,255,0.07);
        color: #D7DCE5;
        font-size: 13px;
        font-weight: 600;
    }


    /* =====================================================
       METRICS
       ===================================================== */

    .metric-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 18px 10px;
        text-align: center;
        min-height: 95px;
    }

    .metric-title {
        font-size: 11px;
        color: #8992A3;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        font-size: 18px;
        font-weight: 700;
        color: #F4F6FA;
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
        color: #ffffff;
        margin-bottom: 12px;
    }

    .info-card p {
        color: #9AA3B2;
        line-height: 1.7;
    }


    /* =====================================================
       TIER BAR
       ===================================================== */

    .tier-container {
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .tier-bar {
        height: 8px;
        border-radius: 20px;
        background:
            linear-gradient(
                90deg,
                #39404D 0%,
                #65707F 30%,
                #8D7B55 55%,
                #A34D9C 75%,
                #E24B67 100%
            );
    }

    .tier-labels {
        display: flex;
        justify-content: space-between;
        color: #697383;
        font-size: 10px;
        margin-top: 8px;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;
        color: #515968;
        font-size: 12px;
        margin-top: 45px;
        padding-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.05);
    }


    /* =====================================================
       BOTÃO
       ===================================================== */

    div.stButton > button {
        border-radius: 12px;
        height: 48px;
        font-weight: 800;
        letter-spacing: 1px;
        border: none;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 8px 25px rgba(100,100,255,0.20);
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 600px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .main-title {
            font-size: 30px;
        }

        .result-perfection {
            font-size: 44px;
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

    st.markdown(
        '<div class="logo-container">',
        unsafe_allow_html=True
    )

    st.image(
        logo,
        width=180
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
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
    f'<div class="subtitle">{t["subtitle"]}</div>',
    unsafe_allow_html=True
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.markdown(
    f"""
    <div class="custom-card">
        <div class="section-title">
            ⚙️ {t["configuration"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


tipo = st.radio(
    t["lugh_type"],
    ["Lugh Normal", "Lugh Prismático"],
    horizontal=True
)


min_valor = TIPOS[tipo]["min"]
max_valor = TIPOS[tipo]["max"]
min_perfeicao = TIPOS[tipo]["min_perfeicao"]

cor = TIPOS[tipo]["color"]
glow = TIPOS[tipo]["glow"]


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
# BOTÃO
# ============================================================

if st.button(
    f"✨ {t['calculate']}",
    use_container_width=True
):

    # ========================================================
    # CONVERSÃO PERFECTION → SCORE
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

    if pontos <= centro_pontos:

        combinacoes_favoraveis = sum(
            quantidade
            for score, quantidade in dp.items()
            if score <= pontos
        )

        lado_curva = t["lower_tail"]

    else:

        combinacoes_favoraveis = sum(
            quantidade
            for score, quantidade in dp.items()
            if score >= pontos
        )

        lado_curva = t["upper_tail"]


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
        tier_desc = t["common_desc"]

    elif chance < 100:

        tier = t["rare"]
        tier_desc = t["rare_desc"]

    elif chance < 1000:

        tier = t["very_rare"]
        tier_desc = t["very_rare_desc"]

    else:

        tier = t["extremely_rare"]
        tier_desc = t["extremely_rare_desc"]


    # ========================================================
    # RESULTADO
    # ========================================================

    st.markdown(
        f"""
        <div
            class="result-card"
            style="
                --glow: {glow};
                border-color: {cor}35;
            "
        >

            <div class="result-label">
                {tipo}
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

            <div
                style="
                    color:#737D8D;
                    font-size:12px;
                    margin-top:8px;
                "
            >
                {tier_desc}
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
            <div class="metric-card">

                <div class="metric-title">
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
            <div class="metric-card">

                <div class="metric-title">
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
            <div class="metric-card">

                <div class="metric-title">
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
    # POSIÇÃO NA CURVA
    # ========================================================

    st.markdown(
        f"""
        <div
            style="
                text-align:center;
                color:#737D8D;
                font-size:12px;
                margin-top:18px;
            "
        >
            {t["distribution_position"]}: {lado_curva}
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CURVA
    # ========================================================

    st.markdown(
        f"""
        <div class="custom-card">

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


    chart_data = pd.DataFrame({
        "Score": scores,
        "Probability": probabilities
    })


    # ========================================================
    # GRÁFICO
    # ========================================================

    st.line_chart(
        chart_data,
        x="Score",
        y="Probability",
        height=380,
        use_container_width=True
    )


    # ========================================================
    # MARCADOR DO LUGH
    # ========================================================

    st.markdown(
        f"""
        <div
            style="
                text-align:center;
                margin-top:-5px;
                margin-bottom:15px;
            "
        >

            <span
                style="
                    display:inline-block;
                    padding:7px 14px;
                    border-radius:20px;
                    background:{cor}18;
                    border:1px solid {cor}40;
                    color:{cor};
                    font-size:12px;
                    font-weight:700;
                "
            >
                ✦ {t["your_lugh"]}: {pontos}
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # TIER BAR
    # ========================================================

    st.markdown(
        f"""
        <div class="tier-container">

            <div class="tier-bar"></div>

            <div class="tier-labels">

                <span>{t["common"]}</span>

                <span>{t["rare"]}</span>

                <span>{t["very_rare"]}</span>

                <span>{t["extremely_rare"]}</span>

            </div>

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
            {t["how_works_text"].strip().replace(chr(10), "<br>")}
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

        <h3>{t["prismatic"]}</h3>

        <p>
            {t["prismatic_text"].strip().replace(chr(10), "<br>")}
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
            {t["attributes_text"].strip().replace(chr(10), "<br>")}
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
```
