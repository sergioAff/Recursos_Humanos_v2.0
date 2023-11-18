import tkinter as tk
from tkinter import filedialog, messagebox
from funciones import borrar, abrir, actualizar
from registro_trabajador import Registro
from PIL import Image, ImageTk
import sqlite3 as sql

class SecondScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1000x800')
        self.root.title('Recursos Humanos')
        self.root.resizable(0, 0)
        self.root.config(bg='#082d44')
        self.photoTablas = self.cargar_imagen('Tablas.png')
        self.photoAbrir = self.cargar_imagen('Abrir.png')

        try:
            self.archivo = filedialog.askopenfilename(
                initialdir="/",
                title="Selecciona la base de datos",
                filetypes=(("Bases de datos", "*.db"), ("all files", "*.*"))
            )
            if not self.archivo.endswith('.db'):
                messagebox.showerror('Alerta', 'No se seleccionó una base de datos correcta')
                self.root.destroy()
                return
        except Exception as e:
            messagebox.showerror('Error', f'Error al seleccionar la base de datos: {e}')

        self.frameMostrar = self.crear_frame_mostrar()

        opciones = self.obtener_opciones_tablas()

        self.botonTablas = self.crear_boton_tablas(opciones)

        self.botonAbrir = self.crear_boton(
            image_path='Abrir.png',
            command=lambda: Registro(self.archivo, self.root),
            height=40, width=95, x=130, y=20
        )

        self.botonActualizar = self.crear_boton(
            image_path='Actualizar.png',
            command=lambda: actualizar(self.archivo),
            height=30, width=145, x=250, y=23
        )

        self.botonBorrar = self.crear_boton(
            image_path='Borrar.png',
            command=lambda: borrar(self.archivo),
            height=40, width=110, x=430, y=21
        )

        self.root.mainloop()

    def crear_frame_mostrar(self):
        frame = tk.Frame(self.root, bg='#082d44', borderwidth=0, highlightthickness=0)
        frame.place(height=650, width=900, x=50, y=130)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        return frame

    def obtener_opciones_tablas(self):
        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            opciones = [fila[0] for fila in cursor.fetchall() if fila[0] != 'sqlite_sequence']
        return opciones

    def crear_boton_tablas(self, opciones):
        boton = tk.Menubutton(
            self.root,
            image=self.cargar_imagen('Tablas.png'),
            cursor='hand2',
            borderwidth=0,
            highlightthickness=0
        )

        boton.menu = tk.Menu(boton, tearoff=0)
        boton["menu"] = boton.menu

        for opcion in opciones:
            boton.menu.add_command(
                label=opcion,
                command=lambda opt=opcion: abrir(self.frameMostrar, self.archivo, opt)
            )

        boton.place(height=30, width=70, x=20, y=26)

        return boton

    def cargar_imagen(self, imagen_path):
        imagen = Image.open(imagen_path)
        imagen_tk = ImageTk.PhotoImage(imagen)
        return imagen_tk


    def crear_boton(self, image_path, command, height, width, x, y):
        boton = tk.Button(
            image=self.cargar_imagen(image_path),
            cursor='hand2',
            command=command,
            borderwidth=0,
            highlightthickness=0
        )

        boton.place(height=height, width=width, x=x, y=y)
        return boton

if __name__ == "__main__":
    SecondScreen()
