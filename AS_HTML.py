class AS_HTML:
        tokenG = None #Arreglo para guardar el valor del token analizado
        detalles = [] #Lista de errores encontrados
        cU = 0  #Contador de etiquetas unicas 
        cA = 0  #Contador de etiquetas de apertura
        cC = 0  #Contador de etiquetas de cierre
        bS = 0 #Bandera para el resultado del analisis sintactico                
        
        #Obtenemos la lista de tokens 
        def __init__(self, tokens):
            self.tokens = tokens
            self.index = 0 #iniciamos el indice en 1
            self.elemetosA = [] #Lista para almacenar la construccion de mi arbol
            self.errores = [] #Lista de correcciones
            
        #Obetenemos uno a uno los valores de los tokens de acuerdo a sus posiciones
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
            self.elemetosA.append(["TIPO" , "BLOQUE"]) #Cargamos el no terminal a la lista    
            if self.tipo():
                self.elemetosA.append(["\nTIPO"]) #Cargamos el no terminal a la lista    
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el terminal a la lista
                if self.bloque():
                    self.bS = True
                    return True
            else:
                self.errores.append(["REVISAR ETIQUETA TIPO DOCUMENTO: " , self.tokenG[2]])
            return False

        def tipo(self):
            token = self.obtener_token()
            self.tokenG =token
            return token and token[0] == "Tipo Documento" and token[2].strip().lower() == "<!doctype html>"


        def bloque(self):
            if self.contenedor_abierto():
                self.cA += 1
                self.elemetosA.append(["\nBLOQUE"]) #Cargamos el no terminal a la lista    
                self.elemetosA.append(["CONTENEDOR_ABIERTO", "ENCABEZADO" , "CUERPO", "CONTENEDOR_CERRADO"]) #Cargamos el no terminal a la lista - Si se encuentra que el siguiente token es un contenedor de apertura
                self.elemetosA.append(["\nCONTENEDOR_ABIERTO"]) #Cargamos el no terminal a la lista    
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                
                self.elemetosA.append(["\nENCABEZADO"]) #Cargamos el no terminal a la lista    
                self.elemetosA.append(["ENCABEZADO_A", "METADATOS", "ENCABEZADO_C"]) #Cargamos el no terminal a la lista
                if self.encabezado():
                    if self.cuerpo():                
                        if self.contenedor_cerrado():
                            self.cC += 1
                            self.elemetosA.append(["\nCONTENEDOR_CERRADO"]) #Cargamos el no terminal a la lista
                            self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                            return True
                        else:
                           self.errores.append(["REVISAR CONTENEDOR CIERRE: " , self.tokenG[2]])
            
            else:
                self.errores.append(["REVISAR CONTENEDOR APERTURA: ", self.tokenG[2]])
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
            self.elemetosA.append(["\nENCABEZADO_A"]) #Cargamos el no terminal a la lista
            if self.encabezadoA():
                self.cA += 1
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                while self.metadatos():                    
                    pass
                if self.encabezadoC():
                    self.cC += 1
                    self.elemetosA.append(["\nENCABEZADO_C"]) #Cargamos el no terminal a la lista
                    self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                    return True
                else:
                    self.errores.append(["REVISAR ENCABEZADO CIERRE: " , self.tokenG[2]])
            else:
                self.errores.append(["REVISAR ENCABEZADO APERTURA: " , self.tokenG[2]])
            return False

        def encabezadoA(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<head")

        def encabezadoC(self):
            token = self.obtener_token()
            self.tokenG =  token
            #print("Sali: "+ token[1])
            return token and token[0] == "Etiqueta de Cierre" and token[2].strip().lower() == "</head>"

        def metadatos(self):
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
                self.cA += 1
                self.elemetosA.append(["\nMETADATOS"]) #Cargamos el no terminal a la lista
                self.elemetosA.append(["TITULO"]) #Cargamos el no terminal a la lista
                self.elemetosA.append(["\nTITULO"]) #Cargamos el no terminal a la lista
                self.elemetosA.append(["TITULO_A", "RELLENO", "TITULO_C"]) #Cargamos el no terminal a la lista

                
                self.elemetosA.append(["\nTITULO_A"]) #Cargamos el no terminal a la lista
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                if self.relleno():
                    self.elemetosA.append(["\nRELLENO"]) #Cargamos el no terminal a la lista
                    self.elemetosA.append(["TEXTO"]) #Cargamos el no terminal a la lista
                    self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                    if self.tituloC():
                        self.cC += 1
                        self.elemetosA.append(["\nTITULO_C"]) #Cargamos el no terminal a la lista
                        self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                        return True                    
            return False

        def tituloA(self):
            token = self.obtener_token()
            self.tokenG = token
            if((token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<title"))==False):
                self.errores.append(["REVISAR TITULO APERTURA: " , self.tokenG[2]])
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<title")

        def tituloC(self):
            token = self.obtener_token()
            self.tokenG = token
            if((token[0] == "Etiqueta de Cierre" and token[2].strip().lower() == "</title>")==False):
                self.errores.append(["REVISAR TITULO APERTURA: " , self.tokenG[2]])
            return token and token[0] == "Etiqueta de Cierre" and token[2].strip().lower() == "</title>"

        def metaetiqueta(self):
            self.index -= 1 
            token = self.obtener_token()
            if((token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<meta"))==False):
                self.errores.append(["REVISAR METAETIQUETA: " , self.tokenG[2]])
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<meta")

        def enlace(self):
            self.index -= 1 
            token = self.obtener_token()
            if((token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<link"))==False):
                self.errores.append(["REVISAR ENLACE: " , self.tokenG[2]])
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<link")

        def cuerpo(self):
            self.elemetosA.append(["\nCUERPO"]) #Cargamos el no terminal a la lista
            self.elemetosA.append(["CUERPO_A", "CONTENIDO", "CUERPO_C"]) #Cargamos el no terminal a la lista

            if self.cuerpoA():
                self.cA += 1
                self.elemetosA.append(["\nCUERPO_A"]) #Cargamos el no terminal a la lista
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                if self.contenido():
                    if self.cuerpoC():                        
                        self.elemetosA.append(["\nCUERPO_C"]) #Cargamos el no terminal a la lista
                        self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
                        return True
                    else:
                        self.errores.append(["REVISAR CUERPO CIERRE: " , self.tokenG[2]])
            else:
                self.errores.append(["REVISAR CUERPO APERTURA: " , self.tokenG[2]])
            return False

        def cuerpoA(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Apertura" and token[2].strip().lower().startswith("<body")

        def cuerpoC(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and token[0] == "Etiqueta de Cierre" and token[2].strip().lower() == "</body>"

        def contenido(self):
            self.elemetosA.append(["\nCONTENIDO"]) #Cargamos el no terminal a la lista
            self.elemetosA.append(["ELEMENTO*\n"]) #Cargamos el no terminal a la lista
            while self.elemento():
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
            if((token[0] == "Etiqueta de Apertura" and (token[2].strip().lower().startswith("<br") or token[2].strip().lower().startswith("<img") or token[2].strip().lower().startswith("<input")))):
                self.elemetosA.append(["\nELEMENTO"]) #Cargamos el no terminal a la lista
                self.elemetosA.append(["ETIQUETA_U"]) #Cargamos el no terminal a la lista
                self.tokenG = token
                self.cU += 1
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
            else:
                self.errores.append(["REVISAR ETIQUETA: " , self.tokenG[2]])
            return token and token[0] == "Etiqueta de Apertura" and (token[2].strip().lower().startswith("<br") or token[2].strip().lower().startswith("<img") or token[2].strip().lower().startswith("<input"))
        

        def etiquetaA(self):
            self.index -=1
            token = self.obtener_token()
            if(token[0] == "Atributo"):
                self.index +=1
                token = self.obtener_token()
            if(token[0] == "Etiqueta de Apertura" and (token[2].strip().lower().startswith("<h1") or token[2].strip().lower().startswith("<a") or token[2].strip().lower().startswith("<h2") or token[2].strip().lower().startswith("<label") or token[2].strip().lower().startswith("<form") or token[2].strip().lower().startswith("<button") or token[2].strip().lower().startswith("<p") or token[2].strip().lower().startswith("<ol") or token[2].strip().lower().startswith("<li") or token[2].strip().lower().startswith("<div"))):
                self.elemetosA.append(["\nELEMENTO"]) #Cargamos el no terminal a la lista
                self.elemetosA.append(["ETIQUETA_A"]) #Cargamos el no terminal a la lista
                self.tokenG = token
                self.cA += 1
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
            else:
                self.errores.append(["REVISAR ETIQUETA APERTURA: " , self.tokenG[2]])
            #print("ELemento p: "+self.tokenG[2])
            return token and token[0] == "Etiqueta de Apertura" and (token[2].strip().lower().startswith("<h1") or token[2].strip().lower().startswith("<a") or token[2].strip().lower().startswith("<h2") or token[2].strip().lower().startswith("<label") or token[2].strip().lower().startswith("<form") or token[2].strip().lower().startswith("<button") or token[2].strip().lower().startswith("<p") or token[2].strip().lower().startswith("<ol") or token[2].strip().lower().startswith("<li") or token[2].strip().lower().startswith("<div"))

        def etiquetaC(self):
            self.index -=1
            token = self.obtener_token()
        
            if(token[0] == "Etiqueta de Cierre" and (token[2].strip().lower() == "</h1>" or token[2].strip().lower().startswith("</a>")  or token[2].strip().lower() == "</h2>" or token[2].strip().lower() == "</label>" or token[2].strip().lower() == "</form>" or token[2].strip().lower() == "</div>" or token[2].strip().lower() == "</button>" or token[2].strip().lower() == "</p>" or token[2].strip().lower() == "</ol>" or token[2].strip().lower() == "</li>")):
                self.elemetosA.append(["\nELEMENTO"]) #Cargamos el no terminal a la lista
                self.elemetosA.append(["ETIQUETA_C"]) #Cargamos el no terminal a la lista
                self.tokenG = token
                self.cC +=1
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
            else:
                self.errores.append(["REVISAR ETIQUETA CIERRE: " , self.tokenG[2]])
            return token and token[0] == "Etiqueta de Cierre" and (token[2].strip().lower() == "</h1>" or token[2].strip().lower().startswith("</a>")  or token[2].strip().lower() == "</h2>" or token[2].strip().lower() == "</label>" or token[2].strip().lower() == "</form>" or token[2].strip().lower() == "</div>" or token[2].strip().lower() == "</button>" or token[2].strip().lower() == "</p>" or token[2].strip().lower() == "</ol>" or token[2].strip().lower() == "</li>")

        def relleno(self):
            token = self.obtener_token()
            self.tokenG = token
            return token and (token[0] == "Texto")
        
        def relleno2(self):
            self.index -=1
            token = self.obtener_token()
            if(token[0] == "Texto"):
                self.elemetosA.append(["\nELEMENTO"]) #Cargamos el no terminal a la lista
                self.elemetosA.append(["RELLENO"]) #Cargamos el no terminal a la lista
                self.elemetosA.append(["TEXTO"]) #Cargamos el no terminal a la lista
                self.tokenG = token
                self.elemetosA.append([self.tokenG[2]]) #Cargamos el no terminal a la lista
            else:
                self.errores.append(["REVISAR RELLENO: " , self.tokenG[2]])
            return token and (token[0] == "Texto")
        
        def erroresR(self):
            if(self.bS):
                self.errores.append(["ANALISIS SINTÁCTICO EXITOSO"])
            else:
                self.errores.append(["ANÁLISIS SINTÁCTICO FALLIDO"])
            
            '''self.errores.append(["ETIQUETAS UNICAS: ", self.cU])
            self.errores.append(["ETIQUETAS DE APERTURA: ", self.cA])
            self.errores.append(["ETIQUETAS DE CIERRE: ", self.cC])'''
            
            if(self.cA != self.cC):
               self.errores.append(["!VERIFICAR APERTURA Y CIERRE DE ETIQUETAS!"])
            return self.errores
        
        
        def arbol(self):
            return self.elemetosA