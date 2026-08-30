import streamlit as st


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
        "max": 25,
        "min_perfeicao": 4.0
    },

    "Lugh Prismático": {
        "min": 12,
        "max": 25,
        "min_perfeicao": 48.0
    }
}


# ==========================================
# CALCULA A DISTRIBUIÇÃO EXATA
# ==========================================

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
min_perfeicao = TIPOS[tipo]["min_perfeicao"]


# ==========================================
# PONTUAÇÃO MÍNIMA E MÁXIMA
# ==========================================

min_pontos = ATRIBUTOS * min_valor
max_pontos = ATRIBUTOS * max_valor


# Quantidade de valores possíveis por atributo
quantidade_valores = max_valor - min_valor + 1


# Número total de combinações possíveis
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
# INPUT
# ==========================================

perfeicao = st.number_input(
    "Perfection",
    min_value=min_perfeicao,
    max_value=100.0,
    value=min_perfeicao,
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

    # ======================================
    # CONVERSÃO PERFECTION → SCORE
    # ======================================

    # A escala é diretamente proporcional:
    #
    # NORMAL
    # 4%   → 16/200
    # 80%  → 160/200
    # 100% → 200/200
    #
    # PRISMÁTICO
    # 48%  → 96/200
    # 60%  → 120/200
    # 100% → 200/200

    proporcao = (
        (perfeicao - min_perfeicao)
        / (100.0 - min_perfeicao)
    )

    pontos = round(
        min_pontos
        + proporcao * (max_pontos - min_pontos)
    )


    # ======================================
    # GARANTE OS LIMITES
    # ======================================

    pontos = max(
        min_pontos,
        min(pontos, max_pontos)
    )


    # ======================================
    # CENTRO DA DISTRIBUIÇÃO
    # ======================================

    centro_pontos = (
        min_pontos + max_pontos
    ) / 2


    # ======================================
    # DECIDE QUAL CAUDA DA CURVA USAR
    # ======================================

    # A distribuição é simétrica.
    #
    # Perfection abaixo do centro:
    # procuramos a cauda inferior.
    #
    # Perfection acima do centro:
    # procuramos a cauda superior.
    #
    # Isso garante:
    #
    # 100% ↔ mínimo
    # 99%  ↔ 5%
    # 98%  ↔ 6%
    # etc.

    if pontos <= centro_pontos:

        combinacoes_favoraveis = sum(
            quantidade
            for score, quantidade in dp.items()
            if score <= pontos
        )

    else:

        combinacoes_favoraveis = sum(
            quantidade
            for score, quantidade in dp.items()
            if score >= pontos
        )


    # ======================================
    # SEGURANÇA
    # ======================================

    combinacoes_favoraveis = max(
        1,
        combinacoes_favoraveis
    )


    # ======================================
    # PROBABILIDADE REAL
    # ======================================

    porcentagem_real = (
        combinacoes_favoraveis
        / combinacoes_totais
    ) * 100


    # ======================================
    # RARIDADE
    # ======================================

    chance = (
        combinacoes_totais
        / combinacoes_favoraveis
    )


    # ======================================
    # RESULTADO
    # ======================================

    st.divider()

    st.subheader(tipo)

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


    # ======================================
    # INFORMAÇÃO DA POSIÇÃO NA CURVA
    # ======================================

    if pontos < centro_pontos:

        lado_curva = "Lower tail"

    elif pontos > centro_pontos:

        lado_curva = "Upper tail"

    else:

        lado_curva = "Center"


    st.caption(
        f"Distribution position: {lado_curva}"
    )


    # ======================================
    # CURVA
    # ======================================

    st.divider()

    st.subheader("Rarity Distribution")


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
        "The closer a score is to the center of the curve, "
        "the more common it is. Extreme values are rarer."
    )
