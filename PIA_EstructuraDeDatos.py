from collections import namedtuple
import csv
import sqlite3
import sys
from sqlite3 import Error
import datetime
from datetime import datetime
from datetime import timedelta

Datos = namedtuple("Ventas",("descripcion", "cantidad_pzas","precio_venta", "fecha"))
lista_ventas = []
diccionario_ventas = {}
today = datetime.today()
fecha_actual = today.strftime("%d/%m/%y")
total = 0
folioActualizado = 1
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
        try:
            with sqlite3.connect("PIADB.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT count(folio), fecha FROM FechaID;")
                registro = mi_cursor.fetchall()
                if registro:
                    for folio, fecha in registro:
                        folioActualizado = folio + 1
        except Error as e:
                print(e)
        except Exception:
            print(f"Error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()            
        while True:
            # Insercion de datos
            while True:
                try:
                    descripcion = input(f'\nIngrese la descripcion de la llanta: ')
                    cantidad_pzas = int(input('Ingrese la cantidad de piezas a comprar: '))
                    precio_venta = int(input('Ingrese el precio unitario de cada pieza: '))
                    
                    if descripcion.replace(" ","") != "" and cantidad_pzas != 0 and precio_venta != 0:
                        break
                    else:
                        print("\nPor favor, no ingrese datos vacios, o coloque 0's")
                except Exception:
                    print("Porfavor, ingrese en los campos, el formato correcto")
            print("-----------------------------------------------------------\n")
            # Lista
            ventas = Datos(descripcion,cantidad_pzas, precio_venta, fecha_actual)
            lista_ventas.append(ventas)
            # Diccionario
            diccionario_ventas[folioActualizado] = lista_ventas
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
                NextDay_Date = datetime.today() + timedelta(days=1)
                if fecha_venta_convertido > NextDay_Date:
                    print(f"\nFecha no valida!, porfavor ingresa otra.")
                else:
                    break
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
    elif respuesta == 3:
        print("Finalizando")
        break
    else:
        print("\n°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        print("°Ingrese una opcion valida°")
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°")
