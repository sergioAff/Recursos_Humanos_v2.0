from tkinter import *
from PIL import ImageTk, Image
import sqlite3 as sql
from tkinter import messagebox
import re
from tkinter import ttk
from datetime import datetime
import traceback
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

        self.boton_limpiar = Button(self.frame_botones, text="LIMPIAR",command=lambda: self.limpiar(), height=2, width=10, bg="gray", fg="black",
                               font=("Comic Sans", 10, "bold"))
        self.boton_limpiar.pack(side='left', padx=3, pady=3)

        self.boton_cancelar = Button(self.frame_botones, text="CERRAR", command=lambda: self.window.destroy(), height=2, width=10, bg="red",
                                fg="black", font=("Comic Sans", 10, "bold"))
        self.boton_cancelar.pack(side='left', padx=3, pady=3)
        
        with sql.connect(self.archivo) as conn:
            self.cursor = conn.cursor()
            self.cursor.execute(f'PRAGMA table_info({tabla_actual})')
            self.atributos = self.cursor.fetchall()
            self.altrua_ventana=len(self.atributos) * 40 + 200
            self.window.geometry(f'500x{self.altrua_ventana}+{self.window.winfo_screenmmwidth()+600}+{0}')

            # Consulta PRAGMA foreign_key_list
            self.cursor.execute(f'PRAGMA foreign_key_list({tabla_actual})')
            self.foraneas = {foranea[3]:(foranea[2],foranea[3],foranea[4]) for foranea in self.cursor.fetchall()}

            self.entries = {}  # Diccionario para almacenar las Entry widgets
            self.identificadores_combobox = {}

            for atributo in self.atributos:
                if atributo[1] in self.foraneas:
                    self.label = Label(self.marco, text=atributo[1], font=('Comic Sans', 15))
                    self.label.grid(row=atributo[0], column=0, sticky=W, padx=5, pady=5)

                    # Crear una variable controladora para el combobox
                    codigo_var = StringVar()

                    # Asignar un identificador único al ComboBox
                    identificador_combobox = f"{self.tabla_actual}_{atributo[1]}"
                    self.identificadores_combobox[identificador_combobox] = codigo_var

                    # Consultar los valores del campo nombre de la tabla provincia
                    with sql.connect(self.archivo) as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT nombre FROM {self.foraneas[atributo[1]][0]}")
                        nombres_tablas = [nombre[0] for nombre in cursor.fetchall()]

                    # Crear el combobox con los valores obtenidos
                    combobox = ttk.Combobox(self.marco, values=nombres_tablas, textvariable=codigo_var, width=30, height=10)
                    combobox.grid(row=atributo[0], column=1, padx=5, pady=5, sticky=W)

                    # Al tocar el combobox, actualizar la variable controladora con el código correspondiente
                    combobox.bind("<<ComboboxSelected>>", lambda event, identificador=identificador_combobox: self.actualizar_codigo_var(identificador))
                    
                    combobox['state']='readonly'

                    self.entries[atributo[1]] = combobox  # Almacenar el combobox en el diccionario de entries

                    if atributo[1]=='codigoMunicipio':
                        combobox['state']='disable'

                else:

                    self.label = Label(self.marco, text=atributo[1], font=('Comic Sans', 15))
                    self.label.grid(row=atributo[0], column=0, sticky=W, padx=5, pady=5)

                    if atributo[1].lower()=='sexo':
                        self.sexo_var=StringVar()
                        self.radio_masculino=Radiobutton(self.marco, text="M", font=('Cosmic Sans',15), variable=self.sexo_var, value='M')
                        self.radio_femenino=Radiobutton(self.marco, text='F', font=('Cosmic Sans', 15), variable=self.sexo_var, value='F')
                        self.radio_masculino.grid(row=atributo[0], column=1, padx=5, pady=5, sticky=W)
                        self.radio_femenino.grid(row=atributo[0], column=1, padx=5, pady=5, sticky=E)
                        self.marco.rowconfigure(atributo[0],weight=1)
               
                        self.entries[atributo[1]] = self.sexo_var

                    elif atributo[1].lower() == 'correo':
                        self.correo = StringVar()
                        self.entry_correo = Entry(self.marco, textvariable=self.correo, font=('Comic Sans', 15))
                        self.entry_correo.grid(row=atributo[0], column=1, padx=5, pady=5)
                        self.entries[atributo[1]] = self.entry_correo

                    elif atributo[1].lower()=='tipoplaza':
                        self.tipo_plaza=StringVar()
                        self.opcionesPlaza=('','Plaza fija','Adiestr. laboral con plaza fija','Adiestr. laboral sin plaza fija','Rva. científica con plaza fija','Rva. científica sin plaza fija','Disponibles', 'Sin plaza')
                        self.spin_plaza=Spinbox(self.marco, values=self.opcionesPlaza, textvariable=self.tipo_plaza, font=('Cosmic Sans',15))
                        self.spin_plaza.config(state='readonly')
                        self.spin_plaza.grid(row=atributo[0], column=1, padx=5, pady=5, sticky=W)
                        self.entries[atributo[1]]=self.spin_plaza                
                
                    elif atributo[1].lower()=='cantidad':
                        self.cantidad=Spinbox(self.marco, from_=0, to=1000, width= 10, font=('Comic Sans', 15))
                        self.cantidad.grid(row=atributo[0], column=1, padx=5, pady=5, sticky=W)
                        self.entries[atributo[1]]=self.cantidad

                    elif atributo[1].lower()=='rangoedad':
                        self.rango_edad=StringVar()
                        self.opcionesEdades=('','Menores de 30','De 30 a 50', 'De 51 a 60', 'Mayores de 60')
                        self.spin_edades=Spinbox(self.marco, values=self.opcionesEdades,textvariable=self.rango_edad, font=('Comic Sans',15))
                        self.spin_edades.config(state='readonly')
                        self.spin_edades.grid(row=atributo[0], column=1, padx=5, pady=5, sticky=W)
                        self.entries[atributo[1]]=self.spin_edades

                    elif atributo[1].lower()=='nivelensenanza':
                        self.nivel=StringVar()
                        self.opcionesNivel=('','Nivel Superior','Técnico medio','Obrero calificado')
                        self.spin_niveles=Spinbox(self.marco, values=self.opcionesNivel,textvariable=self.nivel, font=('Comic Sans',15))
                        self.spin_niveles.config(state='readonly')
                        self.spin_niveles.grid(row=atributo[0], column=1, padx=5,pady=5, sticky=W)
                        self.entries[atributo[1]]=self.spin_niveles

                    elif atributo[1].lower()=='causa':
                        self.casuas=StringVar()
                        self.opcionesCausa=('','Jubilación','Personal')
                        self.sepin_causas=Spinbox(self.marco, values=self.opcionesCausa, textvariable=self.casuas, font=('Comic Sans',15))
                        self.sepin_causas.config(state='readonly')
                        self.sepin_causas.grid(row=atributo[0], column=1, padx=5,pady=5, sticky=W)
                        self.entries[atributo[1]]=self.sepin_causas
                  
                    else:
                        self.entry = Entry(self.marco, font=('Comic Sans', 15))
                        self.entry.grid(row=atributo[0], column=1, padx=5, pady=5)

                        self.entries[atributo[1]] = self.entry
                
                    # Deshabilitar el Entry correspondiente a la clave primaria en la función actualizar
                    if tipo == 'Actualizar' and atributo[5] == 1:  
                        self.entry.configure(state='readonly')
  
    def limpiar(self):
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set('')  
            elif isinstance(entry, Entry):
                entry.delete(0, END)
            elif isinstance(entry, StringVar):
                entry.set('')
            elif isinstance(entry,Spinbox):
                if entry.cget('state') == 'readonly':
                    entry.config(state='normal')
                    entry.delete(0,END)
                    entry.config(state='readonly')
                else:
                   entry.delete(0,END)
                   entry.insert(0,0)
        self.entries["codigoMunicipio"].configure(state='disable')
            
                   
    def anadir(self):
        # Verificar si todos los campos obligatorios están llenos
        for atributo in self.atributos:
            entry_widget = self.entries[atributo[1]]

            if atributo[2] == 1 and entry_widget.get() == "":
                messagebox.showerror("Error", f"El campo '{atributo[1]}' no puede estar vacío.")
                return
        
        if self.tabla_actual =='Demanda':
            self.cantidad_validacion()
            self.validar_demanda() 

        elif self.tabla_actual=='Especialidad':
            self.validar_especialidad()

        elif self.tabla_actual=='Municipio':
            self.validar_municipio()

        elif self.tabla_actual=='Provincia':
            self.validar_provincia()

        elif self.tabla_actual=='Entidad':
            self.validar_entidad()

        elif self.tabla_actual=='Organismo':
            self.validar_organismo()

        elif self.tabla_actual=='Carrera':
            self.validar_carrera()

        elif self.tabla_actual=='Trabajador':
            self.validar_correo()
            self.validar_correo_existente()
            self.validar_edad_y_sexo()
        
        elif self.tabla_actual=='Bajas':
            self.validar_causa()
        
    # Todos los campos obligatorios están llenos, guardar el registro en la base de datos
        self.valores = [entry_widget.get() for entry_widget in self.entries.values()]

        if self.atributos[0][1].lower()=='sexo':
            self.valores[0]=self.sexo_var.get()

        with sql.connect(self.archivo) as conn:
            self.cursor = conn.cursor()
            try:
                self.cursor.execute(f"INSERT INTO {self.tabla_actual} VALUES ({', '.join(['?']*len(self.valores))})", self.valores)
                conn.commit()
                self.actualizar_treeview(self.tabla_actual)
                messagebox.showinfo("Éxito", "Registro guardado exitosamente.")
            except sql.IntegrityError:
                messagebox.showerror('Error','El ID ya existe')
                raise Exception
            self.window.destroy()

    def cargar(self, datos):
        self.datos = datos
        # Carga las Entry widgets con los nuevos datos
        for i, atributo in enumerate(self.atributos):
            entry_widget = self.entries[atributo[1]]

            # Verifica si hay suficientes elementos en la lista datos
            if i < len(datos):
                if isinstance(entry_widget, Entry) or isinstance(entry_widget,Spinbox) :
                    if entry_widget.cget('state') == 'readonly':
                        entry_widget.config(state='normal')
                        entry_widget.delete(0, END)
                        entry_widget.insert(0, datos[i])
                        entry_widget.config(state='readonly')
                    elif isinstance(entry_widget,ttk.Combobox):
                        entry_widget.set(datos[i])

                    else:
                        entry_widget.delete(0, END)
                        entry_widget.insert(0, datos[i])

                else:
                    self.cargar_demas_valores(atributo, datos[i])

    def cargar_demas_valores(self, atributo, valor):
        if atributo[1].lower() == 'rangoedad':
            self.rango_edad.set(valor)
        elif atributo[1].lower() == 'tipoplaza':
            self.tipo_plaza.set(valor)
        elif atributo[1].lower() == 'sexo':
            self.sexo_var.set(valor)

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

        if self.tabla_actual =='Demanda':
            self.cantidad_validacion()
            self.validar_demanda() 
        
        elif self.tabla_actual=='Trabajador':
            self.validar_correo()
            self.validar_correo_existente()
            self.validar_edad_y_sexo()

        elif self.tabla_actual=='Especialidad':
            self.validar_especialidad() 

        elif self.tabla_actual=='Municipio':
            self.validar_municipio()

        elif self.tabla_actual=='Provincia':
            self.validar_provincia()

        elif self.tabla_actual=='Entidad':
            self.validar_entidad()

        elif self.tabla_actual=='Organismo':
            self.validar_organismo()

        elif self.tabla_actual=='Carrera':
            self.validar_carrera()
    
        elif self.tabla_actual=='Bajas':
            self.validar_causa()

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

