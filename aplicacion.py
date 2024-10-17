class Aplicacion:
    def __init__(self, nombre, tamanio, esencial = False):
        self.nombre = nombre
        self.tamanio = tamanio
        self.esencial = esencial
        
    def __str__(self) -> str:
        return f"Nombre: {self.nombre}\nEsencial: {self.esencial}\nTamaño: {self.tamanio}"