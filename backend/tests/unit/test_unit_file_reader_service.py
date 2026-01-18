import io
import pytest
from fastapi import HTTPException
from starlette.datastructures import UploadFile, Headers

from app.services.file_reader_service import extrair_texto_de_upload

# Para gerar PDF válido em memória
from reportlab.pdfgen import canvas


def make_upload_file(
    filename: str,
    content: bytes,
    content_type: str | None = None,
) -> UploadFile:
    file_obj = io.BytesIO(content)

    headers = Headers({"content-type": content_type}) if content_type else Headers({})

    # OBS: Em várias versões do Starlette, UploadFile NÃO aceita content_type= no construtor.
    return UploadFile(file=file_obj, filename=filename, headers=headers)


def make_pdf_bytes(text: str) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(72, 720, text)
    c.showPage()
    c.save()
    return buffer.getvalue()


@pytest.mark.anyio
async def test_extrair_txt_utf8():
    up = make_upload_file(
        filename="email.txt",
        content="Olá, isso é um teste.".encode("utf-8"),
        content_type="text/plain",
    )

    texto = await extrair_texto_de_upload(up)
    assert "Olá" in texto


@pytest.mark.anyio
async def test_extrair_txt_latin1_fallback():
    conteudo = "ação".encode("latin-1")
    up = make_upload_file(
        filename="email.txt",
        content=conteudo,
        content_type="text/plain",
    )

    texto = await extrair_texto_de_upload(up)
    assert "ação" in texto


@pytest.mark.anyio
async def test_arquivo_vazio_retorna_422():
    up = make_upload_file(
        filename="vazio.txt",
        content=b"",
        content_type="text/plain",
    )

    with pytest.raises(HTTPException) as err:
        await extrair_texto_de_upload(up)

    assert err.value.status_code == 422


@pytest.mark.anyio
async def test_tipo_nao_suportado_retorna_415():
    up = make_upload_file(
        filename="imagem.png",
        content=b"fake",
        content_type="image/png",
    )

    with pytest.raises(HTTPException) as err:
        await extrair_texto_de_upload(up)

    assert err.value.status_code == 415


@pytest.mark.anyio
async def test_pdf_invalido_retorna_422():
    up = make_upload_file(
        filename="email.pdf",
        content=b"%PDF-1.4 fake",
        content_type="application/pdf",
    )

    with pytest.raises(HTTPException) as err:
        await extrair_texto_de_upload(up)

    assert err.value.status_code == 422


@pytest.mark.anyio
async def test_pdf_valido_extrai_texto():
    pdf_bytes = make_pdf_bytes("Teste PDF com texto")
    up = make_upload_file(
        filename="email.pdf",
        content=pdf_bytes,
        content_type="application/pdf",
    )

    texto = await extrair_texto_de_upload(up)
    assert "Teste PDF com texto" in texto
