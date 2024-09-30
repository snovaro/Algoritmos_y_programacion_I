import random
import requests
import os
import csv
import matplotlib.pyplot as plt
import matplotlib.image
import io
from passlib.hash import pbkdf2_sha256
from datetime import datetime

ANIO_ACTUAL = 2024
API_KEY = "827b3d5d7a5cfec03074a4fbe415dc37"

def es_float(num:str) -> bool:
    """
    PRE: Recibe un string
    POST: Devuelve True si puede ser convertido a float.
    """
    try:
        float(num)
        return True
    except ValueError:
        return False

def input_float() -> float:
    """
    PRE: -
    POST: Devuelve un valor numérico float.
    """
    numero = input("")
    while not es_float(numero):
        numero = input("El valor ingresado debe ser un número. Inténtelo nuevamente.\n$ ")
    numero = float(numero)
    return numero

def input_num() -> int:
    """
    PRE: -
    POST: Devuelve un valor numérico int.
    """
    numero = input("")
    while numero.isnumeric() != True:
        numero = input("El valor ingresado debe ser un número. Inténtelo nuevamente: ")
    numero = int(numero)
    return numero

def input_alfa() -> str:
    """
    PRE: -
    POST: Devuelve un valor alfabético, en minúsculas y sin tildes.
    """
    palabra = input("").lower()
    while palabra.isalpha() != True:
        palabra = input("El valor ingresado no es alfabético. Inténtelo nuevamente: ").lower()
    return palabra

def validador_num(valor:int, valores:list) -> int:
    """
    PRE: Ingresa un entero y una lista.
    POST: Devuelve el entero solo cuando verifique que el mismo pertenezca a la lista.
    """
    while valor not in valores:
        print(f"\"{valor}\" es una opción inválida. Inténtelo nuevamente: ", end="")
        valor = input_num()
    return valor

def validador_str(valor:str, valores:list) -> str:
    """
    PRE: Ingresa un string y una lista.
    POST: Devuelve el string solo cuando verifique que el mismo pertenezca a la lista.
    """
    while valor not in valores:
        print(f"\"{valor}\" es una opción inválida. Inténtelo nuevamente: ", end="")
        valor = input_alfa()
    return valor

def espacios_menu (nombre:str, dinero:str) -> int:
    """
    PRE: Ingresa el nombre de usuario y su dinero.
    POST: Devuelve la cantidad de puntos (.) de separación entre los mismo. Es solo una función para darle estética al menú.
    """
    cantidad_espacios = 33 - len(nombre) - len(dinero)
    if cantidad_espacios > 0:
        espacios = (" "*cantidad_espacios)
    else:
        espacios = ("\n")
    
    return espacios

def menu_principal(usuario) -> None:
    """
    PRE: -
    POST: Imprime el menú principal de la aplicación.
    """
    nombre = [*usuario.values()][0][0]
    dinero = [*usuario.values()][0][4]
    espacios = espacios_menu(nombre, dinero)
    os.system("cls")
    print("------------ MENU PRINCIPAL ------------")
    print(f"User: {nombre}{espacios}${dinero}")
    print("-"*40)
    print(f"a. Mostrar plantel completo de un equipo (temporada {ANIO_ACTUAL}).")
    print("b. Mostrar tabla para una temporada.")
    print("c. Consultar estadio y escudo de un equipo.")
    print("d. Gráficar goles y minutos de un equipo.")
    print("e. Cargar dinero en cuenta.")
    print("f. Mostrar Usuario que más dinero apostó.")
    print("g. Mostrar Usuario que más apuestas ganó.")
    print("h. Apostar.")
    print("i. Salir.")
    print("-"*40)

def posicion_jugador(pos:str) -> str:
    """
    PRE: Ingresa la posicion en la que juega el jugador (en inglés)
    POST: Devuelve la posicion pero en español. En caso de no coincidir con alguna de las 4 posiciones, devuelve la posición en ingles sin cambios.
    """
    if pos == "Attacker":
        pos = "Delantero"
    elif pos == "Defender":
        pos = "Defensor"
    elif pos == "Goalkeeper":
        pos = "Arquero"
    elif pos == "Midfielder":
        pos = "Mediocampista"
    
    return pos

def imprimir_equipos_LPA(lista_equipos:list) -> list:
    """
    PRE: Entra una lista de los equipos de la LPA
    POST: Imprime los equipos para el usuario y devuelve una lista de las opciones (numericas) posibles a elegir.
    """
    lista_opciones = []
    print("Equipos de la Liga Profesional Argentina:")
    print("-"*20)
    for i in range(len(lista_equipos)):
        lista_opciones.append(i+1)
        print(f"{i+1}. {lista_equipos[i]}")
    print("-"*20)
    return lista_opciones

def mostrar_plantel(dicc_equipos:dict) -> None:
    """
    PRE: Ingresa un diccionario con los equipos de la LPA y sus respectivos IDs.
    POST: Imprime el plantel de jugadores del equipo que indique el usuario.
    """
    lista_equipos_ids = [*dicc_equipos.keys()]
    lista_equipos = [*dicc_equipos.values()]
    respuesta = []
    page = 0
    lista_opciones = imprimir_equipos_LPA(lista_equipos)
    print("Ingrese de que equipo desea buscar su plantel: ", end="")
    equipo = validador_num(input_num(), lista_opciones)
    
    id_equipo = lista_equipos_ids[equipo-1]
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}
    params ={"league":"128", "season": ANIO_ACTUAL, "team": id_equipo}
    url = "https://v3.football.api-sports.io/players"
    paginas_respuesta = requests.get(url, params=params, headers=headers).json()["paging"]
    total_pages = paginas_respuesta["total"]
    while page < total_pages:
        page += 1
        params["page"] = page
        respuesta_2 = requests.get(url, params=params, headers=headers).json()["response"]
        for i in respuesta_2:
            respuesta.append(i)
    os.system("cls")
    
    print(f"Plantel de {lista_equipos[equipo-1]}:")
    print("-"*40)

    for i in range(len(respuesta)):
        apellido = (respuesta[i]["player"]["lastname"]).split()
        nombre = (respuesta[i]["player"]["firstname"]).split()
        puntitos = "." * (32 - (len(apellido[0])+len(nombre[0])))
        posicion = posicion_jugador(respuesta[i]["statistics"][0]["games"]["position"])
        print("{} {}{}{}".format(apellido[0], nombre[0], puntitos, posicion))
    print("-"*40)

