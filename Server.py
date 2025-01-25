import socket
import threading
import Graph

class ServerTCP:
    def __init__(self, host = "127.0.0.1", port = 65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = []
        self.grafo = Graph

    # Configuración del servidor
    def iniciar(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Servidor escuchando en {self.host}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"Cliente conectado desde {addr}")
            self.clients.append(conn)
            hilo = threading.Thread(target=self.manejar_cliente, args=(conn, addr))
            hilo.start()

    def manejar_cliente(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Mensaje de {addr}: {data.decode()}")
                respuesta = f"Servidor recibió: {data.decode()}"
                conn.sendall(respuesta.encode())
        except ConnectionResetError:
            print(f"Conexión perdida con {addr}")
        finally:
            print(f"Cliente {addr} desconectado")
            self.clients.remove(conn)
            conn.close()

    def cerrar(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()
        print("Servidor cerrado.")

# Instanciar y ejecutar el servidor
if __name__ == "__main__":
    servidor = ServerTCP()
    try:
        servidor.iniciar()
    except KeyboardInterrupt:
        servidor.cerrar()