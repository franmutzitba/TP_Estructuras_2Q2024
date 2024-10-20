class Comunicacion():
    
    def __init__(self, emisor, receptor, tipo):
        self.emisor = emisor
        self.receptor = receptor
        self.tipo = tipo



class Llamada(Comunicacion):
    
    def __init__(self, emisor, receptor, duracion):
        super().__init__(self, emisor, receptor, 'Llamada realizada')
        self.duracion = duracion

    def __str__(self):
        return f"Emisor: {self.emisor}, Receptor: {self.receptor}, Duracion: {self.duracion}"
    
class Llamada_perdida(Comunicacion):

    def __init__(self, emisor, receptor, tipo="Llamada perdida"):
        super().__init__(self, emisor, receptor, 'Llamada no realizada')
        self.tipo = tipo
    
class Mensaje(Comunicacion):

    def __init__(self, emisor, receptor, mensaje):
        super().__init__(self, emisor, receptor, 'Mensaje')
        self.mensaje = mensaje

    def __str__(self):
        return f"Emisor: {self.emisor}, Receptor: {self.receptor}, Duracion: {self.mensaje}"

    
        