def mostrar_tabla() -> None:
    """
    PRE: -
    POST: Imprime la tabla de posiciones de la LPA del año que indique el usuario.
    """
    años_ligas = range(2015, ANIO_ACTUAL+1)
    print("-"*25)
    print("Temporadas de la Liga Profesional Argentina.")
    for año in años_ligas:
        print(f" - {año}")
    print("-"*25)
    print("Ingrese el año de la temporada que desea conocer: ", end="")
    año_liga = int(validador_num(input_num(), años_ligas))

    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}
    params = {"league":"128", "season": año_liga}
    url = "https://v3.football.api-sports.io/standings"
    respuesta = requests.get(url, params=params, headers=headers).json()["response"][0]["league"]["standings"][0]
    os.system("cls")
    print(f"--- Liga Profesional Argentina {año_liga} ---")
    iterador = 0
    for equipo in respuesta:
        iterador += 1
        if iterador <= 9:
            puntitos = "." * (32 - len(equipo["team"]["name"]))
        else:
            puntitos = "." * (31 - len(equipo["team"]["name"]))
        
        print("{}. {}{}{}pts".format(equipo["rank"], equipo["team"]["name"], puntitos, equipo["points"]))
    print("-"*39)

def mostrar_imagen(respuesta:dict, escudo_estadio:int) -> None:
    """
    PRE: Ingresa la información de la API y un int (puede ser 1 o 2) que sirve de referencia para saber que imagen se va a imprimir. 
    POST: Imprime el escudo o el estadio del equipo ingresante.
    """
    escudo = respuesta["team"]["logo"]
    estadio = respuesta["venue"]["image"]
    nombre_estadio = respuesta["venue"]["name"]
    capacidad_estadio = respuesta["venue"]["capacity"]
    
    if escudo_estadio == 1: #IMPRIME ESCUDO
        link = escudo
        titulo = respuesta["team"]["name"]
    else:                   #IMPRIME ESTADIO
        link = estadio
        titulo = f"{nombre_estadio}\nCapacidad: {capacidad_estadio} espectadores"
    
    respuesta = requests.get(url = link)
    archivo_en_bytes = io.BytesIO(respuesta.content)
    imagen = matplotlib.image.imread(archivo_en_bytes, format = "jpg")
    plt.imshow(imagen)
    plt.title(titulo)
    plt.show()

def mostrar_estadio_y_escudo(dicc_equipos:dict) -> None:
    """
    PRE: Ingresa un diccionario con los equipos de la LPA y sus respectivos IDs. 
    POST: Imprime información sobre el club que indique el usuario.
    """
    lista_equipos_ids = [*dicc_equipos.keys()]
    lista_equipos = [*dicc_equipos.values()]    
    lista_opciones = imprimir_equipos_LPA(lista_equipos)
    print("Ingrese el equipo del que desea obtener información sobre el estadio: ", end="")
    equipo_a_buscar = validador_num(input_num(), lista_opciones)

    id_equipo_a_buscar = lista_equipos_ids[equipo_a_buscar-1]
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}
    params ={"league":"128","season": ANIO_ACTUAL}
    url = "https://v3.football.api-sports.io/teams"

    respuesta = requests.get(url, params=params, headers=headers).json()["response"] #team, venue["name", "address", "city", "capacity", " surface", "image"]
    os.system("cls")
    for i in range(len(respuesta)):
        if respuesta[i]["team"]["id"] == id_equipo_a_buscar:
            nombre = respuesta[i]["team"]["name"]
            input(f"Presione enter para ver el escudo de {nombre}.\n<Luego debe cerrar la imagen para continuar>")
            mostrar_imagen(respuesta[i], 1)
            print("-"*45)
            input(f"Presione enter para ver el estadio de {nombre}.\n<Luego debe cerrar la imagen para continuar>")
            mostrar_imagen(respuesta[i], 2)
            print("-"*45)
            input(f"Presione enter para más información sobre {nombre}")
            print("-------" + nombre.upper() + "-------")
            print("Año de fundación:", respuesta[i]["team"]["founded"])
            print("País:", respuesta[i]["team"]["country"])
            print("Ciudad:", respuesta[i]["venue"]["city"])
            print("Dirección:", respuesta[i]["venue"]["address"])
            if respuesta[i]["venue"]["surface"] == "grass": print("Superficie: Césped")
            print("-"*40)

