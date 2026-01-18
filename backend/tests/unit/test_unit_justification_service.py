from app.services.justification_service import gerar_justificativa


def test_justificativa_produtivo_para_erro_menciona_motivo():
    texto = "Estou com erro no sistema e não consigo acessar"
    j = gerar_justificativa(texto=texto, classificacao="Produtivo")

    assert isinstance(j, str)
    assert len(j.strip()) > 0
    # Deve ter sentido: falar de problema/ação
    assert ("problema" in j.lower()) or ("erro" in j.lower()) or ("ação" in j.lower())


def test_justificativa_produtivo_para_solicitacao_menciona_solicitacao():
    texto = "Solicito suporte para ajustar meu acesso"
    j = gerar_justificativa(texto=texto, classificacao="Produtivo")

    assert isinstance(j, str)
    assert len(j.strip()) > 0
    assert ("solicit" in j.lower()) or ("retorno" in j.lower()) or ("ação" in j.lower())


def test_justificativa_improdutivo_para_agradecimento_menciona_feedback():
    texto = "Obrigado pelo atendimento, parabéns pela equipe!"
    j = gerar_justificativa(texto=texto, classificacao="Improdutivo")

    assert isinstance(j, str)
    assert len(j.strip()) > 0
    assert ("agradec" in j.lower()) or ("feedback" in j.lower()) or ("elog" in j.lower())


def test_justificativa_improdutivo_generica_nao_vazia():
    texto = "Bom dia, tudo bem?"
    j = gerar_justificativa(texto=texto, classificacao="Improdutivo")

    assert isinstance(j, str)
    assert len(j.strip()) > 0
