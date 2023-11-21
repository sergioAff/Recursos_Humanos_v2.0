import sqlite3 as sql
from tkinter import messagebox, simpledialog
from tkinter import *
from tkinter import ttk
from registros import Registro_Trabajador


def tablas(frameMostrar, archivo, tabla):
    for widget in frameMostrar.winfo_children():
        widget.destroy()

    tituloTabla = Label(text=f'Tabla: {tabla}', anchor='w')
    tituloTabla.config(bg='#082d44', font=(['Arial', 20]), fg='white')
    tituloTabla.place(
        height=40,
        width=500,
        x=10,
        y=80
    )

    if tabla:
        # Conectar a la base de datos
        conn = sql.connect(archivo)
        cursor = conn.cursor()

        # Verificar si la tabla existe
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tabla,))
        tabla_existe = cursor.fetchone()

        if tabla_existe:
            # Obtener los nombres de los atributos de la tabla
            cursor.execute(f"PRAGMA table_info({tabla})")
            atributos = [column[1] for column in cursor.fetchall()]

            # Obtener los valores de la tabla
            cursor.execute(f"SELECT * FROM {tabla}")
            valores = cursor.fetchall()

            # Crear el Treeview con estilo
            tree = ttk.Treeview(frameMostrar, columns=atributos, show='headings', height=min(len(valores), 10))

            # Estilo para hacer las líneas más visibles
            style = ttk.Style()
            style.configure("Treeview", font=('Arial', 14), rowheight=45)
            style.configure("Treeview.Heading", font=('Arial', 14, 'bold'))
            style.configure("Treeview.Treeview", background="#E1E1E1", fieldbackground="#E1E1E1", foreground="black")
            

            for atributo in atributos:
                tree.heading(atributo, text=atributo)

                # Ajustar el ancho de la columna según el texto más largo
                ancho = max(tree.heading(atributo)["text"].__len__(), *[len(str(valor[atributos.index(atributo)])) for valor in valores])
                tree.column(atributo, width=ancho * 15)  # Puedes ajustar el factor multiplicador según sea necesario

            for valor in valores:
                tree.insert('', 'end', values=valor)

            # Barras de desplazamiento
            scrollbar_y = Scrollbar(frameMostrar, orient="vertical", command=tree.yview)
            scrollbar_y.pack(side="right", fill="y")
            tree.configure(yscrollcommand=scrollbar_y.set)

            scrollbar_x = Scrollbar(frameMostrar, orient=HORIZONTAL, command=tree.xview)
            scrollbar_x.pack(side="bottom", fill="x")
            tree.configure(xscrollcommand=scrollbar_x.set)

            tree.pack(fill="both", expand=True)

        conn.close()

def actualizar(frameMostrar ,archivo, tabla_actual):

    with sql.connect(archivo) as conn:
            cursor = conn.cursor()

    while True:
        accion = simpledialog.askinteger("Actualizar Base de Datos", "Seleccione la acción:\n\n1. Cambiar valor de campo\n2. Añadir un valor de campo\n3-Para salir")

        if accion == 1:
                # Solicita el nombre del atributo (campo) a modificar
            campo = simpledialog.askstring("Cambiar Valor de Campo", "Introduce el nombre del atributo al que pertenece el valor que deseas cambiar:")
            if campo:
                    # Solicita el ID del registro que deseas modificar
                id_registro = simpledialog.askstring("Cambiar Valor de Campo", "Introduce el ID del registro al que pertenece el valor que deseas cambiar:")
                if id_registro:
                        # Solicita el nuevo valor para el campo
                    nuevo_valor = simpledialog.askstring("Cambiar Valor de Campo", "Introduce el nuevo valor para el campo:")
                    if nuevo_valor is not None:
                        try:
                                # Actualiza el valor en la base de datos
                            cursor.execute(f"UPDATE {tabla_actual} SET {campo} = ? WHERE id = ?", (nuevo_valor, int(id_registro)))
                            conn.commit()
                            messagebox.showinfo("Éxito", f"Valor del campo '{campo}' actualizado para el registro con ID {id_registro}.")
                            tablas(frameMostrar,archivo,tabla_actual)
                        except Exception as e:
                            messagebox.showerror("Error", str(e), ': Algun dato de los que insertó es erróneo' )

                    else:
                        continue
                else:
                    continue
            else:
                continue
        
        elif accion == 2:
            campo = simpledialog.askstring("Añadir Valor de Campo", "Introduce el nombre del atributo donde se quiere añadir el valor:")
            if campo:
                nuevo_valor = simpledialog.askstring("Añadir Valor de Campo", "Introduce el valor a añadir:")
                if nuevo_valor:
                    try:
                        cursor.execute(f"INSERT INTO {tabla_actual} ({campo}) VALUES (?)", (nuevo_valor,))
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Valor '{nuevo_valor}' añadido al campo '{campo}'.")
                        tablas(frameMostrar,archivo,tabla_actual)
                    except Exception as e:
                        messagebox.showerror(f'No se encontró el atributo : {e}')
                else:
                    continue
            else:
                continue
        
        elif accion==3:
            break

