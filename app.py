import streamlit as st
import pandas as pd
from PIL import Image


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Lugh Perfection Calculator",
    page_icon="✨",
    layout="centered"
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
        "glow": "rgba(76, 201, 240, 0.18)"
    },

    "Lugh Prismático": {
        "min": 12,
        "max": 25,
        "min_perfeicao": 48.0,
        "color": "#D946EF",
        "glow": "rgba(217, 70, 239, 0.18)"
    }
}


# ============================================================
# TRADUÇÕES
# ============================================================

TEXT = {

    "pt": {
        "subtitle": "Descubra o quão raro seu Lugh realmente é.",
        "configuration": "Configuração",
        "lugh_type": "Tipo de Lugh",
        "normal": "Lugh Normal",
        "prismatic": "Lugh Prismático",
        "perfection": "Perfection",
        "calculate": "CALCULAR",
        "rarity": "Raridade",
        "equivalent_score": "Pontuação Equivalente",
        "exact_probability": "Probabilidade Exata",
        "possible_combinations": "Combinações Possíveis",
        "distribution": "Distribuição de Raridade",
        "lower_tail": "Cauda inferior",
        "upper_tail": "Cauda superior",
        "center": "Centro",
        "common": "Comum",
        "rare": "Raro",
        "very_rare": "Muito Raro",
        "extremely_rare": "Extremamente Raro",
        "how_works": "Como funciona a raridade?",
        "how_works_text": "A raridade é calculada utilizando a distribuição estatística de todas as combinações possíveis de atributos. Quanto mais próximo um Lugh estiver do centro da distribuição, mais comum ele será. Lughs com pontuações extremamente baixas ou extremamente altas são progressivamente mais raros.",
        "prismatic_title": "✨ Lughs Prismáticos",
        "prismatic_text": "Lughs Prismáticos possuem uma faixa de atributos diferente dos Lughs Normais. Por isso, sua raridade é calculada utilizando sua própria distribuição de atributos.",
        "attributes": "Sobre os Atributos dos Lughs",
        "attributes_text": "Cada Lugh possui 8 atributos. A pontuação total é determinada pela soma desses atributos. A calculadora compara essa pontuação com todas as combinações matematicamente possíveis para aquele tipo de Lugh.",
        "your_lugh": "SEU LUGH",
        "distribution_position": "Posição na distribuição",
        "footer": "Lugh Perfection Calculator"
    },

    "en": {
        "subtitle": "Discover how rare your Lugh really is.",
        "configuration": "Configuration",
        "lugh_type": "Lugh Type",
        "normal": "Lugh Normal",
        "prismatic": "Lugh Prismatic",
        "perfection": "Perfection",
        "calculate": "CALCULATE",
        "rarity": "Rarity",
        "equivalent_score": "Equivalent Score",
        "exact_probability": "Exact Probability",
        "possible_combinations": "Possible Combinations",
        "distribution": "Rarity Distribution",
        "lower_tail": "Lower tail",
        "upper_tail": "Upper tail",
        "center": "Center",
        "common": "Common",
        "rare": "Rare",
        "very_rare": "Very Rare",
        "extremely_rare": "Extremely Rare",
        "how_works": "How does rarity work?",
        "how_works_text": "Rarity is calculated using the statistical distribution of all possible attribute combinations. The closer a Lugh is to the center of the distribution, the more common it is. Lughs with extremely low or extremely high scores are progressively rarer.",
        "prismatic_title": "✨ Prismatic Lughs",
        "prismatic_text": "Prismatic Lughs have a different attribute range from Normal Lughs. Their rarity is therefore calculated using their own attribute distribution.",
        "attributes": "About Lugh Attributes",
        "attributes_text": "Each Lugh has 8 attributes. The total score is determined by adding these attributes together. The calculator compares this score against every mathematically possible combination for that type of Lugh.",
        "your_lugh": "YOUR LUGH",
        "distribution_position": "Distribution position",
        "footer": "Lugh Perfection Calculator"
    }
}


# ============================================================
# IDIOMA
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "en"

language_col1, language_col2, language_col3 = st.columns([1, 1, 1])

