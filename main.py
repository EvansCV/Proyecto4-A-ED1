from threading import Thread
<<<<<<< HEAD
from Client import ClientTCP
import tkinter as tk
from Server import ServerTCP
from Interfaz import LoginWindow

def iniciar_servidor():
    """Inicia el servidor en un hilo separado."""
    servidor = ServerTCP()
    servidor.iniciar()

# Ejecutar servidor en un hilo
servidor_hilo = Thread(target=iniciar_servidor, daemon=True)
servidor_hilo.start()

def iniciar_cliente():
    """Inicia la ventana de login en el hilo principal."""
    root = tk.Tk()
    cliente = ClientTCP()
    LoginWindow(root, cliente)
    root.mainloop()

=======
from Server import ServerTCP
from Client import ClientTCP
import tkinter as tk
from Interfaz import LoginWindow

>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5
def main():
    print("Socialtec - Red Social\n")

    while True:
        print("Seleccione una opción:")
<<<<<<< HEAD
        print("1. Iniciar Cliente")
        print("2. Salir")

        opcion = input()

        if opcion == "1":
            iniciar_cliente()

=======
        print("1. Iniciar Servidor/Cliente")
        print("2. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            servidor = ServerTCP()
            root = tk.Tk()
            cliente = ClientTCP()
            login = LoginWindow(root, servidor.grafo)
            # Ejecutar el server
            servidor_hilo = Thread(target=ejecutar_servidor, args=(servidor,))
            servidor_hilo.daemon = True
            servidor_hilo.start()
            root.mainloop()
            try:
                cliente.conectar()
                cliente.enviar_mensajes()
            except KeyboardInterrupt:
                print("\nPrograma interrumpido por el usuario.")
            finally:
                servidor.cerrar()
>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5
        elif opcion == "2":
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Intente nuevamente.")

<<<<<<< HEAD
if __name__ == "__main__":
    main()


=======
def ejecutar_servidor(servidor):
    try:
        servidor.iniciar()
    except Exception as e:
        print(f"Error en el servidor: {e}")

if __name__ == "__main__":
    main()
>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5
