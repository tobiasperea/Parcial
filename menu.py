import os  
import datetime
from funciones import *

if lista_elementos: 
    for i in range(len(lista_elementos)):

        id_auto_incremental = (i +1)
else:
    id_auto_incremental = 0



def incrementar_id():
    global id_auto_incremental
    id_auto_incremental +=1
    
def decrementar_id():
    global id_auto_incremental
    id_auto_incremental +=-1

def imprimir_menu ():
    
    print("Menu Principal\n\n1)Ingresar proyecto\n2)Modificar proyecto\n3)Cancelar proyecto\n4)Comprobar proyecto\n5)Mostrar todos\n6)Calcular presupuesto promedio\n7)Buscar proyecto por nombre\n8)Ordenar proyectos\n9)Retomar proyecto\n10)Generar reporte\n11)Generar reporte segun proyecto\n12)Mostrar proyectos finalizados en pandemia\n13)Mostrar proyectos que duren menos de 3 anios\n14)Salir")

def menu ():
    while (True):
        imprimir_menu()
        opcion = ingresar_entero("Elija una opcion:")
        match opcion:
            case 1:
                incrementar_id()
                if agregar_proyecto(id_auto_incremental,lista_elementos):
                    print("SE DIO DE ALTA")
                    
                else:
                    decrementar_id()
                mostrar_proyectos(lista_elementos)
            case 2: 

                modificar_proyecto(lista_elementos)
            case 3:
                cancelar_proyecto(lista_elementos)
                mostrar_proyectos(lista_elementos)
            case 4: 
                comprobar_proyecto(lista_elementos)
            case 5:
                mostrar_proyectos(lista_elementos)
            case 6: 
                calcular_presupuesto_promedio(lista_elementos)
            case 7:
                busqueda_por_nombre(lista_elementos)
            case 8:
                ordenar()
            case 9: 
                volver_activar_proyecto(lista_elementos)
                mostrar_proyectos(lista_elementos)
            case 10:
                presupuesto = ingresar_entero("Ingrese un presupuesto:")
                generar_reporte(lista_elementos,presupuesto)
            case 11:
                mostrar_proyectos(lista_elementos)
                nombre_proyecto = ingresar_str("Ingrese el nombre del proyecto:")
                generar_reporte_nombre_proyecto(lista_elementos,nombre_proyecto)
            case 12:
                lista_finalizados_en_pandemia = guardar_proyectos_finalizados_pandemia(lista_elementos)
                mostrar_proyectos(lista_finalizados_en_pandemia)
            case 13:
                lista_proyectos_corta_duracion = guardar_proyectos_segun_duracion(lista_elementos)
                mostrar_proyectos(lista_proyectos_corta_duracion)

            case 14:
                generar_csv("Proyectos.csv",lista_elementos)
                lista_finalizados = guardar_proyectos_finalizados(lista_elementos)
                convertir_fechas_str(lista_finalizados)
                generar_json("ProyectosFinalizados.json",lista_finalizados)
                break


menu()