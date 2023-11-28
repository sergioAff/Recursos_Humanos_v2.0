from tkinter import *
from PIL import ImageTk, Image
import sqlite3 as sql
from tkinter import messagebox

class Especialidad:

    def __init__(self, archivo, actualizar_treeview_callback, registro) :
        self.archivo=archivo
        self.actualizar_treeview = actualizar_treeview_callback
        self.registro=registro

        self.window_especialidades=Toplevel()
        self.window_especialidades.title("Especialidades")
        self.window_especialidades.resizable(0,0)
        self.window_especialidades.config(bd=10)

        self.titulo_especialidades = Label(self.window_especialidades, text=f'Modificar las especialidades de {self.registro[1]}', fg='black', font=('Comic Sans', 13, 'bold'), pady=5).pack()

        self.imagen_registro = Image.open("nuevo_usuario.png")
        self.nueva_imagen = self.imagen_registro.resize((40, 40))
        self.render = ImageTk.PhotoImage(self.nueva_imagen)
        self.label_imagen = Label(self.window_especialidades, image=self.render)
        self.label_imagen.image = self.render
        self.label_imagen.pack(pady=5)

        self.marco = LabelFrame(self.window_especialidades, text="Especialidades", font=("Comic Sans", 10, "bold"))
        self.marco.config(bd=2, pady=5)
        self.marco.pack()

        self.frame_botones = Frame(self.window_especialidades)
        self.frame_botones.pack(side='bottom')

        self.boton_eliminar = Button(self.frame_botones, text="ELIMINAR", height=2, width=10, bg="blue", fg="black",
                                font=("Comic Sans", 10, "bold"), command=lambda: self.eliminar())
        self.boton_eliminar.pack(side='left', padx=3, pady=3)

        self.boton_limpiar = Button(self.frame_botones, text="LIMPIAR",command=lambda: self.limpiar(), height=2, width=10, bg="gray", fg="black",
                               font=("Comic Sans", 10, "bold"))
        self.boton_limpiar.pack(side='left', padx=3, pady=3)

        self.boton_cancelar=Button(self.frame_botones, text='CERRAR', command=lambda:self.window_especialidades.destroy(), height=2, width=10, bg='red',fg='black', font=('Comic Sans',10,'bold'))
        self.boton_cancelar.pack(side='left',padx=3,pady=3)




    def limpiar(self):
        for entry in self.entries.values():
            if type(entry) == Entry:
                entry.delete(0,END)

    def eliminar(self):
        pass