#!/usr/bin/env python3

import socket
import sys

HOST = 'localhost'  # Debe coincidir con la IP del servidor
PORT = 9500
BUFSIZE = 1024

def main():
    try:
        # Crear socket TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket de cliente creado.")
    except Exception as err:
        print("No se pudo crear el socket:", err)
        sys.exit(1)

    try:
        # Conectar con el servidor
        client_socket.connect((HOST, PORT))
        print(f"Conectado al servidor en {HOST}:{PORT}")
    except Exception as err:
        print("Falla de conexión:", err)
        client_socket.close()
        sys.exit(1)

    try:
        # Enviar mensaje al servidor
        mensaje = "Hola desde el cliente TCP"
        client_socket.sendall(mensaje.encode('utf-8'))
        
        # Recibir respuesta del servidor
        respuesta = client_socket.recv(BUFSIZE)
        print("Respuesta del servidor:", respuesta.decode('utf-8'))
    except Exception as err:
        print("Error al enviar/recibir datos:", err)
    finally:
        # Cerrar socket
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()
