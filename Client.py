import socket

class ClientTCP:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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