def output_mostrar_grafico_goles(dicc_equipos:dict, año_liga:int, id_equipo:int) -> None:
    """
    PRE: Ingresa un diccionario con los equipos de la LPA y sus respectivos IDs y los parametros de la API. 
    POST: Imprime el gráfico de los goles del equipo seleccionado en la temporada ANIO_ACTUAL.
    """    
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}
    params ={"league":128,"season":año_liga,"team":id_equipo}
    url = "https://v3.football.api-sports.io/teams/statistics"
    respuesta = requests.get(url, params=params, headers=headers).json()["response"]["goals"]["for"]
    numeros_porcentajes= []
    porcentajes =[] #["0-15"],["16-30"],["31-45"],["46-60"],["61-75"],["76-90"],["91-105"],["106-120"] ej: ['31.58%', '10.53%', '10.53%', '15.79%', '10.53%', '15.79%', '5.26%', None]
    porcentajes_str = ""
    os.system("cls")
    print("-----",dicc_equipos[id_equipo].upper(),"-----")
    print(f"Temporada: {año_liga}")
    print("Goles a favor:", respuesta["total"]["total"])
    print("-"*25)
    print("Presione enter para abrir el gráfico.")
    input("Cierre el gráfico para volver a la aplicación.")
        
    for minutos in respuesta["minute"]:
        porcentajes.append(respuesta["minute"][minutos]["percentage"])
    for i in range(len(porcentajes)):
        if type(porcentajes[i]) is not str:
            porcentajes[i] = "0.00%"
    porcentajes_str = " ".join(porcentajes)
    porcentajes_str = porcentajes_str.replace("%", "")
    numeros_porcentajes = porcentajes_str.split()
    for i in range(len(numeros_porcentajes)):
        numeros_porcentajes[i] = float(numeros_porcentajes[i])

    plt.figure(figsize=(12, 8))
    x = ["Min 0 al 15", "Min 16 al 30", "Min 31 al 45", "Min 46 al 60", "Min 61 al 75", "Min 76 al 90", "Min 90 al 105", "Min 105 al 120"]
    y = numeros_porcentajes
    plt.xlabel("Minutos")
    plt.ylabel("Porcentaje de goles")
    plt.yticks(sorted(numeros_porcentajes))
    plt.title("PORCENTAJE DE GOLES POR MINUTO\n TOTAL DE GOLES EN LA TEMPORADA {}: {}".format(año_liga, respuesta["total"]["total"]))
    plt.bar(x,y, linewidth=2, edgecolor="black")
    plt.show()

def mostrar_grafico_goles(dicc_equipos:dict) -> None:
    """
    PRE: Ingresa un diccionario con los equipos de la LPA y sus respectivos IDs. 
    POST: Valida los inputs de las elecciones del usuario y los manda a otra función para que se impriman.
    """
    lista_equipos_ids = [*dicc_equipos.keys()]
    lista_equipos = [*dicc_equipos.values()]   
    años_ligas = range(2015, ANIO_ACTUAL+1)
    print("Temporadas de la Liga Profesional Argentina:")
    for año in años_ligas:
        print(f" - {año}")
    print("-"*20)
    print("Ingrese el año de la temporada que desea conocer: ", end="")
    año_liga = (validador_num(input_num(), años_ligas))
    os.system("cls")
    lista_opciones = imprimir_equipos_LPA(lista_equipos)
    print("Ingrese de que equipo desea buscar sus estadísticas de goles: ", end="")
    equipo = (validador_num(input_num(), lista_opciones))
    id_equipo = (lista_equipos_ids[equipo-1])
    output_mostrar_grafico_goles(dicc_equipos, año_liga, id_equipo)

def mail_validado() -> str:
    """
    PRE: - 
    POST: Valida y devuelve el input del usuario si cumple con un formato de mail (que no acepta puntos en el nombre o servicio de mail, unicamente acepta ".com").
    """
    os.system("cls")
    print("El mail debe cumplir las siguientes condiciones:")
    print("-"*25)
    print(" - Formato: nombre_usuario@nombre_servicio_correo.com\n - \"nombre_usuario\" y \"nombre_servicio_correo\" no deben contener espacios ni caracteres especiales.\n - Ejemplo: Leonel@gmail.com")
    print("-"*25)
    mail = input("Ingrese un mail: ")
    while len(mail) == 0:
        mail = input("Ingrese un mail: ")

    cantidad_puntos = mail.count(".")
    mail_spliteado:list = mail.split("@")

    if len(mail_spliteado) != 2:
        print("El mail debe contener una única \"arroba\"(@) para separar usuario del servicio de correo electrónico")
        input("Presione enter para intentarlo nuevamente.")
        return mail_validado()
    if cantidad_puntos != 1:
        print("El mail debe contener un único \"punto\"(.) para poder finalizar con \".com\"")
        input("Presione enter para intentarlo nuevamente.")
        return mail_validado()
    if mail_spliteado[1].count(".") == 0:
        print("El \"punto\"(.) del mail debe estar después de la \"arroba\"(@)")
        input("Presione enter para intentarlo nuevamente.")
        return mail_validado()

    usuario, correo, com  = mail_spliteado[0], mail_spliteado[1].split(".")[0], mail_spliteado[1].split(".")[1]
    cond1:bool = usuario.isalnum()
    cond2:bool = correo.isalnum()
    cond3:bool = com == "com"

    if cond1 != True or cond2 != True or cond3 != True:
        print(f"{mail} es un mail inválido.")
        input("Presione enter para intentarlo nuevamente.")
        return mail_validado()

    return mail

def obtener_usuarios_existentes() -> dict:
    """
    PRE: Supone que hay al menos un usuario guardado.
    POST: Devuelve un dict con todos los usuarios.
    """
    usuarios_existentes: dict = {}
    with open('usuarios.csv', newline='') as usuariosCsv:
        csvReader = csv.reader(usuariosCsv, delimiter = ",")
        next(csvReader)
        for row in csvReader:
            usuarios_existentes[row[0]] = [row[1],row[2],row[3],row[4], row[5]]
    return usuarios_existentes

def obtener_transacciones_existentes() -> list:
    """
    PRE: Supone que hay al menos una transaccion guardada.
    POST: Devuelve una lista con todas las transacciones.
    """
    transacciones_existentes: list = []
    with open('transacciones.csv', newline='') as transaccionesCsv:
        csvReader = csv.reader(transaccionesCsv, delimiter = ",")
        next(csvReader)
        for row in csvReader:
            transacciones_existentes.append([row[0], row[1],row[2],row[3]])
    return transacciones_existentes

def pedir_data_inicio_sesion() -> list:
    """
    PRE: -
    POST: Devuelve una lista con email y contraseña ingresados.
    """
    email: str = mail_validado()
    contrasena: str = input("Ingrese su contraseña: ")
    while contrasena == '':
        contrasena = input("Ingrese su contraseña: ")
    return [email, contrasena]

