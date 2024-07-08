import os 
import json
import csv
from datetime import datetime




def archivo_csv_vacio(nombre_archivo):
    return os.stat(nombre_archivo).st_size == 0

def parse_csv(nombre_archivo:str) -> list:
    """Esta funcion parsea un archivo .csv"""
    lista_elementos = []

    if not os.path.exists(nombre_archivo) or archivo_csv_vacio(nombre_archivo):
        print(f"El archivo '{nombre_archivo}' está vacío o no existe.")
        return lista_elementos
    
    with open(nombre_archivo, "r") as archivo:
        primer_linea = archivo.readline()
        primer_linea = primer_linea.replace("\n", "")
        lista_claves = primer_linea.split(",")
        
        for linea in archivo:
            linea_aux = linea.replace("\n", "")
            lista_valores = linea_aux.split(",")
            diccionario_aux = {}
            
            for i in range(len(lista_claves)):
                diccionario_aux[lista_claves[i]] = lista_valores[i]
            
            lista_elementos.append(diccionario_aux)
    
    return lista_elementos



def normalizar_id (lista_elementos:list):
    """Esta funcion convierte en entero las id de la lista anterior"""
    datos_modificados = False
    for proyectos in lista_elementos:
        if type(proyectos["id"]) == str:
            proyectos["id"] = int(proyectos["id"])
            
            datos_modificados=True
        
    return datos_modificados


def normalizar_presupuesto(lista_elementos:list):
    """Esta funcion convierte en Entero los presupuestos"""
    datos_modificados: False
    for proyecto in lista_elementos:
       if type(proyecto["Presupuesto"])== str:
           valor_clave = int(proyecto["Presupuesto"])
           proyecto["Presupuesto"] = valor_clave
           datos_modificados = True
    
    return datos_modificados
   


