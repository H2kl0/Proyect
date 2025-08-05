import requests

prompt = input("Escribe tu prompt: ")

response = requests.post("http://127.0.0.1:8000/generar", json={
    "prompt": prompt
})

print("Imagen generada:", response.json()["imagen_url"])
