from aplicacion import Aplicacion
from central import Central
import re

class MailApp(Aplicacion): #Pertenece a cada telefono
    def __init__(self, numero, central:Central):
        super().__init__("Mail", 100, True)
        self.numero = numero
        self.central = central
        self.cuenta_mail = None
        self.cuenta_iniciada = False
        self.mensajes = ListaMail()
    
    def enviar_mail(self, receptor, mensaje):
        #Le consulta a la central si el emisor tiene LTE
        if self.central.consultar_LTE(self.numero):
            if self.cuenta_iniciada:
                #Esto hay q verlo bien
                self.mensajes.agregar_mail(mensaje)
                print(f"Mensaje enviado a {receptor} con éxito")
            else:
                raise ValueError("No se pudo enviar el mensaje. Inicie sesión para continuar")
        else:
            raise ValueError("No se pudo enviar el mensaje. No tiene cobertura LTE")
    
    def iniciar_sesion(self, mail, contrasenia):
        if mail in CuentaMail.cuentas and CuentaMail.cuentas[mail] == contrasenia:
            self.cuenta_mail = mail
            self.cuenta_iniciada = True
            print("Sesión iniciada con éxito")
        else:
            print("No se pudo iniciar sesión. Verifique los datos ingresados")
    
    def cerrar_sesion(self):
        self.cuenta_mail = None
        self.cuenta_iniciada = False
        print("Sesión cerrada con éxito")
    
    def crear_cuenta(self, mail, contrasenia):
        try:
            cuenta = CuentaMail(mail, contrasenia)
            print("Cuenta creada con éxito. Inicie sesión para comenzar a utilizarla")
        except ValueError as e:
            print(e)
        pass
 
class CuentaMail():
    cuentas = {}
    
    def __init__(self, mail, contrasenia):
        if not self.validar_mail(mail):
            raise ValueError("El mail no es válido")       
        if not self.validar_contrasenia(contrasenia):
            raise ValueError("La contraseña no es válida")
        
        self.mail = mail #Debe ser único por eso las validaciones previas
        self.contrasenia = contrasenia
        self.cuentas[mail] = contrasenia

    @classmethod
    def validar_mail(cls, mail):
        # Expresión regular para validar un correo electrónico
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return (re.match(regex, mail) is not None) and (mail not in cls.cuentas) #Si la expresión regular coincide con el email, retorna True
    
    @staticmethod
    def validar_contrasenia(contrasenia):
        # Expresión regular para validar una contraseña
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.match(regex, contrasenia) is not None
    
    def __str__(self):
            return f"La cuenta es: {self.mail} y la contrasenia es: {self.contrasenia}"


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