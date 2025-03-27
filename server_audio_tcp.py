#!/usr/bin/env python3
import socket
import os

HOST = 'localhost'
PORT = 9500
BUFSIZE = 1024
AUDIO_FILE = "audio.mp3"  # Cambia este nombre al de tu archivo de audio

def main():
    # Crear y configurar el socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"[Audio Server] Esperando conexión en {HOST}:{PORT}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[Audio Server] Conexión desde: {addr}")

        # Verificar que el archivo exista
        if not os.path.exists(AUDIO_FILE):
            print(f"[Audio Server] Archivo no encontrado: {AUDIO_FILE}")
            client_socket.sendall("0".encode('utf-8'))
            client_socket.close()
            continue

        # Enviar el tamaño del archivo
        file_size = os.path.getsize(AUDIO_FILE)
        client_socket.sendall(str(file_size).encode('utf-8'))

        # Esperar confirmación del cliente para iniciar la transferencia
        confirm = client_socket.recv(BUFSIZE)
        if confirm.decode('utf-8') != 'OK':
            print("[Audio Server] El cliente no confirmó la transferencia.")
            client_socket.close()
            continue

        # Enviar el archivo en bloques
        bytes_enviados = 0
        with open(AUDIO_FILE, "rb") as f:
            while True:
                data = f.read(BUFSIZE)
                if not data:
                    break
                client_socket.sendall(data)
                bytes_enviados += len(data)
        print(f"[Audio Server] Transferencia completada: {bytes_enviados} bytes enviados.")
        client_socket.close()

if __name__ == "__main__":
    main()
