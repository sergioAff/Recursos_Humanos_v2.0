from tkinter import *
from PIL import ImageTk, Image
import sqlite3 as sql
from tkinter import messagebox

class Especialidad:

    def __init__(self,tabla_actual, archivo, actualizar_treeview_callback, registro) :
        self.archivo=archivo
        self.actualizar_treeview = actualizar_treeview_callback
        self.registro=registro
        self.tabla_actual=tabla_actual
        self.codigo_carrera=registro[0]

        self.window_especialidades=Toplevel()
        self.window_especialidades.title("Especialidades")
        self.window_especialidades.resizable(0,0)
        self.window_especialidades.config(bd=10)

        # Obtener la posición actual de la ventana principal
        x_pos, y_pos = self.window_especialidades.winfo_x(), self.window_especialidades.winfo_y()

        # Obtener el ancho de la pantalla
        screen_width = self.window_especialidades.winfo_screenwidth()

        # Calcular la nueva posición para la ventana de especialidades
        nueva_x_pos = screen_width - self.window_especialidades.winfo_reqwidth() - 300  # Puedes ajustar el valor 10 según tus necesidades
        nueva_y_pos = y_pos + 250  # Ajusta este valor según tus necesidades

        # Establecer la geometría de la nueva ventana
        self.window_especialidades.geometry(f'+{nueva_x_pos}+{nueva_y_pos}')

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

        self.boton_salir=Button(self.frame_botones, text='SALIR', command=lambda:self.window_especialidades.destroy(), height=2, width=10, bg='red',fg='black', font=('Comic Sans',10,'bold'))
        self.boton_salir.pack(side='left',padx=3,pady=3)

        with sql.connect(self.archivo) as conn:
            self.cursor=conn.cursor()
            self.cursor.execute('SELECT nombre FROM Especialidad WHERE codigoCarrera=?', (self.codigo_carrera,))
            self.resultados=self.cursor.fetchall()
            
            self.fila=0

            if self.resultados==[]:
                self.label=Label(self.marco, text=f'No hay especialidades para {self.registro[1]}', font=('Cosmic Sans', 15))
                self.label.grid(row=self.fila, column=0, sticky=W, padx=5, pady=5)
            
            else:
                for especialidad in self.resultados:
                    self.label=Label(self.marco, text=especialidad[0], font=('Cosmic Sans', 15))
                    self.label.grid(row=self.fila, column=0, sticky=W,padx=5, pady=5)

                    self.boton_eliminar = Button(self.marco, text='X', command=lambda esp=especialidad[0]: self.confirmar_eliminar(esp))
                    self.boton_eliminar.grid(row=self.fila, column=1, padx=5, pady=5)

                    self.fila+=1

    def confirmar_eliminar(self, especialidad):
        respuesta = messagebox.askokcancel("Confirmar", f"¿Eliminar la especialidad '{especialidad}'?")
        if respuesta:
            # Eliminar la especialidad de la base de datos y actualizar la GUI
            self.eliminar_especialidad(especialidad)

    def eliminar_especialidad(self, especialidad):

        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Especialidad WHERE codigoCarrera=? AND nombre=?', (self.codigo_carrera, especialidad))
            conn.commit()
        
        self.actualizar_treeview(self.tabla_actual)
        self.actualizar_toplevel()

    def actualizar_toplevel(self):

        self.window_especialidades.destroy()
        self.__init__(self.tabla_actual, self.archivo, self.actualizar_treeview, self.registro)