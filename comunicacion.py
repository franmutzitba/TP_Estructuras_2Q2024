from datetime import datetime

class Comunicacion:
    def __init__(self, emisor, receptor, tipo):
        self.emisor = emisor
        self.receptor = receptor
        self.tipo = tipo

    def get_emisor(self):
        return self.emisor

    def get_receptor(self):
        return self.receptor

class Llamada(Comunicacion):
    def __init__(self, emisor, receptor, duracion, fecha):
        super().__init__(emisor, receptor, 'Llamada realizada')
        self.duracion = duracion
        self.fecha = fecha
        self.perdida = False
    
    def set_duracion(self, tiempo):
        self.duracion = tiempo

    def get_duracion(self):
        return self.duracion
    # Faltan getters y setters de emisor y receptor
    def get_fecha(self):
        return self.fecha
    
    def get_perdida(self):
        return self.perdida
    
    def set_perdida(self, perdida):
        self.perdida = perdida

    def __str__(self):
        return f"Emisor: {self.emisor}, Receptor: {self.receptor}, Duracion: {self.duracion}"
    
    
class Mensaje(Comunicacion):
    def __init__(self, emisor, receptor, mensaje, fecha):
        super().__init__(emisor, receptor, 'Mensaje')
        self.mensaje = mensaje
        self.fecha = fecha
        self.sincronizado = False #El mensaje se sincroniza cuando el receptor es capaz de recibirlo en su bandeja de entrada

    def get_sincronizado(self):
        return self.sincronizado
    
    def set_sincronizado(self):
        self.sincronizado = True
    
    def get_mensaje(self):
        return self.mensaje
    
    def get_fecha(self):
        return self.fecha

    def __str__(self):
        fecha_min = self.fecha.strftime("%Y-%m-%d %H:%M")
        return f"Emisor: {self.emisor}, Receptor: {self.receptor}, Texto: {self.mensaje}, Fecha: {fecha_min}"

