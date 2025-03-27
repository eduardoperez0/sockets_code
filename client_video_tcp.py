#!/usr/bin/env python3
import socket
import sys

HOST = 'localhost'
PORT = 9500
BUFSIZE = 4096

def receive_file(client_socket, output_file):
    # Recibir el tamaño del archivo
    file_size_str = client_socket.recv(BUFSIZE).decode('utf-8')
    try:
        file_size = int(file_size_str)
    except ValueError:
        print("[Video Client] Error al recibir el tamaño del archivo.")
        return

    if file_size == 0:
        print("[Video Client] El servidor indica que el archivo no existe o es de tamaño 0.")
        return

    # Confirmar para iniciar la transferencia
    client_socket.sendall(b"OK")
    print(f"[Video Client] Recibiendo archivo de {file_size} bytes... Guardando como '{output_file}'")

    bytes_recibidos = 0
    with open(output_file, "wb") as f:
        while bytes_recibidos < file_size:
            data = client_socket.recv(BUFSIZE)
            if not data:
                break
            f.write(data)
            bytes_recibidos += len(data)
    print(f"[Video Client] Transferencia completada: {bytes_recibidos} bytes recibidos.")

def main():
    # Validar argumentos: se debe indicar el tipo de video ('normal' o '4k')
    if len(sys.argv) != 2 or sys.argv[1] not in ['normal', '4k']:
        print("Uso: python3 client_video_tcp.py [normal|4k]")
        sys.exit(1)
    video_type = sys.argv[1].lower()
    output_file = f"recibido_{video_type}.mp4"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"[Video Client] Conectado a {HOST}:{PORT}")

    # Enviar solicitud de video al servidor
    client_socket.sendall(video_type.encode('utf-8'))
    receive_file(client_socket, output_file)
    client_socket.close()

if __name__ == "__main__":
    main()
