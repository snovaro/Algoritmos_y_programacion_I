import random
import os

def Validar_numero(numero:str)->int:
    """
    PRE: Recibe un valor ingresado por el usuario que se quiere que sea un número entero.
    POS: Devuelve un numero entero.
    """
    while not(numero.isnumeric()) or int(numero)<0:
        print("El valor ingresado no es válido.")
        numero = input("Ingrese un numero positivo por favor: ")
    numero = int(numero)
    return numero

def Busca_palabras(palabras_y_definiciones:dict, lista_palabras:list)->list:
    """
    PRE: Recibe un diccionario de palabras y una lista de palabras.
    POS: Devuelve la lista de palabras recibida ahora con doce palabras sacando del diccionario aleatoreamente las necesarias para llegar a doce.
    """
    keys = list(palabras_y_definiciones.keys())
    while len(lista_palabras)<12:
        numero = random.randint(0, len(keys)-1)
        palabra = keys[numero]  
        if palabra not in lista_palabras:
            lista_palabras.append(palabra)
    return lista_palabras

def Creador_tablero_vacio()->None:
    """
    PRE: Se lo llama al querer una matriz 20x20 vacía.
    POS: Devuelve una lista de veinte listas que cada una tiene veinte caracteres ASCII 219.
    """
    matriz = []
    for i in range(20):
        lista = []
        for j in range(20):
                lista.append("■")
        matriz.append(lista)
    return(matriz)

def ImpresionMatriz(matriz)->None:
    """
    PRE: Recibe una lista de listas .
    POS: Imprime la lista de listas.
    """
    for i in range(len(matriz)):
        print("\t\t\t\t\t", end = " ")
        for j in range (len(matriz[i])):
            print(matriz[i][j], end = " ")
        print("")
    print("\n")

def Impresion_adivinadas(palabras_adivinadas)->None:
    """
    PRE: Recibe una lista
    POS: Imprime cada valor de la lista separado por comas.
    """
    lista_adivinadas = []
    for palabra in palabras_adivinadas:
        lista_adivinadas.append(palabra)
        lista_adivinadas.append(", ")
    lista_adivinadas.pop()
    lista_adivinadas.append(".")
    for caracter in lista_adivinadas:
        print(caracter, end = "")
    print("\n\n")

def Completa_verticales(tablero_completo:list, palabras_verticales:list, diccionario_posiciones:dict, diccionario_posiciones_verticales:dict)->None:
    """
    PRE: Recibe el tablero, las palabras que se deben poner en vertical, y dos diccionarios a llenar con la informacion de lo que haga.
    POS: Devuelve el tablero con las palabras agregadas verticalmente y los diccionarios con los datos de donde se han colocado las letras iniciales de cada palabra.
    """
    for palabra in palabras_verticales:
        espacios_vacios = 0
        while espacios_vacios != len(palabra):
            numero_i = random.randint(1,18-len(palabra))
            numero_j = random.randint(1,18)
            if tablero_completo[numero_i-1][numero_j] == "■" and tablero_completo[numero_i + 1 + len(palabra)][numero_j] == "■":
                for j in range(len(palabra)):
                    if tablero_completo[numero_i][numero_j] == "■" and tablero_completo[numero_i][numero_j+1] == "■" and tablero_completo[numero_i][numero_j-1] == "■": 
                        espacios_vacios += 1
                        numero_i += 1
            if espacios_vacios == len(palabra):
                for k in range(len(palabra)):
                    tablero_completo[numero_i - len(palabra)  + k][numero_j] = palabra[k]
            else: espacios_vacios = 0
        diccionario_posiciones[palabra] = [numero_i-len(palabra), numero_j]
        diccionario_posiciones_verticales[palabra] = [numero_i-len(palabra), numero_j]
    
