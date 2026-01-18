from app.services.response_service import gerar_resposta


def test_resposta_produtivo_tem_tom_de_atendimento():
    msg = gerar_resposta("Produtivo")
    assert isinstance(msg, str)
    assert len(msg.strip()) > 0
    assert "Recebemos" in msg or "solicitação" in msg or "analisar" in msg


def test_resposta_improdutivo_tem_tom_de_encerramento():
    msg = gerar_resposta("Improdutivo")
    assert isinstance(msg, str)
    assert len(msg.strip()) > 0
    assert "Obrigado" in msg or "não é necessária" in msg


def test_resposta_para_classificacao_desconhecida_cai_no_default():
    msg = gerar_resposta("QualquerCoisa")
    assert isinstance(msg, str)
    assert len(msg.strip()) > 0
