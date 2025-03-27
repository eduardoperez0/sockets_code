#!/usr/bin/env python3
import socket
import os

HOST = 'localhost'
PORT = 9501  # Puerto distinto para no interferir con el servidor de audio
BUFSIZE = 4096
# Ruta completa al archivo de video
VIDEO_FILE = "/home/debian/Descargas/WhatsApp Video 2025-03-27 at 1.51.17 PM.mp4"

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"[Video Server] Esperando conexión en {HOST}:{PORT}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[Video Server] Conexión desde: {addr}")

        if not os.path.exists(VIDEO_FILE):
            print(f"[Video Server] Archivo no encontrado: {VIDEO_FILE}")
            client_socket.sendall("0".encode('utf-8'))
            client_socket.close()
            continue

        # Enviar el tamaño del archivo
        file_size = os.path.getsize(VIDEO_FILE)
        client_socket.sendall(str(file_size).encode('utf-8'))

        # Esperar confirmación del cliente
        confirm = client_socket.recv(BUFSIZE)
        if confirm.decode('utf-8') != 'OK':
            print("[Video Server] El cliente no confirmó la transferencia.")
            client_socket.close()
            continue

        # Enviar el archivo en bloques
        bytes_enviados = 0
        with open(VIDEO_FILE, "rb") as f:
            while True:
                data = f.read(BUFSIZE)
                if not data:
                    break
                client_socket.sendall(data)
                bytes_enviados += len(data)
        print(f"[Video Server] Transferencia completada: {bytes_enviados} bytes enviados.")
        client_socket.close()

if __name__ == "__main__":
    main()
