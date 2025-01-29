import socket
import threading
from Graph import Graph

class ServerTCP:
    def __init__(self, host = "127.0.0.1", port = 65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.grafo = Graph()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Configuración del servidor
    def iniciar(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Servidor escuchando en {self.host}:{self.port}")

        while True:
            try:
                conn, addr = self.server_socket.accept()
                print(f"Cliente conectado desde {addr}")
                self.clients.append(conn)
                hilo = threading.Thread(target=self.manejar_cliente, args=(conn, addr))
                hilo.start()
            except OSError:
                # Si el socket fue cerrado, termina el bucle
                break


    def manejar_cliente(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                comando, *args = data.split()
                if comando == "agregar_usuario":
                    respuesta = self.grafo.agregar_usuario(*args)
                elif comando == "autenticar":
                    autenticado, mensaje = self.grafo.autenticar_usuario(*args)
                    respuesta = mensaje
                else:
                    respuesta = "Comando no reconocido."
                conn.sendall(respuesta.encode())
        except Exception as e:
            print(f"Error: {e}")

    def cerrar(self):
        for client in self.clients:
            try:
                client.close()
            except OSError:
                pass
        self.server_socket.close()
        print("Servidor cerrado.")
