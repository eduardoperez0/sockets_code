#!/usr/bin/env python3

import socket
import sys

HOST = 'localhost'   # Puedes usar '0.0.0.0' si quieres escuchar en todas las interfaces
PORT = 9500
BUFSIZE = 1024
ADDR = (HOST, PORT)

def main():
    try:
        # Crear socket TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Reutilizar la dirección para evitar errores de "Address already in use"
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Enlazar el socket a la dirección y puerto
        server_socket.bind(ADDR)
        
        # Poner el socket en modo "escucha"
        server_socket.listen(5)  # Permite hasta 5 conexiones en cola
        print(f"Servidor TCP esperando conexiones en {ADDR}...")
    except Exception as err:
        print("Error al iniciar el servidor:", err)
        sys.exit(1)

    while True:
        # Aceptar una conexión entrante
        client_socket, client_addr = server_socket.accept()
        print(f"Cliente conectado desde: {client_addr}")

        try:
            # Recibir datos del cliente
            data = client_socket.recv(BUFSIZE)
            if not data:
                print("No se recibieron datos, cerrando conexión.")
                client_socket.close()
                continue
            
            print("Mensaje del cliente:", data.decode('utf-8'))
            
            # Enviar respuesta al cliente
            respuesta = "¡Hola, cliente! Mensaje recibido."
            client_socket.sendall(respuesta.encode('utf-8'))
        except Exception as err:
            print("Error al recibir/enviar datos:", err)
        finally:
            # Cerrar la conexión con este cliente
            client_socket.close()
            print("Conexión con el cliente cerrada.")

if __name__ == "__main__":
    main()