def normalizar_fechas(lista_elementos: list):
    """Esta funcion convierte las fechas en formato date"""
    for proyecto in lista_elementos:
        fecha_inicio = datetime.strptime(proyecto["Fecha de inicio"], "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(proyecto["Fecha de Fin"], "%Y-%m-%d").date()
        proyecto["Fecha de inicio"] = fecha_inicio
        proyecto["Fecha de Fin"] = fecha_fin



lista_elementos = parse_csv("Proyectos.csv")
if lista_elementos:
    normalizar_id(lista_elementos)
    normalizar_presupuesto(lista_elementos)
    normalizar_fechas(lista_elementos)




def ingresar_str (mensaje:str):
    """Esta funcion ingresa un string"""
    
    dato = input(mensaje)
    dato = dato
    
    return dato

def ingresar_entero (mensaje:str):
    """Esta funcion ingresa un entero"""
    dato = int(input(mensaje))
   
        
    
    return dato
    

def validar_nombre_proyecto()->str:
    """Esta funcion valida el nombre de un proyecto"""
    nombre = ingresar_str("Ingrese el nombre del proyecto")
    while len(nombre) == 0 or len(nombre) > 30 and (nombre.isalpha()):
        nombre = ingresar_str("Error, reingrese el nombre del proyecto")
    
    
    
    return nombre



def validar_descripcion_proyecto ()-> str:
    """Esta funcion valida la descripcion de un proyecto"""
    descripcion = ingresar_str("Ingresar descripcion del proyecto")
    while len(descripcion) == 0 or len(descripcion) > 200 and (descripcion.isalnum()):
        descripcion = ingresar_str("Error,reingrese la descripcion")
    
   
    
    return descripcion

def validar_presupuesto_proyecto ()-> int:
    """Esta funcion valida el presupuesto de un proyecto"""
    presupuesto = ingresar_entero("Ingrese el presupuesto")
    while presupuesto < 500000 :
        presupuesto = ingresar_entero("Error, reingrese el presupuesto")
    
    return presupuesto






def ingresar_fecha():
    """Esta función ingresa una fecha"""
    while True:
        try:
            dia = int(input("Ingrese el día: "))
            mes = int(input("Ingrese el mes: "))
            anio = int(input("Ingrese el año: "))

            fecha = datetime(anio, mes, dia)
            return fecha

        except ValueError:
            print("Error: Ingrese una fecha válida (dd-mm-yyyy).")

    

def confirmar(mensaje:str,mensaje_error:str):
    """Esta funcion da un mensaje de confirmacion S O N"""
    confirmacion = input(mensaje)
    confirmacion = confirmacion.upper()
    retorno = False
    
    while confirmacion != "S" and confirmacion != "N":
        confirmacion = input(mensaje_error)
        confirmacion = confirmacion.upper()
        
    if confirmacion == "S":
        retorno = True

    return retorno

def mostrar_proyectos(lista_elementos:list):
    """Esta funcion muestra los proyectos"""
    if lista_elementos:
        informacion = "Proyecto\nID | NOMBRE DEL PROYECTO | DESCRIPCION | FECHA DE INICIO | FECHA DE FIN | PRESUPUESTO | ESTADO\n"
        for proyecto in lista_elementos:
            for clave in proyecto:
                informacion += str(proyecto[clave]) + " | "
        
            informacion += "\n" 
        print(informacion)
    else:
        print("No hay proyectos")


def mostrar_proyecto(proyecto:dict):
    """Esta funcion muestra un proyecto pasado por parametro"""
    informacion = "Proyecto\nID | NOMBRE DEL PROYECTO | DESCRIPCION | FECHA DE INICIO | FECHA DE FIN | PRESUPUESTO | ESTADO\n"
    for clave in proyecto:
        informacion += str(proyecto[clave]) + " | "
    
    print(informacion)

def buscar_proyecto(lista_elementos:list,id_a_buscar):
    """Esta funcion busca un proyecto en una lista mediante un id que se pasa por parametro"""
    retorno = None

    for i in range(len(lista_elementos)):
        if lista_elementos[i]["id"]== id_a_buscar:
            print("SE ENCONTRO EL PROYECTO")
            mostrar_proyecto(lista_elementos[i])
            retorno = i
            
            break
    
    return retorno

def contador_proyectos_activos(lista_elementos:list)->bool:
    """Esta funcion cuenta los proyectos activos"""
    cantidad_activos = 0
    for i in range (len(lista_elementos)):
        if lista_elementos[i]["Estado"] == "Activo":
            cantidad_activos += 1
    
    return cantidad_activos


def agregar_proyecto(id_auto_incremental: int, lista_elementos: list) -> bool:
    """Esta función agrega un proyecto a la lista"""
    retorno = False
    if contador_proyectos_activos(lista_elementos) < 50:
        
        nombre_proyecto = validar_nombre_proyecto()
        descripcion_proyecto = validar_descripcion_proyecto()
        
        print("Ingrese la fecha de inicio")
        fecha_inicio = ingresar_fecha()
        
        print("Ingrese la fecha de fin")
        fecha_fin = ingresar_fecha()

        while fecha_fin <= fecha_inicio:
            print("La fecha de fin no puede ser anterior a la fecha de inicio, ingrese la fecha de fin")
            fecha_fin = ingresar_fecha()

        presupuesto_proyecto = validar_presupuesto_proyecto()
        estado_proyecto = "Activo"

        proyecto = {
            "id": id_auto_incremental,
            "Nombre del Proyecto": nombre_proyecto,
            "Descripcion": descripcion_proyecto,
            "Fecha de inicio": fecha_inicio.date(),  
            "Fecha de Fin": fecha_fin.date(),  
            "Presupuesto": presupuesto_proyecto,
            "Estado": estado_proyecto
        }

        mostrar_proyecto(proyecto)
        
        if confirmar("¿Quiere dar de alta este proyecto (S/N)?", "Error, debe elegir entre (S o N)"):
            lista_elementos.append(proyecto)
            retorno = True
        else:
            print("Se canceló el alta de proyecto")
            
    else:
        print("Cambie el estado de algún proyecto para agregar otro")    
    return retorno



def modificar_proyecto(lista_elementos: list):
    """Esta función modifica un proyecto ya existente"""
    retorno = "Modificación errónea"
    mostrar_proyectos(lista_elementos)

    id_a_modificar = ingresar_entero("Ingrese el ID del proyecto a modificar: ")
    indice = buscar_proyecto(lista_elementos, id_a_modificar)

    if indice is not None:
        while True:
            print("\nOpciones de modificación:\n"
                  "1. Nombre del proyecto\n"
                  "2. Descripción\n"
                  "3. Fecha de inicio\n"
                  "4. Fecha de fin\n"
                  "5. Presupuesto\n"
                  "6. Salir\n")

            opcion = ingresar_entero("Seleccione la opción que desea modificar: ")

            if opcion == 6:
                break

            if opcion == 1:
                nombre_proyecto = validar_nombre_proyecto()
                lista_elementos[indice]["Nombre del Proyecto"] = nombre_proyecto
            elif opcion == 2:
                nueva_descripcion = validar_descripcion_proyecto()
                lista_elementos[indice]["Descripcion"] = nueva_descripcion  
            elif opcion == 3:
                print("Ingrese la nueva fecha de inicio")
                fecha_inicio = ingresar_fecha()
                while fecha_inicio > lista_elementos[indice]["Fecha de Fin"]:
                    print("La fecha de inicio no puede ser posterior a la fecha de fin, ingrese la fecha de inicio nuevamente")
                    fecha_inicio = ingresar_fecha()
                lista_elementos[indice]["Fecha de inicio"] = fecha_inicio
            elif opcion == 4:
                print("Ingrese la nueva fecha de fin")
                fecha_fin = ingresar_fecha()
                while fecha_fin < lista_elementos[indice]["Fecha de inicio"]:
                    print("La fecha de fin no puede ser anterior a la fecha de inicio, ingrese la fecha de fin nuevamente")
                    fecha_fin = ingresar_fecha()
                lista_elementos[indice]["Fecha de Fin"] = fecha_fin
            elif opcion == 5:
                presupuesto_proyecto = validar_presupuesto_proyecto()
                lista_elementos[indice]["Presupuesto"] = presupuesto_proyecto
            else:
                print("Opción no válida, intente de nuevo")

            mostrar_proyecto(lista_elementos[indice])

            if not confirmar("¿Desea realizar otra modificación? (S/N)", "Error, ¿desea realizar otra modificación? (S/N)"):
                break

        retorno = "Modificación realizada"
    else:
        print("No se encontró ningún proyecto con ese ID")

    return retorno


def cancelar_proyecto(lista_elementos:list):
    """Esta función cambia el estado de un proyecto a cancelado solo si está activo."""
    while True:
        opcion = ingresar_entero("Ingrese opción\n1)Para cancelar proyectos\n2)Para salir")
        match opcion:
            case 1:
                retorno = "Cancelación errónea"
                mostrar_proyectos(lista_elementos)

                id_a_cancelar = ingresar_entero("Ingrese el ID del proyecto a cancelar")
                indice = buscar_proyecto(lista_elementos, id_a_cancelar)

                if indice is not None:
                    proyecto = lista_elementos[indice]
                    if proyecto["Estado"] == "Activo":
                        if confirmar("¿Desea cancelar este proyecto (S/N)?", "Error, ¿desea cancelar este proyecto (S/N)?"):
                            lista_elementos[indice]["Estado"] = "Cancelado"
                            retorno = "Proyecto cancelado"
                        else:
                            retorno = "Cancelación cancelada"
                    else:
                        print("ERROR---Solo se pueden cancelar proyectos activos.")
                else:
                    print("No se encontró el proyecto con el ID especificado.")
            case 2:
                retorno = "cancelacion cancelada"
                break

    return retorno


def comprobar_proyecto(lista_elementos: list):
    """Comprueba que las fechas de fin de los proyectos sean correctas"""
    retorno = "Todas las fechas están en orden"
   
    fecha_hoy = datetime.now().date()  
    for proyecto in lista_elementos:
        if proyecto["Fecha de Fin"] <= fecha_hoy:
            proyecto["Estado"] = "Finalizado"
            retorno = "Proyecto finalizado"
    
    mostrar_proyectos(lista_elementos)
    return retorno




def acumulador_presupuesto(lista_elementos:list) -> int:
    """Esta función suma y acumula los presupuestos de los proyectos"""
    presupuesto_acumulado = 0
    for proyecto in lista_elementos:
        presupuesto_acumulado += int(proyecto["Presupuesto"])
    return presupuesto_acumulado

def calcular_presupuesto_promedio(lista_elementos:list) -> str:
    """Esta función calcula el promedio de los presupuestos"""
    if not lista_elementos:
        return "No hay proyectos disponibles para calcular el promedio de presupuestos."

    presupuesto_acumulado = acumulador_presupuesto(lista_elementos)
    cantidad_proyectos = len(lista_elementos)

    promedio = presupuesto_acumulado / cantidad_proyectos
    mensaje = print(f"El promedio de presupuestos es {promedio}")

    return mensaje

    
def mostrar_nombres_proyectos(lista_elementos: list):
    """Esta función muestra los nombres de todos los proyectos"""
    print("Proyectos disponibles:")
    for proyecto in lista_elementos:
        print(proyecto["Nombre del Proyecto"])

def busqueda_por_nombre(lista_elementos: list) -> bool:
    """Esta función busca un proyecto en una lista por su nombre"""
    retorno = None
    
    
    mostrar_nombres_proyectos(lista_elementos)
    
    nombre_a_buscar = ingresar_str("Ingrese el nombre del proyecto")
    for proyecto in lista_elementos:
        if proyecto["Nombre del Proyecto"] == nombre_a_buscar:
            print("Se encontró el proyecto")
            mostrar_proyecto(proyecto)
            retorno = True
            break  
    
    if not retorno:
        print("No se encontró ningún proyecto con ese nombre.")
    
    return retorno

def ordenar_por_nombre(lista_elementos:list):
    """Esta funcion ordena por nombre segun se le indique"""
    retorno = False

    
    if confirmar("Desea ordenar de la A a la Z (S/N)","Error, desea ordenar de la A a la Z (S/N)"):
        for i in range (len(lista_elementos)):
            for j in range (i+1,len(lista_elementos),1):
                if lista_elementos[i]["Nombre del Proyecto"] > lista_elementos[j]["Nombre del Proyecto"]:
                    aux = lista_elementos[i]
                    lista_elementos[i] = lista_elementos[j]
                    lista_elementos[j] = aux
        retorno = True
    elif confirmar("Desea ordenar de la Z a la A (S/N)","Error, desea ordenar de la Z a la A (S/N)"):
        for i in range (len(lista_elementos)):
            for j in range (i+1,len(lista_elementos),1):
                if lista_elementos[i] < lista_elementos[j]["Nombre del Proyecto"]:
                    aux = lista_elementos[i]
                    lista_elementos[i] = lista_elementos[j]
                    lista_elementos[j] = aux
        retorno = True
    
    return retorno

def ordenar_por_presupuesto (lista_elementos:list):
    """Esta funcion ordena la lista por los presupuestos segun se le indique"""
    retorno = False

    if confirmar ("Desea ordenar de menor a mayor (S/N)","Error, desea ordenar de menor a mayor (S/N)"):
        for i in range (len(lista_elementos)):
            for j in range (i+1,len(lista_elementos),1):
                if lista_elementos[i]["Presupuesto"] > lista_elementos[j]["Presupuesto"]:
                    aux = lista_elementos[i]
                    lista_elementos[i]= lista_elementos[j]
                    lista_elementos[j] = aux
        retorno = True
    
    elif confirmar ("Desea ordenar de mayor a menor (S/N)","Error, desea ordenar de mayor a menor (S/N)"):
        for i in range (len(lista_elementos)):
            for j in range (i+1,len(lista_elementos),1):
                if lista_elementos[i]["Presupuesto"] < lista_elementos[j]["Presupuesto"]:
                    aux = lista_elementos[i]
                    lista_elementos[i] = lista_elementos[j]
                    lista_elementos[j] = aux
        retorno = True

    return retorno 

def ordenar_por_fechas (lista_elementos:list):
    """Esta funcion ordena la lista por las fechas segun se le indique"""

    retorno = False
    if confirmar("Desea ordenar la lista por orden de las fechas de inicio (S/N)","Error, desea ordenar por orden de las fecha de inicio(S/N)"):
        for i in range (len(lista_elementos)):
            for j in range (i+1,len(lista_elementos),1):
                if lista_elementos[i]["Fecha de inicio"] > lista_elementos[j]["Fecha de inicio"]:
                    aux = lista_elementos[i]
                    lista_elementos[i]= lista_elementos[j]
                    lista_elementos[j] = aux
        retorno = True
        
    elif confirmar("Desea ordenar la lista por orden de las fechas de fin (S/N)","Error, Desea ordenar las listas por orden de las fechas de fin"):
        for i in range (len(lista_elementos)):
            for j in range (i+1,len(lista_elementos),1):
                if lista_elementos[i]["Fecha de Fin"] < lista_elementos[j]["Fecha de Fin"]:
                    aux = lista_elementos[i]
                    lista_elementos[i]= lista_elementos[j]
                    lista_elementos[j] = aux
        retorno = True

    return retorno

def ordenar ():
    """Esta funcion da un menu que ordena la lista segun se le indique"""
    opcion= ingresar_entero("Ingrese su opcion\n1)Para ordenar por nombre\n2)Para ordenar por presupuesto\n3)Para ordenar por fechas\n4)Paracancelar\nIngrese su opcion:")
    match opcion:
        case 1:
            ordenar_por_nombre(lista_elementos)
        case 2:
            ordenar_por_presupuesto(lista_elementos)
        case 3: 
            ordenar_por_fechas(lista_elementos)
        case 4:
            print("Ordenamiento cancelado")
    
    mostrar_proyectos(lista_elementos)

def volver_activar_proyecto(lista_elementos:list):
    """Esta función cambia el estado de un proyecto a activo solo si está cancelado."""
    retorno = "Alta errónea"
    while True:
        opcion = ingresar_entero("Ingrese opción\n1)Para dar de alta proyectos\n2)Para salir")
        match opcion:
            case 1:
                mostrar_proyectos(lista_elementos)

                id_a_dar_alta = ingresar_entero("Ingrese el ID del proyecto a dar de alta")

                indice = buscar_proyecto(lista_elementos, id_a_dar_alta)

                if indice is not None:
                    proyecto = lista_elementos[indice]
                    if proyecto["Estado"] == "Cancelado":
                        if confirmar("¿Desea dar de alta a este proyecto (S/N)?", "Error, ¿desea dar de alta este proyecto (S/N)?"):
                            lista_elementos[indice]["Estado"] = "Activo"
                            retorno = "Alta realizada"
                        else:
                            retorno = "Alta cancelada"
                    else:
                        print("Solo se pueden activar proyectos cancelados.")
                else:
                    print("No se encontró el proyecto con el ID especificado.")
            case 2:
                retorno = "Alta cancelada"
                break

    return retorno
            
            
    
   

def generar_csv(nombre_archivo:str,lista:list):
    """Genera un csv y actualiza el archivo"""
    if len(lista) > 0:
        lista_claves = list(lista[0].keys())
        separador = ","
        cabecera = separador.join(lista_claves)
        print(cabecera)
        
        with open(nombre_archivo,"w") as archivo:
            archivo.write(cabecera + "\n")
            for elemento in lista:
                lista_valores = list(elemento.values())
                for i in range(len(lista_valores)):
                    lista_valores[i] = str(lista_valores[i])

                dato = separador.join(lista_valores)
                dato += "\n"
                archivo.write(dato)
    else:
        print("ERROR LISTA VACIA")

def guardar_proyectos_finalizados (lista_elementos:list)->list:
    """Esta funcion devuelve la lista de los proyectos finalizados"""
    lista_finalizados = []
    for proyecto in lista_elementos:
        if proyecto["Estado"] == "Finalizado":
            lista_finalizados.append(proyecto)
    
    return lista_finalizados






def convertir_fechas_str(lista_elementos: list):
    """Convierte los campos de fecha en formato string para ser serializados en JSON"""
    for proyecto in lista_elementos:
        if isinstance(proyecto["Fecha de inicio"], datetime):
            proyecto["Fecha de inicio"] = proyecto["Fecha de inicio"].strftime("%d-%m-%Y")
        if isinstance(proyecto["Fecha de Fin"], datetime):
            proyecto["Fecha de Fin"] = proyecto["Fecha de Fin"].strftime("%d-%m-%Y")

def generar_json(nombre_archivo: str, lista: list):
    """Genera un archivo JSON con la lista de proyectos finalizados"""
    convertir_fechas_str(lista)
    with open(nombre_archivo, "w") as archivo:
        json.dump(lista, archivo, default=str, indent=4)




def guardar_proyectos_finalizados_pandemia(lista_elementos: list) -> list:
    """Esta función devuelve la lista de los proyectos finalizados en la pandemia"""
    proyectos_finalizados_pandemia = []
    fecha_inicio_pandemia = datetime(2020, 3, 1).date()
    fecha_final_pandemia = datetime(2021, 12, 31).date()

    for proyecto in lista_elementos:
        if proyecto["Estado"] == "Finalizado":
            fecha_finalizacion_proyecto = proyecto["Fecha de Fin"]  
            if fecha_inicio_pandemia <= fecha_finalizacion_proyecto <= fecha_final_pandemia:
                proyectos_finalizados_pandemia.append(proyecto)
    
    return proyectos_finalizados_pandemia


def calcular_años(fecha_inicio: datetime, fecha_fin: datetime) -> float:
    """Calcula los años entre las fechas de inicio y fin."""
    tiempo = fecha_fin - fecha_inicio
    años = tiempo.days / 365
    return años

def guardar_proyectos_segun_duracion(lista_elementos: list) -> list:
    """Devuelve los proyectos finalizados con menos de 3 años de duración."""
    proyectos_corta_duracion = []
    
    for proyecto in lista_elementos:
        if proyecto["Estado"] == "Finalizado":
            fecha_inicio = proyecto["Fecha de inicio"]
            fecha_fin = proyecto["Fecha de Fin"]
            
            if fecha_inicio and fecha_fin:  
                años = calcular_años(fecha_inicio, fecha_fin)
                if años < 3:
                    proyectos_corta_duracion.append(proyecto)
            else:
                print(f"Advertencia: Proyecto con ID {proyecto['id']} tiene fechas inválidas.")
    
    return proyectos_corta_duracion


def generar_reporte(lista_elementos: list, presupuesto: float):
    """Genera un reporte de los proyectos que superen el presupuesto dado."""
   
    proyectos_superan_presupuesto = [proyecto for proyecto in lista_elementos if proyecto["Presupuesto"] > presupuesto]
    
    
    cantidad_proyectos = len(proyectos_superan_presupuesto)
    
    
    if not any(fname.startswith("reporte_") for fname in os.listdir() if fname.endswith(".txt")):
        numero_reporte = 0
    else:
        
        if os.path.exists("contador_reporte.txt"):
            with open("contador_reporte.txt", "r") as archivo:
                numero_reporte = int(archivo.read().strip())
        else:
            numero_reporte = 0

    
    numero_reporte += 1

    
    with open("contador_reporte.txt", "w") as archivo:
        archivo.write(str(numero_reporte))

    
    fecha_solicitud = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    nombre_reporte = f"reporte_{numero_reporte}.txt"

    
    contenido_reporte = f"Reporte Numero: {numero_reporte}\n"
    contenido_reporte += f"Fecha de Solicitud: {fecha_solicitud}\n"
    contenido_reporte += f"Cantidad de Proyectos que Superan el Presupuesto: {cantidad_proyectos}\n"
    contenido_reporte += "Listado de Proyectos:\n\n"
    
    for proyecto in proyectos_superan_presupuesto:
        contenido_reporte += (
            f"ID: {proyecto['id']}, Nombre: {proyecto['Nombre del Proyecto']}, Descripcion: {proyecto['Descripcion']}, "
            f"Fecha de Inicio: {proyecto['Fecha de inicio']}, Fecha de Fin: {proyecto['Fecha de Fin']}, "
            f"Presupuesto: {proyecto['Presupuesto']}, Estado: {proyecto['Estado']}\n"
        )
    
    
    with open(nombre_reporte, "w") as archivo:
        archivo.write(contenido_reporte)
    
    print(f"Reporte guardado en '{nombre_reporte}'")





def generar_reporte_nombre_proyecto(lista_elementos: list, nombre_proyecto: str):
    """Genera un informe de los proyectos que superan el presupuesto del proyecto con el nombre ingresado."""
    
    presupuesto_proyecto = None
    for proyecto in lista_elementos:
        if proyecto["Nombre del Proyecto"].lower() == nombre_proyecto.lower():
            presupuesto_proyecto = proyecto["Presupuesto"]
            break
    
    if presupuesto_proyecto is None:
        print(f"No se encontró ningún proyecto con el nombre '{nombre_proyecto}'.")
        return

    
    proyectos_superan_presupuesto = [proyecto for proyecto in lista_elementos if proyecto["Presupuesto"] > presupuesto_proyecto]

    
    if not any(fname.startswith("informe_nombre_") for fname in os.listdir() if fname.endswith(".txt")):
        numero_informe = 0
    else:
        
        if os.path.exists("contador_informe_nombre.txt"):
            with open("contador_informe_nombre.txt", "r") as archivo:
                numero_informe = int(archivo.read().strip())
        else:
            numero_informe = 0

    
    numero_informe += 1

    
    with open("contador_informe_nombre.txt", "w") as archivo:
        archivo.write(str(numero_informe))

    
    fecha_solicitud = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    nombre_informe = f"informe_nombre_{numero_informe}.txt"

    
    contenido_informe = f"Informe Numero: {numero_informe}\n"
    contenido_informe += f"Fecha de Solicitud: {fecha_solicitud}\n"
    contenido_informe += f"Cantidad de Proyectos que Superan el Presupuesto de '{nombre_proyecto}': {len(proyectos_superan_presupuesto)}\n"
    contenido_informe += "Listado de Proyectos:\n\n"
    
    for proyecto in proyectos_superan_presupuesto:
        contenido_informe += (
            f"ID: {proyecto['id']}, Nombre: {proyecto['Nombre del Proyecto']}, Descripcion: {proyecto['Descripcion']}, "
            f"Fecha de Inicio: {proyecto['Fecha de inicio']}, Fecha de Fin: {proyecto['Fecha de Fin']}, "
            f"Presupuesto: {proyecto['Presupuesto']}, Estado: {proyecto['Estado']}\n"
        )
    
    
    with open(nombre_informe, "w") as archivo:
        archivo.write(contenido_informe)
    
    print(f"Informe guardado en '{nombre_informe}'")