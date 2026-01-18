from app.ml.model import model, normalize

MIN_CHARS = 10
MIN_WORDS = 3
MIN_CONFIDENCE = 0.50


def classificar_email(texto: str) -> dict:
    texto_limpo = (texto or "").strip()
    texto_norm = normalize(texto_limpo)

    # 1) Texto vazio
    if not texto_norm:
        return {
            "classificacao": "Improdutivo",
            "justificativa": (
                "O email está vazio ou não contém conteúdo suficiente "
                "para exigir ação."
            ),
        }

    # 2) Texto curto / sem contexto
    palavras = texto_norm.split()
    if len(texto_norm) < MIN_CHARS or len(palavras) < MIN_WORDS:
        return {
            "classificacao": "Improdutivo",
            "justificativa": (
                "O conteúdo é muito curto e não apresenta contexto "
                "suficiente para indicar uma solicitação ou ação necessária."
            ),
        }

    # 3) Classificação com confiança
    classificacao, confianca = model.predict_with_confidence(texto_limpo)

    # 4) Baixa confiança → improdutivo por segurança
    if confianca < MIN_CONFIDENCE:
        return {
            "classificacao": "Improdutivo",
            "justificativa": (
                "O conteúdo não apresenta sinais claros de solicitação "
                "ou problema, e a confiança da classificação foi baixa."
            ),
        }

    # 5) Casos normais (confiança ok)
    if classificacao == "Produtivo":
        return {
            "classificacao": "Produtivo",
            "justificativa": (
                "O email foi classificado como produtivo porque apresenta "
                "indícios claros de solicitação, problema relatado ou "
                "necessidade de retorno por parte da equipe."
            ),
        }

    # 6) Fallback explícito (improdutivo)
    return {
        "classificacao": "Improdutivo",
        "justificativa": (
            "O email foi classificado como improdutivo por não apresentar "
            "uma demanda clara que exija ação imediata."
        ),
    }
