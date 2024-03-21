import imageio.v2 as iio
import os
import graphviz
os.environ["PATH"] += os.pathsep + f'{os.getcwd()}/Graphviz/bin/'


class Nodo:
    def __init__(self, dir_img):
        self.categoria, self.nombre = dir_img.split("/")[-2:]
        self.img = iio.imread(dir_img)
        self.peso = os.path.getsize(dir_img)
        self.altura = 1
        
        self.izq = None
        self.der = None
    
    def __repr__(self) -> str:
        return f'{self.nombre}\t\t\t{self.categoria}\t\t\t{self.peso}Kb'

class Arbol:
    
    def __init__ (self):
        self.raiz = None

    def obtenerValorMinimo(self, raiz):
        if raiz is None or raiz.izq is None:
            return raiz
        return self.obtenerValorMinimo(raiz.izq)
    
    def balancear (self, raiz):
        equilibrio = self.factorEquilibrio(raiz)
        print(equilibrio)

        if equilibrio > 1 and raiz.nombre < raiz.izq.nombre:
            return self.RotacionDerecha(raiz)
        
        elif equilibrio < -1 and raiz.nombre > raiz.der.nombre:
            return self.RotacionIzquierda(raiz)
        
        elif equilibrio > 1 and raiz.nombre > raiz.izq.nombre:
            raiz.izq = self.RotacionIzquierda(raiz.izq)
            return self.RotacionDerecha(raiz)
        
        elif equilibrio < -1 and raiz.nombre < raiz.der.nombre:
            raiz.der = self.RotacionDerecha(raiz.der)
            return self.RotacionIzquierda(raiz)
        
        return raiz
    
    def factorEquilibrio(self, raiz):
        return 0 if not raiz else self.altura(raiz.izq) - self.altura(raiz.der)
    
    def altura(self, raiz):
        return 0 if not raiz else raiz.altura
    
    def actualizarAltura (self, raiz):
        raiz.altura = 1 + max(self.altura(raiz.izq), self.altura(raiz.der))
     
    def insertar (self, dir):
        categoria, nombre = dir.split("/")[-2:]
        self.raiz = self.insertarRecursivo(self.raiz, nombre, dir)
        self.graficarArbol()
 
    def insertarRecursivo(self, raiz, nombre, dir):
         
        # Step 1 - Perform normal BST
        if not raiz:
            return Nodo(dir)
        elif nombre < raiz.nombre:
            raiz.izq = self.insertarRecursivo(raiz.izq, nombre, dir)
        else:
            raiz.der = self.insertarRecursivo(raiz.der, nombre, dir)
 
        # Actualizar la altura del nodo raíz
        raiz.altura = 1 + max(self.altura(raiz.izq),
                          self.altura(raiz.der))
 
        # En caso de que esté desequilibrado -> Hacer la rotación respectiva
        balance = self.factorEquilibrio(raiz)
 
        if balance > 1 and nombre < raiz.izq.nombre:
            return self.RotacionDerecha(raiz)
 
        if balance < -1 and nombre > raiz.der.nombre:
            return self.RotacionIzquierda(raiz)
 
        if balance > 1 and nombre > raiz.izq.nombre:
            raiz.izq = self.RotacionIzquierda(raiz.izq)
            return self.RotacionDerecha(raiz)
 
        if balance < -1 and nombre < raiz.der.nombre:
            raiz.der = self.RotacionDerecha(raiz.der)
            return self.RotacionIzquierda(raiz)
 
        return raiz
    
    def eliminar (self, nombre):
        self.raiz = self.eliminarRecursivo (self.raiz, nombre)
        self.graficarArbol()
    
    def eliminarRecursivo (self, raiz, nombre):
        # Si el árbol está vacío -> Detener proceso
        if not raiz:
            return raiz
        elif nombre < raiz.nombre:
            raiz.izq = self.eliminarRecursivo(raiz.izq, nombre)
        elif nombre > raiz.nombre:
            raiz.der = self.eliminarRecursivo(raiz.der, nombre)
 
        else:
            # Si el nombre del nodo a eliminar coincide -> Aplicar proceso eliminado
            if raiz.izq is None:
                temp = raiz.der
                raiz = None
                return temp
 
            elif raiz.der is None:
                temp = raiz.izq
                raiz = None
                return temp
 
            temp = self.obtenerValorMinimo(raiz.der)
            raiz.nombre = temp.nombre
            raiz.der = self.eliminarRecursivo(raiz.der, temp.nombre)
            
        if raiz is None:
            return raiz
 
        # Actualizar la altura del nodo raíz
        self.actualizarAltura(raiz)
 
        # En caso de que esté desequilibrado -> Hacer la rotación respectiva
        return self.balancear(raiz)
    
    def obtenerTioNodo (self, nodo):
        padre = self.obtenerPadreNodo(nodo)
        
        if not padre:
            return None
        
        if padre.izq == nodo:
            return padre.der
        
        if padre.der == nodo:
            return padre.izq
        
        return None
    
    def obtenerAbueloNodo (self, nodo):        
        padre = self.obtenerPadreNodo(nodo)
        return self.obtenerPadreNodo(padre)
    
    def obtenerPadreNodo (self, nodo):
        return self.obtenerPadreNodoRecursivo(self.raiz, nodo)
    
    def obtenerPadreNodoRecursivo (self, raiz, nodo):
        # Si el árbol está vacío -> Detener proceso
        if not raiz:
            return None
        
        res=None
        if raiz.izq == nodo or raiz.der == nodo:
            return raiz
        
        if raiz.izq:
            res = self.obtenerPadreNodoRecursivo(raiz.izq, nodo)
        
        if raiz.der and res == None:
            res = self.obtenerPadreNodoRecursivo(raiz.der, nodo)
        
        return res
    
    def buscarPorNombre (self, nombre):
        return self.buscarPorNombreRecursivo(self.raiz, nombre)
        
    def buscarPorNombreRecursivo (self, raiz, nombre):
        # Si el árbol está vacío -> Detener proceso
        if not raiz:
            return None
        
        if raiz.nombre == nombre:
            return raiz
        
        res = None
        if raiz.izq:
            res = self.buscarPorNombreRecursivo(raiz.izq, nombre)
        
        if raiz.der and res == None:
            res = self.buscarPorNombreRecursivo(raiz.der, nombre)
        
        return res
    
    def obtenerNodos (self):
        return self.obtenerNodosRecursivo(self.raiz)
    
    def obtenerNodosRecursivo (self, raiz, lista):
        # Si el árbol está vacío -> Detener proceso
        if not raiz:
            return lista
        
        lista.append(raiz)
        
        if raiz.izq:
            lista = self.buscarPorCategoriaRecursivo(raiz.izq, lista)
        
        if raiz.der:
            lista = self.buscarPorCategoriaRecursivo(raiz.der, lista)
        
        return lista
    
    def buscarPorCategoria (self, categoria):
        return self.buscarPorCategoriaRecursivo(self.raiz, categoria, [])
        
    def buscarPorCategoriaRecursivo (self, raiz, categoria, lista):
        # Si el árbol está vacío -> Detener proceso
        if not raiz:
            return None
        
        if raiz.categoria == categoria:
            lista.append(raiz)
        
        if raiz.izq:
            lista = self.buscarPorCategoriaRecursivo(raiz.izq, categoria, lista)
        
        if raiz.der:
            lista = self.buscarPorCategoriaRecursivo(raiz.der, categoria, lista)
        
        return lista
    
    def buscarPorPeso (self, peso_min, peso_max):
        return self.buscarPorCategoriaRecursivo(self.raiz, peso_min, peso_max, [])
        
    def buscarPorPesoRecursivo (self, raiz, peso_min, peso_max, lista):
        # Si el árbol está vacío -> Detener proceso
        if not raiz:
            return None
        
        if raiz.peso <= peso_max and raiz.peso >= peso_min:
            lista.append(raiz)
        
        if raiz.izq:
            lista = self.buscarPorPesoRecursivo(raiz.izq, peso_min, peso_max, lista)
        
        if raiz.der:
            lista = self.buscarPorPesoRecursivo(raiz.der, peso_min, peso_max, lista)
        
        return lista
    
    def RotacionIzquierda(self, z):
        y = z.der
        T2 = y.izq
 
        y.izq = z
        z.der = T2
 
        self.actualizarAltura(z)
        self.actualizarAltura(y)
 
        return y
 
    def RotacionDerecha(self, z):
        y = z.izq
        T3 = y.der
        
        y.der = z
        z.izq = T3
 
        self.actualizarAltura(z)
        self.actualizarAltura(y)
 
        return y
    
    def graficarArbol (self):
        arbol = graphviz.Digraph()
        arbol = self.graficarArbolConGraphviz(self.raiz, arbol)
        arbol.render('ArbolAVL', view=False)
    
    def graficarArbolConGraphviz (self, raiz, arbol):
        arbol.node(f'{raiz.nombre}', f'{raiz.nombre}\n{raiz.categoria}')
        
        if raiz.izq:
            arbol = self.graficarArbolConGraphviz(raiz.izq, arbol)
            arbol.edge(f'{raiz.nombre}', f'{raiz.izq.nombre}', '')
            
        if raiz.der:
            arbol = self.graficarArbolConGraphviz(raiz.der, arbol)
            arbol.edge(f'{raiz.nombre}', f'{raiz.der.nombre}', '')
            
        return arbol
    
    def escribirPorNiveles (self):
        texto = ""
        for i in range(1, self.altura(self.raiz) + 1)[::-1]:
            texto += f"Nivel {self.altura(self.raiz)-i} :\n"
            texto += "Nombre\t\t\tCategoría\t\t\tPeso\n\n"
            texto = self.escribirNivel(self.raiz, i, texto)
            texto += "\n\n"
        return texto
    
    def escribirNivel (self, raiz, nivel, texto):
        if not raiz:
            return texto
 
        if self.altura(raiz) == nivel:
            texto += f' - {raiz}\n'
        
        texto = self.escribirNivel(raiz.izq, nivel, texto)
        texto = self.escribirNivel(raiz.der, nivel, texto)
        
        return texto
        
