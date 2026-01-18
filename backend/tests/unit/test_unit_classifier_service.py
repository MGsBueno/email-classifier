from app.services.classifier_service import classificar_email

def test_texto_curto_sem_contexto_retorna_improdutivo():
    r = classificar_email("meu carro")
    assert r["classificacao"] == "Improdutivo"
    assert "curto" in r["justificativa"].lower() or "contexto" in r["justificativa"].lower()
