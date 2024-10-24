from aplicacion import Aplicacion
from central import Central
import re

class MailApp(Aplicacion): #Pertenece a cada telefono
    cuentas = [] #Para chequear si el mail ya existe
    
    def __init__(self, numero, central:Central):
        super().__init__("Mail", 100, True)
        self.numero = numero
        self.central = central
        self.cuenta = None
        self.cuenta_iniciada = False
        self.mensajes = ListaMail()
    
    def enviar_mail(self, receptor, mensaje):
        #Le consulta a la central si el emisor tiene LTE
        pass
    
    def iniciar_sesion(self, cuenta, contrasenia):
        pass
    
    def cerrar_sesion(self):
        pass
    
    def crear_cuenta(self, cuenta, contrasenia):
        pass
    
    # @classmethod
    # def validar_cuenta(cls, cuenta):
    #     pass
    
    @staticmethod
    def validar_contrasenia(contrasenia):
        pass

 
class CuentaMail():
    def __init__(self, mail, contrasenia):
        if not self.validar_mail(mail):
            raise ValueError("El mail no es válido")       
        if not self.validar_contrasenia(contrasenia):
            raise ValueError("La contraseña no es válida")
        
        self.mail = mail
        self.contrasenia = contrasenia

    @staticmethod
    def validar_mail(mail):
        # Expresión regular para validar un correo electrónico
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, mail) is not None #Si la expresión regular coincide con el email, retorna True
    
    @staticmethod
    def validar_contrasenia(contrasenia):
        # Expresión regular para validar una contraseña
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.match(regex, contrasenia) is not None
    
    def __str__(self):
            return f"La cuenta es: {self.cuenta} y la contrasenia es: {self.contrasenia}"

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