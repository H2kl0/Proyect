from fastapi import FastAPI
from endpoints import router

app = FastAPI(
    title="Generador de Imágenes IA",
    description="API para generar imágenes usando texto y modelos de Replicate",
    version="1.0.0"
)

app.include_router(router)
