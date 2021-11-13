# Importacion de librerias
from collections import namedtuple
import sqlite3
import sys
from sqlite3 import Error
import datetime
from datetime import datetime
from datetime import timedelta

# Creacion de la tupla Ventas
Datos = namedtuple("Ventas",("descripcion", "cantidad_pzas","precio_venta", "fecha"))
#Creacion de la lista_ventas
lista_ventas = []
#Creacion diccionario ventas
diccionario_ventas = {}
#Fecha hoy
today = datetime.today()
fecha_actual = today.strftime("%d/%m/%y")
total = 0
folioActualizado = 1
# inicio del ciclo
while True:
    print("\n\tLlantas Michelin")
    print("Bienvenido al programa por favor elige una opcion: \n")
    print("\t1) Registrar una venta")
    print("\t2) Busqueda por fecha")
    print("\t3) Salir")
    print("\nPuede ingresar la opcion mediante \nel teclado numerico")
    respuesta = int(input("Elija una opción: "))
    # ----------------------------------------#
    if respuesta == 1:
        # Vaciamos la lista de ventas
        lista_ventas = []
        try:
            # Creamos la conexion, a la base, para crear el folio automatico
            with sqlite3.connect("PIADB.db") as conn:
                # guardamos la conexion en el cursor
                mi_cursor = conn.cursor()
                # contamos la cantidad de folios que hay en la tabla, junto con una fecha del folio
                mi_cursor.execute("SELECT count(folio), fecha FROM FechaID;")
                # guardamos en registro
                registro = mi_cursor.fetchall()
                # comprobamos si trajo registros
                if registro:
                    # por cada folio y fecha en registros
                    for folio, fecha in registro:
                        # le asignamos la cantidad de folios contabilizados
                        # y le sumamos uno, y lo guardamos en folio actualizado
                        folioActualizado = folio + 1
        except Error as e:
                print(e)
        except Exception:
            print(f"Error: {sys.exc_info()[0]}")
        # Si hubo o no huno ningun error, cerramos la conexion
        finally:
            if conn:
                conn.close()            
        while True:
            # Pedida de datos
            while True:
                try:
                    descripcion = input(f'\nIngrese la descripcion de la llanta: ')
                    cantidad_pzas = int(input('Ingrese la cantidad de piezas a comprar: '))
                    precio_venta = int(input('Ingrese el precio unitario de cada pieza: '))
                    # Comprobacion de que no sean datos vacios, o 0
                    if descripcion.replace(" ","") != "" and cantidad_pzas != 0 and precio_venta != 0:
                        break
                    else:
                        print("\nPor favor, no ingrese datos vacios, o coloque 0's")
                except Exception:
                    print("Porfavor, ingrese en los campos, el formato correcto")
            print("-----------------------------------------------------------\n")
            #---------------------------------------------------------------------------------------#
            # Lista
            ventas = Datos(descripcion,cantidad_pzas, precio_venta, fecha_actual)
            lista_ventas.append(ventas)
            # Diccionario
            diccionario_ventas[folioActualizado] = lista_ventas
            # Seguir agregando pregunta
            respuesta1 = int(input('¿Quieres seguir agregando productos?\n\t 1: Si\n\t 2: No\n\t'))
            # En caso de que no quiera seguir agregando
            if (respuesta1 != 1):
                total_ventas = 0
                # Cargado de datos a sqlite3
                try:
                    with sqlite3.connect("PIADB.db") as conn:
                        mi_cursor = conn.cursor()
                        # por cada folio en el diccionario ventas
                        for folio in diccionario_ventas:
                            # recorre cada item, en el diccionario, con el folio asignado
                            for items in diccionario_ventas[folio]:
                                # Generamos una consulta que verifique si ya existe el folio recorrido
                                # en la tabla
                                mi_cursor.execute(f"SELECT * FROM FechaID WHERE folio = ?",(folio,))
                                # guardamos el registro con la funcion fetchall
                                registro1 = mi_cursor.fetchall()
                                # en caso de que encontremos un registro, pasamos, y en caso de que no
                                # insertamos a la tabla los valores del folio y la fecha
                                if registro1:
                                    pass
                                else:
                                    mi_cursor.execute(f"INSERT INTO FechaID VALUES(?, ?);",(folio, items.fecha))
                                # al final, insertamos los datos que se encontraron en ese momento
                                mi_cursor.execute(f"""INSERT INTO Venta\
                                VALUES(?, ?, ?, ?);""",(folio, items.descripcion, items.cantidad_pzas, items.precio_venta))
                # En caso de error, los except se encargaran de agarrarlo
                except Error as e:
                    print(e)
                except Exception:
                    print(f"Error: {sys.exc_info()[0]}")
                finally:
                    # al final comprobamos si la conexion existe o no
                    if conn:
                        conn.close()
                # por cada item en el diccionario ventas, con el id del folio
                for items in diccionario_ventas[folio]:
                    # genera un total de ventas, llamado total_ventas
                    total_ventas = (int(items.precio_venta) * int(items.cantidad_pzas)) + total_ventas
                print(f"Total de las ventas: ${total_ventas:,.2f}")
                print(f"El iva aplicable es de: ${total_ventas * .16:,.2f}")
                print(f"El total con iva aplicado es de: ${total_ventas*1.16:,.2f}")
                break

    elif respuesta == 2:
        # Creamos una variable total, para mas a futuro
        total = 0
        # inicializamos un ciclo para preguntar la fecha
        while True:
            # Le indicamos el formato al usuario
            print("\nEl formato para ingresar la fecha, es el siguiente:")
            print("\tDIA/MES/AÑO\nEjemplo: 12/10/20")
            # colocamos el try, por si se ingresa mal el formato
            try:
                #Preguntamos la fecha a buscar
                busqueda = input('\nIngrese la fecha a buscar: ')
                # convertimos la fecha a tipo datetime
                fecha_venta_convertido = datetime.strptime(busqueda, '%d/%m/%y')
                # A la fecha de hoy, le sumamos un dia, para tener
                # la fecha del dia siguiente
                NextDay_Date = datetime.today() + timedelta(days=1)
                # Si la fecha a buscar es mayor a la actual, pero del dia siguiente
                # le mandamos el mensaje de la linea 135, en caso contrario
                # rompemos el ciclo
                if fecha_venta_convertido > NextDay_Date:
                    print(f"\nFecha no valida!, porfavor ingresa otra.")
                else:
                    break
            # utilizamos el except en caso de que el formato haya sido mal escrito
            except Exception:
                print("\nPor favor, ingresa un formato valido!")
        #-------------------------------------------------------------------------#
        # inicializamos try, para evitar errores
        try:
            # creamos la conexion a la base de datos
            with sqlite3.connect("PIADB.db") as conn:
                # creamos un cursor, para guardar la conexcion
                mi_cursor = conn.cursor()
                # hacemos una sentencia multitabla con inner join, donde comparamos la fecha buscada, con la fechas de la
                # tabla
                mi_cursor.execute("""SELECT fechaID.folio, Venta.descripcion, Venta.canitdad, Venta.precio, fechaID.fecha \
                                    FROM FechaID\
                                    INNER JOIN Venta on FechaID.folio = Venta.folio\
                                    WHERE FechaID.fecha = ?""",(busqueda,))
                # al final, recibimos el registro de las fechas encontradas
                resultados = mi_cursor.fetchall()
                # comprobamos que haya recibido fechas
                if resultados:
                    # en caso de que si, creamos el encabezdo
                    print("Folio\tDescripcion\tCantidad\tPrecio\tFecha")
                    # por cada folio, descripcion, cantidad, precio, fecha en resultados
                    # imprime el folio, descripcion, cantidad, precio, fecha
                    # y total, sumale total mas el precio por la cantidad
                    for folio, descripcion, cantidad, precio, fecha in resultados:
                        print(f"{folio}\t{descripcion}\t{cantidad}\t\t{precio}\t{fecha}")
                        total = (precio * cantidad) + total
                    # hacemos la impresion del IVA, el total, y el GRAN TOTAL
                    print(f"Total de las ventas: ${total:,.2f}")
                    print(f"El iva aplicable es de: ${total * .16:,.2f}")
                    print(f"El total con iva aplicado es de: ${total*1.16:,.2f}")
                else:
                    print("\nLa fecha solicitada no existe")
        # En caso de algun error, el except recoje el error        
        except Error as e:
            print(e)
        except Exception:
            print(f"Error: {sys.exc_info()[0]}")
        finally:
            #al final comprobamos si la base esta abierta, en ese caso, la cerramos
            if conn:
                conn.close()
    elif respuesta == 3:
        # imprimimos finalizando, para salir de programa
        print("Finalizando")
        break
    else:
        # en caso de que el usuario elegio una opcion no valida
        print("\n°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        print("°Ingrese una opcion valida°")
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°")
