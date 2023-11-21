import sqlite3 as sql
from tkinter import messagebox, simpledialog, Label, Scrollbar, HORIZONTAL
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from registros import registro


def tablas(frame_mostrar, archivo, tabla):

    def crear_treeview(frame, atributos, valores):
        tree = ttk.Treeview(frame, columns=atributos, show='headings', height=min(len(valores), 10))

        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 14), rowheight=45)
        style.configure("Treeview.Heading", font=('Arial', 14, 'bold'))
        style.configure("Treeview.Treeview", background="#E1E1E1", fieldbackground="#E1E1E1", foreground="black")

        for atributo in atributos:
            tree.heading(atributo, text=atributo)

            ancho = max(tree.heading(atributo)["text"].__len__(), *[len(str(valor[atributos.index(atributo)])) for valor in valores])
            tree.column(atributo, width=ancho * 15)

        for valor in valores:
            tree.insert('', 'end', values=valor)

        return tree

    for widget in frame_mostrar.winfo_children():
        widget.destroy()

    titulo_tabla = Label(text=f'Tabla: {tabla}', anchor='w')
    titulo_tabla.config(bg='#082d44', font=(['Arial', 20]), fg='white')
    titulo_tabla.place(
        height=40,
        width=500,
        x=10,
        y=80
    )

    if tabla:
        with sql.connect(archivo) as conn:
            cursor = conn.cursor()

            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tabla,))
            tabla_existe = cursor.fetchone()

            if tabla_existe:
                cursor.execute(f"PRAGMA table_info({tabla})")
                atributos = [column[1] for column in cursor.fetchall()]

                cursor.execute(f"SELECT * FROM {tabla}")
                valores = cursor.fetchall()

                tree = crear_treeview(frame_mostrar, atributos, valores)

                scrollbar_y = Scrollbar(frame_mostrar, orient="vertical", command=tree.yview)
                scrollbar_y.pack(side="right", fill="y")
                tree.configure(yscrollcommand=scrollbar_y.set)

                scrollbar_x = Scrollbar(frame_mostrar, orient=HORIZONTAL, command=tree.xview)
                scrollbar_x.pack(side="bottom", fill="x")
                tree.configure(xscrollcommand=scrollbar_x.set)

                tree.pack(fill="both", expand=True)

def actualizar(frame_mostrar, archivo, tabla_actual):
    pass

def borrar(frame_mostrar, archivo, tabla_actual):
    pass


def anadir(frameMostrar,archivo, tabla_actual):

    registro(archivo,tabla_actual)