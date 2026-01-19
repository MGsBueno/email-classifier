from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes import router
from app.config.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# CORS (em produção você trocar para o domínio do Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas da API
app.include_router(router, prefix=settings.API_PREFIX)

# Servir FRONT (static)
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Serve /static/*
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Página inicial em /
@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")
