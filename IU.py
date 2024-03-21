from tkinter import *
from tkinter import messagebox
from ArbolAVL import Arbol

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename

from PIL import Image,ImageTk

from pdf2image import convert_from_path
import os

root = Tk()
root.title('Árboles AVL')
root.geometry('1280x720')

root.configure(bg='#fff')
root.resizable(False, False)


arbol = Arbol()

widgets = []
eliminar = None
buscar_n = None
buscar_c = None
buscar_pmax = None
buscar_pmin = None
nodo_slc = None

id_nodo_slc = 0

img_portada = PhotoImage(file='img\Portada.png')
menu = PhotoImage(file='img\Menu.png')

def graficarPortada ():
    limpiarPantalla ()
    
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    bg = canvas.create_image(0, 0, anchor=NW, image=img_portada)
    widgets.append(canvas)

    button = Button(root, width=25, height=2, text="Ingresar", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=graficarMenuPrincipal, autostyle=False)
    button_window = canvas.create_window(880, 260, anchor=NW, window=button)
    widgets.append(button)

    button = Button(root, width=25, height=2, text="Salir", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=cerrar, autostyle=False)
    button_window = canvas.create_window(880, 420, anchor=NW, window=button)
    widgets.append(button)
    
def graficarMenuPrincipal ():
    limpiarPantalla ()
    
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    bg = canvas.create_image(0, 0, anchor=NW, image=menu)
    widgets.append(canvas)

    button = Button(root, width=25, height=2, text="Insertar Nodo", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=insertarNodo, autostyle=False)
    button_window = canvas.create_window(450, 200, anchor=NW, window=button)
    widgets.append(button)
    
    button = Button(root, width=25, height=2, text="Eliminar Nodo", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=eliminarNodo, autostyle=False)
    button_window = canvas.create_window(450, 280, anchor=NW, window=button)
    widgets.append(button)
    
    # Entrada Nombre de Nodo
    def on_enter(e):
        eliminar.delete(0, 'end')
    
    def on_leave(e):
        name = eliminar.get()
        if name == '':
            eliminar.insert(0, 'Nodo a Eliminar')
    
    global eliminar

    eliminar = Entry(root, width=20, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), autostyle=False)
    eliminar.place(x=780, y=300)
    eliminar.insert(0, 'Nodo a Eliminar')
    frame = Frame(root, width=250, height=2, bg='black')
    frame.place(x=780, y=325)
    widgets.append(frame)
    eliminar.bind('<FocusIn>', on_enter)
    eliminar.bind('<FocusOut>', on_leave)
    widgets.append(eliminar)
    
    button = Button(root, width=25, height=2, text="Buscar Nodo por Nombre", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=buscarPorNombre, autostyle=False)
    button_window = canvas.create_window(450, 360, anchor=NW, window=button)
    widgets.append(button)
    
    # Entrada Nombre de Nodo
    def on_enter(e):
        buscar_n.delete(0, 'end')
    
    def on_leave(e):
        name = buscar_n.get()
        if name == '':
            buscar_n.insert(0, 'Nombre del Nodo')
    
    global buscar_n

    buscar_n = Entry(root, width=20, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), autostyle=False)
    buscar_n.place(x=780, y=380)
    buscar_n.insert(0, 'Nombre del Nodo')
    frame = Frame(root, width=250, height=2, bg='black')
    frame.place(x=780, y=405)
    widgets.append(frame)
    buscar_n.bind('<FocusIn>', on_enter)
    buscar_n.bind('<FocusOut>', on_leave)
    widgets.append(buscar_n)
    
    button = Button(root, width=25, height=2, text="Buscar Nodo por Categoría", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=buscarPorCategoria, autostyle=False)
    button_window = canvas.create_window(450, 440, anchor=NW, window=button)
    widgets.append(button)
    
    # Entrada Nombre de Nodo
    def on_enter(e):
        buscar_c.delete(0, 'end')
    
    def on_leave(e):
        name = buscar_c.get()
        if name == '':
            buscar_c.insert(0, 'Nombre del Nodo')
    
    global buscar_c

    buscar_c = Entry(root, width=20, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), autostyle=False)
    buscar_c.place(x=780, y=460)
    buscar_c.insert(0, 'Nombre del Nodo')
    frame = Frame(root, width=250, height=2, bg='black')
    frame.place(x=780, y=485)
    widgets.append(frame)
    buscar_c.bind('<FocusIn>', on_enter)
    buscar_c.bind('<FocusOut>', on_leave)
    widgets.append(buscar_c)
    
    button = Button(root, width=25, height=2, text="Buscar Nodo por Tamaño", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=buscarPorPeso, autostyle=False)
    button_window = canvas.create_window(450, 520, anchor=NW, window=button)
    widgets.append(button)
    
    # Entrada Nombre de Nodo
    def on_enter(e):
        buscar_pmin.delete(0, 'end')
    
    def on_leave(e):
        name = buscar_pmin.get()
        if name == '':
            buscar_pmin.insert(0, 'Mínimo')
    
    global buscar_pmin

    buscar_pmin = Entry(root, width=10, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), autostyle=False)
    buscar_pmin.place(x=780, y=540)
    buscar_pmin.insert(0, 'Mínimo')
    frame = Frame(root, width=100, height=2, bg='black')
    frame.place(x=780, y=565)
    widgets.append(frame)
    buscar_pmin.bind('<FocusIn>', on_enter)
    buscar_pmin.bind('<FocusOut>', on_leave)
    widgets.append(buscar_pmin)
    
    # Entrada Nombre de Nodo
    def on_enter(e):
        buscar_pmax.delete(0, 'end')
    
    def on_leave(e):
        name = buscar_pmax.get()
        if name == '':
            buscar_pmax.insert(0, 'Máximo')
    
    global buscar_pmax

    buscar_pmax = Entry(root, width=10, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), autostyle=False)
    buscar_pmax.place(x=900, y=540)
    buscar_pmax.insert(0, 'Máximo')
    frame = Frame(root, width=100, height=2, bg='black')
    frame.place(x=900, y=565)
    widgets.append(frame)
    buscar_pmax.bind('<FocusIn>', on_enter)
    buscar_pmax.bind('<FocusOut>', on_leave)
    widgets.append(buscar_pmax)
    
    button = Button(root, width=25, height=2, text="Imprimir por Nivel", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=imprimirPorNivel, autostyle=False)
    button_window = canvas.create_window(450, 600, anchor=NW, window=button)
    widgets.append(button)