def Completa_horizontales(tablero_completo:list, palabras_horizontales:list, diccionario_posiciones:dict, diccionario_posiciones_horizontales:dict)->None:
    """
    PRE: Recibe el tablero, las palabras que se deben poner en horizontal, y dos diccionarios a llenar con la informacion de lo que haga.
    POS: Devuelve el tablero con las palabras agregadas horizontalmente y los diccionarios con los datos de donde se han colocado las letras iniciales de cada palabra.
    """
    numero_palabra = 0
    for palabra in palabras_horizontales:
        espacios_vacios = 0
        numero_palabra += 1
        while espacios_vacios != len(palabra):
            numero_i = random.randint(0,19)
            numero_j = random.randint(1,19 -len(palabra))
            if tablero_completo[numero_i][numero_j-1] == "■" and tablero_completo[numero_i][numero_j + len(palabra)] == "■":  
                for j in range(len(palabra)):
                    if tablero_completo[numero_i][numero_j] == "■": 
                        espacios_vacios += 1
                        numero_j += 1
            if espacios_vacios == len(palabra):
                for k in range(len(palabra)):
                    tablero_completo[numero_i][numero_j- len(palabra) + k] = palabra[k]
            else:  
                espacios_vacios = 0
        diccionario_posiciones[palabra] = [numero_i, numero_j-len(palabra)]
        diccionario_posiciones_horizontales[palabra] = [numero_i, numero_j-len(palabra)]

def Completa_tableros(palabras_crucigrama:list)->list:
    """
    PRE: Recibe doce palabras que se quieren poner en un tablero de veinte por veinte
    POS: Devuelve un tablero con 6 palabras verticales y 6 horizontales, y 3 diccionarios con las posiciones de las letras iniciales de cada palabra en el tablero.
    (un diccionario tiene de todas las palabras, otro tiene solo de las horizontales, y el ultimo solo de las verticales)
    """
    tablero_completo = Creador_tablero_vacio()
    diccionario_posiciones:dict = {}
    diccionario_posiciones_verticales:dict = {}
    diccionario_posiciones_horizontales:dict = {}
    palabras_verticales = []
    palabras_horizontales = []
    for i in range(len(palabras_crucigrama)):
        if i < 6:
            palabras_verticales.append(palabras_crucigrama[i])
        else:
            palabras_horizontales.append(palabras_crucigrama[i])
    Completa_verticales(tablero_completo, palabras_verticales, diccionario_posiciones, diccionario_posiciones_verticales)
    Completa_horizontales(tablero_completo, palabras_horizontales, diccionario_posiciones, diccionario_posiciones_horizontales)
    return tablero_completo, diccionario_posiciones, diccionario_posiciones_horizontales, diccionario_posiciones_verticales

def Tablero_Usuario(tablero_incompleto:list, palabras_crucigrama:list, diccionario_posiciones:dict)->list:
    """
    PRE: Recibe el tablero con todas las palabras colocadas.
    POS: Devuelve un tablero donde los espacios donde iban las palabras estan vacios y cada lugar tiene una letra para representarse.
    """
    coordenadas_iniciales = list([*diccionario_posiciones.values()])
    diccionario_posicion_palabra = {}
    letra = 0
    lista_letras = "ABCDEFGHIJKL"
    for i in range(len(palabras_crucigrama)):
        diccionario_posicion_palabra[palabras_crucigrama[i]] = coordenadas_iniciales[i]
    for i in range(len(tablero_incompleto)):
        for j in range(len(tablero_incompleto[i])):
            if str(tablero_incompleto[i][j]).isalpha():
                tablero_incompleto[i][j] = " "
            coordenada = [i,j]
            if coordenada in coordenadas_iniciales:
                tablero_incompleto[i][j] = lista_letras[letra]
                letra += 1
    return tablero_incompleto, diccionario_posicion_palabra

def Creo_diccionario_letra_numerodef(tablero_incompleto:list, diccionario_posicion_palabra:dict)->dict:
    """
    PRE: Recibe el tablero con los espacios de las palabras vacios representados con una letra.
    POS: Devuelve un diccionario que asocia las doce palabras a las letras de la A a la L.
    """
    diccionario_verificador = {}
    for i in range(len(tablero_incompleto)):
        for j in range(len(tablero_incompleto[i])):
            if str(tablero_incompleto[i][j]) in "ABCDEFGHIJKL":
                for elemento in [*diccionario_posicion_palabra.keys()]:
                    if [i,j] == diccionario_posicion_palabra[elemento]:
                        diccionario_verificador[elemento] = str(tablero_incompleto[i][j])
    return diccionario_verificador

