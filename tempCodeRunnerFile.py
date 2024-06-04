#Importamos la libreria de expresiones regulares 
import re

class AL_HTML:
    cadena = None
    # Lista de tokens
    tokens_html = {
        "!DOCTYPE": "Declaracion de tipo documento",
        "a": "Enlace a pagina de internet",
        "p": "Parrafo",
        "h1": "Titulo 1",
        "h2": "Titulo 2",
        "h3": "Titulo 3",
        "h4": "Titulo 4",
        "h5": "Titulo 5",
        "h6": "Titulo 6",
        "strong": "Enfasis texto",
        "em": "Enfasis cursiva",
        "abbr": "Abreviatura",
        "address": "Direccion de contacto",
        "cite": "Titulos de libros o trabajos web",
        "q": "Cita online",
        "code": "Seccion de codigo",
        "del": "Texto borrado del documento",
        "div": "Seccion de contenido", 
        "br": "Salto de linea",
        "img": "Imagen",
        "ul": "lista no ordenada",
        "ol": "lista ordenada",
        "html": "Raiz del documento HTML",
        "head": "Informacion general sobre el documento",
        "title": "Titulo del documento",
        "body": "Contenido principal",
        "li": "Elemento de una lista",
        "table": "Tabla",
        "tr": "Fila de tabla",
        "td": "Columna de tabla",
        "form": "Formulario",
        "input": "Entrada por teclado",
        "textarea": "Area de texto",
        "select": "Menu desplegable-formulario",
        "option": "Opcion  de menu",
        "span": "Grupo de elementos en linea",
        "hr": "Linea horizontal",
        "b": "Texto en negritas",
        "i": "Texto en cursiva",
        "u": "Texto subrayado",
        "s": "Texto tachado",
        "em": "Enfasis de texto",
        "font": "Tamaño y estilo de fuente",
        "basefont": "Tamaño base de la fuente",
        "center": "Centrado de contenido",
        "blockquote": "Cita en bloque",
        "pre": "Texto preformateado",
        "meta": "Metadatos",
        "link": "Enlace a una hoja de estilo",
        "base": "URL base para todos los enlaces",
        "embed": "Contenido incrustado",
        "iframe": "Macro de pagina incrustado",
        "var": "Variable",
        "sub": "Subíndice",
        "sup": "Superíndice",
        "kbd": "Marca entrada por teclado",
        "big": "Texto en grande",
        "small": "Texto en pequeño",
        "frameset": "Conjunto de macros",
        "frame": "Macro",
        "dir": "Directorio",
        "applet": "Applet",
        "style": "Seccion de estilos",
        "section": "Seccion de contenido ",   
        "footer": "Pie de pagina", 
        "article": "Articulo", 
        "video": "Contenido multimedia de video",
        "label": "Etiqueta de texto",
        "button": "Boton"
    }
    
    def __init__(self, cadena):
        self.cadena = cadena

    def A_Lex(self):
        componentes_lex = self.obtener_tokens()
        return componentes_lex
           
    def tipo_etiqueta(self, t_e):
        #print("Estamos validando la etiqueta:", t_e)
        v_etiqueta = r"</?([a-zA-Z][a-zA-Z0-9]*)\s*[^>]*>"
        validacion = re.match(v_etiqueta, t_e)
        if validacion:
            tipo_etiqueta = validacion.group(1).lower()
            tipo_etiqueta = self.tokens_html.get(tipo_etiqueta, "No reconocido")
            return tipo_etiqueta
        else:
            print("Etiqueta No Valida Para HTML 3.2", "\n")
      
    def extraer_atributos(self, t_e):
        atributos = {}
        v_atributos = r'([a-zA-Z_:][a-zA-Z0-9_.:-]*)\s*=\s*"([^"]*)"'
        matches = re.findall(v_atributos, t_e)
        for match in matches:
            atributos[match[0]] = match[1]
        return atributos
    
    def obtener_tokens(self):
        tokens = []
        scan = ""
        estado = "comenzar"
        i = 0
        while i < len(self.cadena):
            caracter = self.cadena[i]
            if estado == "comenzar":
                if caracter.isspace():
                    estado = "espacio"
                elif caracter == "<":
                    if self.cadena[i:i+4] == "<!--":
                        fin_comentario = self.cadena.find("-->", i+4)
                        if fin_comentario != -1:
                            tokens.append(["Comentario", "Comentario HTML", self.cadena[i:fin_comentario+3]])
                            i = fin_comentario + 3
                            estado = "comenzar"
                            continue
                    elif self.cadena[i: i+9].lower() == "<!doctype":
                        estado = "tipo documento"
                        fin_tipo_documento = self.cadena.find(">", i+14)
                        if fin_tipo_documento != -1:
                            tokens.append(["Tipo Documento", "Declaracion del Tipo de Documento", self.cadena[i:fin_tipo_documento+1]])
                            i = fin_tipo_documento + 1
                            estado = "comenzar"
                            continue
                    scan += caracter
                    estado = "etiquetas"
                else:
                    estado = "texto plano"
                    scan += caracter
            elif estado == "espacio":
                if not caracter.isspace():
                    estado = "comenzar"
                    continue
            elif estado == "etiquetas":
                if caracter == ">":
                    scan += caracter
                    if scan.startswith("</"):
                        tipo_etiqueta = scan
                        etiqueta = self.tipo_etiqueta(tipo_etiqueta)
                        tokens.append(["Etiqueta de Cierre", etiqueta, scan])
                    else:
                        tipo_etiqueta = scan
                        etiqueta = self.tipo_etiqueta(tipo_etiqueta)
                        atributos = self.extraer_atributos(scan)
                        tokens.append(["Etiqueta de Apertura", etiqueta, scan])
                        if atributos:
                            for attr, val in atributos.items():
                                tokens.append(["Atributo", attr, val])
                    scan = ""
                    estado = "comenzar"
                else:
                    scan += caracter
            elif estado == "texto plano":
                if caracter == "<":
                    tokens.append(["Texto", "Texto plano", scan])
                    scan = ""
                    estado = "etiquetas"
                    continue
                else:
                    scan += caracter
            i += 1
        if scan:
            tokens.append(["Texto", "Texto plano", scan])
        return tokens
                
    def valida_atributos(self):
        pass
      
    def valida_aperturas_cierres(self):
        pass