def graficarMenuSecundario ():
    global id_nodo_slc
    try:
        id_nodo_slc = nodo_slc.get()
    except:
        pass
    
    limpiarPantalla ()
    
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    bg = canvas.create_image(0, 0, anchor=NW, image=menu)
    widgets.append(canvas)

    button = Button(root, width=25, height=2, text="Obtener Nivel", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=nivelNodo, autostyle=False)
    button_window = canvas.create_window(450, 200, anchor=NW, window=button)
    widgets.append(button)
    
    button = Button(root, width=25, height=2, text="Factor de Balanceo", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=balanceoNodo, autostyle=False)
    button_window = canvas.create_window(450, 280, anchor=NW, window=button)
    widgets.append(button)

    button = Button(root, width=25, height=2, text="Padre del Nodo", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=padreNodo, autostyle=False)
    button_window = canvas.create_window(450, 360, anchor=NW, window=button)
    widgets.append(button)
    
    button = Button(root, width=25, height=2, text="Abuelo del Nodo", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=abueloNodo, autostyle=False)
    button_window = canvas.create_window(450, 440, anchor=NW, window=button)
    widgets.append(button)
    
    button = Button(root, width=25, height=2, text="Tío del Nodo", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=tioNodo, autostyle=False)
    button_window = canvas.create_window(450, 520, anchor=NW, window=button)
    widgets.append(button)
    
    button = Button(root, width=25, height=2, text="Volver", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=graficarMenuPrincipal, autostyle=False)
    button_window = canvas.create_window(450, 600, anchor=NW, window=button)
    widgets.append(button)