def obtener_usuario(email:str) -> dict:
    """
    PRE: Supone que existe un usuario con cuyo id coincide con el string ingresado.
    POST: Devuelve un dict con el usuario buscado.
    """
    usuarios: dict = obtener_usuarios_existentes()
    for id in usuarios:
        if email == id:
            return {email: usuarios[id]}

def obtener_fecha() -> str:
    return datetime.today().strftime('%Y%m%d')

def crear_nuevo_usuario(data_inicio_sesion:list) -> None:
    """
    PRE: Recibe una lista con email, contraseña y nombre de usuario. Supone que no hay un usuario cuyo id coincide con el email ingresado.
    POST: Guarda los datos en el CSV de Usuarios.
    """
    usuarios_existentes: dict = obtener_usuarios_existentes()
    contrasena_encriptada: str = pbkdf2_sha256.hash(data_inicio_sesion[1])
    with open('usuarios.csv', 'w', newline='') as usuariosCsv:
        csvWriter = csv.writer(usuariosCsv, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_NONNUMERIC)
        csvWriter.writerow(("ID Usuario", "Nombre Usuario", "Contraseña", "Dinero Apostado", "Fecha Última Apuesta", "Dinero Disponible"))
        for id in usuarios_existentes:
            csvWriter.writerow((id, usuarios_existentes[id][0], usuarios_existentes[id][1], usuarios_existentes[id][2], usuarios_existentes[id][3], usuarios_existentes[id][4]))
        csvWriter.writerow((data_inicio_sesion[0], data_inicio_sesion[2], contrasena_encriptada, "0", "DDMMYYYY", "0"))

def crear_nueva_transaccion(id_usuario:str, fecha:str, tipo:str, importe:float) -> None:
    """
    PRE: Recibe la informacion de la transaccion a crear.
    POST: Guarda la transacción en el CSV de transacciones.
    """
    transacciones_existentes: list = obtener_transacciones_existentes()
    with open('transacciones.csv', 'w', newline='') as transaccionesCsv:
        csvWriter = csv.writer(transaccionesCsv, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_NONNUMERIC)
        csvWriter.writerow(("ID Usuario", "Fecha de Transaccion", "Tipo de Resultado", "Importe"))
        for transaccion in transacciones_existentes:
            csvWriter.writerow((transaccion[0], transaccion[1], transaccion[2], transaccion[3]))
        csvWriter.writerow((id_usuario, fecha, tipo, importe))

def crear_usuario() -> dict:
    """
    PRE: -
    POST: Devuelve un dict con el usuario creado.
    """
    #Busco Usuarios existentes
    usuarios_existentes: dict = obtener_usuarios_existentes()
    #Pido usuario y contraseña
    data_inicio_sesion: list = pedir_data_inicio_sesion()
    #Ver que no exista
    while data_inicio_sesion[0] in usuarios_existentes.keys():
        print("El usuario ya existe. Intente con otro e-mail.")
        data_inicio_sesion = pedir_data_inicio_sesion()
    #Pido nombre de usuario
    nombre_de_usuario: str = input("Ingrese su nombre de usuario: ")
    while nombre_de_usuario == "":
        nombre_de_usuario = input("Ingrese su nombre de usuario: ")
    data_inicio_sesion.append(nombre_de_usuario)
    #Guardar Usuario en usuarios.csv
    crear_nuevo_usuario(data_inicio_sesion)
    usuario:dict = obtener_usuario(data_inicio_sesion[0])
    print("-"*25)
    print(f"Bienvenido {usuario[data_inicio_sesion[0]][0]}!")
    print(f"Tienes ${usuario[data_inicio_sesion[0]][4]} disponible.")
    print("-"*25)
    input("Presione enter para ingresar al menú.")
    return usuario

def verificar_contrasena(contrasena_encriptada:str, contrasena_ingresada:str) -> bool:
    """
    PRE: Recibe la contraseña encriptada guardada en usuarios.csv y la ingresada por el usuario.
    POST: Devuelve True si verifica.
    """
    if(pbkdf2_sha256.verify(contrasena_ingresada, contrasena_encriptada)):
        return True
    return False

def ingresar_usuario() -> dict:
    """
    PRE: -
    POST: Devuelve un dict con el usuario ingresado.
    """
    usuarios_existentes: dict = obtener_usuarios_existentes()
    #Pido usuario y contraseña
    data_inicio_sesion: list = pedir_data_inicio_sesion()
    #Ver que exista
    while data_inicio_sesion[0] not in usuarios_existentes.keys():
        print("-"*25)
        input("El usuario no existe. Presione enter para intentar con otro e-mail.")
        data_inicio_sesion = pedir_data_inicio_sesion()
    #Chequeo contraseña
    while not verificar_contrasena(usuarios_existentes[data_inicio_sesion[0]][1], data_inicio_sesion[1]):
        print("-"*25)
        print("La contraseña ingresada es incorrecta.")
        data_inicio_sesion[1] = input("Intente nuevamente: ")
    usuario: dict = {data_inicio_sesion[0]: usuarios_existentes[data_inicio_sesion[0]]}
    print("-"*25)
    print(f"Bienvenido {usuario[data_inicio_sesion[0]][0]}!")
    print(f"Tienes ${usuario[data_inicio_sesion[0]][4]} disponible.")
    print("-"*25)
    input("Presione enter para ingresar al menú.")
    return usuario

def modificar_usuario(usuarios_actualizados:dict) -> None:
    """
    PRE: Recibe un dict con todos los usuarios actualizados.
    POST: Devuelve un dict con el usuario ingresado.
    """
    with open('usuarios.csv', 'w', newline='') as usuariosCsv:
        csvWriter = csv.writer(usuariosCsv, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_NONNUMERIC)
        csvWriter.writerow(("ID Usuario", "Nombre Usuario", "Contraseña", "Dinero Apostado", "Fecha Última Apuesta", "Dinero Disponible"))
        for id in usuarios_actualizados:
            csvWriter.writerow((id, usuarios_actualizados[id][0], usuarios_actualizados[id][1], usuarios_actualizados[id][2], usuarios_actualizados[id][3], usuarios_actualizados[id][4]))

