"""
FORMULARIO DE REGISTRO DE USUARIO
-Guardar en bd SQlite

"""
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
#Python image Library
from PIL import ImageTk, Image

import sqlite3

class Registro_Trabajador():
    def __init__(self, archivo, raiz):
        self.archivo=archivo
        self.window=tk.Toplevel(raiz)  
        self.window.title("FORMULARIO DE REGISTRO")
        self.window.geometry("390x630")
        self.window.resizable(0,0)
        self.window.config(bd=10)

        "--------------- Titulo --------------------"
        titulo= Label(self.window, text="REGISTRO DE TRABAJADOR",fg="black",font=("Comic Sans", 13,"bold"),pady=5).pack()

        "--------------- Nuevo usuario logo --------------------"
        imagen_registro=Image.open("nuevo_usuario.png")
        nueva_imagen=imagen_registro.resize((40,40))
        render=ImageTk.PhotoImage(nueva_imagen)
        label_imagen= Label(self.window, image= render)
        label_imagen.image=render
        label_imagen.pack(pady=5)

        "--------------- Marco --------------------"
        marco = LabelFrame(self.window, text="Datos personales",font=("Comic Sans", 10,"bold"))
        marco.config(bd=2,pady=5)
        marco.pack()

        "--------------- Formulario --------------------"
        label_dni=Label(marco,text="DNI: ",font=("Comic Sans", 10,"bold")).grid(row=0,column=0,sticky='s',padx=5,pady=8)
        self.dni=Entry(marco,width=25)
        self.dni.focus()
        self.dni.grid(row=0, column=1, padx=5, pady=8)

        label_nombres=Label(marco,text="Nombre: ",font=("Comic Sans", 10,"bold")).grid(row=1,column=0,sticky='s',padx=10,pady=8)
        self.nombres=Entry(marco,width=25)
        self.nombres.grid(row=1, column=1, padx=10, pady=8)

        label_apellidos=Label(marco,text="Apellidos: ",font=("Comic Sans", 10,"bold")).grid(row=2,column=0,sticky='s',padx=10,pady=8)
        self.apellidos=Entry(marco,width=25)
        self.apellidos.grid(row=2, column=1, padx=10, pady=8)

        label_sexo=Label(marco,text="Sexo: ",font=("Comic Sans", 10,"bold")).grid(row=3,column=0,sticky='s',padx=10,pady=8)
        self.combo_sexo=ttk.Combobox(marco,values=["Masculino", "Femenino"], width=22,state="readonly")
        self.combo_sexo.set("")
        self.combo_sexo.grid(row=3,column=1,padx=10,pady=8)

        label_edad=Label(marco,text="Edad: ",font=("Comic Sans", 10,"bold")).grid(row=4,column=0,sticky='s',padx=10,pady=8)
        self.edad=Entry(marco,width=25)
        self.edad.grid(row=4, column=1, padx=10, pady=8)

        label_correo=Label(marco,text="Correo electronico: ",font=("Comic Sans", 10,"bold")).grid(row=5,column=0,sticky='s',padx=10,pady=8)
        self.correo=Entry(marco,width=25)
        self.correo.grid(row=5, column=1, padx=10, pady=8)

        label_telefono = Label(marco, text="Teléfono: ", font=("Comic Sans", 10, "bold")).grid(row=6, column=0, sticky='s', padx=10, pady=8)
        self.telefono = Entry(marco, width=25)
        self.telefono.grid(row=6, column=1, padx=10, pady=8)

        label_direccion = Label(marco, text="Dirección: ", font=("Comic Sans", 10, "bold")).grid(row=7, column=0, sticky='s', padx=10, pady=8)
        self.direccion = Entry(marco, width=25)
        self.direccion.grid(row=7, column=1, padx=10, pady=8)

        label_edad = Label(marco, text="Edad: ", font=("Comic Sans", 10, "bold")).grid(row=8, column=0, sticky='s', padx=10, pady=8)
        self.edad = Entry(marco, width=25)
        self.edad.grid(row=8, column=1, padx=10, pady=8)

        label_tipo_plaza = Label(marco, text="Tipo de Plaza: ", font=("Comic Sans", 10, "bold")).grid(row=9, column=0, sticky='s', padx=10, pady=8)
        self.tipo_plaza = Entry(marco, width=25)
        self.tipo_plaza.grid(row=9, column=1, padx=10, pady=8)

        frame_botones=Frame(self.window)
        frame_botones.pack()

        "--------------- Botones --------------------"
        boton_registrar=Button(frame_botones,text="REGISTRAR" ,height=2,width=10,bg="green",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=1, padx=10, pady=15)
        boton_limpiar=Button(frame_botones,text="LIMPIAR",height=2,width=10,bg="gray",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=2, padx=10, pady=15)
        boton_cancelar=Button(frame_botones,text="CERRAR",command=self.window.destroy ,height=2,width=10,bg="red",fg="white",font=("Comic Sans", 10,"bold")).grid(row=0, column=3, padx=10, pady=15)
        

        self.window.mainloop()


