# Código principal
# Proyecto 4: Socialtec
# Autores: Evans Josué Corrales Valverde
# Fecha de creación 24 de enero del 2024.

from Server import ServerTCP
from Client import ClientTCP

print("Socialtec\n\n")

while True:
    print("Seleccione alguna opción")
    print("1. Iniciar programa con funcionalidad servidor/cliente.")
    print("2. Salir")

    opcion = input("Opción: ")
    match opcion:
        case "1":
            # Iniciar servidor y cliente
            servidor = ServerTCP()
            cliente = ClientTCP()
            try:
                servidor.iniciar()
                cliente.conectar()
                cliente.enviar_mensajes()
            except KeyboardInterrupt:
                print("\nPrograma interrumpido por el usuario.")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                servidor.cerrar()
                print("Servidor detenido.")
                cliente.cerrar()
                print("Cliente desconectado.")
        case "2":
            print("Saliendo del programa...")
            break
        case _:
            print("Opción inválida, intente nuevamente.")
