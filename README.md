# 📧 Email Classifier – Produtivo vs Improdutivo

Aplicação web que infere a classificação de e-mails em **Produtivos** ou **Improdutivos**,
utilizando técnicas de **NLP e Machine Learning**, e sugere resposta automática
de acordo com a categoria identificada.

---

## 🚀 Tecnologias

- Python 3.11
- FastAPI
- Scikit-learn (TF-IDF + Logistic Regression)
- PDFPlumber
- HTML, CSS, TypeScript
- Pytest

---

## ⚙️ Como rodar localmente

```bash
git clone https://github.com/SEU_USUARIO/email-classifier.git
cd email-classifier/backend

python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Compilação TypeScript

Para compilar os arquivos TypeScript:

```bash
cd frontend
npm install
npx tsc
