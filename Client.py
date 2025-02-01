import socket
from Graph import Graph

class ClientTCP:
    def __init__(self, host='127.0.0.1', port=65432):
        self.grafo = Graph()
        #self.grafo.mostrar_matriz()
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Funciones Xd que fueron necesarias de replicar en el cliente

    def agregar_usuario(self, nombre, contrasena, **kwargs):
        return self.grafo.agregar_usuario(nombre, contrasena, **kwargs)

    def autenticar_usuario(self, nombre, contrasena):
        return self.grafo.autenticar_usuario(nombre, contrasena)

    def get_node(self, nombre):
        return self.grafo.get_node(nombre)

    def agregar_arista(self, nodo1, nodo2):
        return self.grafo.agregar_arista(nodo1, nodo2)

    def eliminar_arista(self, nodo1, nodo2):
        return self.grafo.eliminar_arista(nodo1, nodo2)

    def get_edges(self):
        return self.grafo.get_edges()

    def get_nodes(self):
        return self.grafo.get_nodes()

    def mostrar_matriz(self):
        return self.grafo.mostrar_matriz()

    def is_friend(self, nodo1, nodo2):
        return self.grafo.is_friend(nodo1, nodo2)

    # Funciones que sí son propias del cliente.
    def conectar(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Conectado al servidor en {self.host}:{self.port}")

    def enviar_mensajes(self):
        try:
            while True:
                mensaje = input("Escribe un mensaje ('salir' para terminar): ")
                if mensaje.lower() == 'salir':
                   break
                self.client_socket.sendall(mensaje.encode())
                respuesta = self.client_socket.recv(1024)
                print(f"Respuesta del servidor: {respuesta.decode()}")
        except ConnectionResetError:
            print("Conexión cerrada por el servidor.")
        finally:
            self.client_socket.close()
            print("Cliente desconectado.")







