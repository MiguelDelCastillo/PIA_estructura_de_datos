# Importamos las librerias de SQLite, sys, y el error de SQLite
import sys
import sqlite3
from sqlite3 import Error

try:
    # Creamos la conexion con la base de datos
    with sqlite3.connect("PIADB.db") as conn:
        # guardamos la conexion en un cursor
        mi_cursor = conn.cursor()
        # Creamos la tabla de FechaID que guarda Folio y Fecha, donde Folio es PRIMARY KEY
        mi_cursor.execute("""CREATE TABLE IF NOT EXISTS FechaID \
                            (folio INTEGER PRIMARY KEY,\
                            fecha TEXT NOT NULL);""")
        #Creamos la tabla Venta, donde guardamos el folio, descripcion cantidad, precio
        # y asignamos a folio, como llave foranea
        mi_cursor.execute("""CREATE TABLE IF NOT EXISTS Venta\
                            (folio INTEGER NOT NULL,\
                            descripcion TEXT NOT NULL,\
                            canitdad INTEGER NOT NULL,\
                            precio INTEGER NOT NULL, \
                            FOREIGN KEY (folio) REFERENCES FechaID(folio));""")
        # Si todo salio exitoso, imprimos el mensaje siguiente
        print("Tabla creada exitosamente")
# En caso de que haya algun error, los except lo tomaran, e informaran del problema
except Error as e:
    print(e)
except Exception:
    print(f"Error: {sys.exc_info()[0]}")
finally:
    # finalmente, si la conexion esta abierta, la cerramos
    if conn:
        conn.close()
