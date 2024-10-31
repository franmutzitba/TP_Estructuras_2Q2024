import csv

import numpy as np
from io import FileIO
from collections import deque
from comunicacion import Mensaje
from datetime import datetime

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
        except IOError:
            print("Error al exportar archivo")
        
    def leer_archivo(self, skip_first = False):
        try:
            with open(self.nombre_archivo, "r", encoding='utf-8') as archivo_csv:
                lector = csv.reader(archivo_csv)
                if skip_first:
                    next(lector)
                return list(lector)
        except FileNotFoundError:
            print("Archivo no encontrado")
            
        except IOError:
            print("Error al leer archivo")
            
        
    def leer_matriz(self):
        try:
            matriz = np.genfromtxt(self.nombre_archivo, delimiter=',', dtype=str, skip_header=1)
            return matriz
        except FileNotFoundError:
            print("Archivo no encontrado")

class ManejadorSMS(ManejadorCSV):
    def __init__(self, nombre_archivo):
        super().__init__(nombre_archivo)
    
    def exportar_mensajes(self, mensajes: dict):
        colas = mensajes.values()
        lista_a_exportar = []
        titulo = ["Emisor","Receptor","Texto","Fecha","Sincronizado"]
        lista_a_exportar.append(titulo)
        for cola in colas:
            cola_2 = cola.copy() #??
            while cola_2:
                mensaje = cola_2.popleft()
                lista_a_exportar.append([mensaje.get_emisor(), mensaje.get_receptor(), mensaje.get_mensaje(), mensaje.get_fecha(),mensaje.get_sincronizado()])

        self.exportar(lista_a_exportar)
    
    def cargar_mensajes(self, central):
        lista_mensajes = deque(self.leer_archivo(True)) #cola
        while lista_mensajes:
            lista = lista_mensajes.popleft()
            mensaje = Mensaje(lista[0],lista[1],lista[2],datetime.fromisoformat(lista[3]))
            central.registrar_mensaje_nuevo(mensaje)
        
            
            
            
    
    # @staticmethod??
    # def crear_mensaje(emisor, receptor, texto, fecha):
    #     return Mensaje(emisor, receptor, texto, fecha)








