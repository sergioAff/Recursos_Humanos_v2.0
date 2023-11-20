from tkinter import *
from PIL import Image, ImageTk 
from funciones import tablas, actualizar, borrar
from registro_trabajador import Registro
from tkinter import filedialog, messagebox
import sqlite3 as sql
import traceback

class SecondScreen:
    def __init__(self):
        # Creacion y configuracion de la raiz
        self.root = Tk()
        self.root.geometry('1000x800')
        self.root.title('Recursos Humanos')
        self.root.resizable(0, 0)
        self.root.config(bg='#082d44') 

        try:
            self.archivo = filedialog.askopenfilename(initialdir="/", title="Selecciona la base de datos", filetypes=(("Bases de datos", "*.db"), ("all files", "*.*")))
            if self.archivo[-3:] != '.db':
                messagebox.showerror('Alerta', 'No se seleccionó una base de datos correcta')
                self.root.destroy()
                return
        except Exception as e:
            messagebox.showerror('Error', e)

        # Frame donde se mostrarán los datos
        self.frameMostrar = Frame(self.root, bg='#082d44', borderwidth=0, highlightthickness=0)
        self.frameMostrar.place(
            height=650,
            width=900,
            x=50,
            y=130)
        self.frameMostrar.grid_rowconfigure(0, weight=1)
        self.frameMostrar.grid_columnconfigure(0, weight=1)

        # Importar cada imagen para cada botón
        try:
            img_boton_tablas = Image.open('Tablas.png')
            self.photoTablas = ImageTk.PhotoImage(img_boton_tablas)

            img_boton_anadir = Image.open('Añadir.png')
            self.photoAnadir = ImageTk.PhotoImage(img_boton_anadir)            

            img_boton_actualizar = Image.open('Actualizar.png') 
            self.photoActualizar = ImageTk.PhotoImage(img_boton_actualizar)

            img_boton_borrar = Image.open('Borrar.png')
            self.photoBorrar = ImageTk.PhotoImage(img_boton_borrar)

            # Creación de las opciones para el menú desplegable
            with sql.connect(self.archivo) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
                self.opciones = [fila[0] for fila in cursor.fetchall() if fila[0] != 'sqlite_sequence']

            # Creación del menú desplegable
            self.opcionSeleccionada = StringVar(self.root)
            self.opcionSeleccionada.set(self.opciones[0])  # Opción predeterminada

            # Creacion y configuracion de cada botón

            # Modificación del botón para que muestre el menú desplegable
            self.botonTablas = Menubutton(
                image=self.photoTablas,
                cursor='hand2',
                borderwidth=0,
                highlightthickness=0
            )   

            self.botonTablas.menu = Menu(self.botonTablas, tearoff=0)
            self.botonTablas["menu"] = self.botonTablas.menu

            self.leer_tablas(self.botonTablas, tablas)

            self.botonTablas.place(
                height=30,
                width=70,
                x=25,
                y=28,
            )
            
            self.botonAnadir = Menubutton(
                image=self.photoAnadir,
                cursor='hand2',
                borderwidth=0,
                highlightthickness=0
            )

            self.botonAnadir.menu = Menu(self.botonAnadir, tearoff=0)
            self.botonAnadir['menu'] = self.botonAnadir.menu

            self.botonAnadir.place(
                height=34,
                width=110,
                x=150,
                y=24
            )         

            self.botonActualizar = Button(
                image=self.photoActualizar,
                cursor='hand2',
                command=lambda: actualizar(self.archivo),
                borderwidth=0,
                highlightthickness=0
            )

            self.botonActualizar.place(
                height=35,
                width=183,
                x=300,
                y=19
            )
            
            self.botonBorrar = Button(
                image=self.photoBorrar,
                cursor='hand',
                command=lambda: borrar(self.archivo),
                borderwidth=0,
                highlightthickness=0
            )

            self.botonBorrar.place(
                height=40,
                width=110,
                x=530,
                y=22

            )

        except Exception as e:
            print(e)
            messagebox.showerror(e)
            traceback.print_exc()

        self.root.mainloop()
                
    # Funcion para asignar tablas a cada botón de la interfaz
    def leer_tablas(self, boton, self_boton):
        for opcion in self.opciones:
            boton.menu.add_command(
                label=opcion, command=lambda opt=opcion: self_boton(self.frameMostrar, self.archivo, opt))
