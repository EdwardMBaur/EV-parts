from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import Base, engine

from app.models import *

from app.routers import auth, usuarios, enderecos, categorias, veiculos, pecas, pedidos, pagamentos, logistica


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.APP_ENV == "development":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "API do marketplace EV.parts — compra e venda de peças para veículos elétricos. "
        "Compatibilidade técnica garantida por dados (VIN/OEM/SoH) com logística especializada."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://ev.parts"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(enderecos.router)
app.include_router(categorias.router)
app.include_router(veiculos.router)
app.include_router(pecas.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)
app.include_router(logistica.router)


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "env": settings.APP_ENV,
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
