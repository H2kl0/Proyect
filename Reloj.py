#In this project the idea is to show a digital clock with the Tkinter library
import tkinter as tk
import time

def actualizar_reloj():
    hora_actual = time.strftime("%H:%M:%S")
    etiqueta.config(text=hora_actual)
    ventana.after(1000, actualizar_reloj)

ventana = tk.Tk()
ventana.title("Reloj Digital")

etiqueta = tk.Label(ventana, font=("Arial", 48), fg="black")
etiqueta.pack(padx=20, pady=20)

actualizar_reloj()

ventana.mainloop();
