import socket
<<<<<<< HEAD
from Graph import Graph
import json

class ClientTCP:
    def __init__(self, host='127.0.0.1', port=65432):
        self.grafo = Graph()
=======

class ClientTCP:
    def __init__(self, host='127.0.0.1', port=65432):
>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

<<<<<<< HEAD
    def agregar_usuario(self, nombre, contrasena, **kwargs):
        return self.grafo.agregar_usuario(nombre, contrasena, **kwargs)

    def autenticar_usuario(self, nombre, contrasena):
        return self.grafo.autenticar_usuario(nombre, contrasena)

    def get_node(self, nombre):
        return self.grafo.get_node(nombre)

=======
>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5
    def conectar(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Conectado al servidor en {self.host}:{self.port}")

    def enviar_mensajes(self):
        try:
            while True:
                mensaje = input("Escribe un mensaje ('salir' para terminar): ")
                if mensaje.lower() == 'salir':
<<<<<<< HEAD
                   break
=======
                    break
>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5
                self.client_socket.sendall(mensaje.encode())
                respuesta = self.client_socket.recv(1024)
                print(f"Respuesta del servidor: {respuesta.decode()}")
        except ConnectionResetError:
            print("Conexión cerrada por el servidor.")
        finally:
            self.client_socket.close()
            print("Cliente desconectado.")

<<<<<<< HEAD
    def get_nodes(self):
        return self.grafo.get_nodes()



=======
>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5


