from pydantic import BaseModel, Field

class EmailRequest(BaseModel):
    texto: str = Field(..., min_length=1)

class EmailResponse(BaseModel):
    classificacao: str
    justificativa: str
    resposta_sugerida: str = Field(..., serialization_alias="respostaSugerida")
