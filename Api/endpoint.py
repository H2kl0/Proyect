from fastapi import APIRouter
from pydantic import BaseModel
import replicate
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/generador",
    tags=["Generador de imágenes"],
    responses={404: {"description": "No encontrado"}}
)

class Prompt(BaseModel):
    prompt: str = "Una ciudad futurista al atardecer con rascacielos brillantes"

    class Config:
        schema_extra = {
            "example": {
                "prompt": "Un dragón volando sobre una ciudad futurista de noche"
            }
        }

@router.post("/generar", summary="Generar imagen desde texto", description="Envía un prompt de texto y devuelve una imagen generada por IA.")
async def generar(p: Prompt):
    output = replicate.run(
        "stability-ai/sdxl:latest",
        input={"prompt": p.prompt}
    )
    return {"imagen_url": output[0]}
