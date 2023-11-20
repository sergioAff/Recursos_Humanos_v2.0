import sqlite3 as sql
from tkinter import messagebox, simpledialog
from tkinter import *
from tkinter import ttk


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

def actualizar(archivo):
    nombre_tabla = simpledialog.askstring('Tabla a trabajar', 'Nombre de la tabla en la que quiere trabajar')
    if not nombre_tabla:
        messagebox.showerror('Aviso', 'No se introdujo ningún nombre para la tabla')
        return

    conn = sql.connect(archivo)
    cursor = conn.cursor()

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nombre_tabla,))
    tabla_existe = cursor.fetchone()

    if not tabla_existe:
        messagebox.showerror('Aviso', f'{nombre_tabla} no existe en la base de datos')
        conn.close()
        return

    while True:
        accion = simpledialog.askinteger("Actualizar Base de Datos", "Seleccione la acción:\n\n1. Cambiar valor de campo\n2. Añadir un valor de campo\n3-Para salir")
        if not accion:
            break

        elif accion == 1:
                # Solicita el nombre del atributo (campo) a modificar
            campo = simpledialog.askstring("Cambiar Valor de Campo", "Introduce el nombre del atributo al que pertenece el valor que deseas cambiar:")
            if campo:
                    # Solicita el ID del registro que deseas modificar
                id_registro = simpledialog.askstring("Cambiar Valor de Campo", "Introduce el ID del registro al que pertenece el valor que deseas cambiar:")
                if id_registro:
                        # Solicita el nuevo valor para el campo
                    nuevo_valor = simpledialog.askstring("Cambiar Valor de Campo", f"Introduce el nuevo valor para el campo '{campo}':")
                    if nuevo_valor is not None:
                        try:
                                # Actualiza el valor en la base de datos
                            cursor.execute(f"UPDATE {nombre_tabla} SET {campo} = ? WHERE id = ?", (nuevo_valor, int(id_registro)))
                            conn.commit()
                            messagebox.showinfo("Éxito", f"Valor del campo '{campo}' actualizado para el registro con ID {id_registro}.")
                        except Exception as e:
                            messagebox.showerror("Error", str(e))

        elif accion == 2:
            campo = simpledialog.askstring("Añadir Valor de Campo", "Introduce el nombre del atributo donde se quiere añadir el valor:")
            if campo:
                nuevo_valor = simpledialog.askstring("Añadir Valor de Campo", "Introduce el valor a añadir:")
                if nuevo_valor:
                    try:
                        cursor.execute(f"INSERT INTO {nombre_tabla} ({campo}) VALUES (?)", (nuevo_valor,))
                        conn.commit()
                        messagebox.showinfo("Éxito", f"Valor '{nuevo_valor}' añadido al campo '{campo}'.")
                    except Exception as e:
                        messagebox.showerror(f'No se encontró el atributo : {e}')

        elif accion == 4:
            cursor.execute(f"PRAGMA table_info({nombre_tabla})")
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
                        cursor.execute(f"SELECT id FROM {nombre_tabla} WHERE id = ?", (provided_id,))
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
                query = f"INSERT INTO {nombre_tabla} ({', '.join(atributos)}) VALUES ({placeholders})"
                cursor.execute(query, valores)
                conn.commit()
                messagebox.showinfo("Éxito", "Registro agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se proporcionaron valores para todos los atributos.")
        elif accion==3:
            break
def borrar(archivo):
        # Crear una ventana
    nombre_tabla=simpledialog.askstring('Tabla a modificar','Nombre de la tabla que quieres modificar')
    if not nombre_tabla:
        messagebox.showerror('Aviso', 'No se introdujo ningún nombre para la tabla')
        return
    
    with sql.connect(archivo) as conn:
        cursor=conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nombre_tabla,))
        tabla_existe=cursor.fetchall()

        if not tabla_existe:
            messagebox.showerror('Alerta',f'{nombre_tabla} no existe en la base de datos')
            return
        
        while True:
            accion=simpledialog.askinteger('Borrar','Seleccione la acción\n\n1-Borrar registro\n2-Borrar un valor de un campo\n3-Para salir')
            if not accion:
                break
        
            elif accion ==1:
                id_reg=simpledialog.askstring('Borrar','Ingrese el id del registro que se quiere eliminar o deje en blanco para regresar: ')
                if not id_reg:
                    continue

                cursor.execute(f'SELECT * FROM {nombre_tabla} WHERE id=?',(id_reg,))    
                registro=cursor.fetchall()

                if registro is None:
                    messagebox.showerror(f'El id {id_registro} no existe en la tabla {nombre_tabla}')

                else:
                    cursor.execute(f'DELETE FROM {nombre_tabla} WHERE id = ?',(id_reg,))
                    messagebox.showinfo('Éxito',f'Se ha eliminado el registro con id {id_reg} de la tabla {nombre_tabla}')
            
            elif accion == 2:
                campo = simpledialog.askstring("Borrar Valor de Campo", "Introduce el nombre del atributo al que pertenece el valor que quieres borrar: (Columna)")
                if campo:
                    id_registro = simpledialog.askstring("Borrar Valor de Campo", "Introduce el ID del registro al que pertenece el valor que quieres borrar: (Fila)")
                    if id_registro:
                        try:
                            cursor.execute(f"UPDATE {nombre_tabla} SET {campo} = ? WHERE id = ?", (None, int(id_registro)))
                            conn.commit()
                            messagebox.showinfo("Éxito", f"Valor del campo '{campo}' eliminado para el registro con ID {id_registro}.")
                        except Exception as e:
                            messagebox.showerror("Error", str(e))

            elif accion == 3:
                break
