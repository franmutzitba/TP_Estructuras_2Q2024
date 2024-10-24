from aplicacion import Aplicacion
from central import Central

class MailApp(Aplicacion):
    def __init__(self, numero, central:Central):
        super().__init__("Mail", 100, True)
        self.numero = numero
        self.central = central
        self.mensajes = ListaMail()
        
    def enviar_mail(self, receptor, mensaje):
        #Le consulta a la central si el emisor tiene LTE
        pass
        
class NodoMail():
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.siguiente = None
        
    def __str__(self):
        return f"El nodo contiene el mensaje: {self.mensaje}"
        
class ListaMail():
    def __init__(self, inicio = None):
        self.inicio = inicio
    
    def agregar_mail(self, mensaje):
        nodo = NodoMail(mensaje)
        if self.inicio == None:
            self.inicio = nodo
        else:
            actual = self.inicio
            while actual.siguiente != None:
                actual = actual.siguiente
            actual.siguiente = nodo