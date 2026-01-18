from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ---------- JSON / textarea ----------

def test_api_produtivo_json():
    r = client.post("/classificar", json={"texto": "Erro no sistema ao acessar"})
    assert r.status_code == 200
    data = r.json()
    assert data["classificacao"] == "Produtivo"
    assert data["respostaSugerida"]


def test_api_improdutivo_json():
    r = client.post("/classificar", json={"texto": "Obrigado pelo atendimento"})
    assert r.status_code == 200
    data = r.json()
    assert data["classificacao"] == "Improdutivo"
    assert data["respostaSugerida"]


def test_api_texto_vazio_json():
    r = client.post("/classificar", json={"texto": ""})
    assert r.status_code == 422


# ---------- TXT / PDF ----------

def test_api_txt_upload():
    content = "Obrigado pelo excelente atendimento"
    files = {
        "file": ("email.txt", content.encode("utf-8"), "text/plain")
    }

    r = client.post("/classificar/arquivo", files=files)
    assert r.status_code == 200

    data = r.json()
    assert data["classificacao"] == "Improdutivo"
    assert data["respostaSugerida"]


def test_api_pdf_invalido_retorna_erro():
    files = {
        "file": ("email.pdf", b"%PDF-1.4 fake", "application/pdf")
    }

    r = client.post("/classificar/arquivo", files=files)

    # Pode variar conforme pdfplumber/pdfminer
    assert r.status_code in (400, 415, 422)
