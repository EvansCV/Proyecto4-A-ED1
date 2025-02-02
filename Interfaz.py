import tkinter as tk
from tkinter import filedialog, messagebox, Image, PhotoImage
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from MergeSort import MSort

class GraphWindow:
    def __init__(self, master, graph):
        self.master = master
        self.graph = graph

        self.master.title("Grafo de Usuarios")
        self.master.geometry("800x600")

        # Crear frame para el grafo
        self.graph_frame = tk.Frame(self.master)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        # Crear vista de grafo
        self.create_graph_view()

        # Botón para actualizar
        tk.Button(self.master, text="Actualizar Grafo", command=self.update_graph_view).pack(pady=10)

    def create_graph_view(self):
        # Figura de Matplotlib para el grafo
        self.figure = plt.Figure(figsize=(8, 6))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Actualizar vista inicial
        self.update_graph_view()

    def update_graph_view(self):
        # Limpiar la vista anterior
        self.ax.clear()

        # Crear un grafo con NetworkX
        graph_nx = nx.Graph()

        # Agregar nodos.
        for nombre in self.graph.get_nodes():
            graph_nx.add_node(nombre)

        #Agregar aristas.
        for edge in self.graph.get_edges():
            graph_nx.add_edge(*edge)

        # Dibujar el grafo en la figura de matplotlib
        nx.draw(graph_nx,
                ax=self.ax,
                with_labels=True,
                node_color='lightblue',
                node_size=500,
                font_size=10,
                font_weight='bold')

        # Actualizar el canvas de la GUI sin bloquear la ejecución
        self.canvas.draw()