def Crea_dic_palabra_letra_numero(diccionario_palabra_letra_numero:dict, lista_palabras:list)->dict:
    """
    PRE: Recibe el diccionario de las palabras asociadas a las letras en el tablero, junto con la lista de las palabras y sus definiciones.
    POS: Devuelve dos diccionarios, uno con la palabra como key siendo sus valores la letra y el numero de su definicion. Y el otro es un diccionario en el cual se guardan las 
    definiciones con sus respectivos numeros de forma que se los pueda llamar para imprimirlos con un iterador ya que sus keys son los numeros de definicion.
    """
    definiciones = []
    numero_definiciones = []
    for palabra in [*diccionario_palabra_letra_numero.keys()]:
        definiciones.append(lista_palabras[palabra])
        numero = random.randint(1,12)
        while numero in numero_definiciones:
            numero = random.randint(1,12)
        numero_definiciones.append(numero)
        diccionario_palabra_letra_numero[palabra] += str(numero)
    definiciones_con_numero = {}
    for numeros in range(len(numero_definiciones)):
        definiciones_con_numero[numero_definiciones[numeros]] = f"{numero_definiciones[numeros]}) {definiciones[numeros]}"
    return definiciones_con_numero

def Valida_ingreso(ingreso:str, letra_definiciones_adivinadas:list)->bool:
    """
    PRE: Recibe el ingreso del usuario y una lista de las definiciones adivinadas.
    POS: Devuelve si el ingreso del usuario es válido por medio de un booleano. 
    """
    if ingreso.count(" ") != 1 or ((ingreso[0])+(ingreso[1])+(ingreso[2])).capitalize() in letra_definiciones_adivinadas or not((ingreso[1]).isnumeric()) or not(ingreso[0].isalpha()) or not((ingreso[2].isspace()) or (ingreso[2].isnumeric())):
        return True
    else: return False

def Ingreso_usuario(diccionario_palabra_letra_numero:dict, palabras_adivinadas:list)->bool:
    """
    PRE: Recibe un diccionario que asocia las palabras a la letra en el tablero impreso y a su número de definición, junto con una lista de las palabras adivinadas por el usuario.
    POS: Devuelve un booleano segun si un ingreso del usuario es correcto.
    """
    print("La letra de la palabra a adivinar, seguido por el número de la definición que es y luego, espaciada, la palabra (ej: ´B11 Palabra´) \nAclaración: se valora la ortografía por lo que se deben colocar las tíldes")
    ingreso = input("Ingrese la posición, el número de definición, y la palabra de la forma antes mencionada: ")
    print("")
    letra_definiciones_adivinadas = []

    for palabra_adivinada in palabras_adivinadas:
        letra_definiciones_adivinadas.append(diccionario_palabra_letra_numero[palabra_adivinada])

    for i in range(len(letra_definiciones_adivinadas)):
        if len(letra_definiciones_adivinadas[i]) == 2:
            letra_definiciones_adivinadas[i] += " "

    while Valida_ingreso(ingreso, letra_definiciones_adivinadas):
        print("Ingreso inválido. Recuerde que el ingreso debe ser un conjunto letra-número que no se haya divinado y debe haber un único espacio.")
        if len(letra_definiciones_adivinadas)>0:
            print("Los ya adivinados son: ")
            Impresion_adivinadas(letra_definiciones_adivinadas)
            print("Para las palabras: ")
            Impresion_adivinadas(palabras_adivinadas)
        ingreso = input("Intente de nuevo: ")
    coordenada, palabra_ingresada = ingreso.split(" ")
    palabra_ingresada = palabra_ingresada.capitalize()
    coordenada = coordenada.capitalize()
    for palabra_key in diccionario_palabra_letra_numero:
        if coordenada == diccionario_palabra_letra_numero[palabra_key] and palabra_ingresada == palabra_key:
            if palabra_ingresada not in palabras_adivinadas:
                print(f"Correctoo !!!:) Has adivinado la palabra {palabra_ingresada} del conjunto letra-numero definición {coordenada}\n")
                palabras_adivinadas.append(palabra_ingresada)
            else:
                print(f"La palabra {palabra_ingresada} es correcta para la posición y letra {coordenada}, pero ya habia sido adivinada. No va a ser enviado al dado ya que no se ha equivocado.")
            return True
    return False