def resolver_carga_dinero(usuario:dict) -> None:
    """
    PRE: Recibe un diccionario de un usuario.
    POST: Deriva a las funciones que le carga dinero al usuario y crea la transacción de depósito en el CSV.
    """
    print("Ingrese el dinero a cargar a su cuenta:")
    print("-"*25)
    print("$ ", end = "")
    cantidad_a_cargar: float = input_float()
    while cantidad_a_cargar <= 0:
        print("No se puede cargar la cantidad ingresada. Intente nuevamente.")
        print("$ ", end = "")
        cantidad_a_cargar: float = input_float()
    cargar_dinero(usuario, cantidad_a_cargar)
    crear_nueva_transaccion([*usuario.keys()][0], obtener_fecha(), "Deposito", str(cantidad_a_cargar))

def cargar_dinero(usuario:dict, cantidad_a_cargar:float) -> None:
    """
    PRE: Recibe un diccionario de un usuario y la cantidad de dinero a cargar.
    POST: Le carga dinero al usuario en el diccionario.
    """
    usuarios_existentes: dict = obtener_usuarios_existentes()
    email: str = list(usuario.keys())[0]
    dinero_disponible = float(usuarios_existentes[email][4])
    usuarios_existentes[email][4] = str(dinero_disponible + cantidad_a_cargar)
    os.system("cls")
    print("------Carga exitosa------")
    print(f"{[*usuario.values()][0][0]}, cargaste ${cantidad_a_cargar}!")
    print(f"Ahora dispones de ${usuarios_existentes[email][4]}.")
    print("-"*25)
    modificar_usuario(usuarios_existentes)

def iniciar_sesion() -> dict:
    """
    PRE: -
    POST: Menú de inicio de sesión. Devuelve un diccionario con el usuario que ingresó al programa.
    """
    print("-"*38)
    print("a. Iniciar sesión.\nb. Crear nuevo usuario.")
    print("-"*38)
    print("Indique que desea hacer: ", end = "")
    opcion: str = validador_str(input_alfa(), ["a","b"])
    
    os.system("cls")
    if(opcion == 'a'):
        usuario: dict = ingresar_usuario()
    if(opcion == 'b'):
        usuario: dict = crear_usuario()
    return usuario

def mostrar_usuario_que_mas_aposto() -> None:
    """
    PRE: -
    POST: Busca información del CSV de Usuarios y muestra el que más dinero haya apostado.
    """
    os.system("cls")
    usuarios_existentes: dict = obtener_usuarios_existentes()
    mayor_monto_apostado: float = 0.0
    usuarios_que_mas_apostaron: dict = {}
    for id in usuarios_existentes:
        monto_apostado_usuario: float = float(usuarios_existentes[id][2])
        if(monto_apostado_usuario > mayor_monto_apostado):
            mayor_monto_apostado = monto_apostado_usuario
            usuarios_que_mas_apostaron = {id: usuarios_existentes[id]}
        elif(monto_apostado_usuario == mayor_monto_apostado):
            usuarios_que_mas_apostaron = usuarios_que_mas_apostaron | {id: usuarios_existentes[id]}
    if(mayor_monto_apostado == 0.0):
        print("Todavia no se realizaron apuestas.")
        print("-"*25)
    else:
        print("Usuarios que más dinero apostaron")
        print("-"*33)
        for id in usuarios_que_mas_apostaron:
            print(f" - {usuarios_que_mas_apostaron[id][0]}")
        print("-"*28)
        print(f"Monto apostado: ${[*usuarios_que_mas_apostaron.values()][0][2]}")
        print("-"*28)

def obtener_cant_victorias_usuarios() -> dict:
    """
    PRE: -
    POST: Busca información del CSV de transacciones y devuelve un diccionario de key "mail" y value "cantidad_veces_ganadas(int)".
    """
    transacciones_existentes:list = obtener_transacciones_existentes()
    victorias_usuarios:dict = {}
    for transaccion in transacciones_existentes:
        if transaccion[2] == "Gana":
            if transaccion[0] not in [*victorias_usuarios.keys()]:
                victorias_usuarios[transaccion[0]] = 1
            else:
                victorias_usuarios[transaccion[0]] += 1

    return victorias_usuarios

def mostrar_usuario_que_mas_gano() -> None:
    """
    PRE: -
    POST: Muestra en pantalla que usuario/s ganaron más apuestas.
    """
    balance_usuarios: dict = obtener_cant_victorias_usuarios() # {mail:cantidad_veces_ganadas(int)}
    usuario_que_mas_gano: list = [["", 0]]
    for mail in balance_usuarios:
        if balance_usuarios[mail] > usuario_que_mas_gano[0][1]:
            usuario_que_mas_gano = [[mail, balance_usuarios[mail]]]
        elif balance_usuarios[mail] == usuario_que_mas_gano[0][1] and balance_usuarios[mail] > 0:
            usuario_que_mas_gano.append([mail, balance_usuarios[mail]])
       
    if usuario_que_mas_gano[0][0] == "":
        print("Ningun usuario ganó apuestas aún.")
    else:
        print("Los usuarios que mas ganaron son:")
        print("-"*33)
        for usuario in usuario_que_mas_gano:
            dict_usuario = obtener_usuario(usuario[0])
            nombre_de_usuario = [*dict_usuario.values()][0][0]
            print(f" - {nombre_de_usuario}")
        print("-"*28)
        print(f"Cantidad de apuestas exitosas: {usuario_que_mas_gano[0][1]}")
        print("-"*28)

