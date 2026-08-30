```python
import streamlit as st
import plotly.graph_objects as go
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

    "normal": {
        "min": 1,
        "max": 25,
        "min_perfeicao": 4.0,
        "color": "#4CC9F0"
    },

    "prismatic": {
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

        "title":
            "✨ Calculadora de Perfection de Lugh",

        "subtitle":
            "Descubra o quão raro seu Lugh realmente é.",

        "configuration":
            "⚙️ Configuração",

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
            "RARIDADE",

        "equivalent":
            "Pontuação Equivalente",

        "probability":
            "Probabilidade Exata",

        "combinations":
            "Combinações Possíveis",

        "distribution":
            "📊 Distribuição de Raridade",

        "your_lugh":
            "SEU LUGH",

        "how":
            "📖 Como funciona a raridade?",

        "how_text":
            "A raridade é calculada utilizando a distribuição estatística de todas as combinações possíveis de atributos. Quanto mais próximo um Lugh estiver do centro da distribuição, mais comum ele será. Lughs com pontuações extremamente baixas ou extremamente altas são progressivamente mais raros.",

        "prismatic_title":
            "✨ Lughs Prismáticos",

        "prismatic_text":
            "Lughs Prismáticos possuem uma faixa de atributos diferente dos Lughs Normais. Por isso, sua raridade é calculada utilizando sua própria curva de distribuição.",

        "attributes":
            "📚 Sobre os Atributos dos Lughs",

        "attributes_text":
            "Cada Lugh possui 8 atributos. A pontuação total é determinada pela soma desses atributos. A calculadora compara essa pontuação com todas as combinações matematicamente possíveis para aquele tipo de Lugh.",

        "common":
            "Comum",

        "rare":
            "Raro",

        "very_rare":
            "Muito Raro",

        "extreme":
            "Extremamente Raro",

        "lower":
            "Cauda inferior",

        "upper":
            "Cauda superior",

        "center":
            "Centro",

        "score":
            "Pontuação",

        "probability_axis":
            "Probabilidade (%)",

        "position":
            "Posição na distribuição"
    },


    "en": {

        "title":
            "✨ Lugh Perfection Calculator",

        "subtitle":
            "Discover how rare your Lugh really is.",

        "configuration":
            "⚙️ Configuration",

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
            "RARITY",

        "equivalent":
            "Equivalent Score",

        "probability":
            "Exact Probability",

        "combinations":
            "Possible Combinations",

        "distribution":
            "📊 Rarity Distribution",

        "your_lugh":
            "YOUR LUGH",

        "how":
            "📖 How does rarity work?",

        "how_text":
            "Rarity is calculated using the statistical distribution of all possible attribute combinations. The closer a Lugh is to the center of the distribution, the more common it is. Lughs with extremely low or extremely high scores are progressively rarer.",

        "prismatic_title":
            "✨ Prismatic Lughs",

        "prismatic_text":
            "Prismatic Lughs have a different attribute range from Normal Lughs. Their rarity is therefore calculated using their own distribution curve.",

        "attributes":
            "📚 About Lugh Attributes",

        "attributes_text":
            "Each Lugh has 8 attributes. The total score is determined by adding these attributes together. The calculator compares this score against every mathematically possible combination for that type of Lugh.",

        "common":
            "Common",

        "rare":
            "Rare",

        "very_rare":
            "Very Rare",

        "extreme":
            "Extremely Rare",

        "lower":
            "Lower tail",

        "upper":
            "Upper tail",

        "center":
            "Center",

        "score":
            "Score",

        "probability_axis":
            "Probability (%)",

        "position":
            "Distribution position"
    }
}


# ============================================================
# SESSION STATE
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "pt"

if "result" not in st.session_state:
    st.session_state.result = None


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       FUNDO
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 50% -10%,
                rgba(100, 70, 255, 0.18),
                transparent 45%
            ),
            #080A0F;
    }


    /* ======================================================
       CONTAINER
       ====================================================== */

    .main .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }


    /* ======================================================
       LOGO
       ====================================================== */

    .logo-container {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
    }

    .logo-container img {
        width: 220px;
        max-width: 80%;
        height: auto;
        display: block;
    }


    /* ======================================================
       TÍTULO
       ====================================================== */

    h1 {
        text-align: center;
        font-weight: 800;
        letter-spacing: -1px;
    }


    /* ======================================================
       SUBTÍTULO
       ====================================================== */

    .subtitle {
        text-align: center;
        color: #8992A3;
        font-size: 16px;
        margin-top: -10px;
        margin-bottom: 25px;
    }


    /* ======================================================
       NÚMERO DE PERFECTION
       ====================================================== */

    .perfection-number {
        text-align: center;
        font-size: 58px;
        font-weight: 900;
        margin-top: 15px;
        line-height: 1.1;
    }


    /* ======================================================
       TÍTULO RARIDADE
       ====================================================== */

    .rarity-title {
        text-align: center;
        color: #858E9E;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 20px;
    }


    /* ======================================================
       NÚMERO RARIDADE
       ====================================================== */

    .rarity-number {
        text-align: center;
        font-size: 46px;
        font-weight: 900;
        margin-top: 5px;
    }


    /* ======================================================
       TIER
       ====================================================== */

    .tier {
        text-align: center;
        color: #AAB2C0;
        font-weight: 700;
        margin-bottom: 25px;
    }


    /* ======================================================
       BOTÕES
       ====================================================== */

    div.stButton > button {
        border-radius: 12px;
        min-height: 45px;
        font-weight: 700;
    }


    /* ======================================================
       MÉTRICAS
       ====================================================== */

    div[data-testid="stMetric"] {
        background:
            rgba(255,255,255,0.035);

        border:
            1px solid rgba(255,255,255,0.07);

        border-radius: 16px;
        padding: 15px;
    }


    div[data-testid="stMetricValue"] {
        font-size: 21px;
    }


    /* ======================================================
       EXPANDERS
       ====================================================== */

    div[data-testid="stExpander"] {
        border-radius: 14px;
        border-color:
            rgba(255,255,255,0.08);
    }


    /* ======================================================
       RESPONSIVIDADE
       ====================================================== */

    @media (max-width: 600px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .perfection-number {
            font-size: 45px;
        }

        .rarity-number {
            font-size: 36px;
        }

        h1 {
            font-size: 30px;
        }

        .logo-container img {
            width: 180px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TEXTOS
# ============================================================

t = TEXT[st.session_state.language]


# ============================================================
# LOGO
# ============================================================

try:

    logo = Image.open("logo.png")

    # Centraliza a logo utilizando columns do Streamlit
    logo_left, logo_center, logo_right = st.columns(
        [1, 2, 1]
    )

    with logo_center:

        st.image(
            logo,
            width=220
        )

except FileNotFoundError:

    st.warning(
        "Arquivo logo.png não encontrado."
    )


# ============================================================
# TÍTULO
# ============================================================

st.title(
    t["title"]
)


# ============================================================
# SUBTÍTULO
# ============================================================

st.markdown(
    f"""
    <div class="subtitle">
        {t["subtitle"]}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# IDIOMAS
# ============================================================

lang_left, lang_pt, lang_en, lang_right = st.columns(
    [2, 1, 1, 2]
)


with lang_pt:

    if st.button(
        "🇧🇷 Português",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.language == "pt"
            else "secondary"
        )
    ):

        if st.session_state.language != "pt":

            st.session_state.language = "pt"
            st.rerun()


with lang_en:

    if st.button(
        "🇺🇸 English",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.language == "en"
            else "secondary"
        )
    ):

        if st.session_state.language != "en":

            st.session_state.language = "en"
            st.rerun()


# Atualiza idioma

t = TEXT[st.session_state.language]


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

    for _ in range(
        quantidade_atributos
    ):

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


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.divider()


with st.container(border=True):

    st.subheader(
        t["configuration"]
    )

    with st.form(
        "calculator_form"
    ):

        tipo_visual = st.radio(

            t["lugh_type"],

            [
                t["normal"],
                t["prismatic"]
            ],

            horizontal=True
        )


        if tipo_visual == t["normal"]:

            tipo = "normal"

        else:

            tipo = "prismatic"


        configuracao = TIPOS[tipo]

        min_valor = configuracao["min"]

        max_valor = configuracao["max"]

        min_perfeicao = (
            configuracao["min_perfeicao"]
        )


        perfeicao = st.number_input(

            t["perfection"],

            min_value=min_perfeicao,

            max_value=100.0,

            value=min_perfeicao,

            step=0.01,

            format="%.2f"
        )


        calcular = st.form_submit_button(

            f"✨ {t['calculate']}",

            use_container_width=True
        )


# ============================================================
# CÁLCULO
# ============================================================

if calcular:

    dp = calcular_distribuicao(

        ATRIBUTOS,

        min_valor,

        max_valor
    )


    min_pontos = (
        ATRIBUTOS * min_valor
    )

    max_pontos = (
        ATRIBUTOS * max_valor
    )


    quantidade_valores = (
        max_valor
        - min_valor
        + 1
    )


    combinacoes_totais = (
        quantidade_valores
        ** ATRIBUTOS
    )


    # --------------------------------------------------------
    # PERFECTION → SCORE
    # --------------------------------------------------------

    proporcao = (
        (perfeicao - min_perfeicao)
        /
        (100.0 - min_perfeicao)
    )


    pontos = round(

        min_pontos
        +
        proporcao
        *
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
        min_pontos
        +
        max_pontos
    ) / 2


    # --------------------------------------------------------
    # CAUDA
    # --------------------------------------------------------

    if pontos < centro_pontos:

        combinacoes_favoraveis = sum(

            quantidade

            for score, quantidade
            in dp.items()

            if score <= pontos
        )

        lado_curva = t["lower"]


    elif pontos > centro_pontos:

        combinacoes_favoraveis = sum(

            quantidade

            for score, quantidade
            in dp.items()

            if score >= pontos
        )

        lado_curva = t["upper"]


    else:

        combinacoes_favoraveis = sum(

            quantidade

            for score, quantidade
            in dp.items()

            if score <= pontos
        )

        lado_curva = t["center"]


    combinacoes_favoraveis = max(
        1,
        combinacoes_favoraveis
    )


    porcentagem_real = (
        combinacoes_favoraveis
        /
        combinacoes_totais
    ) * 100


    chance = (
        combinacoes_totais
        /
        combinacoes_favoraveis
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


    # --------------------------------------------------------
    # SALVA RESULTADO
    # --------------------------------------------------------

    st.session_state.result = {

        "tipo":
            tipo,

        "tipo_visual":
            tipo_visual,

        "perfeicao":
            perfeicao,

        "pontos":
            pontos,

        "max_pontos":
            max_pontos,

        "chance":
            chance,

        "porcentagem_real":
            porcentagem_real,

        "combinacoes_totais":
            combinacoes_totais,

        "dp":
            dp,

        "min_pontos":
            min_pontos,

        "max_pontos":
            max_pontos,

        "cor":
            configuracao["color"],

        "lado_curva":
            lado_curva,

        "tier":
            tier
    }


# ============================================================
# RESULTADO
# ============================================================

if st.session_state.result is not None:

    resultado = st.session_state.result

    tipo = resultado["tipo"]

    cor = resultado["cor"]

    pontos = resultado["pontos"]

    max_pontos = resultado["max_pontos"]

    perfeicao = resultado["perfeicao"]

    chance = resultado["chance"]

    porcentagem_real = (
        resultado["porcentagem_real"]
    )

    combinacoes_totais = (
        resultado["combinacoes_totais"]
    )

    dp = resultado["dp"]

    min_pontos = resultado["min_pontos"]

    max_pontos = resultado["max_pontos"]

    lado_curva = resultado["lado_curva"]

    tier = resultado["tier"]


    # ========================================================
    # RESULTADO PRINCIPAL
    # ========================================================

    st.divider()


    st.subheader(
        resultado["tipo_visual"]
    )


    st.markdown(
        f"""
        <div
            class="perfection-number"
            style="color:{cor};"
        >
            {perfeicao:.2f}%
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="rarity-title">
            {t["rarity"]}
        </div>

        <div
            class="rarity-number"
            style="color:{cor};"
        >
            1 in {chance:,.0f}
        </div>

        <div class="tier">
            {tier}
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # MÉTRICAS
    # ========================================================

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
        f"{t['position']}: "
        f"{lado_curva}"
    )


    # ========================================================
    # GRÁFICO
    # ========================================================

    st.divider()


    st.subheader(
        t["distribution"]
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
            /
            combinacoes_totais
        ) * 100

        for score in scores
    ]


    probabilidade_score = (
        dp[pontos]
        /
        combinacoes_totais
    ) * 100


    # ========================================================
    # PLOTLY
    # ========================================================

    fig = go.Figure()


    if tipo == "normal":

        fill_color = (
            "rgba(76,201,240,0.12)"
        )

    else:

        fill_color = (
            "rgba(217,70,239,0.12)"
        )


    fig.add_trace(

        go.Scatter(

            x=scores,

            y=probabilities,

            mode="lines",

            name=t["distribution"],

            line=dict(

                color=cor,

                width=4,

                shape="spline"
            ),

            fill="tozeroy",

            fillcolor=fill_color,

            hovertemplate=(

                f"{t['score']}: %{{x}}"

                f"<br>"

                f"{t['probability_axis']}: "

                f"%{{y:.8f}}%"

                "<extra></extra>"
            )
        )
    )


    fig.add_vline(

        x=pontos,

        line_width=2,

        line_dash="dash",

        line_color=cor
    )


    fig.add_trace(

        go.Scatter(

            x=[pontos],

            y=[probabilidade_score],

            mode="markers",

            name=t["your_lugh"],

            marker=dict(

                size=18,

                color=cor,

                line=dict(

                    color="white",

                    width=3
                )
            ),

            hovertemplate=(

                f"{t['perfection']}: "

                f"{perfeicao:.2f}%"

                f"<br>"

                f"{t['score']}: "

                f"{pontos}"

                f"<br>"

                f"{t['probability']}: "

                f"{porcentagem_real:.9f}%"

                "<extra></extra>"
            )
        )
    )


    # ========================================================
    # LAYOUT
    # ========================================================

    fig.update_layout(

        height=460,

        margin=dict(
            l=15,
            r=15,
            t=25,
            b=45
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#8992A3"
        ),

        xaxis=dict(

            title=t["score"],

            gridcolor=
                "rgba(255,255,255,0.05)",

            zeroline=False
        ),

        yaxis=dict(

            title=t["probability_axis"],

            gridcolor=
                "rgba(255,255,255,0.05)",

            zeroline=False
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
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
            "displayModeBar": False,
            "responsive": True
        }
    )


    # ========================================================
    # ESCALA DE RARIDADE
    # ========================================================

    scale1, scale2, scale3, scale4 = st.columns(4)


    with scale1:

        st.caption(
            f"● {t['common']}"
        )


    with scale2:

        st.caption(
            f"● {t['rare']}"
        )


    with scale3:

        st.caption(
            f"● {t['very_rare']}"
        )


    with scale4:

        st.caption(
            f"● {t['extreme']}"
        )


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


st.markdown(
    f"""
    <div style="
        text-align: center;
        color: #697386;
        font-size: 13px;
        padding: 10px 0 20px 0;
    ">
        ✨ Lugh Perfection Calculator
        • Version {APP_VERSION}
        • Created by Caio "Laion" Melo
    </div>
    """,
    unsafe_allow_html=True
)
```
