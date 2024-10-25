import csv
import numpy as np
from io import FileIO

class ManejadorCSV:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def exportar(self, lista: list, modo = "w"): #Por default escribe un archivo nuevo. Se puede cambiar a "a" para agregar al final
        try:
            with open(self.nombre_archivo, mode = modo, newline="", encoding='utf-8') as archivo_csv:
                escritor = csv.writer(archivo_csv)
                escritor.writerows(lista)
        except FileNotFoundError:
            print("Archivo no encontrado")
            raise FileNotFoundError
        except IOError:
            print("Error al exportar archivo")
            raise FileIO
        
    def leer_archivo(self, skip_first = False):
        try:
            with open(self.nombre_archivo, "r", encoding='utf-8') as archivo_csv:
                lector = csv.reader(archivo_csv)
                if skip_first:
                    next(lector)
                return list(lector)
        except FileNotFoundError:
            print("Archivo no encontrado")
            raise FileNotFoundError
        except IOError:
            print("Error al leer archivo")
            raise FileIO
        
    def leer_matriz(self):
        try:
            matriz = np.genfromtxt(self.nombre_archivo, delimiter=',', dtype=str, skip_header=1)
            return matriz
        except FileNotFoundError:
            print("Archivo no encontrado")