def Impresion_definiciones(definiciones_con_numero:dict)->None:
    """
    PRE: Recibe un diccionario con definiciones donde sus keys son números del 1 al 12.
    POS: Imprime las definiciones en orden.
    """
    print("Definiciones:")
    for i in range(1,13):
        print(definiciones_con_numero[i])
    print("\n")
        
def Completador_palabra_adivinada(tablero_incompleto:list, posiciones_verticales:dict, posiciones_horizontales:dict, palabras_adivinadas:list)->list:
    """
    PRE: Recibe el tablero, las palabras adivinadas, y dos diccionarios que contienen que palabras son verticales y cuales horizontales junto con sus coordenadas iniciales.
    POS: Devuelven el tablero con las palabras adivinadas impresas.
    """
    for palabra in palabras_adivinadas:
        if palabra in posiciones_horizontales.keys():
            coordenada = posiciones_horizontales[palabra]
            for i in range(len(palabra)):
                tablero_incompleto[coordenada[0] + i][coordenada[1]] = palabra[i]
        elif palabra in posiciones_verticales.keys():
            coordenada = posiciones_verticales[palabra]
            for i in range(len(palabra)):
                tablero_incompleto[coordenada[0]][coordenada[1] + i] = palabra[i]
    return tablero_incompleto

def Completa_vocales(tablero_incompleto:list, posiciones_verticales:dict, posiciones_horizontales:dict)->None:
    """
    PRE: Recibe el tablero, y dos diccionarios que contienen que palabras son verticales y cuales horizontales junto con sus coordenadas iniciales.
    POS: Se imprime un tableto con todas las vocales.
    """
    vocales = "AÁaáEÉeéIÍiíOÓoóUÚuú"
    for i in range(len(tablero_incompleto)):
        for j in range(len(tablero_incompleto[i])):
            if str(tablero_incompleto[i][j]).isalpha():
                tablero_incompleto[i][j] = " "
    for palabra in posiciones_horizontales.keys():
        coordenada = posiciones_horizontales[palabra]
        for i in range(len(palabra)):
            if palabra[i] in vocales:
                tablero_incompleto[coordenada[0] + i][coordenada[1]] = palabra[i]
    for palabra in posiciones_verticales.keys():
        coordenada = posiciones_verticales[palabra]
        for i in range(len(palabra)):
            if palabra[i] in vocales:
                tablero_incompleto[coordenada[0]][coordenada[1] + i] = palabra[i]

def Elije_palabra_comodin(tablero_incompleto:list, diccionario_palabra_letra_numero:dict, posiciones_palabras_verticales:dict, posiciones_palabras_horizontales:dict, palabras_adivinadas:list)->list:
    """
    PRE: Recibe un ingreso numerico del usuario referido a una de las definiciones dadas.
    POS: Agrega a las palabras adivinadas la palabra que pertenece al numero de definicion ingresado por el usuario.
    """
    definiciones_adivinadas = []
    for palabra in palabras_adivinadas:
        if len(diccionario_palabra_letra_numero[palabra]) == 3:
            definiciones_adivinadas.append(str(diccionario_palabra_letra_numero[palabra][1])+str(diccionario_palabra_letra_numero[palabra][2]))
        elif len(diccionario_palabra_letra_numero[palabra]) == 2:
            definiciones_adivinadas.append(str(diccionario_palabra_letra_numero[palabra][1]))

    definicion = Validar_numero(input("Ingrese el número de la definición de la palabra que quiere descubrir: "))

    while str(definicion) in definiciones_adivinadas or definicion > 12:
        if definicion > 12: definicion = Validar_numero(input("El ingreso no fue valido ya que solo hay 12 definiciones. Por favor ingrese un número valido: "))
        else: definicion = Validar_numero(input("Esa definición pertenece a una palabra ya adivinada. Ingrese una nueva: "))
    
    for palabra in [*diccionario_palabra_letra_numero.keys()]:
        if definicion > 9 and len(diccionario_palabra_letra_numero[palabra])> 2:
            if int(diccionario_palabra_letra_numero[palabra][2]) + 10 == definicion:
                    print(f"La palabra para la definición {definicion} es {palabra}. Se agregará automaticamente al tablero ♥.")
                    palabras_adivinadas.append(palabra)
        else:
            if int(diccionario_palabra_letra_numero[palabra][1]) == definicion:
               palabras_adivinadas.append(palabra) 
    Completador_palabra_adivinada(tablero_incompleto, posiciones_palabras_verticales, posiciones_palabras_horizontales, palabras_adivinadas)
    return(palabras_adivinadas, tablero_incompleto)

