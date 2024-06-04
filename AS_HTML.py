class AS_HTML:
        tokenG = None #Arreglo para guardar el valor del token analizado
        errores = [] #Lista de errores encontrados
        
        #Obtenemos la lista de tokens 
        def __init__(self, tokens):
            self.tokens = tokens
            self.index = 0 #iniciamos el indice en 1
            self.elemetosA = [] #Lista para almacenar la construccion de mi arbol
        
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
            return True

        def tipo(self):
            token = self.obtener_token()
            self.tokenG =token
            return token and token[0] == "Tipo Documento" and token[2].strip().lower() == "<!doctype html>"


        def bloque(self):
            if self.contenedor_abierto():
                self.elemetosA.append(["CONTENEDOR_ABIERTO", "ENCABEZADO" , "CUERPO", "CONTENEDOR_CERRADO"]) #Cargamos el no terminal a la lista - Si se encuentra que el siguiente token es un contenedor de apertura
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
            self.elemetosA.append(["ENCABEZADO_A"]) #Cargamos el no terminal a la lista
            if self.encabezadoA():
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                while self.metadatos():                    
                    pass
                if self.encabezadoC():
                    self.elemetosA.append(["ENCABEZADO_C"]) #Cargamos el no terminal a la lista
                    self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                    return True
            return False

        def encabezadoA(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<head")

        def encabezadoC(self):
            token = self.obtener_token()
            self.tokenG =  token
            print("Sali: "+ token[1])
            return token and token[0] == "Etiqueta de Cierre" and token[2].strip().lower() == "</head>"

        def metadatos(self):
            self.elemetosA.append(["METADATOS"]) #Cargamos el no terminal a la lista
            if self.titulo():
                return True
            elif self.metaetiqueta():
                return True
            elif self.enlace():
                return True
            self.index -=1
            return False   
         
        #Validamos el metadato  title en mi encabezadp
        def titulo(self):
            if self.tituloA():
                self.elemetosA.append(["TITULO_A"]) #Cargamos el no terminal a la lista
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                if self.relleno():
                    self.elemetosA.append(["RELLENO"]) #Cargamos el no terminal a la lista
                    self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                    if self.tituloC():
                        self.elemetosA.append(["TITULO_C"]) #Cargamos el no terminal a la lista
                        self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                        return True
            return False

        def tituloA(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<title")

        def tituloC(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Cierre" and token[2].strip().lower() == "</title>"

        def metaetiqueta(self):
            self.index -= 1 
            token = self.obtener_token()
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<meta")

        def enlace(self):
            self.index -= 1 
            token = self.obtener_token()
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<link")

        def cuerpo(self):
            if self.cuerpoA():
                self.elemetosA.append(["CUERPO_A"]) #Cargamos el no terminal a la lista
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                if self.contenido():
                    if self.cuerpoC():                        
                        self.elemetosA.append(["CUERPO_C"]) #Cargamos el no terminal a la lista
                        self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                        return True
            return False

        def cuerpoA(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<body")

        def cuerpoC(self):
            token = self.obtener_token()
            return token and token[0] == "Etiqueta de Cierre" and token[2].strip().lower() == "</body>"

        def contenido(self):
            while self.elemento():
                self.elemetosA.append(["ELEMENTO"]) #Cargamos el no terminal a la lista
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                pass
            return True

        def elemento(self):
            if self.etiquetaU():
                return True
            elif self.etiquetaA():
                return True
            elif self.relleno2():
                return True
            elif self.etiquetaC():
                return True
            self.index -=1
            return False

        def etiquetaU(self):
            token = self.obtener_token()
            if(token[0] == "Atributo"):
                self.index +=1
                token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Apertura" and (token[2].strip().lower().startswith("<br") or token[2].strip().lower().startswith("<img") or token[2].strip().lower().startswith("<input"))

        def etiquetaA(self):
            self.index -=1
            token = self.obtener_token()
            if(token[0] == "Atributo"):
                self.index +=1
                token = self.obtener_token()
            self.tokenG = token
            print("ELemento p: "+self.tokenG[2])
            return token and token[0] == "Etiqueta de Apertura" and (token[2].strip().lower().startswith("<h1") or token[2].strip().lower().startswith("<a") or token[2].strip().lower().startswith("<h2") or token[2].strip().lower().startswith("<label") or token[2].strip().lower().startswith("<form") or token[2].strip().lower().startswith("<button") or token[2].strip().lower().startswith("<p") or token[2].strip().lower().startswith("<ol") or token[2].strip().lower().startswith("<li") or token[2].strip().lower().startswith("<div"))

        def etiquetaC(self):
            self.index -=1
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Cierre" and (token[2].strip().lower() == "</h1>" or token[2].strip().lower().startswith("</a>")  or token[2].strip().lower() == "</h2>" or token[2].strip().lower() == "</label>" or token[2].strip().lower() == "</form>" or token[2].strip().lower() == "</div>" or token[2].strip().lower() == "</button>" or token[2].strip().lower() == "</p>" or token[2].strip().lower() == "</ol>" or token[2].strip().lower() == "</li>")

        def relleno(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and (token[0] == "Texto")
        
        def relleno2(self):
            self.index -=1
            token = self.obtener_token()
            self.tokenG = token
            return token and (token[0] == "Texto")
        
        def erroresR(self):
            return self.errores
        
        
        def arbol(self):
            return self.elemetosA