def validarEntrada (opciones_validas = None):
    while (True):
        try:
            num = int(input())
            
            if not opciones_validas:
                return num
            else:
                if num in opciones_validas:
                    return num
        except:
            print("...Ingrese un valor válido para continuar")

'''
arbol = Arbol()

while(True):
    print("........................................................................")
    print('1. Insertar un nodo')
    print('2. Eliminar un nodo utilizando la métrica dada')
    print('3. Buscar un nodo utilizando la métrica dada')
    print('4. Buscar todos los nodos que cumplan los siguientes criterios')
    print('5. Mostrar el recorrido por niveles del árbol (de manera recursiva)')
    print('6. Salir')
    print("........................................................................")
    print("Ingrese la opción deseada:\t")
    
    op = validarEntrada([1, 2, 3, 4, 5, 6])   
    lista = []
    
    if (op == 1):
        print("Ingrese la dirección de la imagen:")
        dir_img = input()
        arbol.insertar(dir_img)
    elif (op == 2):
        print("Ingrese el nombre del nodo a eliminar: ")
        nombre = input()
        arbol.eliminar(nombre)
    elif (op == 3):
        print("Ingrese el nombre del nodo buscado: ")
        nombre = input()
        nodo = arbol.buscarPorNombre(nombre)
        lista = [nodo] if nodo else []
    elif (op == 4):
        print("........................................................................")
        print("1. Buscar por Categoría")
        print("2. Buscar por Tamaño del Archivo")
        print("........................................................................")
        print("Ingrese la opción deseada:\t")
        op2 = validarEntrada([1, 2])   
        
        if (op2 == 1):
            print("Ingrese el nombre de la categoría a buscar:")
            categoria = input()
            lista = arbol.buscarPorCategoria(categoria)
        elif (op2 == 2):
            print("Ingrese el intervalo del tamaño:")
            print("Mínimo: ", end="")
            peso_min = validarEntrada()
            print("Máximo: ", end="")
            peso_max = validarEntrada()
            lista =  arbol.buscarPorPeso(peso_min, peso_max)
    elif (op == 5):
        arbol.escribirPorNiveles()
    elif (op == 6):
        break
    
    if (op == 3 or op == 4):
        
        if (len(lista) > 0):
            
            n = 0
            if (len(lista) > 1):
                print("Seleccione uno de los Nodos para ejecutar operación")
                input("Presione Enter para mostrar...")
                print("........................................................................")
                print("Resultado de la Búsqueda")
                print("........................................................................")
                print("ID\t\t\tNombre\t\t\tCategoría\t\t\tPeso\n")
                for i, nodo in enumerate(lista):
                    print(f'{i}\t\t\t{nodo}')
                print("........................................................................")
                
                print("Seleccione la ID del Nodo al que quiere revisar")
                n = validarEntrada()
            
            nodo = lista[n]
            
            op2 = 0
            while (op2 != 6):
                print("........................................................................")
                print("Para el Nodo : ")
                print(nodo)
                print("........................................................................")
                print("1. Obtener nivel del nodo")
                print("2. Obtener el factor de balanceo")
                print("3. Encontrar el padre del nodo")
                print("4. encontrar el abuelo del nodo")
                print("5. Encontrar el tío del nodo")
                print("6. Volver al menú principal")
                print("........................................................................")
                print("Ingrese la opción deseada:\t")
                op2 = validarEntrada([1, 2, 3, 4, 5, 6])
                
                if (op2 == 1):
                    print("El Nivel del nodo es:")
                    print(arbol.altura(nodo))
                elif (op2 == 2):
                    print("El factor de balanceo del nodo es:")
                    print(arbol.factorEquilibrio(nodo))
                elif (op2 == 3):
                    print("El padre del nodo es:")
                    print(arbol.obtenerPadreNodo(nodo))
                elif (op2 == 4):
                    print("El abuelo del nodo es:")
                    print(arbol.obtenerAbueloNodo(nodo))
                elif (op2 == 5):
                    print("El tío del nodo es:")
                    print(arbol.obtenerTioNodo(nodo))
        else:
            print("No se encontró ningún Nodo")
    '''

    
    