def Dado(num_dado:int, lista_palabras:list, palabras_adivinadas:list, tablero_incompleto:list,  diccionario_palabra_letra_numero:dict, posiciones_palabras_verticales:dict, posiciones_palabras_horizontales:dict, posiciones_palabras:dict)->list:
    """
    PRE: Recibe un numero de dado junto con todos las listas y diccionarios necesarias para las funciones: Completador_palabra_adivinada, Completa_vocales, y Tablero_usuario.
    POS: Segun el numero de dado recibido, se devuelven la lista de palabras del crucigrama y la lista de palabras adivinadas, las cuales pudieron haber sido cambiadas.
    """
    if num_dado < 3:
        if len(palabras_adivinadas) > 0:
            palabra_eliminada = palabras_adivinadas.pop()
            print(f"Lamentablemente como salio el {num_dado} en el dado, será eliminada la última palabra adivinada ({palabra_eliminada}) y se mezclará el tablero con una palabra nueva agregada. Suerte! :)\n")
            for palabra in lista_palabras:
                if palabra == palabra_eliminada:
                    lista_palabras.remove(palabra)
        else:
            print("Como aún no se ha adivinado ninguna palabra continua el juego tal como estaba.. Te salvaste")
    elif num_dado < 5:
        os.system('cls')
        print(f"Que buena suerte!! Como salio el {num_dado} en el dado, serán reveladas las vocales de todas las palabras que aún no has adivinado. Espero te sirvan! :)\n")
        #Tablero_Usuario(tablero_incompleto, lista_palabras, posiciones_palabras)
        Completa_vocales(tablero_incompleto, posiciones_palabras_verticales, posiciones_palabras_horizontales)
        Completador_palabra_adivinada(tablero_incompleto, posiciones_palabras_verticales, posiciones_palabras_horizontales, palabras_adivinadas)
        ImpresionMatriz(tablero_incompleto)
        print("ATENCIÓN!! ESTE TABLERO SE MOSTRARÁ UNA ÚNICA VEZ Y LUEGO SE VOLVERÁ A IMPRIMIR EL TABLERO CON LAS PALABRAS NO ADIVINADAS VACÍAS TOTALMENTE\n\n")
        Tablero_Usuario(tablero_incompleto, lista_palabras, posiciones_palabras)
        Completador_palabra_adivinada(tablero_incompleto, posiciones_palabras_verticales, posiciones_palabras_horizontales, palabras_adivinadas)
        tablero_incompleto, diccionario_posicion_palabra = Tablero_Usuario(tablero_incompleto, lista_palabras, posiciones_palabras)
    elif num_dado == 5:
        print(f"Felicitaciones! Como salio el {num_dado} en el dado tienes la posibilidad de descubrir una palabra que te falte. Escoge bien cual quieres revelar (: \n")
        palabras_adivinadas, tablero_incompleto = Elije_palabra_comodin(tablero_incompleto, diccionario_palabra_letra_numero, posiciones_palabras_verticales, posiciones_palabras_horizontales, palabras_adivinadas)
    return lista_palabras, palabras_adivinadas

