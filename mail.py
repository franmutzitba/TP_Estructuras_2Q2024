from aplicacion import Aplicacion
from central import Central
from collections import deque
import re
from enum import Enum

class CriterioLectura(Enum):
    NO_LEIDOS_PRIMEROS = 1
    POR_FECHA = 2

class Mail:
    def __init__(self, cuerpo, email_emisor, email_receptor, encabezado, leido=False):
        self.cuerpo = cuerpo
        self.email_emisor = email_emisor
        self.email_receptor = email_receptor
        self.encabezado = encabezado
        self.leido = leido

    def __str__(self):
        return f"Encabezado: {self.encabezado}, Emisor: {self.email_emisor}, Leído: {self.leido}, Cuerpo: {self.cuerpo}"
    
class MailApp(Aplicacion): #Pertenece a cada telefono
    def __init__(self, numero, central:Central):
        super().__init__("Mail", 100, True)
        self.numero = numero
        self.central = central
        self.cuenta_mail = None
        self.cuenta_iniciada = False
        
    def ver_bandeja_entrada(self, criterio):
        if self.cuenta_iniciada and self.central.consultar_LTE(self.numero):
            if criterio == CriterioLectura.NO_LEIDOS_PRIMEROS:
                no_leidos = deque(mail for mail in CuentaMail.cuentas[self.cuenta_mail].bandeja_entrada if not mail.leido)
                while no_leidos:
                    print(no_leidos.popleft())
            elif (criterio == CriterioLectura.POR_FECHA):
                pila = CuentaMail.cuentas[self.cuenta_mail].bandeja_entrada.copy()
                while pila:
                    print(pila.pop())
            else:
                raise ValueError("Criterio no válido")
        else: 
            raise ValueError("No se pudo ver la bandeja de entrada. Inicie sesión para continuar")
        
    def enviar_mail(self, mensaje: Mail):
        #Le consulta a la central si el emisor tiene LTE
        if self.central.consultar_LTE(self.numero):
            if self.cuenta_iniciada:
                #Esto hay q verlo bien
                CuentaMail.cuentas[self.cuenta_mail].bandeja_enviados.append(mensaje) #Agrega el mensaje a la bandeja de enviados sin importar si el receptor existe o no
                if mensaje.email_receptor in CuentaMail.cuentas:
                    CuentaMail.cuentas[mensaje.email_receptor].bandeja_entrada.append(mensaje) #Agrega el mensaje a la bandeja de entrada del receptor (si existe). Sino se pierde el mail
                print(f"Mensaje enviado a {mensaje.email_receptor} con éxito") #Con receptor me refiero al mail del receptor
            else:
                raise ValueError("No se pudo enviar el mensaje. Inicie sesión para continuar")
        else:
            raise ValueError("No se pudo enviar el mensaje. No tiene cobertura LTE")
    
    def iniciar_sesion(self, mail, contrasenia):
        if mail in CuentaMail.cuentas and CuentaMail.cuentas[mail].contrasenia == contrasenia:
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
            CuentaMail(mail, contrasenia)
            print("Cuenta creada con éxito. Inicie sesión para comenzar a utilizarla")
        except ValueError as e:
            print(e)
        pass
    
    @staticmethod
    def crear_mail(cuerpo, email_emisor, email_receptor, encabezado):
        return Mail(cuerpo, email_emisor, email_receptor, encabezado)
 
class CuentaMail():
    cuentas = {}
    
    def __init__(self, mail, contrasenia):
        if not self.validar_mail(mail):
            raise ValueError("El mail no es válido")       
        if not self.validar_contrasenia(contrasenia):
            raise ValueError("La contraseña no es válida")
        
        self.mail = mail #Debe ser único por eso las validaciones previas
        self.contrasenia = contrasenia
        self.bandeja_entrada = deque()
        self.bandeja_enviados = deque()
        CuentaMail.cuentas[mail] = self

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

