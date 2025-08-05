from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import replicate
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.post("/generar", response_class=HTMLResponse)
async def generar(request: Request, prompt: str = Form(...)):
    output = replicate.run(
        "stability-ai/sdxl@7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
        input={"prompt": prompt}
    )
    return templates.TemplateResponse("formulario.html", {"request": request, "imagen": output[0]})
