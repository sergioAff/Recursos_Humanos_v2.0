from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk 
from tkinter import messagebox
import sqlite3 as sql
from registros import Registro

class SecondScreen:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800

    def __init__(self):
        self.setup_ui()

    def setup_ui(self):
        # Configuración de la interfaz gráfica principal
        self.root = Tk()
        self.root.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')
        self.root.title('Recursos Humanos')
        self.root.resizable(0, 0)
        self.root.config(bg='#082d44') 

        try:
            # Selección del archivo de base de datos
            self.archivo ='recursosHumanos.db'
        except Exception as e:
            messagebox.showerror('Error','Error al abrir la base de datos')
            self.root.destroy()
            return

        # Carga de las opciones para el menú desplegable
        self.load_options()

        # Creación de los elementos de la interfaz gráfica
        self.create_widgets()

        # Bucle principal de la interfaz gráfica
        self.root.mainloop()

    def create_widgets(self):
        # Creación de los elementos gráficos (botones, frames, etc.)
        self.create_data_frame()
        self.load_images()
        self.create_tablas_button()

    def create_data_frame(self):
        # Creación del frame para mostrar los datos
        self.frameMostrar = Frame(self.root, bg='#082d44', borderwidth=0, highlightthickness=0)
        self.frameMostrar.place(
            height=660,
            width=970,
            x=20,
            y=130)
        self.frameMostrar.grid_rowconfigure(0, weight=1)
        self.frameMostrar.grid_columnconfigure(0, weight=1)

    def load_images(self):
        try:
            # Carga de las imágenes para los botones
            img_boton_tablas = Image.open('Tablas.png')
            self.photoTablas = ImageTk.PhotoImage(img_boton_tablas)

            img_boton_anadir = Image.open('Añadir.png')
            self.photoAnadir = ImageTk.PhotoImage(img_boton_anadir)            

            img_boton_actualizar = Image.open('Actualizar.png') 
            self.photoActualizar = ImageTk.PhotoImage(img_boton_actualizar)

            img_boton_borrar = Image.open('Borrar.png')
            self.photoBorrar = ImageTk.PhotoImage(img_boton_borrar)

        except Exception as e:
            messagebox.showerror('Error', 'Falta algún archivo')

    def create_tablas_button(self):
        # Creación del botón de tablas
        self.botonTablas = Menubutton(
            image=self.photoTablas,
            cursor='hand2',
            borderwidth=0,
            highlightthickness=0
        )   

        self.botonTablas.menu = Menu(self.botonTablas, tearoff=0)
        self.botonTablas["menu"] = self.botonTablas.menu

        for opcion in self.opciones:
            self.botonTablas.menu.add_command(
                label=opcion,
                command=lambda opt=opcion: self.show_table_and_buttons(opt)
            )
        
        self.botonTablas.place(
            height=35,
            width=110,
            x=22,
            y=28,
        )

    def show_table_and_buttons(self, table_name):
        # Muestra la tabla seleccionada y activa los otros botones
        self.tabla_actual = table_name
        tree = self.tablas(self.frameMostrar, self.archivo, table_name)
        self.create_all_buttons(tree)

    def create_all_buttons(self, tree):
        # Creación de los botones de la interfaz gráfica
        self.create_button(self.photoAnadir, 34, 110, 160, 26, lambda: self.create_command("Añadir", tree))
        self.create_button(self.photoActualizar, 35, 183, 310, 21, lambda: self.create_command("Actualizar", tree))
        self.create_button(self.photoBorrar, 40, 110, 540, 22, lambda: self.create_command("Borrar"))

    def create_button(self, image, height, width, x, y, command):
        # Función genérica para crear botones
        button = Button(
            image=image,
            cursor='hand2',
            borderwidth=0,
            highlightthickness=0,
            command=command
        )

        button.place(
            height=height,
            width=width,
            x=x,
            y=y
        )

    def create_command(self, option, treeview):
        # Función para crear el comando asociado a cada botón
        if option == 'Añadir':
            registro = Registro(self.archivo, self.tabla_actual, 'Añadir')
            registro.anadir()
            self.tablas(self.frameMostrar, self.archivo, self.tabla_actual)
        elif option == 'Actualizar':
            val=self.cargar_registro_seleccionado(treeview)
            if val is not False:
                registro = Registro(self.archivo, self.tabla_actual, 'Actualizar')
                registro.cargar(val)

        elif option == "Borrar":
            registro.borrar()

    def cargar_registro_seleccionado(self, treeview):
        # Función para cargar el registro seleccionado en un Toplevel
        seleccion = treeview.focus()

        if seleccion:
            # Obtener los valores de la fila seleccionada
            valores_fila = treeview.item(seleccion, 'values')
            
            # Mostrar los valores en un Toplevel
            return valores_fila

        else:
            # Mostrar un cuadro de diálogo indicando que no se ha seleccionado ningún registro
            messagebox.showinfo("Advertencia", "Seleccione un registro en el TreeView")
            return False

    def load_options(self):
        # Obtención de las opciones para el menú desplegable
        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
            self.opciones = [fila[0] for fila in cursor.fetchall() if fila[0] != 'sqlite_sequence']

    def tablas(self, frame_mostrar, archivo, tabla):
        def crear_treeview(frame, atributos, valores):
            tree = ttk.Treeview(frame, columns=atributos, show='headings', height=min(len(valores), 10))

            style = ttk.Style()
            style.configure("Treeview", font=('Arial', 14), rowheight=45)
            style.configure("Treeview.Heading", font=('Arial', 14, 'bold'))
            style.configure("Treeview.Treeview", background="#E1E1E1", fieldbackground="#E1E1E1", foreground="black")

            for atributo in atributos:
                tree.heading(atributo, text=atributo)

                ancho = max(tree.heading(atributo)["text"].__len__(), *[len(str(valor[atributos.index(atributo)])) for valor in valores])
                tree.column(atributo, width=ancho * 15)

            for valor in valores:
                tree.insert('', 'end', values=valor)

            return tree

        for widget in frame_mostrar.winfo_children():
            widget.destroy()

        titulo_tabla = Label(text=f'Tabla: {tabla}', anchor='w')
        titulo_tabla.config(bg='#082d44', font=(['Arial', 20]), fg='white')
        titulo_tabla.place(
            height=40,
            width=500,
            x=10,
            y=80
        )

        if tabla:
            with sql.connect(archivo) as conn:
                cursor = conn.cursor()

                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tabla,))
                tabla_existe = cursor.fetchone()

                if tabla_existe:
                    cursor.execute(f"PRAGMA table_info({tabla})")
                    atributos = [column[1] for column in cursor.fetchall()]

                    cursor.execute(f"SELECT * FROM {tabla}")
                    valores = cursor.fetchall()

                    tree = crear_treeview(frame_mostrar, atributos, valores)

                    scrollbar_y = Scrollbar(frame_mostrar, orient="vertical", command=tree.yview)
                    scrollbar_y.pack(side="right", fill="y")
                    tree.configure(yscrollcommand=scrollbar_y.set)

                    scrollbar_x = Scrollbar(frame_mostrar, orient=HORIZONTAL, command=tree.xview)
                    scrollbar_x.pack(side="bottom", fill="x")
                    tree.configure(xscrollcommand=scrollbar_x.set)

                    tree.pack(fill="both", expand=True)
                    
                    return tree


