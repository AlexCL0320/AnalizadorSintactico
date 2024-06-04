class AS_HTML:
        tokenG = None #Arreglo para guardar el valor del token analizado
        elemetosA = [] #Lista para almacenar la construccion de mi arbol
        #Obtenemos la lista de tokens 
        def __init__(self, tokens):
            self.tokens = tokens
            self.index = 0 #iniciamos el indice en 1

        #Obetemos uno a uno los valores de los tokens de acuerdo a sus posiciones
        def obtener_token(self):
            if self.index < len(self.tokens):
                token = self.tokens[self.index]
                self.index += 1
                return token
            else:
                return None

        #Comenzamos a analizar los tokens pasados por el analizador lexico
        def programa(self):
            self.elemetosA.append(["PROGRAMA"]) #Cargamos el no terminal a la lista
            #Validamos la declaracion del inicio del programa
            if self.tipo():
                self.elemetosA.append(["TIPO" , "BLOQUE"]) #Cargamos el no terminal a la lista    
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el terminal a la lista
                if self.bloque():
                    return True
            return self.elemetosA

        def tipo(self):
            token = self.obtener_token()
            self.tokenG =token
            return token and token[0] == "Tipo Documento" and token[2].strip().lower() == "<!doctype html>"


        def bloque(self):
            self.elemetosA.append(["CONTENEDOR_ABIERTO", "ENCABEZADO" , "CUERPO", "CONTENEDOR_CERRADO"]) #Cargamos el no terminal a la lista    
            if self.contenedor_abierto():
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                if self.encabezado():
                    if self.cuerpo():
                        if self.contenedor_cerrado():
                            return True
            return False

        def contenedor_abierto(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<html")

        def contenedor_cerrado(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Cierre" and token[2].strip().lower() == "</html>"

        def encabezado(self):
            self.elemetosA.append(["ENCABEZADOA"]) #Cargamos el no terminal a la lista
            if self.encabezadoA():
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                while self.metadatos():                    
                    pass
                if self.encabezadoC():
                    self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                    return True
            return False

        def encabezadoA(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<head")

        def encabezadoC(self):
            token = self.obtener_token()
            return token and token[0] == "Etiqueta de Cierre" and token[2].strip().lower() == "</head>"

        def metadatos(self):
            self.elemetosA.append(["METADATOS"]) #Cargamos el no terminal a la lista
            if self.titulo():
                return True

        def titulo(self):
            if self.tituloA():
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                while self.relleno():
                    pass
                if self.tituloC():
                    return True
            return False

        def tituloA(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<title")

        def tituloC(self):
            token = self.obtener_token()
            return token and token[0] == "Etiqueta de Cierre" and token[2].strip().lower() == "</title>"

        def metaetiqueta(self):
            token = self.obtener_token()
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<meta")

        def enlace(self):
            token = self.obtener_token()
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<link")

        def cuerpo(self):
            if self.cuerpoA():
                if self.contenido():
                    if self.cuerpoC():
                        return True
            return False

        def cuerpoA(self):
            token = self.obtener_token()
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<body")

        def cuerpoC(self):
            token = self.obtener_token()
            return token and token[0] == "Etiqueta de Cierre" and token[2].strip().lower() == "</body>"

        def contenido(self):
            while self.elemento():
                pass
            return True

        def elemento(self):
            return self.etiquetaU() or self.etiquetaA() or self.relleno()

        def etiquetaU(self):
            token = self.obtener_token()
            return token and token[0] == "Etiqueta de Apertura" and (token[2].strip().lower().startswith("<br") or token[2].strip().lower().startswith("<img") or token[2].strip().lower().startswith("<input"))

        def etiquetaA(self):
            token = self.obtener_token()
            if token and token[0] == "Etiqueta de Apertura" and (token[2].strip().lower().startswith("<h1") or token[2].strip().lower().startswith("<h2") or token[2].strip().lower().startswith("<label") or token[2].strip().lower().startswith("<form") or token[2].strip().lower().startswith("<button") or token[2].strip().lower().startswith("<p") or token[2].strip().lower().startswith("<ol") or token[2].strip().lower().startswith("<li") or token[2].strip().lower().startswith("<div")):
                if self.contenido():
                    if self.etiquetaC():
                        return True
            return False

        def etiquetaC(self):
            token = self.obtener_token()
            return token and token[0] == "Etiqueta de Cierre" and (token[2].strip().lower() == "</h1>" or token[2].strip().lower() == "</h2>" or token[2].strip().lower() == "</label>" or token[2].strip().lower() == "</form>" or token[2].strip().lower() == "</div>" or token[2].strip().lower() == "</button>" or token[2].strip().lower() == "</p>" or token[2].strip().lower() == "</ol>" or token[2].strip().lower() == "</li>")

        def relleno(self):
            token = self.obtener_token()
            return token and (token[0] == "Texto")