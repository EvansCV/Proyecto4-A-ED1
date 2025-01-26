from passlib.hash import bcrypt

# Clase de los nodos, tomando en cuenta que cada nodo debe tener el nombre, entre otras cosas.
class Node:
    def __init__(self, nombre, posicion):
        if not isinstance(nombre, str) or not isinstance(posicion, int):
            raise TypeError("El nombre debe ser un string, y la posición un número entero.")
        self.nombre = nombre
        self.posicion = posicion
        self.contrasena = None  # Se almacena como hash
        self.amigos = set()    # Amigos o conexiones directas

    def set_contrasena(self, contrasena):
        from passlib.hash import bcrypt
        self.contrasena = bcrypt.hash(contrasena)

    def verificar_contraseña(self, contrasena):
        from passlib.hash import bcrypt
        return bcrypt.verify(contrasena, self.contrasena) if self.contrasena else False

    def __str__(self):
        return f"Nodo({self.nombre}, posición: {self.posicion})"


class Graph:
    def __init__(self):
        self.nodos = {}  # Diccionario {nombre: Nodo}
        self.matriz = []

    def agregar_nodo(self, nombre):
        if nombre in self.nodos:
            return f"Error: El nodo '{nombre}' ya existe."
        nuevo_nodo = Node(nombre, len(self.nodos))
        self.nodos[nombre] = nuevo_nodo

        # Expande la matriz de adyacencia
        for fila in self.matriz:
            fila.append(0)
        self.matriz.append([0] * (len(self.nodos)))

        return f"Nodo '{nombre}' agregado con éxito."

    def agregar_arista(self, nodo1, nodo2):
        if nodo1 not in self.nodos or nodo2 not in self.nodos:
            return "Error: Uno o ambos nodos no existen."
        idx1, idx2 = self.nodos[nodo1].posicion, self.nodos[nodo2].posicion
        self.matriz[idx1][idx2] = 1
        self.matriz[idx2][idx1] = 1
        return f"Conexión entre '{nodo1}' y '{nodo2}' creada."

    def mostrar_matriz(self):
        for fila in self.matriz:
            print(fila)

    def agregar_usuario(self, nombre, contrasena):
        mensaje = self.agregar_nodo(nombre)
        nodo = self.nodos[nombre]
        nodo.set_contraseña(contrasena)
        return mensaje + f" Usuario '{nombre}' registrado con contraseña."

    def autenticar_usuario(self, nombre, contrasena):
        if nombre not in self.nodos:
            return False, "Error: El usuario no existe."
        nodo = self.nodos[nombre]
        if nodo.verificar_contraseña(contrasena):
            return True, f"Autenticación exitosa. Bienvenido, {nombre}."
        return False, "Error: Contraseña incorrecta."
