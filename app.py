import streamlit as st

st.set_page_config(
    page_title="Lugh Perfection Calculator",
    page_icon="🎯",
    layout="centered"
)

# CONFIGURAÇÕES
ATRIBUTOS = 8
MIN_VALOR = 1
MAX_VALOR = 25

MIN_PONTOS = ATRIBUTOS * MIN_VALOR
MAX_PONTOS = ATRIBUTOS * MAX_VALOR

COMBINACOES_TOTAIS = MAX_VALOR ** ATRIBUTOS


# CALCULA AS COMBINAÇÕES
@st.cache_data
def calcular_combinacoes():

    dp = {0: 1}

    for _ in range(ATRIBUTOS):

        proximo_dp = {}

        for pontos, quantidade in dp.items():

            for valor in range(MIN_VALOR, MAX_VALOR + 1):

                nova_soma = pontos + valor

                proximo_dp[nova_soma] = (
                    proximo_dp.get(nova_soma, 0) + quantidade
                )

        dp = proximo_dp

    return dp


dp = calcular_combinacoes()


# INTERFACE
st.title("🎯 Lugh Perfection Calculator")

st.write(
    "Discover how rare your Lugh's attribute combination is."
)

st.divider()

perfeicao = st.number_input(
    "Digite a porcentagem de perfeição",
    min_value=4.0,
    max_value=100.0,
    value=50.0,
    step=0.01,
    format="%.2f"
)


if st.button("CALCULAR", use_container_width=True):

    proporcao = (perfeicao - 4) / 96

    pontos = round(
        MIN_PONTOS +
        proporcao * (MAX_PONTOS - MIN_PONTOS)
    )

    combinacoes_favoraveis = dp[pontos]

    chance = (
        COMBINACOES_TOTAIS /
        combinacoes_favoraveis
    )

    porcentagem_real = (
        combinacoes_favoraveis /
        COMBINACOES_TOTAIS
    ) * 100

    st.divider()

    st.subheader(
        f"Resultado para {perfeicao:.2f}% de perfeição"
    )

    st.metric(
        "Chance",
        f"1 em {chance:,.2f}"
    )

    st.write(
        f"**Pontuação equivalente:** "
        f"{pontos} / {MAX_PONTOS}"
    )

    st.write(
        f"**Chance real:** "
        f"{porcentagem_real:.9f}%"
    )
