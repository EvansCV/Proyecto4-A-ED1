import tkinter as tk
from threading import Thread
from Server import ServerTCP
from Client import ClientTCP
from Interfaz import LoginWindow

# Creamos una instancia global de Tk() para la aplicación principal
root = tk.Tk()
root.withdraw()  # Ocultamos la ventana principal si no es necesaria

def iniciar_servidor():
    servidor = ServerTCP()
    servidor.iniciar()

# Iniciar el servidor en un hilo separado
servidor_thread = Thread(target=iniciar_servidor, daemon=True)
servidor_thread.start()

def abrir_ventana_login():
    # Para cada login, creamos una ventana secundaria (Toplevel) en el hilo principal
    ventana_login = tk.Toplevel(root)
    cliente = ClientTCP()  # Instancia del cliente para que se cargue el grafo.
    # Se asume que ClientTCP ahora se pasa junto con el grafo u otro objeto similar
    LoginWindow(ventana_login, cliente)

def main_menu():
    print("Socialtec - Red Social\n")
    while True:
        print("\nSeleccione una opción:")
        print("1. Iniciar Cliente (Login)")
        print("2. Salir")
        opcion = input()
        if opcion == "1":
            # En lugar de iniciar un nuevo mainloop en un hilo secundario,
            # programamos la apertura de una ventana de login en el hilo principal.
            root.after(0, abrir_ventana_login)
        elif opcion == "2":
            print("Saliendo del programa.")
            root.quit()  # Finalizamos la aplicación Tkinter
            exit()
        else:
            print("Opción inválida. Intente nuevamente.")

# Ejecutar el menú de consola en un hilo separado
menu_thread = Thread(target=main_menu, daemon=True)
menu_thread.start()

# Ejecutar el mainloop en el hilo principal
root.mainloop()



