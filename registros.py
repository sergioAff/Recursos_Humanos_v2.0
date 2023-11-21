from tkinter import *
from PIL import ImageTk, Image
import sqlite3 as sql

class Registro:

    def __init__(self, archivo, tabla_actual):
        self.archivo=archivo
        self.tabla_actual=tabla_actual

        window = Toplevel()
        window.title('Añadir')
        window.resizable(0, 0)
        window.config(bd=10)

        # Título
        titulo = Label(window, text=f"Añadir a la tabla {tabla_actual}", fg="black", font=("Comic Sans", 13, "bold"),
                   pady=5).pack()

        # Logo
        imagen_registro = Image.open("nuevo_usuario.png")
        nueva_imagen = imagen_registro.resize((40, 40))
        render = ImageTk.PhotoImage(nueva_imagen)
        label_imagen = Label(window, image=render)
        label_imagen.image = render
        label_imagen.pack(pady=5)

        # Marco
        marco = LabelFrame(window, text="Datos", font=("Comic Sans", 10, "bold"))
        marco.config(bd=2, pady=5)
        marco.pack()

        # Botones
        frame_botones = Frame(window)
        frame_botones.pack(side='bottom')

        boton_registrar = Button(frame_botones, text="REGISTRAR", height=2, width=5, bg="green", fg="black",
                             font=("Comic Sans", 10, "bold"))
        boton_registrar.pack(side='left', padx=3, pady=3)

        boton_limpiar = Button(frame_botones, text="LIMPIAR", height=2, width=5, bg="gray", fg="black",
                           font=("Comic Sans", 10, "bold"))
        boton_limpiar.pack(side='left', padx=3, pady=3)

        boton_cancelar = Button(frame_botones, text="CERRAR", command=window.destroy, height=2, width=5, bg="red",
                            fg="black", font=("Comic Sans", 10, "bold"))
        boton_cancelar.pack(side='left', padx=3, pady=3)

        with sql.connect(archivo) as conn:
            cursor = conn.cursor()
            cursor.execute(f'PRAGMA table_info({tabla_actual})')
            atributos = cursor.fetchall()

            window.geometry(f'380x{len(atributos) *40+200}')

            for atributo in atributos:
                label=Label(marco, text=atributo[1], font=('Comic Sans',15))
                label.grid(row=atributo[0],column=0, sticky=W, padx=5, pady=5)

                entry=Entry(marco,font=('Comic Sans', 15))
                entry.grid(row=atributo[0], column=1, padx=5, pady=5)

    
    def anadir(self,tabla_actual):
        pass

    def actualizar (self,tabla_actual):
        pass
    
    def borrar(self,tabla_actual):
        pass