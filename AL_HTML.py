import re

class AL_HTML:
    cadena = None
    # Lista de tokens
    tokens_html = {
        "!DOCTYPE html": "Declaracion de tipo documento",
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
    auto_closed_tags = ["br", "img", "hr", "meta", "link", "input"]

    def __init__(self, cadena):
        self.cadena = cadena

    def A_Lex(self):
        componentes_lex = self.obtener_tokens()
        return componentes_lex
           
    def tipo_etiqueta(self, t_e):
        v_etiqueta = r"</?([a-zA-Z][a-zA-Z0-9]*)\s*([^>]*)/?\s*>"
        validacion = re.match(v_etiqueta, t_e)
        if validacion:
            etiqueta_completa = validacion.group(0)
            if etiqueta_completa != t_e:
                return "No reconocido"
            tipo_etiqueta = validacion.group(1).lower()
            if tipo_etiqueta not in self.tokens_html:
                return "No reconocido"
            if t_e.endswith("/>") and tipo_etiqueta not in self.auto_closed_tags:
                return "No reconocido"
            return self.tokens_html.get(tipo_etiqueta, "No reconocido")
        else:
            return "No reconocido"
      
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
                    elif self.cadena[i: i+14].lower() == "<!doctype html":
                        estado = "tipo documento"
                        fin_tipo_documento = self.cadena.find(">")
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
                        if etiqueta == "No reconocido":
                            tokens.append(["Error", etiqueta, scan])
                        else:
                            tokens.append(["Etiqueta de Cierre", etiqueta, scan])
                    else:
                        tipo_etiqueta = scan
                        etiqueta  = self.tipo_etiqueta(tipo_etiqueta)
                        if etiqueta == "No reconocido":
                            tokens.append(["Error", etiqueta, scan])
                        else:
                            tokens.append(["Etiqueta de Apertura", etiqueta, scan])
                            if not scan.endswith("/>"):
                                atributos = self.extraer_atributos(scan)
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