class LoginWindow:
    def __init__(self, master, graph):
        self.master = master
        self.graph = graph

        self.master.title("Iniciar Sesión")
        self.master.geometry("400x350")

        # Username
        tk.Label(master, text="Nombre de Usuario:").pack(pady=10)
        self.username_entry = tk.Entry(master)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(master, text="Contraseña:").pack(pady=10)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=5)

        # Botón de inicio de sesión
        tk.Button(master, text="Iniciar Sesión", command=self.login).pack(pady=20)

        # Botón de registro
        tk.Button(master, text="Registrarse", command=self.open_registration).pack(pady=10)

        # Botón para mostrar el grafo
        tk.Button(master, text="Mostrar Grafo", command=self.open_graph_window).pack(padx=30, pady=5)

        # Botón de las estadísticas
        tk.Button(master, text="Ver estadísticas", command=self.mostrar_estadisticas).pack(pady=10)

    def mostrar_estadisticas(self):
        # Solicitar estadísticas al servidor
        estadisticas = self.obtener_estadisticas_servidor()

        # Crear ventana Toplevel para mostrar los resultados
        stats_window = tk.Toplevel(self.master)
        stats_window.title("Estadísticas de Usuarios")
        stats_window.geometry("400x300")
        max_amigos_text = ", ".join(estadisticas["max_amigos"]) if estadisticas["max_amigos"] else "N/A"
        min_amigos_text = ", ".join(estadisticas["min_amigos"]) if estadisticas["min_amigos"] else "N/A"
        promedio = estadisticas["promedio"]

        # Mostrar la información en etiquetas
        tk.Label(stats_window, text="Estadísticas de la Red Social", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(stats_window, text=f"Usuario con más amigos: {max_amigos_text}", font=("Arial", 12)).pack(
            pady=5)
        tk.Label(stats_window, text=f"Usuario con menos amigos: {min_amigos_text}", font=("Arial", 12)).pack(
            pady=5)
        tk.Label(stats_window, text=f"Promedio de amigos por usuario: {estadisticas['promedio']:.2f}",
                 font=("Arial", 12)).pack(pady=5)

        # Botón para cerrar la ventana
        tk.Button(stats_window, text="Cerrar", command=stats_window.destroy).pack(pady=10)

    def obtener_estadisticas_servidor(self):
        respuesta = self.graph.calcular_estadisticas()
        return respuesta


    def open_graph_window(self):
        graph_window = tk.Toplevel(self.master)  # Crear una ventana secundaria
        graph_window.grab_set()  # Evita que la ventana principal se quede bloqueada
        GraphWindow(graph_window, self.graph)  # Muestra el grafo en la nueva ventana

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Autenticar usuario
        autenticado, mensaje = self.graph.autenticar_usuario(username, password)

        if autenticado:
            messagebox.showinfo("Éxito", mensaje)
            self.master.destroy()
            self.open_user_window(username)
        else:
            messagebox.showerror("Error", mensaje)

    def open_registration(self):
        # Cierra la ventana de login
        self.master.destroy()

        # Abre la ventana de registro
        root = tk.Tk()
        app = RegistrationWindow(root, self.graph)
        root.mainloop()

    def open_user_window(self, username):
        root = tk.Tk()
        UserWindow(root, self.graph, username)
        root.mainloop()

class RegistrationWindow:
    def __init__(self, master, graph):
        self.master = master
        self.graph = graph

        self.master.title("Registro de Usuario")
        self.master.geometry("300x350")

        # Campos de entrada
        campos = [
            ("Nombre de Usuario:", "name"),
            ("Contraseña:", "password"),
            ("Ruta de Foto:", "photo")
        ]

        self.entries = {}
        for label_text, attr_name in campos:
            tk.Label(master, text=label_text).pack(pady=5)

            if attr_name == "password":
                entry = tk.Entry(master, show="*")
            else:
                entry = tk.Entry(master)

            entry.pack(pady=5)
            self.entries[attr_name] = entry

        # Botón para seleccionar foto
        tk.Button(master, text="Seleccionar Foto", command=self.select_photo).pack(pady=5)

        # Botón para registrar
        tk.Button(master, text="Registrarse", command=self.register_user).pack(pady=20)

    def select_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.entries["photo"].delete(0, tk.END)
            self.entries["photo"].insert(0, file_path)

    def register_user(self):
        # Obtener valores de los campos
        name = self.entries["name"].get().strip()
        password = self.entries["password"].get().strip()
        photo = self.entries["photo"].get().strip()

        # Validar campos
        if not all([name, password, photo]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            # Agregar usuario al grafo
            resultado = self.graph.agregar_usuario(name, password, photo=photo)

            messagebox.showinfo("Éxito", resultado)

            # Volver a la ventana de login
            self.master.destroy()
            root = tk.Tk()
            LoginWindow(root, self.graph)
            root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", str(e))

class UserWindow:
    def __init__(self, master, graph, username):
        self.user = graph.get_node(username)
        self.master = master
        self.graph = graph
        self.master.title("Perfil de Usuario")
        self.master.geometry("400x450")

        # Foto de perfil
        self.photo_path = self.user.get_photo_path()
        image = Image.open(self.photo_path)
        image = image.resize((150, 200), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image, master = self.master)

        self.photo_label = tk.Label(master, image=self.photo)
        self.photo_label.image = self.photo
        self.photo_label.pack(pady=10)

        # Nombre de usuario
        tk.Label(master, text=username, font=("Arial", 14, "bold")).pack(pady=5)

        # Botones de acciones
        tk.Button(master, text="Buscar", command=self.search).pack(pady=5)
        tk.Button(master, text="Cerrar Sesión", command=self.logout).pack(pady=5)
        tk.Button(master, text="Lista de amigos", command=self.lista_amigos).pack(pady=10)

    def lista_amigos(self):
        # Creamos la ventana secundaria para desplegar la lista de amigos.
        friends_window = tk.Toplevel(self.master)
        friends_window.title("Lista de Amigos")
        friends_window.geometry("350x400")

        # Creamos un frame que contendrá el Listbox y el scrollbar.
        frame = tk.Frame(friends_window, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Creamos un scrollbar vertical.
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Creamos un Listbox con un estilo agradable.
        listbox = tk.Listbox(frame, font=("Arial", 12), yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configuramos el scrollbar para que controle el Listbox.
        scrollbar.config(command=listbox.yview)

        lista_amigos = []
        for node in self.graph.get_nodes():
            if self.graph.is_friend(self.user.nombre, node):
                lista_amigos.append(node)

        if len(lista_amigos) == 0:
            messagebox.showinfo("Lista de Amigos", "No tienes amigos agregados.")
            return

        # Aplica el MergeSort.
        lista_ordenada = MSort()
        lista_ordenada = lista_ordenada.merge_sort(lista_amigos)
        # Interfaz cuando el usuario posee al menos un amigo
        for amigo in lista_ordenada:
            listbox.insert(tk.END, amigo)
        # Botón para cerrar la ventana de la lista.
        tk.Button(friends_window, text="Cerrar", command=friends_window.destroy, font=("Arial", 12)).pack(pady=10)


    def search(self):
        search_window = tk.Toplevel(self.master)
        search_window.title("Buscar Usuario")
        search_window.geometry("500x350")

        tk.Label(search_window, text="Nombre:").pack(pady=5)
        self.name_entry = tk.Entry(search_window)
        self.name_entry.pack(pady=5)

        tk.Label(search_window, text="Apellido:").pack(pady=5)
        self.surname_entry = tk.Entry(search_window)
        self.surname_entry.pack(pady=5)

        tk.Button(search_window, text="Buscar", command=self.perform_search).pack(pady=10)

        self.result_label = tk.Label(search_window, text="")
        self.result_label.pack()

    def perform_search(self):
        nombre = self.name_entry.get().strip()
        apellido = self.surname_entry.get().strip()

        if not nombre or not apellido:
            self.result_label.config(text="Por favor, ingrese ambos campos.")
            return

        usuario = self.graph.get_node(f"{nombre} {apellido}")

        if usuario:
            v_amistad = self.graph.is_friend(self.user.nombre, usuario.nombre)
            self.result_label.config(text=f"Usuario encontrado: {usuario.nombre}")
            self.mostrar_otro_usuario(usuario, v_amistad)
        else:
            self.result_label.config(text="Usuario no encontrado.")

    def logout(self):
        self.master.destroy()
        root = tk.Tk()
        LoginWindow(root, self.graph)
        root.mainloop()

    def mostrar_otro_usuario(self, usuario, v_amistad):
        user_window = tk.Toplevel(self.master)
        user_window.title("Perfil de Usuario")
        user_window.geometry("400x300")

        # Mostrar el nombre en grande
        tk.Label(user_window, text=usuario.nombre, font=("Arial", 18, "bold")).pack(pady=10)

        # Mostrar la foto de perfil si existe
        if usuario.foto:
            img_path = usuario.get_photo_path()
            image = Image.open(img_path)
            image = image.convert("RGB")  # Convierte a un formato estándar
            image = image.resize((150, 150), Image.Resampling.LANCZOS)  # Ajusta el tamaño
            photo = ImageTk.PhotoImage(image, master=self.master)
            img_label = tk.Label(user_window, image=photo)
            img_label.image = photo  # Mantener referencia para evitar que se elimine
            img_label.pack(pady=5)

        # Crear el botón con la acción correspondiente según el estado de amistad.
        if not v_amistad:
            boton_accion = tk.Button(user_window, text="Agregar a amigos",
                                     command=lambda: self.enviar_solicitud(usuario.nombre, boton_accion))
        else:
            boton_accion = tk.Button(user_window, text="Eliminar de amigos",
                                     command=lambda: self.eliminar_amigo(usuario.nombre, boton_accion))
        boton_accion.pack(pady=10)

    def enviar_solicitud(self, usuario, boton):
        # Agregar la arista que indica la amistad.
        self.graph.agregar_arista(self.user.nombre, usuario)
        print(f"Solicitud de amistad enviada a {usuario}")
        # Cambiar el botón para que ahora permita eliminar de amigos.
        boton.config(
            text="Eliminar de amigos",
            command=lambda: self.eliminar_amigo(usuario, boton)
        )

    def eliminar_amigo(self, usuario, boton):
        # Eliminar la arista que indica la amistad.
        self.graph.eliminar_arista(self.user.nombre, usuario)
        print(f"{usuario} eliminado de la lista de amigos")
        # Cambiar el botón para que ahora permita agregar a amigos.
        boton.config(
            text="Agregar a amigos",
            command=lambda: self.enviar_solicitud(usuario, boton)
        )





