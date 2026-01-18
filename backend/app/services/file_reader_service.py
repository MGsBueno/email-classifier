from __future__ import annotations

import io
from starlette.datastructures import UploadFile
from fastapi import HTTPException
import pdfplumber


ALLOWED_TEXT_TYPES = {"text/plain"}
ALLOWED_PDF_TYPES = {"application/pdf"}


async def extrair_texto_de_upload(file: UploadFile) -> str:
    """
    Extrai texto de um UploadFile (.txt ou .pdf).

    - TXT: decodifica bytes para string
    - PDF: extrai texto usando pdfplumber
    - PDF inválido / sem texto → HTTP 422
    - Tipo não suportado → HTTP 415
    """
    content_type = (file.content_type or "").lower()
    filename = (file.filename or "").lower()

    try:
        file_bytes = await file.read()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Falha ao ler o arquivo enviado."
        )

    if not file_bytes:
        raise HTTPException(
            status_code=422,
            detail="Arquivo vazio. Envie um arquivo com conteúdo."
        )

    # TXT
    if content_type in ALLOWED_TEXT_TYPES or filename.endswith(".txt"):
        texto = _decode_txt(file_bytes).strip()
        if not texto:
            raise HTTPException(
                status_code=422,
                detail="TXT sem conteúdo legível."
            )
        return texto

    # PDF
    if content_type in ALLOWED_PDF_TYPES or filename.endswith(".pdf"):
        texto = _extrair_pdf(file_bytes).strip()
        if not texto:
            raise HTTPException(
                status_code=422,
                detail="PDF sem texto legível (pode ser escaneado ou imagem)."
            )
        return texto

    raise HTTPException(
        status_code=415,
        detail="Tipo de arquivo não suportado. Envie .txt ou .pdf."
    )


def _decode_txt(file_bytes: bytes) -> str:
    """
    Decodifica bytes de TXT tentando UTF-8 e fallback para latin-1.
    """
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1", errors="ignore")


def _extrair_pdf(file_bytes: bytes) -> str:
    """
    Extrai texto de PDF usando pdfplumber.
    PDF inválido / corrompido → HTTP 422.
    """
    try:
        texto_total: list[str] = []

        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    texto_total.append(t)

        return "\n".join(texto_total)

    except Exception:
        raise HTTPException(
            status_code=422,
            detail="PDF inválido ou corrompido."
        )
