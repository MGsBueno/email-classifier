def gerar_justificativa(texto: str, classificacao: str) -> str:
    texto_lower = texto.lower()

    if classificacao == "Produtivo":
        if any(p in texto_lower for p in ["erro", "problema", "falha"]):
            return (
                "O email foi classificado como produtivo pois relata um problema "
                "no sistema que exige análise ou correção."
            )

        if any(p in texto_lower for p in ["solicito", "favor", "necessário"]):
            return (
                "O email foi classificado como produtivo pois contém uma solicitação "
                "que requer retorno ou ação da equipe."
            )

        return (
            "O email foi classificado como produtivo pois apresenta uma demanda "
            "que exige acompanhamento ou resposta."
        )

    # Improdutivo
    if any(p in texto_lower for p in ["obrigado", "agradeço", "parabéns", "elogio"]):
        return (
            "O email foi classificado como improdutivo pois se trata de uma mensagem "
            "de agradecimento ou feedback, sem necessidade de ação."
        )

    return (
        "O email foi classificado como improdutivo pois não apresenta solicitação "
        "ou demanda que exija ação imediata."
    )
