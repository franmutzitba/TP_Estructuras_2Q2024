from celular import Celular
from central import Central


class Comunicacion():
    
    def __init__(self, emisor, receptor, tipo):
        self.emisor = emisor
        self.receptor = receptor
        self.tipo = tipo



class Llamada(Comunicacion):
    
    def __init__(self, emisor: Celular, receptor: Celular, duracion):
        super().__init__(self, emisor, receptor, 'Llamada')
        self.duracion = duracion

    def __str__(self):
        return f"Emisor: {self.emisor}, Receptor: {self.receptor}, Duracion: {self.duracion}"
    
class Mensaje(Comunicacion):

    def __init__(self, emisor: Celular, receptor: Celular, mensaje):
        super().__init__(self, emisor, receptor, 'Mensaje')
        self.mensaje = mensaje

    def __str__(self):
        return f"Emisor: {self.emisor}, Receptor: {self.receptor}, Duracion: {self.mensaje}"

    
        