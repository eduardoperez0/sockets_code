#!/usr/bin/env python3
import socket

HOST = 'localhost'
PORT = 9500
BUFSIZE = 1024
OUTPUT_FILE = "recibido_audio.mp3"  # Nombre para guardar el audio recibido

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"[Audio Client] Conectado a {HOST}:{PORT}")

    # Recibir el tamaño del archivo
    file_size_str = client_socket.recv(BUFSIZE).decode('utf-8')
    try:
        file_size = int(file_size_str)
    except ValueError:
        print("[Audio Client] Error al recibir el tamaño del archivo.")
        client_socket.close()
        return

    if file_size == 0:
        print("[Audio Client] El servidor indica que el archivo no existe o es de tamaño 0.")
        client_socket.close()
        return

    # Enviar confirmación para iniciar la transferencia
    client_socket.sendall(b"OK")
    print(f"[Audio Client] Recibiendo archivo de {file_size} bytes...")

    # Recibir y guardar el archivo
    bytes_recibidos = 0
    with open(OUTPUT_FILE, "wb") as f:
        while bytes_recibidos < file_size:
            data = client_socket.recv(BUFSIZE)
            if not data:
                break
            f.write(data)
            bytes_recibidos += len(data)
    print(f"[Audio Client] Transferencia completada: {bytes_recibidos} bytes recibidos.")
    client_socket.close()

if __name__ == "__main__":
    main()
