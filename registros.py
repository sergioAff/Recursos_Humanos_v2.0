from tkinter import *
from PIL import ImageTk, Image
import sqlite3 as sql
from tkinter import messagebox
class Registro:

    def __init__(self, archivo, tabla_actual, tipo, actualizar_treeview_callback):
        self.archivo = archivo
        self.tabla_actual = tabla_actual
        self.tipo=tipo
        self.actualizar_treeview=actualizar_treeview_callback
        self.entries={}

        self.window = Toplevel() 
        self.window.title(self.tipo)
        self.window.resizable(0, 0)
        self.window.config(bd=10)


        # Título
        self.titulo = Label(self.window, text=f"{self.tipo} Registro {tabla_actual}", fg="black",
                       font=("Comic Sans", 13, "bold"), pady=5).pack()
        # Logo
        self.imagen_registro = Image.open("nuevo_usuario.png")
        self.nueva_imagen = self.imagen_registro.resize((40, 40))
        self.render = ImageTk.PhotoImage(self.nueva_imagen)
        self.label_imagen = Label(self.window, image=self.render)
        self.label_imagen.image = self.render
        self.label_imagen.pack(pady=5)

        # Marco
        self.marco = LabelFrame(self.window, text="Datos", font=("Comic Sans", 10, "bold"))
        self.marco.config(bd=2, pady=5)
        self.marco.pack()

        # Botones
        self.frame_botones = Frame(self.window)
        self.frame_botones.pack(side='bottom')

        if self.tipo == 'Añadir':

            self.boton_registrar = Button(self.frame_botones, text="REGISTRAR", height=2, width=10, bg="green", fg="black",
                                 font=("Comic Sans", 10, "bold"), command=lambda: self.anadir())
            self.boton_registrar.pack(side='left', padx=3, pady=3)

        elif self.tipo == 'Actualizar':

            self.boton_registrar = Button(self.frame_botones, text="ACTUALIZAR", height=2, width=10, bg="blue", fg="black",
                                 font=("Comic Sans", 10, "bold"), command=lambda: self.actualizar())
            self.boton_registrar.pack(side='left', padx=3, pady=3)        

        self.boton_limpiar = Button(self.frame_botones, text="LIMPIAR",command=self.limpiar, height=2, width=10, bg="gray", fg="black",
                               font=("Comic Sans", 10, "bold"))
        self.boton_limpiar.pack(side='left', padx=3, pady=3)

        self.boton_cancelar = Button(self.frame_botones, text="CERRAR", command=lambda: self.window.destroy(), height=2, width=10, bg="red",
                                fg="black", font=("Comic Sans", 10, "bold"))
        self.boton_cancelar.pack(side='left', padx=3, pady=3)
        

        with sql.connect(self.archivo) as conn:
            self.cursor = conn.cursor()
            self.cursor.execute(f'PRAGMA table_info({tabla_actual})')
            self.atributos = self.cursor.fetchall()

            self.window.geometry(f'380x{len(self.atributos) * 40 + 200}')

            self.entries = {}  # Diccionario para almacenar las Entry widgets

            for atributo in self.atributos:
                self.label = Label(self.marco, text=atributo[1], font=('Comic Sans', 15))
                self.label.grid(row=atributo[0], column=0, sticky=W, padx=5, pady=5)

                self.entry = Entry(self.marco, font=('Comic Sans', 15))
                self.entry.grid(row=atributo[0], column=1, padx=5, pady=5)

                self.entries[atributo[1]] = self.entry
                
                # Deshabilitar el Entry correspondiente a la clave primaria en la función actualizar
                if tipo == 'Actualizar' and atributo[5] == 1:  
                    self.entry.configure(state='readonly')

    def limpiar(self):
        for entry in self.entries.values():
            entry.delete(0,END)

    def anadir(self):
        # Verificar si todos los campos obligatorios están llenos
        for atributo in self.atributos:
            entry_widget = self.entries[atributo[1]]
            if atributo[2] == 1 and entry_widget.get() == "":
                messagebox.showerror("Error", f"El campo '{atributo[1]}' no puede estar vacío.")
                return

    # Todos los campos obligatorios están llenos, guardar el registro en la base de datos
        self.valores = [entry_widget.get() for entry_widget in self.entries.values()]

        with sql.connect(self.archivo) as conn:
            self.cursor = conn.cursor()
            try:
                self.cursor.execute(f"INSERT INTO {self.tabla_actual} VALUES ({', '.join(['?']*len(self.valores))})", self.valores)
                conn.commit()
                self.actualizar_treeview(self.tabla_actual)
                messagebox.showinfo("Éxito", "Registro guardado exitosamente.")
            except sql.IntegrityError:
                messagebox.showerror('Error','Dato incorrecto o faltante')
            self.window.destroy()


    def cargar(self, datos):
        self.datos = datos

        # Carga las Entry widgets con los nuevos datos
        for i, atributo in enumerate(self.atributos):
            entry_widget = self.entries[atributo[1]]
        
            # Verifica si hay suficientes elementos en la lista datos
            if i < len(datos):
                if entry_widget.cget('state')=='readonly':
                    entry_widget.config(state='normal')
                    entry_widget.delete(0,END)
                    entry_widget.insert(0,datos[i])
                    entry_widget.config(state='readonly')
                else:
                    entry_widget.delete(0,END)
                    entry_widget.insert(0,datos[i])

            
    def actualizar(self):
        # Obtener la clave primaria y sus índices
        primary_key_index = None
        primary_key_name = None
        for atributo in self.atributos:
            if atributo[5] == 1:  # Comprueba si el atributo es una clave primaria
                primary_key_index = atributo[0] - 1  # Resta 1 porque los índices comienzan desde 0
                primary_key_name = atributo[1]
                break
        
        # guarda el valor de la llave primaria
        primary_key_value = self.entries[primary_key_name].get()

        # Verificar si hay cambios en los valores antes de la actualización
        nuevos_valores = [entry_widget.get() for entry_widget in self.entries.values()]
        if nuevos_valores == list(self.datos):
            messagebox.showinfo("Información", "No hay cambios para actualizar.")
            return
        
        # Construir la sentencia SQL de actualización
        update_sql = f"UPDATE {self.tabla_actual} SET "
        update_sql += ", ".join(f"{atributo[1]} = ?" for atributo in self.atributos)
        update_sql += f" WHERE {primary_key_name} = ?"

        # Ejecutar la sentencia SQL de actualización
        with sql.connect(self.archivo) as conn:
            self.cursor = conn.cursor()
            self.cursor.execute(update_sql, nuevos_valores + [primary_key_value])
            conn.commit()
            self.actualizar_treeview(self.tabla_actual)
            messagebox.showinfo("Éxito", "Registro actualizado exitosamente.")
            self.window.destroy()