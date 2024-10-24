class Aplicacion:
    def __init__(self, nombre, tamanio_mb, esencial = False):
        self.nombre = nombre
        self.tamanio_mb = tamanio_mb
        self.esencial = esencial
        
    def es_esencial(self):
        return self.esencial
        
    def __str__(self) -> str:
        return f"Nombre: {self.nombre}\nEsencial: {self.esencial}\nTamaño: {self.tamanio_mb}"