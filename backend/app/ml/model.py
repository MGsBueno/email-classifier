from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from typing import Tuple

# Normalização
def normalize(text: str) -> str:
    """
    Normaliza texto para reduzir variações:
    - lowercase
    - remove acentos
    - remove pontuação
    - normaliza espaços
    """
    text = (text or "").lower().strip()

    # remove acentos (técnico -> tecnico)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

    # troca pontuação por espaço
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # colapsa espaços
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Dataset inicial 
TRAIN_DATA: list[tuple[str, str]] = [
    # Produtivo (requer ação/resposta)
    ("Estou com erro no sistema ao acessar", "Produtivo"),
    ("Nao consigo fazer login na plataforma", "Produtivo"),
    ("Preciso de ajuda para acessar minha conta", "Produtivo"),
    ("Solicito suporte tecnico para resolver um problema", "Produtivo"),
    ("O sistema esta travando e preciso de retorno", "Produtivo"),
    ("Favor verificar meu acesso, esta dando falha", "Produtivo"),
    ("Tenho uma duvida sobre como usar o sistema", "Produtivo"),
    ("Meu chamado esta em aberto, pode atualizar o status", "Produtivo"),
    ("Nao consigo redefinir minha senha", "Produtivo"),
    ("Pode me orientar sobre essa funcionalidade", "Produtivo"),

    # Improdutivo (não requer ação imediata)
    ("Obrigado pelo atendimento", "Improdutivo"),
    ("Agradeco o retorno", "Improdutivo"),
    ("Parabens pelo trabalho da equipe", "Improdutivo"),
    ("Elogio ao suporte, voces foram otimos", "Improdutivo"),
    ("Felicidades a todos", "Improdutivo"),
    ("So passando para agradecer", "Improdutivo"),
    ("Mensagem de agradecimento", "Improdutivo"),
    ("Bom dia, tudo bem?", "Improdutivo"),
    ("Excelente trabalho, parabens", "Improdutivo"),
    ("So informando que deu tudo certo, obrigado", "Improdutivo"),
]

TEXTS = [t[0] for t in TRAIN_DATA]
LABELS = [t[1] for t in TRAIN_DATA]


# Pipeline de ML (leve)
_pipeline = Pipeline(
    steps=[
        (
            "tfidf",
            TfidfVectorizer(
                preprocessor=normalize,
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.9,
                sublinear_tf=True,
            ),
        ),
        ("clf", LogisticRegression(max_iter=400)),
    ]
)

_pipeline.fit(TEXTS, LABELS)


@dataclass(frozen=True)
class EmailClassifierModel:
    pipeline: Pipeline

    def predict_with_confidence(self, texto: str) -> Tuple[str, float]:
        # scikit retorna ndarray; convertemos
        proba = self.pipeline.predict_proba([texto])[0]
        classes = list(self.pipeline.classes_)  # ex: ["Improdutivo", "Produtivo"]

        # pega a classe mais provável
        best_idx = int(proba.argmax())
        label = str(classes[best_idx])
        conf = float(proba[best_idx])
        return label, conf

    def predict(self, texto: str) -> str:
        label, _ = self.predict_with_confidence(texto)
        return label

# Singleton (modelo carregado uma vez)
model = EmailClassifierModel(_pipeline)
