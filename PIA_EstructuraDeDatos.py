from collections import namedtuple
import csv
import sqlite3
import sys
from sqlite3 import Error
from datetime import datetime


Datos = namedtuple("Ventas",("descripcion", "cantidad_pzas","precio_venta", "fecha"))
lista_ventas = []
diccionario_ventas = {}

fecha_actual = datetime.today()
total = 0
while True:
    print("\n\tLlantas Michelin")
    print("Bienvenido al programa por favor elige una opcion: \n")
    print("\t1) Registrar una venta")
    print("\t2) Busqueda por fecha")
    print("\t3) Salir")
    print("\nPuede ingresar la opcion mediante \nel teclado numerico")
    respuesta = int(input("Elija una opción: "))
    
    if respuesta == 1:
        lista_ventas = []
        while True:
            folio = int(input('\nIngrese el folio de la venta: '))
            try:
                with sqlite3.connect("PIADB.db") as conn:
                    mi_cursor = conn.cursor()
                    mi_cursor.execute("SELECT folio FROM FechaID WHERE folio = ?",(folio,))
                    comprobacion_folio = mi_cursor.fetchall()
                    if comprobacion_folio:
                        print('\nEsta clave ya existe, porfavor ingresa otra')
                    else:
                        break
            except Error as e:
                print(e)
            except Exception:
                print(f"Error: {sys.exc_info()[0]}")
            finally:
                if conn:
                    conn.close()
        while True:
            print("\nPor favor, ingrese la fecha de la venta")
            print("El formato para ingresar la fecha de la venta, es el siguiente:")
            print("\tDIA/MES/AÑO\nEjemplo: 12/10/20")
            try:
                fecha_venta = input('\nIngrese la fecha de venta: ')
                fecha_venta_convertido = datetime.strptime(fecha_venta, '%d/%m/%y')
                if fecha_venta_convertido < fecha_actual:
                    break
                else:
                    print(f"\nFecha no valida!, porfavor ingrese otra.")
            except Exception:
                print("\nPor favor, ingresa un formato valido!\n")
        while True:
            # Insercion de datos
            while True:
                descripcion = input(f'\nIngrese la descripcion de la llanta: ')
                cantidad_pzas = input('Ingrese la cantidad de piezas a comprar: ')
                precio_venta = input('Ingrese el precio unitario de cada pieza: ')
                
                if descripcion.replace(" ","") != "" and cantidad_pzas != 0 and precio_venta != 0:
                    break
                else:
                    print("\nPor favor, no ingrese datos vacios, o coloque 0")
            
            print("-----------------------------------------------------------\n")
            # Lista
            ventas = Datos(descripcion,cantidad_pzas, precio_venta, fecha_venta)
            lista_ventas.append(ventas)
            
            # Diccionario
            diccionario_ventas[folio] = lista_ventas
            
            # Seguir agregando
            respuesta1 = int(input('¿Quieres seguir agregando productos?\n\t 1: Si\n\t 2: No\n\t'))
            
            # En caso de que no quiera seguir agregando
            if (respuesta1 != 1):
                total_ventas = 0
                # Cargado de datos a sqlite3
                try:
                    with sqlite3.connect("PIADB.db") as conn:
                        mi_cursor = conn.cursor()
                        for folio in diccionario_ventas:
                            for items in diccionario_ventas[folio]:
                                mi_cursor.execute(f"SELECT * FROM FechaID WHERE folio = ?",(folio,))
                                registro1 = mi_cursor.fetchall()
                                if registro1:
                                    pass
                                else:
                                    mi_cursor.execute(f"INSERT INTO FechaID VALUES(?, ?);",(folio, items.fecha))
                                mi_cursor.execute(f"INSERT INTO Venta VALUES(?, ?, ?, ?);",(folio, items.descripcion, items.cantidad_pzas, items.precio_venta))
                except Error as e:
                    print(e)
                except Exception:
                    print(f"Error: {sys.exc_info()[0]}")
                finally:
                    if conn:
                        conn.close()
                for items in diccionario_ventas[folio]:
                    total_ventas = (int(items.precio_venta) * int(items.cantidad_pzas)) + total_ventas
                print(f"Total de las ventas: ${total_ventas:,.2f}")
                print(f"El iva aplicable es de: ${total_ventas * .16:,.2f}")
                print(f"El total con iva aplicado es de: ${total_ventas*1.16:,.2f}")
                break

    elif respuesta == 2:
        total = 0
        while True:
            print("\nEl formato para ingresar la fecha, es el siguiente:")
            print("\tDIA/MES/AÑO\nEjemplo: 12/10/20")
            try:
                busqueda = input('\nIngrese la fecha a buscar: ')
                fecha_venta_convertido = datetime.strptime(busqueda, '%d/%m/%y')
                if fecha_venta_convertido < fecha_actual:
                    break
                else:
                    print(f"\nFecha no valida!, porfavor ingresa otra.")
            except Exception:
                print("\nPor favor, ingresa un formato valido!")
        try:
            with sqlite3.connect("PIADB.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("""SELECT fechaID.folio, Venta.descripcion, Venta.canitdad, Venta.precio, fechaID.fecha \
                                    FROM FechaID\
                                    INNER JOIN Venta on FechaID.folio = Venta.folio\
                                    WHERE FechaID.fecha = ?""",(busqueda,))
                resultados = mi_cursor.fetchall()
                if resultados:
                    print("Folio\tDescripcion\tCantidad\tPrecio\tFecha")
                    for folio, descripcion, cantidad, precio, fecha in resultados:
                        print(f"{folio}\t{descripcion}\t{cantidad}\t\t{precio}\t{fecha}")
                        total = (precio * cantidad) + total
                    print(f"Total de las ventas: ${total:,.2f}")
                    print(f"El iva aplicable es de: ${total * .16:,.2f}")
                    print(f"El total con iva aplicado es de: ${total*1.16:,.2f}")
                else:
                    print("\nLa fecha solicitada no existe")
                
        except Error as e:
            print(e)
        except Exception:
            print(f"Error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()
#         print("{0:<10} {1:<20} {2:<20} {3:<20} {4:<20}".format("Folio","Descripcion","Cantidad","Precio Unitario","Fecha"))         
#         total_ventas = 0
#         total_ventas = (int(items.precio_venta) * int(items.cantidad_pzas)) + total_ventas
#         print(f"Total de las ventas: {total_ventas}")
#         print(f"El iva aplicable es de: {total_ventas * .16}")
#         print(f"El total con iva aplicado es de: {round(total_ventas*1.16, 2)}")

    elif respuesta == 3:
        print("Finalizando")
        break
    else:
        print("\n°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        print("°Ingrese una opcion valida°")
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°")