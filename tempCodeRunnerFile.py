from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from AL_HTML import AL_HTML
from AS_HTML import AS_HTML

# Crea una ventana principal
lectura = Tk()
# Inicializa TextArea aquí para que sea accesible globalmente
TextArea = scrolledtext.ScrolledText(lectura, font=("nunito", 9), width=90, height=38)

# Obtiene el ancho y el largo de la pantalla analizador lexico
ancho_pantalla = (lectura.winfo_screenwidth() / 2) - 50
largo_pantalla = lectura.winfo_screenheight() - 150

# Obtiene el ancho y el largo de la pantalla analizador sintactico
ancho_pantalla2 = lectura.winfo_screenwidth() - 50
largo_pantalla2 = lectura.winfo_screenheight() - 150

# Espaciado
espacio = None

def main():
    lectura_c()

def mostrarMensaje(componentes):
    # Crea una ventana secundaria
    lectura2 = Toplevel(lectura)
    # Calcula la posición x de la ventana secundaria para que aparezca a la derecha de la ventana principal
    posicion_x_lectura2 = lectura.winfo_x() + lectura.winfo_width() + 10
    # Configura la geometría de la ventana secundaria
    lectura2.geometry('{}x{}+{}+{}'.format(int(ancho_pantalla), int(largo_pantalla), posicion_x_lectura2, lectura.winfo_y()))
    lectura2.title("Analizador Léxico")
    etiqueta = Label(lectura2, text="SALIDA DE TOKENS - HTML")
    etiqueta.pack(pady=(25, 15))

    # Crear el estilo de la tabla
    style = ttk.Style()
    # Configurar el color de fondo y de texto del encabezado
    style.configure("Treeview.Heading", background="#F2F2F2", foreground="black")
    # Configurar el color de fondo y de texto de las filas
    style.configure("Treeview", background="#14283B", foreground="white")

    # Crear la tabla para mostrar los tokens
    tree = ttk.Treeview(lectura2, columns=("Columna 1", "Columna 2", "Columna 3"), show="headings", style="Treeview")
    tree.heading("Columna 1", text="Tipo")
    tree.heading("Columna 2", text="Descripcion")
    tree.heading("Columna 3", text="Valor")
    tree.pack(fill="both", expand=True, padx=15, pady=(15, 0))

    # Insertar datos en la tabla
    data = []
    for tipo, descripcion, valor in componentes:
        data.append([tipo, descripcion, valor])

    for row in data:
        tree.insert("", "end", values=row)

def obtener_cadena():
    analizadorS()

def lectura_c():
    lectura.geometry('{}x{}+{}+{}'.format(int(ancho_pantalla), int(largo_pantalla), 25, 20))
    lectura.title("Lectura Código")
    etiqueta = Label(lectura, text="INGRESA CADENA EN LENGUAJE HTML")
    etiqueta.pack(pady=(25, 15))
    # Configuramos un scroll para el text area
    TextArea.pack()
    # Agregamos un boton de validacion
    boton = Button(lectura, text=" Validar", bg='#253745', fg='white', command=obtener_cadena)
    boton.pack(pady=(15, 0))
    # Ciclamos la interfaz grafica
    lectura.mainloop()

# Función para centrar un elemento en un ancho específico
def centrar_elemento(elemento, ancho_columna):
    elemento_str = str(elemento)
    espacios_izquierda = (ancho_columna - len(elemento_str)) // 2
    return " " * espacios_izquierda + elemento_str 

def analizadorS():
    #Ancho del text area para mostrar el arbol sintactico
    ancho_columna = 396
    #Obtenemos la cadena de texto ingresada
    cadena = TextArea.get("1.0", END)
    # Pasamos la cadena de texto leida al analizador lexico
    AL = AL_HTML(cadena)
    # Obtenemos los componentes lexicos devueltos por el analizador lexico
    tokens = AL.A_Lex()
    mostrarMensaje(tokens)
    
    AS = AS_HTML(tokens)
    elementosA = AS.programa()
    
    # Crear una ventana para mostrar el resultado del análisis sintáctico
    lectura3 = Toplevel(lectura)
    posicion_x_lectura3 = lectura.winfo_x()
    lectura3.geometry('{}x{}+{}+{}'.format(int(ancho_pantalla2), int(largo_pantalla2), posicion_x_lectura3, lectura.winfo_y()))
    lectura3.title("Analizador Sintactico")
    lectura3.configure(bg='#253745')

    etiqueta = Label(lectura3, text="ARBOL SINTÁCTICO - HTML", bg='#253745', fg='white')
    etiqueta.pack(pady=(25, 15))

    TextArea2 = scrolledtext.ScrolledText(lectura3, font=("nunito", 10), width=198, height=39)
    TextArea2.pack()
    
    # Insertar las filas centradas en el TextArea
    if elementosA:
        for fila in elementosA:
            numero_columnas = len(fila) #Obtenemos el numero de columnas
            ancho_columna = ancho_columna // numero_columnas #Obtenemos la division en entero
            for elemento in fila:
                elemento_centrado = centrar_elemento(elemento, ancho_columna)
                if elemento.isupper():
                    TextArea2.insert(END, elemento_centrado, "mayusculas")
                else:
                    TextArea2.insert(END, elemento_centrado)
            TextArea2.insert(END, "\n\n")
    
    else:
        TextArea2.insert(END, "Análisis Sintáctico Fallido.\n")
 
    # Configuramos el color para las mayúsculas
    TextArea2.tag_config("mayusculas", foreground="#6F9292" , font=("nunito", 10, "bold"))
    errores(elementosA)
    lectura3.mainloop()


def errores(res):
    # Crear una ventana para mostrar el resultado del análisis sintáctico
    lectura4 = Toplevel(lectura)
    posicion_x_lectura3 = lectura.winfo_x()
    lectura4.geometry('{}x{}+{}+{}'.format(int(ancho_pantalla2/4), int(500), posicion_x_lectura3, lectura.winfo_y()))
    lectura4.title("Analizador Sintactico")
    lectura4.configure(bg='#870C1B')

    etiqueta = Label(lectura4, text="DETALLES - ANÁLISIS", bg='#870C1B', fg='white')
    etiqueta.pack(pady=(25, 15))

    TextArea3 = scrolledtext.ScrolledText(lectura4, font=("nunito", 10), width=42, height=33)
    TextArea3.pack(pady=(0, 50))  # Añadir un poco menos de espacio vertical
        
    if res:
        TextArea3.insert(END, "Análisis Sintáctico Exitoso.\n")
    else:
        TextArea3.insert(END, "Análisis Sintáctico Fallido.\n")
if __name__ == "__main__":
    main()