from fastapi import FastAPI
from pydantic import BaseModel
import replicate
import os
from dotenv import load_dotenv
import requests
load_dotenv()

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/generar")
def generar(p: Prompt):

    output = replicate.run(
        "stability-ai/sdxl:latest",
        input={"prompt": p.prompt}
    )

    return {"imagen_url": output[0]}