def busca_fixture(dicc_equipos:dict) -> tuple:
    """
    PRE: Ingresa un diccionario con los equipos de la LPA y sus respectivos IDs.
    POST: Devuelve una tupla con la lista de partidos del fixture del ANIO_ACTUAL para el equipo seleccionado y el ID del equipo ingresado por el usuario.
    """    
    lista_equipos = [*dicc_equipos.values()]
    lista_equipos_ids = [*dicc_equipos.keys()]
    #Imprimo equipos
    lista_opciones = imprimir_equipos_LPA(lista_equipos)
    print("Ingrese el equipo del que desea obtener información sobre el fixture: ", end="")
    #Pido a usuario el Equipo
    equipo_a_buscar = validador_num(input_num(), lista_opciones)
    id_equipo_a_buscar = lista_equipos_ids[equipo_a_buscar-1]
    #Get Fixture
    respuesta = []
    intentos = 0
    while len(respuesta) == 0:
        if intentos == 2:
            print("Ha ocurrido un error con la API, lo sentimos")
            exit(-1)    
        respuesta = obtener_fixture(id_equipo_a_buscar)
        intentos +=1

    #Armo Lista de Partidos
    lista_partidos = obtener_lista_partidos(respuesta, id_equipo_a_buscar)
    
    return lista_partidos, id_equipo_a_buscar

def obtener_fixture(id) -> dict:
    """
    PRE: -
    POST: Devuelve un diccionario con el fixture de la API para la season actual fase 1.
    """  
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}
    params = {"league":"128","season": ANIO_ACTUAL, "from":f"{ANIO_ACTUAL}-01-15", "to":f"{ANIO_ACTUAL}-12-20", "team":id}
    url = "https://v3.football.api-sports.io/fixtures"
    return requests.get(url, params=params, headers=headers).json()["response"] #['fixture'],["league"]["round"], ['teams'][home or away]["id","name","logo","winner":bool]

def obtener_wod(id:str)->bool: #SIEMPRE VA A DAR EL WIN_OR_DRAW DEL LOCAL
    """
    PRE: Ingresa el id del partido a buscar.
    POST: Devuelve un booleano, siempre refiriendose al equipo local. Ej.: Si es true, el local tiene win_or_draw = true.
    """  
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}
    params = {"fixture":id}
    url = "https://v3.football.api-sports.io/predictions"
    respuesta = requests.get(url, params=params, headers=headers).json()["response"]
    if len(respuesta) == 0: return True #Hay un problema en el llamado a la API y la lista de respuesta queda vacia
    respuesta = respuesta[0]
    if respuesta["predictions"]["winner"]["name"] == respuesta["teams"]["home"]["name"]:
        wod = respuesta["predictions"]["win_or_draw"]
    else:
        wod = not respuesta["predictions"]["win_or_draw"]
    return wod

def obtener_lista_partidos(fixture:dict, id_equipo_a_buscar:int) -> list:
    """
    PRE: Ingresa el fixture completo de la season actual y el ID del equipo a buscar.
    POST: Devuelve una lista del fixture de esa season con los partidos del equipo seleccionado.
    """  
    lista_partidos = []
    numero_fecha = 0
    for i in range(len(fixture)):
        localias = ["home", "away"]
        for localia in localias:
            if id_equipo_a_buscar == fixture[i]["teams"][localia]["id"]:
                numero_fecha +=1
                estado = fixture[i]["fixture"]["status"]["short"]
                wod:bool = False #es para rellenar, no se va a acceder al wod de una fecha con "estado" == FT.
                if estado != "FT":
                    wod:bool = obtener_wod(fixture[i]["fixture"]["id"])
                lista_partidos.append([numero_fecha, fixture[i]["teams"], estado, wod])

    return sorted(lista_partidos) # Ordenado por fase y fecha. Ej "15" , teams , estado (FT y otros), wod(bool)

def imprimir_fixture(dicc_equipos:dict, lista_partidos:list, id_equipo:str, multiplicador:int) -> None:
    """
    PRE: Ingresa el diccionario de equipos de la LPA con sus IDs, la lista de partidos obtenida del fixture y el ID del equipo seleccionado.
    POST: Imprime el fixture para que el usuario elija a qué partido apostar.
    """  
    os.system("cls")
    print("FIXTURE DE {}".format(dicc_equipos[id_equipo].upper()))
    print(" "*8,"<LOCAL>"," "*67,"<VISITANTE>")
    print(" "*31,"---------------- PRIMERA FASE ----------------")
    
    for partido in lista_partidos:
        if partido[0] < 10:
            partido[0] = "0"+str(partido[0])
        partido[0] = str(partido[0])
        local = partido[1]["home"]["name"]
        visitante = partido[1]["away"]["name"]
        puntitos1= "."*(45 - (len(local)))
        puntitos2= "."*(40 - (len(visitante)))

        if partido[2] == "FT":
            print("Fecha {}.{}{}vs{}{} - TERMINADO".format(partido[0], local, puntitos1, puntitos2, visitante))
        else:
            puntitos1 = "."*(40 - (len(local)))
            if partido[3]:
                paga_local = f"x{round(float(multiplicador*0.1),1)}"
                paga_visitante = f"x{round(float(multiplicador), 1)}"
            else: 
                paga_local = f"x{round(float(multiplicador), 1)}"
                paga_visitante = f"x{round(float(multiplicador*0.1),1)}"
            print("Fecha {}.{} {}{}vs{}{} {}".format(partido[0], local, paga_local, puntitos1, puntitos2, visitante, paga_visitante))
    print("Aclaración!! En caso de realizarse una apuesta por un empate se podrá obtener una ganancia de 0.5 de lo apostado.")

