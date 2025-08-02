import psutil
import tkinter as tk
from plyer import notification
from datetime import datetime

# CONFIGURACIÓN
UMBRAL_BATERIA_BAJA = 25
UMBRAL_CPU = 95
INTERVALO_MS = 60000  # 60 segundos en milisegundos para tkinter

# VARIABLES DE ESTADO
estado_anterior = psutil.sensors_battery().power_plugged
conexion_hora = None
ultima_notificacion_bateria_baja = False

# VENTANA PRINCIPAL
root = tk.Tk()
root.title("Estado del Sistema")
root.geometry("300x180")
root.resizable(False, False)

label_bateria = tk.Label(root, text="", font=("Arial", 14))
label_bateria.pack(pady=10)

label_estado = tk.Label(root, text="", font=("Arial", 12))
label_estado.pack(pady=5)

label_cpu = tk.Label(root, text="", font=("Arial", 12))
label_cpu.pack(pady=5)

label_hora = tk.Label(root, text="", font=("Arial", 10), fg="gray")
label_hora.pack(pady=10)

# FUNCIONES
def actualizar_estado():
    global estado_anterior, conexion_hora, ultima_notificacion_bateria_baja

    # Batería
    bateria = psutil.sensors_battery()
    porcentaje = bateria.percent
    conectado = bateria.power_plugged

    # CPU
    uso_cpu = psutil.cpu_percent(interval=1)

    # Mostrar en la ventana
    estado_txt = "Cargando " if conectado else "Batería "
    label_bateria.config(text=f"Batería: {porcentaje}%")
    label_estado.config(text=f"Estado: {estado_txt}")
    label_cpu.config(text=f"CPU: {uso_cpu}%")
    label_hora.config(text=datetime.now().strftime("Actualizado: %H:%M:%S"))

    # Notificación CPU
    if uso_cpu >= UMBRAL_CPU:
        notification.notify(
            title=" CPU alta",
            message=f"Uso de CPU al {uso_cpu}%.",
            timeout=5
        )

    # Notificación batería baja
    if porcentaje < UMBRAL_BATERIA_BAJA and not conectado and not ultima_notificacion_bateria_baja:
        notification.notify(
            title=" Batería baja",
            message=f"Solo {porcentaje}% restante. Conecta el cargador.",
            timeout=5
        )
        ultima_notificacion_bateria_baja = True
    elif porcentaje >= UMBRAL_BATERIA_BAJA or conectado:
        ultima_notificacion_bateria_baja = False

    # Notificación por cambio de conexión
    if conectado and not estado_anterior:
        conexion_hora = datetime.now().strftime("%H:%M:%S")
        notification.notify(
            title=" Conectado",
            message=f"Conectado a corriente a las {conexion_hora}.",
            timeout=5
        )
    elif not conectado and estado_anterior:
        notification.notify(
            title=" Desconectado",
            message="El equipo se ha desconectado de la corriente.",
            timeout=5
        )
        conexion_hora = None

    estado_anterior = conectado  # Actualizar para la próxima verificación

    # Programar próxima actualización
    root.after(INTERVALO_MS, actualizar_estado)

# INICIAR CICLO
actualizar_estado()
root.mainloop()
