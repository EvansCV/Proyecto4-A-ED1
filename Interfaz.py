import tkinter as tk
from tkinter import filedialog, messagebox, Image, PhotoImage
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        # Limpiar vista anterior
        self.ax.clear()

        # Crear grafo de NetworkX
        graph_nx = nx.Graph()

        # Agregar nodos del grafo personalizado
        for nombre in self.graph.nodos:
            graph_nx.add_node(nombre)

        # Dibujar grafo
        nx.draw(graph_nx,
                ax=self.ax,
                with_labels=True,
                node_color='lightblue',
                node_size=500,
                font_size=10,
                font_weight='bold')

        # Actualizar canvas
        self.canvas.draw()


class LoginWindow:
    def __init__(self, master, graph):
        self.master = master
        self.graph = graph

        self.master.title("Iniciar Sesión")
        self.master.geometry("300x250")

        # Username
        tk.Label(master, text="Nombre de Usuario:").pack(pady=10)
        self.username_entry = tk.Entry(master)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(master, text="Contraseña:").pack(pady=10)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        tk.Button(master, text="Iniciar Sesión", command=self.login).pack(pady=20)

        # Register Button
        tk.Button(master, text="Registrarse", command=self.open_registration).pack(pady=10)

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

    def open_graph_window(self, username):
        root = tk.Tk()
        graph_window = GraphWindow(root, self.graph)
        root.mainloop()

    def open_user_window(self, username):
        root = tk.Tk()
        user_window = UserWindow(root, self.graph, username)
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
        image = image.resize((200, 250), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)

        self.photo_label = tk.Label(master, image=self.photo)
        self.photo_label.image = self.photo
        self.photo_label.pack(pady=10)

        # Nombre de usuario
        tk.Label(master, text=username, font=("Arial", 14, "bold")).pack(pady=5)

        # Botones de acciones
        tk.Button(master, text="Editar Perfil", command=self.edit_profile).pack(pady=5)
        tk.Button(master, text="Cerrar Sesión", command=self.logout).pack(pady=5)

    def edit_profile(self):
        messagebox.showinfo("Editar", "Función de edición en desarrollo")

    def logout(self):
        self.master.destroy()
        root = tk.Tk()
        LoginWindow(root, self.graph)
        root.mainloop()

