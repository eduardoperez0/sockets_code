#!/usr/bin/env python3
import socket

HOST = 'localhost'
PORT = 9501
BUFSIZE = 4096
# Nombre del archivo donde se guardará el video recibido
OUTPUT_FILE = "recibido_video.mp4"

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"[Video Client] Conectado a {HOST}:{PORT}")

    # Recibir el tamaño del archivo
    file_size_str = client_socket.recv(BUFSIZE).decode('utf-8')
    try:
        file_size = int(file_size_str)
    except ValueError:
        print("[Video Client] Error al recibir el tamaño del archivo.")
        client_socket.close()
        return

    if file_size == 0:
        print("[Video Client] El servidor indica que el archivo no existe o es de tamaño 0.")
        client_socket.close()
        return

    # Enviar confirmación para iniciar la transferencia
    client_socket.sendall(b"OK")
    print(f"[Video Client] Recibiendo archivo de {file_size} bytes...")

    bytes_recibidos = 0
    with open(OUTPUT_FILE, "wb") as f:
        while bytes_recibidos < file_size:
            data = client_socket.recv(BUFSIZE)
            if not data:
                break
            f.write(data)
            bytes_recibidos += len(data)
    print(f"[Video Client] Transferencia completada: {bytes_recibidos} bytes recibidos.")
    client_socket.close()

if __name__ == "__main__":
    main()