def Inicio()->None:
    print("Bienvenida/o al juego del crucigrama loco ☻☺☻ \n")
    print("En este juego serás presentado/a un tablero de 20x20 con espacios vacíos (donde deben ir las palabras) referenciados por letras de la A a la L (las cuales no implican ser la primera letra de las palabras)")
    print("Debajo del tablero se imprimirá una lista de definiciones de las palabras que debes adivinar. \nCualquier número de definición puede estar asociado a cualquier letra de referencia del tablero.")
    print("\nNota: A la hora de adivinar las palabras, presta atención a como debes escribir tus respuestas.\n")
    print("\nEn caso de equivocarte se tirará un dado de 6 números, y según lo que salga pueden pasar cosas buenas o malas.. Yo que vos rezaría porque no salga el 6..\n\n")
    print("Te deseo mucha suerte♣!! La vas a necesitar.\n\n")
    input("Enter para comenzar el juego")
    os.system('cls')

def main()->None:
    os.system('cls')
    numero_dado = 0
    palabras_y_definiciones = { #{palabra:definicion}
    "Python": "Un lenguaje de programación interpretado, dinámico y de alto nivel.",
    "Lista": "Una colección ordenada y mutable de elementos.",
    "Tupla": "Una colección ordenada e inmutable de elementos.",
    "Condición": "Una expresión que se evalúa como verdadera o falsa.",
    "Ciclo": "Una estructura de control que repite un bloque de código varias veces.",
    "Función": "Un bloque de código que realiza una tarea específica y puede ser llamado desde cualquier parte del programa.",
    "Clase": "Un modelo para crear objetos que contiene atributos y métodos.",
    "Booleano": "Un tipo de dato que representa verdadero o falso.",
    "Entero": "Un tipo de dato que representa números enteros.",
    "Flotante": "Un tipo de dato que representa números con decimales.",
    "Cadena": "Un tipo de dato que representa una secuencia de caracteres.",
    "Error": "Un problema o fallo que se produce durante la ejecución del programa.",
    "Clonar": "La creación de una copia de un objeto o estructura de datos existente.",
    "Paradoja": "Una declaración o situación que parece contradecir la lógica y el sentido común.",
    "Innovar": "La introducción de algo nuevo o diferente que crea un cambio significativo.",
    "Empatía": "La capacidad de ponerse en el lugar de otra persona y entender sus sentimientos.",
    "Respeto": "Mostrar consideración y aprecio por los demás y sus diferencias.",
    "Animal": "Ser vivo que se mueve por sí mismo, y que tiene sensibilidad y capacidad para responder a estímulos.",
    "Barato": "Que tiene un precio reducido en comparación con otros productos de características similares.",
    "Césped": "Conjunto de plantas herbáceas que crecen juntas y forman una cubierta vegetal uniforme.",
    "Dulces": "Producto de confitería elaborado a partir de azúcar y otros ingredientes, que tiene un sabor dulce.",
    "Guitarra": "Instrumento musical de cuerda, que se toca con los dedos o con una púa.",
    "Héroe": "Persona que realiza una acción extraordinaria que requiere valentía, arrojo o habilidad destacada.",
    "Jardín": "Espacio exterior de una casa o edificio, generalmente con vegetación, destinado a la recreación y el disfrute.",
    "Kilómetro": "Medida de longitud que equivale a mil metros.",
    "Profesor": "Persona que enseña una materia o disciplina a otros.",
    "Noticia": "Información que se comunica sobre un acontecimiento o suceso de interés general.",
    "Independiente" : "Equipo argentino máximo campeón de Libertadores.",
    "Boca": "Equipo argentino reconocido por sus colores azul y oro.",
    "River": "Equipo reconocido por una banda roja cruzada en su vestimenta.",
    "Argentina": "Selección actual campeona del mundo.",
    "Messi": "Mejor jugador de la historia. Apodado la pulga.",
    "Agüero":" Exjugador que actualmente se dedica al streaming.",
    "Zeus": "Dios de dioses griego.",
    "Brasil" : "Única selección pentacampeona del mundo.",
    "Facultad": "Sinónimo de universidad.",
    "Williams": "Apellido de famosas hermanas tenistas.",
    "Cenicienta": "Princesa con zapatos de cristal.",
    "Garfield": "Gato naranja que come lasagna.",
    "Mafalda": "Personaje creado por Quino que odia la sopa.",
    "Flash": "Personaje ficticio conocido como la persona mas rápida del planeta.",
    "Scaloni": "Actual DT de la selección Argentina.",
    "Fémur": "Hueso más grande del cuerpo humano.",
    "Berlín": "Capital de Alemania.",
    "Maradona": "Jugador que hizo la mano de Dios.",
    "Madrd": "Capital de España.",
    "Truco": "Juego de cartas ligado principalmente a Argentina y Uruguay.",
    "Washington": "Capital de Estados Unidos.",
    "Nadal": "Tenista español considerado entre los mejores de la historia.",
    "Federer": "Tenista suizo considerado uno de los mejores de la historia.",
    "Djokovic": "Serbio, actual top 1 del ranking ATP de tenis masculino."
    } 
    palabras_adivinadas = []
    lista_palabras = []
    tablero_incompleto = []
    Inicio()
    
    while numero_dado != 6 and len(palabras_adivinadas) != 12:
        print("\t\t\t\t\t\t    CRUCIGRAMA LOCO:")
        if len(lista_palabras) < 12:
            lista_palabras = Busca_palabras(palabras_y_definiciones, lista_palabras)
            tablero_completo, posiciones_palabras, posiciones_palabras_verticales, posiciones_palabras_horizontales = Completa_tableros(lista_palabras)
            tablero_incompleto, diccionario_posicion_palabra = Tablero_Usuario(tablero_completo, lista_palabras, posiciones_palabras)
            diccionario_palabra_letra_numero = Creo_diccionario_letra_numerodef(tablero_incompleto, diccionario_posicion_palabra)
            definiciones_con_numero = Crea_dic_palabra_letra_numero(diccionario_palabra_letra_numero, palabras_y_definiciones)
        Completador_palabra_adivinada(tablero_incompleto, posiciones_palabras_verticales, posiciones_palabras_horizontales, palabras_adivinadas)
        ImpresionMatriz(tablero_incompleto)
        Impresion_definiciones(definiciones_con_numero)
        ###print(f"Dejo el diccionario que tiene las palabras con su respectivo número de definición y letra de referencia:\n{diccionario_palabra_letra_numero}")   #Ayudita para chequear
        if not(Ingreso_usuario(diccionario_palabra_letra_numero, palabras_adivinadas)):
            print("Incorrecto :c")
            numero_dado = random.randint(1,6)
            print("Se ha sorteado el dado y el numero favorecido ha sido el: ", numero_dado)
            lista_palabras, palabras_adivinadas = Dado(numero_dado, lista_palabras, palabras_adivinadas, tablero_incompleto,  diccionario_palabra_letra_numero, posiciones_palabras_verticales, posiciones_palabras_horizontales, posiciones_palabras)
            if 2<numero_dado<5: Impresion_definiciones(definiciones_con_numero)
        input("Enter para continuar\n")
        os.system('cls')
    Completador_palabra_adivinada(tablero_incompleto, posiciones_palabras_verticales, posiciones_palabras_horizontales, palabras_adivinadas)
    ImpresionMatriz(tablero_incompleto)
    if len(palabras_adivinadas) == 0:
        print("Lo siento, el juego ha terminado. si quiere vuelva a intentarlo :)")

    elif len(palabras_adivinadas) < 12:
        print("El juego ha terminado, sus palabras adivinadas fueron:")
        Impresion_adivinadas(palabras_adivinadas)
        print(f"Estuvo a {12-len(palabras_adivinadas)} palabras de ganar el juego. Si se anima, puede intentarlo de nuevo..")
    else:
        print("FELICITACIONESSSSS!!! HAS GANADO EL JUEGO adivinando las palabras:")
        Impresion_adivinadas(palabras_adivinadas)

main()