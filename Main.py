from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from SecondScreen import Second_Screen

class Screen:
    # Constantes para dimensiones de la ventana y botón
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    BUTTON_WIDTH = 290
    BUTTON_HEIGHT = 90

    def __init__(self):
        # Inicialización de la interfaz de usuario
        self.setup_ui()

    def setup_ui(self):
        # Configuración de la ventana principal
        self.root = Tk()
        self.root.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')
        self.root.title('Recursos Humanos')
        self.root.resizable(0, 0)
        self.root.config(bg='#082d44')
        try:
            self.icono = PhotoImage(file='icono.png')
            self.root.iconphoto(True, self.icono)
        except Exception:
            messagebox.showerror('Alerta','No se pudo cargar el icono')
        # Carga de imágenes
        self.load_images()

        # Creación del botón Comenzar
        self.botonComenzar = Button(
            image=self.photoBotonComenzar,
            command=self.comenzar,
            cursor='hand2',
            borderwidth=0,
            highlightthickness=0
        )

        # Posicionamiento centrado del botón
        self.place_button_centered()

        self.root.mainloop()

    def load_images(self):
        try:
            # Uso de 'with' para garantizar que el recurso se cierre adecuadamente
            with Image.open('Comenzar.png') as img_boton_comenzar:
                self.photoBotonComenzar = ImageTk.PhotoImage(img_boton_comenzar)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def place_button_centered(self):
        # Posiciona el botón en el centro de la ventana
        self.botonComenzar.place(
            height=self.BUTTON_HEIGHT,
            width=self.BUTTON_WIDTH,
            x=(self.WINDOW_WIDTH - self.BUTTON_WIDTH) // 2,
            y=(self.WINDOW_HEIGHT - self.BUTTON_HEIGHT) // 2
        )

    def comenzar(self):
        # Cierra la ventana actual y crea la segunda pantalla
        self.root.destroy()
        self.secondScreen = Second_Screen()

if __name__ == "__main__":
    # Llamada a la función 'run' solo si el script es ejecutado directamente
    Screen()
