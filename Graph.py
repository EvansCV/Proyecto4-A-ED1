import json
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
        self.foto = ''  # Añadido para almacenar ruta de foto

    def set_contrasena(self, contrasena):
        self.contrasena = bcrypt.hash(contrasena)

<<<<<<< HEAD
    def verificar_contrasena(self, contrasena):
=======
    def verificar_contraseña(self, contrasena):
>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5
        return bcrypt.verify(contrasena, self.contrasena) if self.contrasena else False

    def get_photo_path(self):
        return self.foto

    def __str__(self):
        return f"Nodo({self.nombre}, posición: {self.posicion})"


class Graph:
    def __init__(self):
        self.nodos = {}  # Diccionario {nombre: Nodo}
        self.matriz = []
<<<<<<< HEAD
        try:
            print(self.load_from_file("Grafo.JSON"))
        except Exception as e:
            print("Aún no se ha guardado el grafo.")
            pass

=======
>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5

    def get_node(self, nombre):
        for nombre_nodo in self.nodos:
            if nombre_nodo == nombre:
                return self.nodos[nombre_nodo]

    def agregar_nodo(self, nombre, **kwargs):
        if nombre in self.nodos:
            return f"Error: El nodo '{nombre}' ya existe."
        
        # Crear nuevo nodo con atributos adicionales
        nuevo_nodo = Node(nombre, len(self.nodos))
        
        # Establecer contraseña si se proporciona
        if 'password' in kwargs:
            nuevo_nodo.set_contrasena(kwargs['password'])
        
        # Almacenar información adicional como foto
        nuevo_nodo.foto = kwargs.get('photo', '')
        
        self.nodos[nombre] = nuevo_nodo

        # Expande la matriz de adyacencia
        for fila in self.matriz:
            fila.append(0)
        self.matriz.append([0] * (len(self.nodos)))
<<<<<<< HEAD
        self.save_to_file("Grafo.JSON")
=======

>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5
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

    def agregar_usuario(self, nombre, contrasena, **kwargs):
        mensaje = self.agregar_nodo(nombre, password=contrasena, **kwargs)
        return mensaje + f" Usuario '{nombre}' registrado con contraseña."

    def autenticar_usuario(self, nombre, contrasena):
        if nombre not in self.nodos:
            return False, "Error: El usuario no existe."
        nodo = self.nodos[nombre]
<<<<<<< HEAD
        if nodo.verificar_contrasena(contrasena):
=======
        if nodo.verificar_contraseña(contrasena):
>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5
            return True, f"Autenticación exitosa. Bienvenido, {nombre}."
        return False, "Error: Contraseña incorrecta."

    def get_nodes(self):
        """Devuelve los nombres de los nodos en el grafo."""
        return list(self.nodos.keys())

    def get_edges(self):
        """Devuelve las conexiones entre nodos."""
        edges = []
        for i in range(len(self.matriz)):
            for j in range(i+1, len(self.matriz)):
                if self.matriz[i][j] == 1:
                    nombre1 = [n for n, node in self.nodos.items() if node.posicion == i][0]
                    nombre2 = [n for n, node in self.nodos.items() if node.posicion == j][0]
                    edges.append((nombre1, nombre2))
        return edges

    def save_to_file(self, filename):
        """Guarda el grafo en un archivo JSON."""
        grafo_data = {
            "nodos": {},
            "matriz": self.matriz
        }
<<<<<<< HEAD

=======
        
>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5
        for nombre, nodo in self.nodos.items():
            grafo_data["nodos"][nombre] = {
                "posicion": nodo.posicion,
                "contrasena": nodo.contrasena,
                "foto": getattr(nodo, 'foto', '')
            }
<<<<<<< HEAD

=======
        
>>>>>>> b5d15bbe3e95217799df548d73d60345747c78e5
        with open(filename, 'w') as f:
            json.dump(grafo_data, f, indent=4)

    def load_from_file(self, filename):
        """Carga un grafo desde un archivo JSON."""
        with open(filename, 'r') as f:
            grafo_data = json.load(f)
        
        # Reiniciar el grafo
        self.nodos.clear()
        self.matriz.clear()
        
        # Restaurar nodos
        for nombre, datos in grafo_data["nodos"].items():
            nuevo_nodo = Node(nombre, datos["posicion"])
            nuevo_nodo.contrasena = datos.get("contrasena")
            
            # Restaurar foto si existe
            if "foto" in datos:
                nuevo_nodo.foto = datos["foto"]
            
            self.nodos[nombre] = nuevo_nodo
        
        # Restaurar matriz de adyacencia
        self.matriz = grafo_data["matriz"]
        
        return "Grafo cargado exitosamente."