from threading import Thread
from Server import ServerTCP
from Client import ClientTCP
import tkinter as tk
from Interfaz import LoginWindow

def main():
    print("Socialtec - Red Social\n")

    while True:
        print("Seleccione una opción:")
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
        elif opcion == "2":
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Intente nuevamente.")

def ejecutar_servidor(servidor):
    try:
        servidor.iniciar()
    except Exception as e:
        print(f"Error en el servidor: {e}")

if __name__ == "__main__":
    main()