with language_col2:

    idioma = st.radio(
        "Language",
        ["🇺🇸 English", "🇧🇷 Português"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if idioma == "🇧🇷 Português":
        st.session_state.language = "pt"
    else:
        st.session_state.language = "en"

t = TEXT[st.session_state.language]


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       PÁGINA
       ========================= */

    .stApp {
        background:
            radial-gradient(
                circle at 50% -15%,
                rgba(115, 80, 255, 0.16),
                transparent 42%
            ),
            #080A0F;
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }


    /* =========================
       HEADER
       ========================= */

    .logo-wrapper {
        text-align: center;
        margin-bottom: 10px;
    }

    .logo-wrapper img {
        max-width: 180px;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 850;
        letter-spacing: -1px;
        color: white;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #8992A3;
        font-size: 16px;
        margin-bottom: 35px;
    }


    /* =========================
       CARDS
       ========================= */

    .card {
        background: rgba(20, 23, 32, 0.90);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 24px;
        margin-top: 15px;
        margin-bottom: 20px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.20);
    }

    .card-title {
        font-size: 18px;
        font-weight: 750;
        color: white;
        margin-bottom: 12px;
    }


    /* =========================
       RESULTADO
       ========================= */

    .result-card {
        border-radius: 25px;
        padding: 35px 20px;
        text-align: center;
        margin-top: 28px;
        margin-bottom: 22px;

        background:
            radial-gradient(
                circle at 50% 0%,
                var(--glow),
                transparent 60%
            ),
            #11141D;

        border: 1px solid var(--accent-border);

        box-shadow:
            0 15px 50px rgba(0,0,0,0.28);
    }

    .result-type {
        color: #8992A3;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 12px;
        margin-bottom: 10px;
    }

    .result-perfection {
        font-size: 58px;
        line-height: 1;
        font-weight: 900;
        color: white;
    }

    .result-perfection-label {
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
        line-height: 1.1;
        font-weight: 900;
        margin-top: 5px;
    }

    .rarity-tier {
        display: inline-block;
        padding: 7px 16px;
        margin-top: 12px;
        border-radius: 30px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        color: #E3E7EE;
        font-size: 13px;
        font-weight: 700;
    }


    /* =========================
       MÉTRICAS
       ========================= */

    .metric {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 17px;
        padding: 18px 10px;
        text-align: center;
        min-height: 88px;
    }

    .metric-label {
        color: #737D8D;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        color: white;
        font-size: 17px;
        font-weight: 750;
        margin-top: 9px;
    }


    /* =========================
       TIER
       ========================= */

    .tier-bar {
        height: 9px;
        border-radius: 20px;
        background: linear-gradient(
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


    /* =========================
       INFO
       ========================= */

    .info-card {
        background: rgba(20,23,32,0.75);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 25px;
        margin-top: 20px;
    }

    .info-card h3 {
        color: white;
        margin-bottom: 12px;
    }

    .info-card p {
        color: #9AA3B2;
        line-height: 1.75;
        font-size: 14px;
    }


    /* =========================
       BOTÃO
       ========================= */

    div.stButton > button {
        height: 50px;
        border-radius: 13px;
        font-size: 14px;
        font-weight: 850;
        letter-spacing: 1px;
        border: none;
        transition: 0.2s;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(120,100,255,0.25);
    }


    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;
        color: #505866;
        font-size: 12px;
        margin-top: 45px;
        padding-top: 22px;
        border-top: 1px solid rgba(255,255,255,0.05);
    }


    /* =========================
       MOBILE
       ========================= */

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

    st.markdown(
        '<div class="logo-wrapper">',
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
# TÍTULO
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
    <div class="card">
        <div class="card-title">
            ⚙️ {t["configuration"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


tipo = st.radio(
    t["lugh_type"],
    [t["normal"], t["prismatic"]],
    horizontal=True
)


if tipo == t["normal"]:
    tipo_codigo = "Lugh Normal"
else:
    tipo_codigo = "Lugh Prismático"


min_valor = TIPOS[tipo_codigo]["min"]
max_valor = TIPOS[tipo_codigo]["max"]
min_perfeicao = TIPOS[tipo_codigo]["min_perfeicao"]

cor = TIPOS[tipo_codigo]["color"]
glow = TIPOS[tipo_codigo]["glow"]


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
# PERFECTION
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
    # CENTRO DA DISTRIBUIÇÃO
    # ========================================================

    centro_pontos = (
        min_pontos + max_pontos
    ) / 2


    # ========================================================
    # CAUDA DA DISTRIBUIÇÃO
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
    # RESULTADO PRINCIPAL
    # ========================================================

    st.markdown(
        f"""
        <div
            class="result-card"
            style="
                --glow: {glow};
                --accent-border: {cor}45;
            "
        >

            <div class="result-type">
                {tipo}
            </div>

            <div class="result-perfection">
                {perfeicao:.2f}%
            </div>

            <div class="result-perfection-label">
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
    # POSIÇÃO
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
        <div class="card">

            <div class="card-title">
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


    st.line_chart(
        chart_data,
        x="Score",
        y="Probability",
        height=380,
        use_container_width=True
    )


    # ========================================================
    # MARCADOR
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
                padding:7px 15px;
                border-radius:20px;
                background:{cor}18;
                border:1px solid {cor}40;
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
