class Aplicacion:
    """Clase padre de todas las aplicaciones del celular. Agrupa todos los atributos y métodos comunes a las aplicaciones.
    El propósito principal por el cual fue creada esta clase fue para poder distinguir entre apps esenciales y no esenciales.
    """
    def __init__(self, nombre, tamanio_mb, esencial = False):
        self.nombre = nombre
        self.tamanio_mb = tamanio_mb
        self.esencial = esencial
    
    def es_esencial(self):
        """Devuelve True si la aplicación es esencial, False en caso contrario."""
        return self.esencial
        
    def __str__(self) -> str:
        return f"Nombre: {self.nombre}\nEsencial: {self.esencial}\nTamaño: {self.tamanio_mb}"