def nivelNodo():
    limpiarPantalla ()
    
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    bg = canvas.create_image(0, 0, anchor=NW, image=menu)
    widgets.append(canvas)
    
    global nodo_slc
    nodo = lista[int(id_nodo_slc)]
    dato = arbol.altura(arbol.raiz)-arbol.altura(nodo)
    texto = f'El Nivel es : {dato}'
    
    text = Label(root, width=25, height=2, text=texto, font=("Arial", 25))
    widgets.append(text)
    text.place(x=390, y=440)
    
    button = Button(root, width=25, height=2, text="Volver", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=graficarMenuSecundario, autostyle=False)
    button_window = canvas.create_window(450, 600, anchor=NW, window=button)
    widgets.append(button)

def balanceoNodo():
    limpiarPantalla ()
    
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    bg = canvas.create_image(0, 0, anchor=NW, image=menu)
    widgets.append(canvas)
    
    global nodo_slc
    nodo = lista[int(id_nodo_slc)]
    dato = arbol.factorEquilibrio(nodo)
    texto = f'El balanceo es : {dato}'
    
    text = Label(root, width=25, height=2, text=texto, font=("Arial", 25))
    widgets.append(text)
    text.place(x=390, y=440)
    
    button = Button(root, width=25, height=2, text="Volver", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=graficarMenuSecundario, autostyle=False)
    button_window = canvas.create_window(450, 600, anchor=NW, window=button)
    widgets.append(button)

def padreNodo():
    limpiarPantalla ()
    
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    bg = canvas.create_image(0, 0, anchor=NW, image=menu)
    widgets.append(canvas)
    
    global nodo_slc
    nodo = lista[int(id_nodo_slc)]
    try:
        dato = arbol.obtenerPadreNodo(nodo).nombre
        texto = f'El Padre es : {dato}'
    except:
        texto = "El Nodo no tiene padre"
    
    text = Label(root, width=25, height=2, text=texto, font=("Arial", 25))
    widgets.append(text)
    text.place(x=390, y=440)
    
    button = Button(root, width=25, height=2, text="Volver", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=graficarMenuSecundario, autostyle=False)
    button_window = canvas.create_window(450, 600, anchor=NW, window=button)
    widgets.append(button)

def abueloNodo():
    limpiarPantalla ()
    
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    bg = canvas.create_image(0, 0, anchor=NW, image=menu)
    widgets.append(canvas)
    
    global nodo_slc
    nodo = lista[int(id_nodo_slc)]
    
    try:
        dato = arbol.obtenerAbueloNodo(nodo).nombre
        texto = f'El Abuelo es : {dato}'
    except:
        texto = "El Nodo no tiene abuelo"
    
    text = Label(root, width=25, height=2, text=texto, font=("Arial", 25))
    widgets.append(text)
    text.place(x=390, y=440)
    
    button = Button(root, width=25, height=2, text="Volver", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=graficarMenuSecundario, autostyle=False)
    button_window = canvas.create_window(450, 600, anchor=NW, window=button)
    widgets.append(button)

def tioNodo():
    limpiarPantalla ()
    
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    bg = canvas.create_image(0, 0, anchor=NW, image=menu)
    widgets.append(canvas)
    
    global nodo_slc
    nodo = lista[int(id_nodo_slc)]
    try:
        dato = arbol.obtenerTioNodo(nodo).nombre
        texto = f'El Tio es : {dato}'
    except:
        texto = "El Nodo no tiene tio"
    
    text = Label(root, width=25, height=2, text=texto, font=("Arial", 25))
    widgets.append(text)
    text.place(x=390, y=440)
    
    button = Button(root, width=25, height=2, text="Volver", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=graficarMenuSecundario, autostyle=False)
    button_window = canvas.create_window(450, 600, anchor=NW, window=button)
    widgets.append(button)

def insertarNodo():
    dir_nodo = buscarArchivo()
    arbol.insertar(dir_nodo)
    graficarArbol()

def eliminarNodo ():
    nombre = eliminar.get()
    arbol.eliminar(nombre)
    graficarArbol()

def buscarPorNombre ():
    nombre = buscar_n.get()
    
    nodo = arbol.buscarPorNombre(nombre)
    global lista
    lista = [nodo] if nodo else []
    mostrarNodos()

