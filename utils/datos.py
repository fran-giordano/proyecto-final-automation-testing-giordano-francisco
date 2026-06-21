import csv
import pathlib
import json

def leer_csv_login(ruta_archivo):
    """Lee un archivo CSV y devuelve una lista de tuplas para
    usar en parametrizacion de pytest
    """

    datos = []
    with open(ruta_archivo, newline='', encoding='utf-8-sig') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            datos.append((
                fila['usuario'],
                fila['clave'],
                fila['debe_funcionar'].strip().lower() == 'true',
                fila.get('descripcion', '')  # Agrega la descripción si está presente, o una cadena vacía si no lo está
            ))

    return datos

def leer_json_productos(ruta_archivo):
    """Lee un archivo JSON y devuelve una lista de diccionarios con los datos de los productos"""

    with open(ruta_archivo, 'r', encoding='utf-8-sig') as f:
        return json.load(f)


if __name__ == "__main__":
    print (leer_csv_login('datos/login.csv'))
    print (leer_json_productos('datos/productos.json'))