# Validar que self.cantidad sea un entero
    def cantidad_validacion(self):
        try:
            cantidad = int(self.cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            raise ValueError
            
        # Validar que self.cantidad esté entre 0 y 1000
        if not (0 <= cantidad <= 1000):
            messagebox.showerror("Error", "La cantidad debe estar entre 0 y 1000.")
            raise ValueError
        
    def validar_correo(self):
        correo = self.entry_correo.get()

        # Utilizar una expresión regular para validar el formato del correo
        patron_correo = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not patron_correo.match(correo):
            messagebox.showerror("Error", "Formato de correo electrónico no válido.")
            raise ValueError
                
    def validar_especialidad(self):
        nombre_especialidad = self.entries['nombre'].get()
        if nombre_especialidad =='':
            messagebox.showerror('Alerta','No puede estar vacío el nombre de la especialidad')
            raise Exception
        
        if self.tipo == 'Actualizar' and nombre_especialidad ==self.datos[1]:
            return

        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM Especialidad WHERE nombre=?', (nombre_especialidad,))
            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror('Error', f"La especialidad '{nombre_especialidad}' ya existe. Ingrese un nombre único.")
                raise ValueError
            
    def validar_demanda(self):
        demanda = self.entries['nombreCarrera'].get()
        if demanda =='':
            messagebox.showerror('Alerta','No puede estar vacía el nombre de la Carrera')
            raise Exception

        if self.tipo == 'Actualizar' and demanda ==self.datos[1]:
            return

        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM Demanda WHERE nombreCarrera=?', (demanda,))
            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror('Error', f"{demanda} ya existe. Ingrese un nombre único.")
                raise ValueError
            
    def validar_municipio(self):
        municipio = self.entries['nombre'].get()
        if municipio =='':
            messagebox.showerror('Alerta','No puede estar vacía el municipio')
            raise Exception

        if self.tipo == 'Actualizar' and municipio ==self.datos[1]:
            return

        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM Municipio WHERE nombre=?', (municipio,))
            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror('Error', f"{municipio} ya existe. Ingrese un nombre único.")
                raise ValueError
    
    def validar_provincia(self):
        provincia = self.entries['nombre'].get()

        if provincia =='':
            messagebox.showerror('Alerta','No puede estar vacía la provincia')
            raise Exception
        
        if self.tipo == 'Actualizar' and provincia ==self.datos[1]:
            return

        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM Provincia WHERE nombre=?', (provincia,))
            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror('Error', f"{provincia} ya existe. Ingrese un nombre único.")
                raise ValueError
    
    def validar_entidad(self):
        entidad = self.entries['nombre'].get()
        if entidad =='':
            messagebox.showerror('Alerta','No puede estar vacío el nombre de la entidad')
            raise Exception

        if self.tipo == 'Actualizar' and entidad ==self.datos[1]:
            return

        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM Entidad WHERE nombre=?', (entidad,))
            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror('Error', f"{entidad} ya existe. Ingrese un nombre único.")
                raise ValueError
            
    def validar_correo_existente(self):
        correo=self.entries['correo'].get()
        if self.tipo=='Actualizar' and correo==self.datos[3]:
            return
        
        with sql.connect(self.archivo)as conn:
            cursor=conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM Trabajador WHERE correo=?',(correo,))
            count =cursor.fetchall()[0]

            if count[0] > 0:
                messagebox.showerror('Error', f"{correo} ya existe. Ingrese un nombre único.")
                raise ValueError
                        
    def validar_organismo(self):
        organismo = self.entries['nombre'].get()
        if organismo =='':
            messagebox.showerror('Alerta','No puede estar vacío el nombre del organismo')
            raise Exception

        if self.tipo == 'Actualizar' and organismo ==self.datos[1]:
            return

        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM Organismo WHERE nombre=?', (organismo,))
            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror('Error', f"{organismo} ya existe. Ingrese un nombre único.")
                raise ValueError

    def validar_carrera(self):
        carrera = self.entries['nombre'].get()
        if carrera =='':
            messagebox.showerror('Alerta','No puede estar vacío el nombre de la carrera')
            raise Exception

        if self.tipo == 'Actualizar' and carrera ==self.datos[1]:
            return

        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM Carrera WHERE nombre=?', (carrera,))
            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror('Error', f"{carrera} ya existe. Ingrese un nombre único.")
                raise ValueError
        
        if self.spin_niveles.get()==self.opcionesNivel[0]:
            messagebox.showinfo('Alerta','El nivel de enseñanza no puede estar vacío')
            raise Exception
        
    def validar_causa(self):
        causa=self.entries['causa'].get()
        

        if self.sepin_causas.get()==self.opcionesCausa[0]:
            messagebox.showinfo('Alerta','La causa no puede estar vacía')
            raise Exception
        
    def validar_edad_y_sexo(self):
        year=datetime.now().year
        try:
            entry=self.entries['id']
            carnet=entry.get()

            if len(carnet)!=11 or not carnet.isdigit() :
                messagebox.showerror('Error','Carnet incorrecto')
                raise Exception
        
            mes_nacimiento = int(carnet[2:4])
            if mes_nacimiento <1 or mes_nacimiento>12:
                messagebox.showinfo('Alerta','Carnet incorrecto en el 3er o 4to número')
                raise Exception
            else:
                dia_nacimiento = int(carnet[4:6])
                if mes_nacimiento==2 and dia_nacimiento >29:
                    messagebox.showinfo('Alerta','Carnet incorrecto en el 5to o 6to número, febrero no tiene mas de 29 días')
                    raise Exception
                elif dia_nacimiento<1 or dia_nacimiento>31:
                    messagebox.showinfo('Alerta','Carnet incorrecto en el 5to o 6to número')
                    raise Exception


            # Ajustar para manejar el escenario de un solo dígito para el año con cero adelante
            ano_nacimiento_str = carnet[0:2]
            ano_nacimiento = int(ano_nacimiento_str) + (2000 if ano_nacimiento_str.startswith('0') or ano_nacimiento_str.startswith('00') else 1900)

            # Calcular la edad
            edad = year - ano_nacimiento

            # Validar si ya ha cumplido años en este año
            if mes_nacimiento > datetime.now().month or (mes_nacimiento == datetime.now().month and dia_nacimiento > datetime.now().day):
                edad -= 1

            if edad < 30:
                if self.spin_edades.get() != self.opcionesEdades[1]:
                    messagebox.showinfo('Alerta','La edad debería ser menor de 30')
                    raise Exception

            elif 30 <= edad <= 50:
                if self.spin_edades.get() != self.opcionesEdades[2]:
                    messagebox.showinfo('Alerta','La edad debería estar entre 30 y 50')
                    raise Exception
            
            elif 51 <= edad <= 60 :
                if self.spin_edades.get() != self.opcionesEdades[3]:
                    messagebox.showinfo('Alerta','La edad debería estar entre 51 y 60')
                    raise Exception
            
            elif 61 <= edad <=99 :
                if self.spin_edades.get() != self.opcionesEdades[4]:
                    messagebox.showinfo('Alerta','La edad debería ser mayor de 60')
                    raise Exception
        
        except Exception:
            messagebox.showinfo('Alerta','Verifica el id o el rango de edad')
            raise ValueError

        try:            
            digito_sexo=int(carnet[-2])

            if digito_sexo % 2==0:
                if self.sexo_var.get()!='M':
                    messagebox.showinfo('Alerta','El sexo debe ser masculino')
                    raise Exception
            else:
                if self.sexo_var.get() != 'F':
                    messagebox.showinfo('Alerta','El sexo debería ser femenino')
                    raise Exception

        except Exception:
            messagebox.showinfo('Alerta','Revisa el id o el sexo')
            raise ValueError


    def actualizar_codigo_var(self, identificador):
        nombre_seleccionado = self.identificadores_combobox[identificador].get()
        _, atributo = identificador.split('_')

        # Consultar el código del dato seleccionado
        with sql.connect(self.archivo) as conn:
            cursor = conn.cursor()

            cursor.execute(f"SELECT {self.foraneas[atributo][2]} FROM {self.foraneas[atributo][0]} WHERE nombre = ?", (nombre_seleccionado,))
            codigo_tabla = cursor.fetchone()[0]

        # Actualizar la variable controladora con el código correspondiente
        self.entries[atributo].set(codigo_tabla)

        # Actualizar los valores del ComboBox correspondiente a f"{self.tabla_actual}_codigoMunicipio"
        if atributo == "codigoProvincia" and self.tabla_actual != 'Municipio':
            municipio_combobox = self.entries["codigoMunicipio"]

            # Obtener el código de provincia seleccionado
            codigo_provincia = self.entries["codigoProvincia"].get()

            #Modificar el estado y el valor del municipio si fue cambiado el de la provincia
            if codigo_provincia != '':
                municipio_combobox.set('')
                municipio_combobox.configure(state='readonly')

            # Consultar los nombres de municipios que corresponden a la provincia seleccionada
            cursor.execute(f"SELECT nombre FROM Municipio WHERE codigoProvincia = ?", (codigo_provincia,))
            nombres_municipios = [nombre[0] for nombre in cursor.fetchall()]

            # Actualizar los valores del ComboBox de municipios
            municipio_combobox["values"] = nombres_municipios

            municipio_combobox.configure(state='readonly')

    