def elije_partido(dinero_disponible_usuario:float, lista_partidos:list) -> tuple:
    """
    PRE: Ingresa el dinero disponible del usuario y la lista de partidos del fixture.
    POST: Devuelve una tupla con el dinero apostado, la eleccion de la apuesta y el partido al que apostó.
    """  
    #Pido Partido a apostar
    partidos_restantes:list = []
    for partido in lista_partidos:
        if partido[2] != "FT": partidos_restantes.append(int(partido[0]))
    print("-"*25)
    print("Escriba el numero de la fecha del partido (sin definir) en el cual quiere realizar su apuesta: ", end="")
    partido_a_apostar = str(validador_num(input_num(), partidos_restantes))
    for i in range(len(lista_partidos)):
        if lista_partidos[i][0] == partido_a_apostar:
            nombre_local = lista_partidos[i][1]["home"]["name"]
            nombre_visitante = lista_partidos[i][1]["away"]["name"]
    print("-"*45)
    print(f"Elegiste apostar al partido: {nombre_local}(L) vs {nombre_visitante}(V)")
    print("-"*25)
    print("A que resultado quiere apostar:")
    print(f"1. Ganador {nombre_local}(L)\n2. Empate\n3. Ganador {nombre_visitante}(V)")
    apuesta = validador_num(input_num(), [1,2,3])   # 1: APUESTA POR EL LOCAL - 2: EMPATE - 3: APUESTA POR EL VISITANTE
    
    os.system("cls")
    if apuesta == 1:
        impresion = f"Elegiste apostar por el equipo {nombre_local}(L)"
    elif apuesta == 2:
        impresion = f"Elegiste apostar por un empate entre {nombre_local}(L) y {nombre_visitante}(V)"
    else:
        impresion = f"Elegiste apostar por el equipo {nombre_visitante}(V)"
    print(impresion)
    print("-"*25)
    print("Escriba la cantidad de dinero que desea apostar: ", end="")
    dinero_apostado = input_float()
    #Validar que el usuario cuente con ese dinero
    while dinero_apostado > dinero_disponible_usuario or dinero_apostado == 0:
        print("-"*25)
        if dinero_apostado > dinero_disponible_usuario:
            print(f"No cuenta con esa cantidad de dinero. Actualmente dispone de ${dinero_disponible_usuario}.\nEscriba la cantidad de dinero que desea apostar: ", end="")
        else:
            print(f"Debe ingresar una cantidad de dinero mayor a 0.\nEscriba la cantidad de dinero que desea apostar: ", end="")
        dinero_apostado = input_float()
    os.system("cls")
    print("Apuesta realizada exitosamente!")
    print(f"Apostaste ${dinero_apostado} {impresion[17:]}")
    print("-"*25)
    input("Presione enter para conocer los resultados del partido.")
    print("-"*25)
    return dinero_apostado, apuesta, partido_a_apostar

def wod_partido(lista_partidos:list, partido_a_apostar:str) -> tuple:
    """
    PRE: Ingresa la lista de partidos del fixture y el partido a apostar.
    POST: Devuelve una tupla con un booleano que indica si el win_or_draw es true o false para el LOCAL y devuelve una tupla con el equipo local en el índice [0] y el visitante en el [1].
    """  
    for partido in lista_partidos:
        if int(partido[0]) == int(partido_a_apostar):
            local = partido[1]["home"]["name"]
            visitante = partido[1]["away"]["name"]
            equipos = local, visitante
            return partido[3], equipos

def resolver_apuesta(dinero_apostado:float, apuesta:int, win_or_draw:bool, nombres:tuple, multiplicador:int) -> float: #EL WIN OR DRAW ES DEL EQUIPO LOCAL
    """
    PRE: Ingresa el dinero apostado, la eleccion de la apuesta, el win_or_draw del equipo local y una tupla con el nombre del equipo local y el del visitante.
    POST: Devuelve la ganancia del usuario (puede ser positiva o negativa según el resultado).
    """  
    #Dado simula resultado:
    #1 -> Gana Local
    #2 -> Empate
    #3 -> Gana Visitante
    dado = random.randint(1,3)
    if (apuesta == 1 and win_or_draw==True) or (apuesta == 3 and win_or_draw==False):
        multiplicador = multiplicador*0.1
    #Dado == 2 da Empate
    #Falta ver si se quita primero lo apostado y despues lo recupera o si se quita solo en caso de perder
    
    if dado == 2:
        #Dado da Empate y se Aposto Empate
        if apuesta == 2:
            print(f"Felicitacioness!! El partido entre {nombres[0]} y {nombres[1]} fue un empate!! ya puede encontrar su ganancia de ${dinero_apostado*0.5}")
            ganancia = dinero_apostado*0.5
        #Dado da Empate y se Aposto otra cosa
        else:
            print(f"Lo sentimos. El partido entre {nombres[0]} y {nombres[1]} terminó empatado, por lo que lamentablemente pierde lo apostado.")
            ganancia = -dinero_apostado
    #Dado == 1 da que Gana Local
    elif dado == 1:
        #Dado da Gana Local y se Aposto Gana Local
        if apuesta == 1:
            print(f"Felicitaciones!! Ganó {nombres[0]}!! La apuesta ha sido un exito, ya puede encontrar su ganancia de ${dinero_apostado*multiplicador}")
            ganancia = dinero_apostado*multiplicador
        #Dado da gana Local y se Aposto otra cosa
        else:
            print(f"Lo sentimos. El ganador ha sido {nombres[0]}, por lo que lamentablemente pierde lo apostado.")
            ganancia = -dinero_apostado
    #Dado == 3 da que Gana Visitante
    elif dado == 3:
        #Dado da gana V y se Aposto Gana V
        if apuesta == 3:
            print(f"Felicitacioness!! Ganó {nombres[1]}!! La apuesta ha sido un exito, ya puede encontrar su ganancia de ${dinero_apostado*multiplicador}")
            ganancia = dinero_apostado*multiplicador
        #Dado da gana V y se Aposto otra cosa
        else:
            print(f"Lo sentimos. El ganador ha sido {nombres[1]}, por lo que lamentablemente pierde lo apostado.")
            ganancia = -dinero_apostado
    return ganancia

