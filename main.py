# Código principal
# Proyecto 4: Socialtec
# Autores: Evans Josué Corrales Valverde
# Fecha de creación 24 de enero del 2024.

from threading import Thread
from Server import ServerTCP
from Client import ClientTCP

def ejecutar_servidor(servidor):
    try:
        servidor.iniciar()
    except Exception as e:
        print(f"Error en el servidor: {e}")

print("Socialtec\n\n")

while True:
    print("Seleccione alguna opción")
    print("1. Iniciar programa con funcionalidad servidor/cliente.")
    print("2. Salir")

    opcion = input("Opción: ")
    match opcion:
        case "1":
            servidor = ServerTCP()
            cliente = ClientTCP()

            # Iniciar servidor en un hilo separado
            servidor_hilo = Thread(target=ejecutar_servidor, args=(servidor,))
            servidor_hilo.start()

            try:
                cliente.conectar()
                cliente.enviar_mensajes()
            except KeyboardInterrupt:
                print("\nPrograma interrumpido por el usuario.")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                servidor.cerrar()
                print("Servidor detenido.")
                print("Cliente desconectado.")
        case "2":
            print("Saliendo del programa...")
            break
        case _:
            print("Opción inválida, intente nuevamente.")


""""Ejemplo de uso de cada uno de las partes del grafo. "El server en realidad ya está implementando el grafo.
grafo = Graph()
print(grafo.agregar_usuario("Alice", "12345"))
print(grafo.autenticar_usuario("Alice", "12345"))  # Correcto
print(grafo.autenticar_usuario("Alice", "wrong"))  # Incorrecto
print(grafo.agregar_usuario("Bob", "pass"))
print(grafo.agregar_arista("Alice", "Bob"))
grafo.mostrar_matriz()"""

