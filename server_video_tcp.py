#!/usr/bin/env python3
import socket
import os

HOST = 'localhost'
PORT = 9500
BUFSIZE = 4096  # Tamaño de bloque mayor para archivos grandes

# Diccionario con los videos disponibles: clave -> tipo solicitado, valor -> nombre del archivo
VIDEO_FILES = {
    'normal': 'video_normal.mp4',  # Asegúrate de que este archivo exista
    '4k': 'video_4k.mp4'           # Asegúrate de que este archivo exista
}

def send_file(client_socket, file_path):
    if not os.path.exists(file_path):
        client_socket.sendall("0".encode('utf-8'))
        print(f"[Video Server] Archivo no encontrado: {file_path}")
        return

    # Enviar el tamaño del archivo
    file_size = os.path.getsize(file_path)
    client_socket.sendall(str(file_size).encode('utf-8'))

    # Esperar confirmación del cliente
    confirm = client_socket.recv(BUFSIZE)
    if confirm.decode('utf-8') != 'OK':
        print("[Video Server] Cliente no confirmó la transferencia.")
        return

    print(f"[Video Server] Enviando '{file_path}' ({file_size} bytes)...")
    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUFSIZE)
            if not data:
                break
            client_socket.sendall(data)
    print("[Video Server] Transferencia completada.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[Video Server] Escuchando en {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[Video Server] Conexión desde: {addr}")

        # Recibir la solicitud del cliente (tipo de video: 'normal' o '4k')
        request = client_socket.recv(BUFSIZE).decode('utf-8').strip().lower()
        if request in VIDEO_FILES:
            print(f"[Video Server] Solicitud recibida: {request}")
            send_file(client_socket, VIDEO_FILES[request])
        else:
            client_socket.sendall("0".encode('utf-8'))
            print(f"[Video Server] Solicitud inválida: {request}")
        client_socket.close()

if __name__ == "__main__":
    main()
