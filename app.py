import streamlit as st
import math

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Lugh Perfection Calculator",
    page_icon="✨",
    layout="centered"
)


# ==========================================
# CONFIGURAÇÕES
# ==========================================

ATRIBUTOS = 8

TIPOS = {
    "Lugh Normal": {
        "min": 1,
        "max": 25
    },
    "Lugh Prismático": {
        "min": 12,
        "max": 25
    }
}


# ==========================================
# CALCULA A DISTRIBUIÇÃO EXATA
# ==========================================

@st.cache_data
def calcular_distribuicao(quantidade_atributos, minimo, maximo):

    dp = {0: 1}

    for _ in range(quantidade_atributos):

        proximo_dp = {}

        for soma, quantidade in dp.items():

            for valor in range(minimo, maximo + 1):

                nova_soma = soma + valor

                proximo_dp[nova_soma] = (
                    proximo_dp.get(nova_soma, 0)
                    + quantidade
                )

        dp = proximo_dp

    return dp


# ==========================================
# INTERFACE
# ==========================================

st.title("✨ Lugh Perfection Calculator")

st.write(
    "Discover how rare your Lugh's attributes are."
)

st.divider()


# ==========================================
# ESCOLHA DO TIPO
# ==========================================

tipo = st.radio(
    "Tipo de Lugh",
    ["Lugh Normal", "Lugh Prismático"],
    horizontal=True
)

min_valor = TIPOS[tipo]["min"]
max_valor = TIPOS[tipo]["max"]

min_pontos = ATRIBUTOS * min_valor
max_pontos = ATRIBUTOS * max_valor

quantidade_valores = max_valor - min_valor + 1

combinacoes_totais = quantidade_valores ** ATRIBUTOS


# ==========================================
# DISTRIBUIÇÃO
# ==========================================

dp = calcular_distribuicao(
    ATRIBUTOS,
    min_valor,
    max_valor
)


# ==========================================
# INPUT DE PERFEIÇÃO
# ==========================================

perfeicao = st.number_input(
    "Perfection",
    min_value=4.0,
    max_value=100.0,
    value=50.0,
    step=0.01,
    format="%.2f"
)


# ==========================================
# BOTÃO
# ==========================================

if st.button(
    "CALCULATE",
    use_container_width=True
):

    # --------------------------------------
    # TRANSFORMA % EM PONTUAÇÃO
    # --------------------------------------

    proporcao = (perfeicao - 4) / 96

    pontos = round(
        min_pontos
        + proporcao * (max_pontos - min_pontos)
    )

    # --------------------------------------
    # GARANTE OS LIMITES
    # --------------------------------------

    pontos = max(
        min_pontos,
        min(pontos, max_pontos)
    )

    # --------------------------------------
    # COMBINAÇÕES PARA ESSA PONTUAÇÃO
    # --------------------------------------

    combinacoes_favoraveis = dp[pontos]

    # --------------------------------------
    # CHANCE
    # --------------------------------------

    chance = (
        combinacoes_totais
        / combinacoes_favoraveis
    )

    porcentagem_real = (
        combinacoes_favoraveis
        / combinacoes_totais
    ) * 100

    # --------------------------------------
    # RESULTADO
    # --------------------------------------

    st.divider()

    st.subheader(
        f"{tipo}"
    )

    st.markdown(
        f"### {perfeicao:.2f}% Perfection"
    )

    st.metric(
        "Rarity",
        f"1 in {chance:,.0f}"
    )

    st.write(
        f"**Equivalent score:** "
        f"{pontos} / {max_pontos}"
    )

    st.write(
        f"**Exact probability:** "
        f"{porcentagem_real:.9f}%"
    )

    st.write(
        f"**Possible combinations:** "
        f"{combinacoes_totais:,}"
    )

    st.divider()

    # ======================================
    # CURVA DE DISTRIBUIÇÃO
    # ======================================

    st.subheader("Rarity Distribution")

    scores = list(range(min_pontos, max_pontos + 1))

    frequencies = [
        dp[score]
        for score in scores
    ]

    # Normaliza para porcentagem
    probabilities = [
        (frequency / combinacoes_totais) * 100
        for frequency in frequencies
    ]

    # Mostra a curva usando o gráfico nativo
    chart_data = {
        "Score": scores,
        "Probability": probabilities
    }

    st.line_chart(
        chart_data,
        x="Score",
        y="Probability",
        use_container_width=True
    )

    st.caption(
        "The center of the curve represents the most common "
        "attribute combinations. The extremes are the rarest."
    )
