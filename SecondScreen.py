from tkinter import *
from PIL import Image, ImageTk 
from funciones import tablas, anadir, actualizar, borrar
from tkinter import filedialog, messagebox
import sqlite3 as sql

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
            self.archivo = self.select_database()
            if self.archivo[-3:] != '.db':
                messagebox.showerror('Alerta', 'No se seleccionó una base de datos correcta')
                self.root.destroy()
                return
        except Exception as e:
            messagebox.showerror('Error', e)

        # Carga de las opciones para el menú desplegable
        self.load_options()

        # Creación de los elementos de la interfaz gráfica
        self.create_widgets()

        # Bucle principal de la interfaz gráfica
        self.root.mainloop()

    def select_database(self):
        # Diálogo para seleccionar el archivo de base de datos
        return filedialog.askopenfilename(initialdir="/", title="Selecciona la base de datos", filetypes=(("Bases de datos", "*.db"), ("all files", "*.*")))

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
            height=30,
            width=70,
            x=25,
            y=28,
        )

    def show_table_and_buttons(self, table_name):
        # Muestra la tabla seleccionada y activa los otros botones
        self.tabla_actual = table_name
        tablas(self.frameMostrar, self.archivo, table_name)
        self.create_all_buttons()

    def create_all_buttons(self):
        # Creación de los botones de la interfaz gráfica
        self.create_button(self.photoAnadir, 34, 110, 150, 24, lambda: self.create_command("Añadir"))
        self.create_button(self.photoActualizar, 35, 183, 300, 19, lambda: self.create_command("Actualizar"))
        self.create_button(self.photoBorrar, 40, 110, 530, 22, lambda: self.create_command("Borrar"))

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

    def create_command(self, option):
        # Función para crear el comando asociado a cada botón
        if option == "Añadir":
            anadir(self.frameMostrar, self.archivo, self.tabla_actual)
        elif option == "Actualizar":
            actualizar(self.frameMostrar, self.archivo, self.tabla_actual)
        elif option == "Borrar":
            borrar(self.frameMostrar, self.archivo,self.tabla_actual)
    
    def load_options(self):
        # Obtención de las opciones para el menú desplegable
        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
            self.opciones = [fila[0] for fila in cursor.fetchall() if fila[0] != 'sqlite_sequence']