def imprimir_menu_apuestas() -> None:
    """
    PRE: .
    POST: Imprime el menú de las apuestas para dar instrucciones al usuario.
    """    
    print("----------- MENU APUESTAS -----------")
    print("1. Se mostrarán los equipos de la LPA y deberá elegir alguno para conocer su fixture")
    print("2. Se imprimirá el fixture del equipo seleccionado y se mostrarán las pagas por cada apuesta (multiplicador)")
    print("3. Deberá ingresar a qué <partido>, qué <monto> y qué <resultado> desea apostar")
    print("-"*37)
    print(" - La ganancia será mayor si apuesta al equipo con menos chances de ganar")
    print(" - En caso de no acertar al resultado, perderá todo el dinero apostado")
    print("-"*37)
    input("Presione enter para comenzar.")

def actualizar_usuarios(usuario:dict, ganancia:float, dinero_apostado:float) -> None:
    """
    PRE: Ingresa el usuario logeado, la ganancia de la apuesta y el dinero apostado.
    POST: Modifica 3 parametros del diccionario y actualiza el CSV.
    """
    usuarios_existentes: dict = obtener_usuarios_existentes()
    email: str = list(usuario.keys())[0]
    #Modifico Dinero disponible
    dinero_disponible = float(usuarios_existentes[email][4])
    usuarios_existentes[email][4] = str(dinero_disponible + ganancia)
    usuario[email][4] = str(dinero_disponible + ganancia)
    #Modifico Fecha última apuesta
    usuarios_existentes[email][3] = obtener_fecha()
    usuario[email][3] = obtener_fecha()
    #Modifico Dinero apostado
    dinero_apostado_total = float(usuarios_existentes[email][2])
    usuarios_existentes[email][2] = str(dinero_apostado_total + dinero_apostado)
    usuario[email][2] = str(dinero_apostado_total + dinero_apostado)
    modificar_usuario(usuarios_existentes)

def main_apuestas(dicc_equipos:dict, usuario:dict) -> None:
    """
    PRE: Ingresa el diccionario de equipos de la LPA con sus IDs y el usuario logeado.
    POST: Es la función main que organiza y gestiona todo el punto de "apuestas".
    """
    multiplicador = random.randint(2,4)  
    imprimir_menu_apuestas()
    os.system("cls")
    dinero_disponible_usuario:float = float([*usuario.values()][0][4])
    lista_partidos, id_equipo = busca_fixture(dicc_equipos)
    imprimir_fixture(dicc_equipos, lista_partidos, id_equipo, multiplicador)
    dinero_apostado, apuesta, partido_a_apostar = elije_partido(dinero_disponible_usuario, lista_partidos)
    win_or_draw, equipos = wod_partido(lista_partidos, partido_a_apostar)
    ganancia = resolver_apuesta(dinero_apostado, apuesta, win_or_draw, equipos, multiplicador)
    print("-"*30)
    input("Presione enter para volver al menú principal.")
    actualizar_usuarios(usuario, ganancia, dinero_apostado)
    if(ganancia > 0):
        crear_nueva_transaccion([*usuario.keys()][0], obtener_fecha(), "Gana", str(ganancia))
    else:
        crear_nueva_transaccion([*usuario.keys()][0], obtener_fecha(), "Pierde", str(ganancia))

def obtenes_dicc_ids_liga_actual():
    dicc_ids = {}
    headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}
    params = {"league":"128", "season": ANIO_ACTUAL}
    url = "https://v3.football.api-sports.io/standings"
    respuesta = requests.get(url, params=params, headers=headers).json()["response"][0]["league"]["standings"][0]
    for posicion in respuesta:
        dicc_ids[posicion['team']['id']] = posicion['team']['name']
    return dicc_ids
def main() -> None:
    diccionario_equipos = obtenes_dicc_ids_liga_actual()
    print("--------Bienvenido a Jugársela--------")
    input("Pulse Enter para iniciar la aplicación")
    usuario: dict = iniciar_sesion()
    # ↓↓↓↓ USUARIO PARA PROBAR PUNTOS QUE NO TENGAN QUE VER CON APUESTAS Y TARIFAS ↓↓↓↓
    #usuario: dict = {'uma@gmail.com': ['Mofletes', '$pbkdf2-sha256$29000$ba1VqhUiJCQEQGgtJWQMoQ$KwNC.BSCTTMZhIEqXjkShUWe7HY1mh9OHsNfIQ1twK8', '0', 'DDMMYYYY', '0']}
    
    menu_principal(usuario)
    print("Ingrese una opción del menú: ", end="")
    opcion = validador_str(input_alfa(), ["a","b","c","d","e","f","g","h","i"])
    while opcion != 'i':
        os.system("cls")
        if(opcion == 'a'):
            mostrar_plantel(diccionario_equipos)
            input("Pulse enter para continuar.")
        elif(opcion == 'b'):
            mostrar_tabla()
            input("Pulse enter para continuar.")
        elif(opcion == 'c'):
            mostrar_estadio_y_escudo(diccionario_equipos)
            input("Pulse enter para continuar.")
        elif(opcion == 'd'):
            mostrar_grafico_goles(diccionario_equipos)
            input("Pulse enter para continuar.")
        elif(opcion == 'e'):
            resolver_carga_dinero(usuario)
            usuario = obtener_usuario([*usuario.keys()][0])
            input("Pulse enter para continuar.")
        elif(opcion == 'f'):
            mostrar_usuario_que_mas_aposto()
            input("Pulse enter para continuar.")
        elif(opcion == 'g'):
            mostrar_usuario_que_mas_gano()
            input("Pulse enter para continuar.")
        elif(opcion == 'h'):
            main_apuestas(diccionario_equipos, usuario)
        
        menu_principal(usuario)
        print("Ingrese una opción del menú: ", end="")
        opcion = validador_str(input_alfa(), ["a","b","c","d","e","f","g","h","i"])
    os.system("cls")
    print("Saliste de la Aplicación")
    print("-"*34)
    print(f"Hasta la próxima {[*usuario.values()][0][0]}!\nGracias por apostar con Jugársela!")
    print("-"*34)
    input("")

main()