def buscarPorCategoria ():
    categoria = buscar_c.get()
    global lista
    lista = arbol.buscarPorCategoria(categoria)
    mostrarNodos()

def buscarPorPeso ():
    peso_min = int(buscar_pmin.get())
    peso_max = int(buscar_pmax.get())
    global lista
    lista = arbol.buscarPorPeso(peso_min, peso_max)
    mostrarNodos()

def imprimirPorNivel ():
    limpiarPantalla()
    
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    bg = canvas.create_image(0, 0, anchor=NW, image=menu)
    widgets.append(canvas)
    
    texto = arbol.escribirPorNiveles()
    text = Text(root , height = 20, width = 150)
    text.place(x=0, y=180)
    widgets.append(text)
    text.insert(END, texto)

    button = Button(root, width=25, height=2, text="Volver", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=graficarMenuPrincipal, autostyle=False)
    button_window = canvas.create_window(450, 600, anchor=NW, window=button)
    widgets.append(button)
    
def graficarArbol ():
    try:
        pdf_images = convert_from_path(f'{os.getcwd()}/ArbolAVL.pdf', poppler_path=f'{os.getcwd()}/Release-24.02.0-0/poppler-24.02.0/Library/bin')

        for idx in range(len(pdf_images)):
            pdf_images[idx].save('ArbolAVL.png', 'PNG')
    except:
        pass
        
    limpiarPantalla()
    
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    
    global arbol_img
    arbol_img = (Image.open("ArbolAVL.png"))
    resized_image= arbol_img.resize((800,600))
    arbol_img= ImageTk.PhotoImage(resized_image)
    
    bg = canvas.create_image(0, 0, anchor=NW, image=arbol_img)
    widgets.append(canvas)
    
    button = Button(root, width=25, height=2, text="Volver", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=graficarMenuPrincipal, autostyle=False)
    button_window = canvas.create_window(450, 600, anchor=NW, window=button)
    widgets.append(button)
    
def mostrarNodos ():
    limpiarPantalla()

    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    bg = canvas.create_image(0, 0, anchor=NW, image=menu)
    widgets.append(canvas)
    
    global lista
    texto = "\nID\t\t\tNombre\t\t\tCategoría\t\t\tPeso\n\n"
    for i, nodo in enumerate(lista):
        texto+= f"{i}\t\t\t{nodo}\n"
    text = Text(root , height = 20, width = 150)
    text.place(x=0, y=180)
    widgets.append(text)
    text.insert(END, texto)
    
    button = Button(root, width=25, height=2, text="Seleccionar nodo", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=graficarMenuSecundario, autostyle=False)
    button_window = canvas.create_window(450, 520, anchor=NW, window=button)
    widgets.append(button)
    
    # Entrada Nombre de Nodo
    def on_enter(e):
        nodo_slc.delete(0, 'end')
    
    def on_leave(e):
        name = nodo_slc.get()
        if name == '':
            nodo_slc.insert(0, 'ID nodo')
    
    global nodo_slc

    nodo_slc = Entry(root, width=10, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), autostyle=False)
    nodo_slc.place(x=780, y=540)
    nodo_slc.insert(0, 'ID nodo')
    frame = Frame(root, width=100, height=2, bg='black')
    frame.place(x=780, y=565)
    widgets.append(frame)
    nodo_slc.bind('<FocusIn>', on_enter)
    nodo_slc.bind('<FocusOut>', on_leave)
    widgets.append(nodo_slc)
    
    button = Button(root, width=25, height=2, text="Volver", bg='#004080',fg='white', border=0, font=('Microsoft YaHei UI Light', 15, 'bold'), command=graficarMenuPrincipal, autostyle=False)
    button_window = canvas.create_window(450, 600, anchor=NW, window=button)
    widgets.append(button)



def buscarArchivo ():
    filename = askopenfilename()
    print(filename)
    return filename


def cerrar ():
    root.destroy()

def limpiarPantalla ():
    for widget in widgets:
        widget.pack_forget()
        widget.destroy()
        
graficarPortada()

root.mainloop()
