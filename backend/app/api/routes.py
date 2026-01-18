from fastapi import APIRouter, UploadFile, File
from app.schemas.email import EmailRequest, EmailResponse
from app.services.classifier_service import classificar_email
from app.services.response_service import gerar_resposta
from app.services.justification_service import gerar_justificativa
from app.services.file_reader_service import extrair_texto_de_upload

router = APIRouter()


# CLASSIFICAÇÃO VIA TEXTO (textarea / txt já convertido)
@router.post("/classificar", response_model=EmailResponse)
def classificar(req: EmailRequest):
    texto = req.texto

    resultado = classificar_email(texto)
    classificacao = resultado["classificacao"]

    justificativa = gerar_justificativa(
        texto=texto,
        classificacao=classificacao
    )

    resposta = gerar_resposta(classificacao)

    return EmailResponse(
        classificacao=classificacao,
        justificativa=justificativa,
        resposta_sugerida=resposta
    )


# CLASSIFICAÇÃO VIA ARQUIVO (TXT / PDF)

@router.post("/classificar/arquivo", response_model=EmailResponse)
async def classificar_arquivo(file: UploadFile = File(...)):
    texto = await extrair_texto_de_upload(file)

    resultado = classificar_email(texto)
    classificacao = resultado["classificacao"]

    justificativa = gerar_justificativa(
        texto=texto,
        classificacao=classificacao
    )

    resposta = gerar_resposta(classificacao)

    return EmailResponse(
        classificacao=classificacao,
        justificativa=justificativa,
        resposta_sugerida=resposta
    )
