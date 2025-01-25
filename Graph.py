# Clase para
from passlib.hash import bcrypt
# Clase de los nodos, tomando en cuenta que cada nodo debe tener el nombre, entre otras cosas.
class Node:
    # Constructor y sí, el nombre es el dato del nodo.
    def __init__(self, nombre, posicion):
        if not isinstance(nombre, str) or not isinstance(posicion, int):
            raise TypeError("El nombre debe ser un string, y la posicion un número entero.")
        self.nombre = nombre
        self.posicion = posicion

    def get_name(self):
        return self.nombre

    def get_position(self):
        return self.posicion


class Graph:
    # El mentado constructor
    def __init__(self):
        self.matriz = []
        self.posicion = 0
        self.lista_nodos = []

    def single(self):
        if len(self.matriz) <= 1:
            return True
        return False

    # Este método se utilizará para enviar la solicitud de amistad.
    def agregar_arista(self, nodo1, nodo2):
        if not isinstance(nodo1, str) or not isinstance(nodo2, str):
            raise TypeError("Para las aristas se necesita el dato del nombre que se almacena en cada nodo.")
        # Obtener la posición del nodo1
        for nodo in self.lista_nodos:
            if nodo.get_name() == nodo1:
                posicion1 = nodo.get_position()
        # Obtener la posición del nodo1
        for nodo in self.lista_nodos:
            if nodo.get_name() == nodo2:
                posicion2 = nodo.get_position()
        self.matriz[posicion1][posicion2] = 1

    def mostrar_matriz(self):
        for fila in self.matriz:
            print(fila)

    # Agregar gente a la red social, es decir, al grafo.
    def agregar_nodo(self, nodo):
        if not isinstance(nodo, str):
            raise TypeError("El nodo debe ser un string.")

        nodo = Node(nodo, self.posicion)
        self.lista_nodos.append(nodo)
        # Crear el nuevo nodo
        self.posicion += 1

        # Agregar la nueva fila.
        self.matriz.append([])

        # Agregar un 0 a la nueva fila que represente la relación.
        for i in range(len(self.matriz) - 1):
            self.matriz[len(self.matriz) - 1].append(0)

        # Agregar el nodo al final de cada lista
        for lista in self.matriz:
            lista.append(0)

    def mostrar_nombres(self):
        for nodo in self.lista_nodos:
            print(nodo.get_name())
