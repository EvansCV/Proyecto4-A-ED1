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

    def verificar_contrasena(self, contrasena):
        return bcrypt.verify(contrasena, self.contrasena) if self.contrasena else False

    def get_photo_path(self):
        return self.foto

    def __str__(self):
        return f"Nodo({self.nombre}, posición: {self.posicion})"

class Graph:
    def __init__(self):
        self.nodos = {}  # Diccionario {nombre: Nodo}
        self.matriz = []
        try:
            print(self.load_from_file("Grafo.JSON"))
        except Exception as e:
            print("Aún no se ha guardado el grafo.")
            pass


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
        self.save_to_file("Grafo.JSON")
        return f"Nodo '{nombre}' agregado con éxito."

    def agregar_arista(self, nodo1, nodo2):
        if nodo1 not in self.nodos or nodo2 not in self.nodos:
            return "Error: Uno o ambos nodos no existen."
        idx1, idx2 = self.nodos[nodo1].posicion, self.nodos[nodo2].posicion
        self.matriz[idx1][idx2] = 1
        self.save_to_file("Grafo.JSON")
        return f"Conexión desde '{nodo1}' hasta '{nodo2}' creada."

    def eliminar_arista(self, nodo1, nodo2):
        if nodo1 not in self.nodos or nodo2 not in self.nodos:
            return "Error: Uno o ambos nodos no existen."
        idx1, idx2 = self.nodos[nodo1].posicion, self.nodos[nodo2].posicion
        self.matriz[idx1][idx2] = 0
        self.save_to_file("Grafo.JSON")
        return f"Conexión desde '{nodo1}' hasta '{nodo2}' eliminada."

    def is_friend(self, nodo1, nodo2):
        if nodo1 not in self.nodos or nodo2 not in self.nodos:
            return "Error: Uno o ambos nodos no existen."
        idx1, idx2 = self.nodos[nodo1].posicion, self.nodos[nodo2].posicion
        if self.matriz[idx1][idx2] == 1:
            return True
        return False

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
        if nodo.verificar_contrasena(contrasena):
            return True, f"Autenticación exitosa. Bienvenido, {nombre}."
        return False, "Error: Contraseña incorrecta."

    def get_nodes(self):
        """Devuelve los nombres de los nodos en el grafo."""
        return list(self.nodos.keys())

    def get_edges(self):
        """Devuelve las conexiones entre nodos."""
        edges = []
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz)):
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

        for nombre, nodo in self.nodos.items():
            grafo_data["nodos"][nombre] = {
                "posicion": nodo.posicion,
                "contrasena": nodo.contrasena,
                "foto": getattr(nodo, 'foto', '')
            }

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
    def encontrar_camino(self, usuario_inicio, usuario_destino, max_profundidad=4):
        """
        Encuentra un camino entre dos usuarios usando BFS con límite de profundidad.
        Retorna la lista del camino si existe, None si no existe.
        """
        if usuario_inicio not in self.nodos or usuario_destino not in self.nodos:
            return None
            
        visitados = set()
        cola = [(usuario_inicio, [usuario_inicio])]
        
        while cola:
            (actual, camino) = cola.pop(0)
            
            # Si el camino actual excede la profundidad máxima, lo saltamos
            if len(camino) > max_profundidad:
                continue
                
            # Obtener índice del nodo actual
            idx_actual = self.nodos[actual].posicion
            
            # Revisar todas las conexiones del nodo actual
            for nombre_nodo in self.nodos:
                idx_nodo = self.nodos[nombre_nodo].posicion
                
                # Si hay una conexión y no ha sido visitado
                if self.matriz[idx_actual][idx_nodo] == 1 and nombre_nodo not in visitados:
                    if nombre_nodo == usuario_destino:
                        # Encontramos el camino
                        return camino + [nombre_nodo]
                        
                    visitados.add(nombre_nodo)
                    nuevo_camino = camino + [nombre_nodo]
                    cola.append((nombre_nodo, nuevo_camino))
        
        return None

    def obtener_sugerencias(self, usuario_actual, max_profundidad=4):
        """
        Encuentra sugerencias de amigos para un usuario basado en conexiones de amigos.
        Retorna una lista de tuplas (usuario_sugerido, camino).
        """
        sugerencias = []
        visitados = set([usuario_actual])
        
        # Obtener todos los usuarios que no son amigos directos
        for usuario_destino in self.nodos:
            if usuario_destino != usuario_actual and not self.is_friend(usuario_actual, usuario_destino):
                camino = self.encontrar_camino(usuario_actual, usuario_destino, max_profundidad)
                if camino and len(camino) <= max_profundidad + 1:  # +1 porque el camino incluye al usuario actual
                    sugerencias.append((usuario_destino, camino))
        
        return sugerencias