def borrar(frameMostrar,archivo, tabla_actual):
    
    with sql.connect(archivo) as conn:
        cursor=conn.cursor()

        while True:
            accion=simpledialog.askinteger('Borrar','Seleccione la acción\n\n1-Borrar registro\n2-Borrar un valor de un campo\n3-Para salir')

            if accion ==1:
                id_reg=simpledialog.askstring('Borrar','Ingrese el id del registro que se quiere eliminar o deje en blanco para regresar: ')
                if not id_reg:
                    continue

                cursor.execute(f'SELECT * FROM {tabla_actual} WHERE id=?',(id_reg,))    
                registro=cursor.fetchall()

                if registro is None:
                    messagebox.showerror(f'El id {id_registro} no existe en la tabla {tabla_actual}')
                else:
                    cursor.execute(f'DELETE FROM {tabla_actual} WHERE id = ?',(id_reg,))
                    conn.commit()
                    tablas(frameMostrar,archivo,tabla_actual)
                    messagebox.showinfo('Éxito',f'Se ha eliminado el registro con id {id_reg} de la tabla {tabla_actual}')
            
            elif accion == 2:
                campo = simpledialog.askstring("Borrar Valor de Campo", "Introduce el nombre del atributo al que pertenece el valor que quieres borrar:")
                if campo:
                    id_registro = simpledialog.askstring("Borrar Valor de Campo", "Introduce el ID del registro al que pertenece el valor que quieres borrar:")
                    if id_registro:
                        try:
                            cursor.execute(f"UPDATE {tabla_actual} SET {campo} = ? WHERE id = ?", (None, int(id_registro)))
                            conn.commit()
                            tablas(frameMostrar,archivo,tabla_actual)
                            messagebox.showinfo("Éxito", f"Valor del campo eliminado para el registro con ID.")
                        except Exception as e:
                            messagebox.showerror("Error", str(e))
                    else:
                        continue
            elif accion == 3:
                break

def anadir(archivo, tabla_actual):
    pass





#Este codigo puede servir para guardar los nuevos registros en la base de datos
""""elif accion == 4:
            cursor.execute(f"PRAGMA table_info({tabla_actual})")
            atributos_info = cursor.fetchall()
            atributos = [column[1] for column in atributos_info]
            autoincrementable = any(col[1] == 'INTEGER' and 'autoincrement' in col[2].lower() for col in atributos_info)
    
            valores = []

            for atributo in atributos:
                valor = simpledialog.askstring("Añadir Registro", f"Introduce el valor para el atributo '{atributo}':")
                valores.append(valor)

            if not autoincrementable:
                if "id" in atributos:
                    id_index = atributos.index("id")
                    provided_id = valores[id_index]

                    if provided_id:
                        cursor.execute(f"SELECT id FROM {tabla_actual} WHERE id = ?", (provided_id,))
                        existing_id = cursor.fetchone()
                        if existing_id:
                            messagebox.showerror("Error", "El ID proporcionado ya existe en la tabla.")
                            return

            if len(valores) == len(atributos):
                if autoincrementable and "id" not in atributos:
                        # No incluir el campo de ID en la inserción
                    atributos = atributos[1:]  # Ignorar el primer atributo (id)
                    valores = valores[1:]
            
                placeholders = ', '.join(['?' for _ in atributos])
                query = f"INSERT INTO {tabla_actual} ({', '.join(atributos)}) VALUES ({placeholders})"
                cursor.execute(query, valores)
                conn.commit()
                messagebox.showinfo("Éxito", "Registro agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se proporcionaron valores para todos los atributos.")"""