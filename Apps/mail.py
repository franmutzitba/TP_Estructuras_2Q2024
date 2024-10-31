from Apps.aplicacion import Aplicacion
from central import Central
from collections import deque
import re
from enum import Enum
import os
class CriterioLectura(Enum):
    """Enum para los criterios de lectura de los emails"""
    NO_LEIDOS_PRIMEROS = 1
    POR_FECHA = 2

class Mail:
    """Clase que instancia un mail con los atributos cuerpo, email_emisor, email_receptor, encabezado y leido
    
    Atributos:
    ----------
    cuerpo : str
        Cuerpo del mail.
    email_emisor : str
        Email del emisor del mail.
    email_receptor : str
        Email del receptor del mail.
    encabezado : str
        Encabezado del mail.
    leido : bool
        Indica si el mail fue leído o no.
    """
    def __init__(self, cuerpo, email_emisor, email_receptor, encabezado, leido=False):
        self.cuerpo = cuerpo
        self.email_emisor = email_emisor
        self.email_receptor = email_receptor
        self.encabezado = encabezado
        self.leido = leido

    def __str__(self):
        return f"Encabezado: {self.encabezado}, Emisor: {self.email_emisor}, Leído: {self.leido}, Cuerpo: {self.cuerpo}"
    
class MailApp(Aplicacion): #Pertenece a cada telefono
    """Clase que instancia la aplicación de mail de un celular"""
    def __init__(self, numero, central:Central):
        super().__init__(nombre = "Mail", tamanio = "100 MB", esencial = True)
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
        
    def ver_bandeja_enviados(self):
        if not self.central.consultar_LTE(self.numero):
            raise ValueError("No se pudo ver la bandeja de enviados. Consulte su cobertura")
        if not self.cuenta_iniciada:
            raise ValueError("No se pudo ver la bandeja de enviados. Inicie sesión para continuar")
        
        pila = CuentaMail.cuentas[self.cuenta_mail].bandeja_enviados.copy()
        while pila:
            print(pila.pop())

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
        if not self.central.consultar_LTE(self.numero):
            raise ValueError("No se pudo iniciar sesión. Consulte su cobertura")
        
        if mail in CuentaMail.cuentas and CuentaMail.cuentas[mail].contrasenia == contrasenia:
            self.cuenta_mail = mail
            self.cuenta_iniciada = True
            print("Sesión iniciada con éxito")
        else:
            print("No se pudo iniciar sesión. Verifique los datos ingresados")
    
    def cerrar_sesion(self):
        if not self.central.consultar_LTE(self.numero):
            raise ValueError("No se pudo realizar la acción. Consulte su cobertura")
        self.cuenta_mail = None
        self.cuenta_iniciada = False
        print("Sesión cerrada con éxito")
    
    def crear_cuenta(self, mail, contrasenia):
        if not self.central.consultar_LTE(self.numero):
            raise ValueError("No se pudo realizar la acción. Consulte su cobertura")
        try:
            CuentaMail(mail, contrasenia)
            print("Cuenta creada con éxito. Inicie sesión para comenzar a utilizarla")
        except ValueError as e:
            print(e)
        pass
    
    @staticmethod
    def crear_mail(cuerpo, email_emisor, email_receptor, encabezado):
        return Mail(cuerpo, email_emisor, email_receptor, encabezado)
    
    def menu_navegacion(self):
        salir = False
        while not salir:
            print("Menú de navegación de la aplicación Mail")
            print("1. Ver bandeja de entrada")
            print("2. Ver bandeja de enviados")
            print("3. Enviar mail")
            print("4. Iniciar sesión")
            print("5. Cerrar sesión")
            print("6. Crear cuenta")
            print("7. Salir de la aplicación")
            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                os.system("cls")
                try:
                    criterio = int(input("Ingrese el criterio de lectura (1: No leídos primeros, 2: Por fecha): "))
                    self.ver_bandeja_entrada(CriterioLectura(criterio))
                except ValueError as e:
                    print(e)
            elif opcion == "2":
                os.system("cls")
                try:
                    self.ver_bandeja_enviados()
                except ValueError as e:
                    print(e)
            elif opcion == "3":
                os.system("cls")
                email_emisor = input("Ingrese el email del emisor: ")
                email_receptor = input("Ingrese el email del receptor: ")
                encabezado = input("Ingrese el encabezado: ")
                cuerpo = input("Ingrese el cuerpo: ")
                mensaje = self.crear_mail(cuerpo, email_emisor, email_receptor, encabezado)
                try:
                    self.enviar_mail(mensaje)
                except ValueError as e:
                    print(e)
            elif opcion == "4":
                os.system("cls")
                mail = input("Ingrese la direccion de mail: ")
                contrasenia = input("Ingrese la contraseña: ")
                self.iniciar_sesion(mail, contrasenia)
            elif opcion == "5":
                self.cerrar_sesion()
            elif opcion == "6":
                mail = input("Ingrese el mail: ")
                contrasenia = input("Ingrese la contraseña: ")
                self.crear_cuenta(mail, contrasenia)
            elif opcion == "7":
                os.system('cls')
                print("Saliendo del Mail..")
                salir = True
                input("Presione cualquier tecla para volver al menu del celular...")
                os.system('cls')
            else:
                os.system('cls')
                print("Opción inválida, intente nuevamente")
                input("Presione cualquier tecla para volver al menu del mail...")
                os.system('cls')
 
class CuentaMail:
    """
    Clase para gestionar cuentas de correo electrónico. Representa una cuenta de correo electrónico con un mail y una contraseña.
    
    Atributos:
    ----------
    cuentas: dict
        Diccionario que almacena todas las cuentas de correo creadas.
        
    Métodos:
    --------
    __init__(self, mail, contrasenia):
        Inicializa una nueva cuenta de correo electrónico.
    validar_mail(cls, mail):
        Valida si un correo electrónico es válido y único.
    validar_contrasenia(contrasenia):
        Valida si una contraseña cumple con los requisitos de seguridad.
    __str__(self):
        Retorna una representación en cadena de la cuenta de correo.
    """
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

