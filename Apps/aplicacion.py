"""
Módulo que contiene la clase Aplicacion, la cual es la clase padre de todas las aplicaciones 
del celular.
"""

import os
from funciones_utiles import tamanio_a_bytes

class Aplicacion:
    """Clase padre de todas las aplicaciones del celular. Agrupa todos los atributos y métodos 
    comunes a las aplicaciones.El propósito principal por el cual fue creada esta clase fue 
    para poder distinguir entre apps esenciales y no esenciales.
    """
    def __init__(self, nombre, tamanio, esencial = False):
        if nombre == "" or tamanio == "":
            raise ValueError("Los campos nombre y tamanio no pueden estar vacíos.")
        if not isinstance(esencial, bool):
            raise ValueError("El campo esencial debe ser un booleano.")
        self.nombre = nombre
        self.tamanio = tamanio_a_bytes(tamanio)
        self.esencial = esencial

    def es_esencial(self):
        """Devuelve True si la aplicación es esencial, False en caso contrario."""
        return self.esencial

    def menu_navegacion(self):
        """Método que simula el menú de navegación de la aplicación."""
        print(f"Bienvenido a la aplicación {self.nombre}")
        print("Esta aplicación no se encuentra desarrollada aún.")
        input("Presione cualquier tecla para volver al menú del celular...")
        os.system("cls")

    def __str__(self) -> str:
        return f"Nombre: {self.nombre}\nEsencial: {self.esencial}\nTamaño: {self.tamanio} bytes"
