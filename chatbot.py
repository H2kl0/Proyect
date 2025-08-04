import tkinter as tk
from tkinter import scrolledtext
import random


respuestas = {
    "hola": ["¡Hola! 👋 Soy tu amigo virtual. ¿En qué puedo ayudarte?", 
             "¡Bienvenido! 😊 ¿Cómo estás?"],
    "adiós": ["¡Hasta luego! 😊", "¡Nos vemos pronto!", "Adiós, que tengas un buen día 🌟"],
    "gracias": ["¡De nada! 🙌", "Me alegra ayudarte 💬", "Con gusto 😄"],
    "nombre": ["Me llamo ChatBot, pero puedes llamarme Boti 😊",
               "Soy un chatbot amigable, ¡y me encanta ayudar!"],
    "hora": ["Lo siento, no tengo acceso a la hora actual.",
             "Puedes revisar tu reloj o teléfono para ver la hora."],
    "clima": ["No puedo acceder al clima en tiempo real, pero espero que haga buen tiempo ☀️",
              "¡Desconozco el clima! Pero seguro está lindo afuera 🌤️"],
    "ayuda": ["Estoy aquí para ayudarte con preguntas simples. ¡Pregúntame lo que quieras!",
              "¿Necesitas ayuda con algo específico? 😊"],
    "default": ["Hmm... no entendí muy bien. ¿Podrías reformular?",
                "Lo siento, no tengo una respuesta para eso aún. ¡Prueba otra pregunta!",
                "Ups, esa no la tengo lista. ¿Quieres intentar otra cosa?"]
}


def obtener_respuesta(mensaje):
    mensaje = mensaje.lower()
    
    if "nombre" in mensaje:
        return random.choice(respuestas["nombre"])
    elif "hora" in mensaje:
        return random.choice(respuestas["hora"])
    elif "clima" in mensaje:
        return random.choice(respuestas["clima"])
    elif "ayuda" in mensaje or "puedes" in mensaje:
        return random.choice(respuestas["ayuda"])
    elif "hola" in mensaje:
        return random.choice(respuestas["hola"])
    elif "adiós" in mensaje:
        return random.choice(respuestas["adiós"])
    elif "gracias" in mensaje:
        return random.choice(respuestas["gracias"])
    else:
        return random.choice(respuestas["default"])


def enviar_mensaje():
    mensaje_usuario = entrada.get()
    if mensaje_usuario.strip() == "":
        return
    
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, "Tú: " + mensaje_usuario + "\n")
    chat.config(foreground="#000000", font="Arial 10")

    respuesta_bot = obtener_respuesta(mensaje_usuario)
    chat.insert(tk.END, "Boti: " + respuesta_bot + "\n\n")

    chat.config(state=tk.DISABLED)
    chat.yview(tk.END)
    entrada.delete(0, tk.END)


ventana = tk.Tk()
ventana.title("ChatBot Amigable 🤖")
ventana.geometry("500x600")
ventana.resizable(False, False)
ventana.configure(bg="#F0F8FF")

# Historial de chat
chat = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=60, height=30, bg="#FFFFFF", fg="#000000", font=("Arial", 10))
chat.config(state=tk.DISABLED)
chat.pack(padx=10, pady=10)


entrada = tk.Entry(ventana, font=("Arial", 12), width=40)
entrada.pack(pady=10)


boton_enviar = tk.Button(ventana, text="Enviar", font=("Arial", 12), bg="#4CAF50", fg="white", command=enviar_mensaje)
boton_enviar.pack()


ventana.mainloop()
