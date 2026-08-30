import streamlit as st
import plotly.graph_objects as go
import base64
import math
import streamlit.components.v1 as components


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
            "✨ Calculadora de Perfeição de Lugh",

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
            "Each Lugh has 8 attributes. The total score is determined by adding these attributes together. The calculator compares this score against every mathematically possible combination for that type.",

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

    .stApp {
        background:
            radial-gradient(
                circle at 50% -10%,
                rgba(100, 70, 255, 0.18),
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
        letter-spacing: -1px;
    }


    .subtitle {
        text-align: center;
        color: #8992A3;
        font-size: 16px;
        margin-top: -10px;
        margin-bottom: 25px;
    }


    .logo-wrapper {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
    }


    .logo-wrapper img {
        width: 220px;
        max-width: 75%;
        height: auto;
        display: block;
    }


    .perfection-number {
        text-align: center;
        font-size: 58px;
        font-weight: 900;
        margin-top: 15px;
        line-height: 1.1;
    }


    .rarity-title {
        text-align: center;
        color: #858E9E;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 20px;
    }


    .rarity-number {
        text-align: center;
        font-size: 46px;
        font-weight: 900;
        margin-top: 5px;
    }


    .tier {
        text-align: center;
        color: #AAB2C0;
        font-weight: 700;
        margin-bottom: 25px;
    }


    div.stButton > button {
        border-radius: 12px;
        min-height: 45px;
        font-weight: 700;
    }


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


    div[data-testid="stExpander"] {
        border-radius: 14px;
        border-color:
            rgba(255,255,255,0.08);
    }


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

        .logo-wrapper img {
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

t = TEXT[
    st.session_state.language
]


# ============================================================
# LOGO
# ============================================================

logo_left, logo_center, logo_right = st.columns(
    [1, 2, 1]
)


with logo_center:

    try:

        with open(
            "logo.png",
            "rb"
        ) as f:

            logo_base64 = (
                base64.b64encode(
                    f.read()
                ).decode()
            )


        st.markdown(
            f"""
            <div class="logo-wrapper">
                <img
                    src="data:image/png;base64,{logo_base64}"
                >
            </div>
            """,
            unsafe_allow_html=True
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


t = TEXT[
    st.session_state.language
]


# ============================================================
# DISTRIBUIÇÃO
# ============================================================

@st.cache_data
def calcular_distribuicao(
    quantidade_atributos,
    minimo,
    maximo
):

    dp = {
        0: 1
    }


    for _ in range(
        quantidade_atributos
    ):

        proximo_dp = {}


        for soma, quantidade in dp.items():

            for valor in range(
                minimo,
                maximo + 1
            ):

                nova_soma = (
                    soma + valor
                )


                proximo_dp[
                    nova_soma
                ] = (

                    proximo_dp.get(
                        nova_soma,
                        0
                    )
                    +
                    quantidade
                )


        dp = proximo_dp


    return dp


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.divider()


with st.container(
    border=True
):

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


        configuracao = TIPOS[
            tipo
        ]


        min_valor = configuracao[
            "min"
        ]


        max_valor = configuracao[
            "max"
        ]


        min_perfeicao = configuracao[
            "min_perfeicao"
        ]


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
        ATRIBUTOS
        *
        min_valor
    )


    max_pontos = (
        ATRIBUTOS
        *
        max_valor
    )


    quantidade_valores = (

        max_valor
        -
        min_valor
        +
        1
    )


    combinacoes_totais = (

        quantidade_valores
        **
        ATRIBUTOS
    )


    # --------------------------------------------------------
    # PERFECTION → SCORE
    # --------------------------------------------------------

    proporcao = (

        perfeicao
        -
        min_perfeicao

    ) / (

        100.0
        -
        min_perfeicao
    )


    pontos = round(

        min_pontos

        +

        proporcao
        *
        (
            max_pontos
            -
            min_pontos
        )
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


        lado_curva = t[
            "lower"
        ]


    elif pontos > centro_pontos:

        combinacoes_favoraveis = sum(

            quantidade

            for score, quantidade
            in dp.items()

            if score >= pontos
        )


        lado_curva = t[
            "upper"
        ]


    else:

        combinacoes_favoraveis = sum(

            quantidade

            for score, quantidade
            in dp.items()

            if score <= pontos
        )


        lado_curva = t[
            "center"
        ]


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

        tier = t[
            "common"
        ]

    elif chance < 100:

        tier = t[
            "rare"
        ]

    elif chance < 1000:

        tier = t[
            "very_rare"
        ]

    else:

        tier = t[
            "extreme"
        ]


    # --------------------------------------------------------
    # POSIÇÃO VISUAL DA RARIDADE
    #
    # A barra é baseada em CHANCE e não em PERFECTION.
    #
    # Centro:
    #       50%
    #
    # 1 em 10:
    #       aproximadamente região de Raro
    #
    # 1 em 100:
    #       região de Muito Raro
    #
    # 1 em 1000:
    #       extremo
    #
    # Escala logarítmica para representar melhor
    # as diferenças de raridade.
    # --------------------------------------------------------

    if pontos == centro_pontos:

        posicao_barra = 50.0

    else:

        chance_visual = max(
            1.0,
            min(
                chance,
                1000.0
            )
        )


        nivel = (

            math.log10(
                chance_visual
            )
            /
            3.0
        )


        distancia = (
            nivel * 50.0
        )


        if pontos < centro_pontos:

            posicao_barra = (
                50.0
                -
                distancia
            )

        else:

            posicao_barra = (
                50.0
                +
                distancia
            )


    posicao_barra = max(
        2.0,
        min(
            98.0,
            posicao_barra
        )
    )


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

        "min_pontos":
            min_pontos,

        "max_pontos":
            max_pontos,

        "min_perfeicao":
            min_perfeicao,

        "chance":
            chance,

        "porcentagem_real":
            porcentagem_real,

        "combinacoes_totais":
            combinacoes_totais,

        "dp":
            dp,

        "cor":
            configuracao[
                "color"
            ],

        "lado_curva":
            lado_curva,

        "tier":
            tier,

        "posicao_barra":
            posicao_barra
    }


# ============================================================
# RESULTADO
# ============================================================

if st.session_state.result is not None:

    resultado = (
        st.session_state.result
    )


    tipo = resultado[
        "tipo"
    ]


    cor = resultado[
        "cor"
    ]


    pontos = resultado[
        "pontos"
    ]


    min_pontos = resultado[
        "min_pontos"
    ]


    max_pontos = resultado[
        "max_pontos"
    ]


    min_perfeicao = resultado[
        "min_perfeicao"
    ]


    perfeicao = resultado[
        "perfeicao"
    ]


    chance = resultado[
        "chance"
    ]


    porcentagem_real = resultado[
        "porcentagem_real"
    ]


    combinacoes_totais = resultado[
        "combinacoes_totais"
    ]


    dp = resultado[
        "dp"
    ]


    lado_curva = resultado[
        "lado_curva"
    ]


    tier = resultado[
        "tier"
    ]


    posicao_barra = resultado[
        "posicao_barra"
    ]


    # ========================================================
    # RESULTADO PRINCIPAL
    # ========================================================

    st.divider()


    st.subheader(
        resultado[
            "tipo_visual"
        ]
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

    col1, col2, col3 = st.columns(
        3
    )


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
        f"{t['position']}: {lado_curva}"
    )


    # ========================================================
    # GRÁFICO
    # ========================================================

    st.divider()


    st.subheader(
        t["distribution"]
    )


    # Todas as pontuações possíveis
    scores = list(
        range(
            min_pontos,
            max_pontos + 1
        )
    )


    # Converte pontuação em Perfection
    perfection_values = [

        min_perfeicao

        +

        (
            (
                score
                -
                min_pontos
            )
            /
            (
                max_pontos
                -
                min_pontos
            )
        )

        *

        (
            100.0
            -
            min_perfeicao
        )

        for score in scores
    ]


    probabilities = [

        (
            dp[score]
            /
            combinacoes_totais
        )

        *

        100

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

            x=perfection_values,

            y=probabilities,

            mode="lines",

            name=t[
                "distribution"
            ],

            line=dict(

                color=cor,

                width=4,

                shape="spline"
            ),

            fill="tozeroy",

            fillcolor=fill_color,

            hovertemplate=(

                f"{t['perfection']}: "

                f"%{{x:.2f}}%"

                "<br>"

                f"{t['probability_axis']}: "

                f"%{{y:.8f}}%"

                "<extra></extra>"
            )
        )
    )


    # Linha do Lugh
    fig.add_vline(

        x=perfeicao,

        line_width=2,

        line_dash="dash",

        line_color=cor
    )


    # Marcador do Lugh
    fig.add_trace(

        go.Scatter(

            x=[perfeicao],

            y=[probabilidade_score],

            mode="markers",

            name=t[
                "your_lugh"
            ],

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

                "<br>"

                f"{t['probability']}: "

                f"{porcentagem_real:.9f}%"

                "<extra></extra>"
            )
        )
    )


    # ========================================================
    # LAYOUT DO GRÁFICO
    # ========================================================

    fig.update_layout(

        height=460,

        margin=dict(

            l=15,

            r=15,

            t=25,

            b=45
        ),

        paper_bgcolor=(
            "rgba(0,0,0,0)"
        ),

        plot_bgcolor=(
            "rgba(0,0,0,0)"
        ),

        font=dict(
            color="#8992A3"
        ),

        xaxis=dict(

            title=t[
                "perfection"
            ],

            range=[
                min_perfeicao,
                100
            ],

            ticksuffix="%",

            gridcolor=(
                "rgba(255,255,255,0.05)"
            ),

            zeroline=False
        ),

        yaxis=dict(

            title=t[
                "probability_axis"
            ],

            gridcolor=(
                "rgba(255,255,255,0.05)"
            ),

            zeroline=False
        ),

        legend=dict(

            bgcolor=(
                "rgba(0,0,0,0)"
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
            "displayModeBar": False,
            "responsive": True
        }
    )


    # ========================================================
    # POSIÇÃO NA DISTRIBUIÇÃO
    # ========================================================

    st.divider()


    st.subheader(
        f"📊 {t['position']}"
    )


    # ========================================================
    # BARRA DE RARIDADE
    #
    # Renderizada em componente HTML isolado para evitar
    # que o Streamlit mostre o HTML como texto.
    # ========================================================

    html_barra = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <style>

            * {{
                box-sizing: border-box;
            }}


            html,
            body {{
                margin: 0;
                padding: 0;

                background: transparent;

                overflow: hidden;
            }}


            body {{
                font-family:
                    -apple-system,
                    BlinkMacSystemFont,
                    "Segoe UI",
                    sans-serif;
            }}


            .container {{
                width: 100%;

                padding:
                    12px 4px 0 4px;
            }}


            .bar {{
                position: relative;

                width: 100%;

                height: 14px;

                border-radius: 10px;

                background:
                    linear-gradient(
                        to right,

                        #F43F5E 0%,

                        #C084FC 16.67%,

                        #60A5FA 33.33%,

                        #4CC9F0 50%,

                        #60A5FA 66.67%,

                        #C084FC 83.33%,

                        #F43F5E 100%
                    );

                box-shadow:
                    0 0 12px
                    rgba(
                        76,
                        201,
                        240,
                        0.15
                    );
            }}


            .marker {{
                position: absolute;

                left:
                    {posicao_barra:.2f}%;

                top: 50%;

                width: 22px;

                height: 22px;

                transform:
                    translate(
                        -50%,
                        -50%
                    );

                border-radius: 50%;

                background:
                    {cor};

                border:
                    3px solid white;

                box-shadow:
                    0 0 10px {cor};

                z-index: 10;
            }}


            .labels {{
                display: grid;

                grid-template-columns:
                    repeat(
                        7,
                        minmax(0, 1fr)
                    );

                width: 100%;

                margin-top: 14px;

                align-items: start;
            }}


            .label {{
                text-align: center;

                color: #8992A3;

                font-size: 10px;

                font-weight: 600;

                line-height: 1.2;

                padding:
                    0 2px;
            }}


            .icon {{
                font-size: 22px;

                line-height: 22px;

                margin-bottom: 6px;
            }}


            @media (max-width: 600px) {{

                .label {{
                    font-size: 8px;
                }}

                .icon {{
                    font-size: 18px;
                }}

            }}

        </style>

    </head>


    <body>

        <div class="container">


            <div class="bar">

                <div class="marker"></div>

            </div>


            <div class="labels">


                <div class="label">

                    <div class="icon">
                        🔴
                    </div>

                    {t["extreme"]}

                </div>


                <div class="label">

                    <div class="icon">
                        🟣
                    </div>

                    {t["very_rare"]}

                </div>


                <div class="label">

                    <div class="icon">
                        🔵
                    </div>

                    {t["rare"]}

                </div>


                <div class="label">

                    <div class="icon">
                        🔷
                    </div>

                    {t["common"]}

                </div>


                <div class="label">

                    <div class="icon">
                        🔵
                    </div>

                    {t["rare"]}

                </div>


                <div class="label">

                    <div class="icon">
                        🟣
                    </div>

                    {t["very_rare"]}

                </div>


                <div class="label">

                    <div class="icon">
                        🔴
                    </div>

                    {t["extreme"]}

                </div>


            </div>

        </div>

    </body>

    </html>
    """


    components.html(

        html_barra,

        height=105,

        scrolling=False
    )


    # ========================================================
    # INFORMAÇÕES
    # ========================================================

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
        text-align:center;
        color:#697386;
        font-size:13px;
        padding:10px 0 20px 0;
    ">

        ✨ Lugh Perfection Calculator

        • Version {APP_VERSION}

        • Created by Caio "Laion" Melo

    </div>
    """,
    unsafe_allow_html=True
)
