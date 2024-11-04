"""
Módulo que contiene la clase MailApp, la cual es la aplicación de correo electrónico de un celular.
"""

import os
import re
from datetime import datetime
from enum import Enum
from collections import deque
from Apps.aplicacion import Aplicacion
from central import Central

class CriterioLectura(Enum):
    """Enum para los criterios de lectura de los emails"""
    NO_LEIDOS_PRIMEROS = 1
    POR_FECHA = 2

class Mail:
    """
    Clase que instancia un mail con los atributos cuerpo, email_emisor, email_receptor, 
    encabezado y leido
    
    Atributos:
    ----------
    cuerpo (str):
        Cuerpo del mail.
    email_emisor (str):
        Email del emisor del mail.
    email_receptor (str):
        Email del receptor del mail.
    encabezado (str):
        Encabezado del mail.
    leido (bool):
        Indica si el mail fue leído o no.
    """
    def __init__(self, cuerpo, email_emisor, email_receptor, encabezado, fecha,leido=False):
        if not isinstance(cuerpo, str) or not isinstance(email_emisor, str) or not isinstance(email_receptor, str) or not isinstance(encabezado, str) or not isinstance(leido, bool):
            raise ValueError("Los atributos del Mail deben ser del tipo correcto")
        self.cuerpo = cuerpo
        self.email_emisor = email_emisor
        self.email_receptor = email_receptor
        self.encabezado = encabezado
        self.fecha = fecha
        self.leido = leido

    def __str__(self):
        return f"Fecha de emision:{self.fecha}\nEmisor: {self.email_emisor}\nReceptor: {self.email_receptor}\nEncabezado: {self.encabezado}\nLeído: {self.leido}\nCuerpo:\n{self.cuerpo}"

class MailApp(Aplicacion): #Pertenece a cada telefono
    """
    Clase que representa la aplicación de Mail en un celular.
    
    Atributos:
    ----------
    numero (str): 
        Número de teléfono asociado a la aplicación.
    central (Central): 
        Instancia de la central que gestiona la conectividad.
    cuenta_mail (str): 
        Dirección de correo electrónico de la cuenta iniciada.
    cuenta_iniciada (bool): 
        Indica si hay una sesión iniciada en la aplicación.
    
    Métodos:
    --------
    ver_bandeja_entrada(criterio): 
        Muestra los correos de la bandeja de entrada según el criterio especificado.
    ver_bandeja_enviados(): 
        Muestra los correos de la bandeja de enviados.
    enviar_mail(mensaje: Mail): 
        Envía un correo electrónico.
    iniciar_sesion(mail, contrasenia): 
        Inicia sesión en la aplicación de Mail.
    cerrar_sesion(): 
        Cierra la sesión iniciada en la aplicación de Mail.
    crear_cuenta(mail, contrasenia): 
        Crea una nueva cuenta de correo electrónico.
    crear_mail(cuerpo, email_emisor, email_receptor, encabezado): 
        Crea un nuevo correo electrónico.
    menu_navegacion(): 
        Muestra el menú de navegación de la aplicación de Mail.
    """

    def __init__(self, numero, central:Central):
        super().__init__(nombre = "Mail", tamanio = "100 MB", esencial = True)
        self.numero = numero
        self.central = central
        self.cuenta_mail = None
        self.cuenta_iniciada = False

    def ver_bandeja_entrada(self, criterio):
        """
        Muestra los correos de la bandeja de entrada según el criterio especificado.
        
        Args:
            criterio (CriterioLectura): El criterio de lectura de los correos.
        
        Returns:
            None
        
        Raises:
            ValueError: Si el criterio no es válido.
        """
        if self.cuenta_iniciada and self.central.consultar_LTE(self.numero):
            if not CuentaMail.cuentas[self.cuenta_mail].bandeja_entrada:
                raise ValueError("No hay mails en la bandeja de entrada")
            if criterio == CriterioLectura.NO_LEIDOS_PRIMEROS:
                no_leidos = deque(mail for mail in CuentaMail.cuentas[self.cuenta_mail].bandeja_entrada if not mail.leido)
                no_leidos = deque(sorted(no_leidos, key=lambda mail: mail.fecha)) #Ordena los mails por fecha dejando las mas nuevas al final (hay q probarlo)
                while no_leidos:
                    print(no_leidos.popleft())
            elif criterio == CriterioLectura.POR_FECHA:
                pila = CuentaMail.cuentas[self.cuenta_mail].bandeja_entrada.copy()
                pila = sorted(pila, key=lambda mail: mail.fecha) #Ordena los mails por fecha dejando las mas nuevas al final (hay q probarlo)
                while pila:
                    print(pila.pop())
            else:
                raise ValueError("Criterio no válido")
        else:
            raise ValueError("No se pudo ver la bandeja de entrada. Inicie sesión para continuar")

    def ver_bandeja_enviados(self):
        """
        Muestra los correos electrónicos en la bandeja de enviados de la cuenta de correo actual.
        
        Returns:
            None
            
        Raises:
            ValueError: Si no se pudo ver la bandeja de enviados debido a problemas de cobertura.
            ValueError: Si no se pudo ver la bandeja de enviados porque la cuenta no ha 
                        iniciado sesión.
        """
        if not self.central.consultar_LTE(self.numero):
            raise ValueError("No se pudo ver la bandeja de enviados. Consulte su cobertura")
        if not self.cuenta_iniciada:
            raise ValueError("No se pudo ver la bandeja de enviados. Inicie sesión para continuar")
        if not CuentaMail.cuentas[self.cuenta_mail].bandeja_enviados:
            raise ValueError("No hay mails en la bandeja de enviados")

        pila = CuentaMail.cuentas[self.cuenta_mail].bandeja_enviados.copy()
        while pila:
            print(pila.pop())

    def enviar_mail(self, mensaje: Mail):
        """
        Envía un correo electrónico si el emisor tiene cobertura LTE y la cuenta está iniciada.

        Args:
            mensaje (Mail): El mensaje de correo electrónico a enviar.
            
        Returns:
            None

        Raises:
            ValueError: Si la cuenta no está iniciada o no tiene cobertura LTE.
        """
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
        """
        Inicia sesión en la cuenta de correo si las credenciales son correctas y la cobertura 
        LTE está disponible.
        
        Args:
            mail (str): Dirección de correo electrónico de la cuenta.
            contrasenia (str): Contraseña de la cuenta de correo.
            
        Returns:
            None
            
        Raises:
            ValueError: Si no hay cobertura LTE disponible.
        """
        if not self.central.consultar_LTE(self.numero):
            raise ValueError("No se pudo iniciar sesión. Consulte su cobertura")

        if mail in CuentaMail.cuentas and CuentaMail.cuentas[mail].contrasenia == contrasenia:
            self.cuenta_mail = mail
            self.cuenta_iniciada = True
            print("Sesión iniciada con éxito")
        else:
            print("No se pudo iniciar sesión. Verifique los datos ingresados")

    def cerrar_sesion(self):
        """
        Cierra la sesión de la cuenta de correo actual.
        Si la cobertura LTE no está disponible, se lanza una excepción.

        Returns:
            None
            
        Raises:
            ValueError: Si no se pudo realizar la acción debido a la falta de cobertura LTE.
        """
        if not self.central.consultar_LTE(self.numero):
            raise ValueError("No se pudo realizar la acción. Consulte su cobertura")
        self.cuenta_mail = None
        self.cuenta_iniciada = False
        print("Sesión cerrada con éxito")

    def crear_cuenta(self, mail, contrasenia):
        """
        Crea una cuenta de correo electrónico si hay cobertura disponible.

        Args:
            mail (str): La dirección de correo electrónico para la nueva cuenta.
            contrasenia (str): La contraseña para la nueva cuenta.

        Returns:
            None
            
        Raises:
            ValueError: Si no hay cobertura disponible o si ocurre un error al crear la cuenta.
        """
        if not self.central.consultar_LTE(self.numero):
            raise ValueError("No se pudo realizar la acción. Consulte su cobertura")
        try:
            CuentaMail(mail, contrasenia)
            print("Cuenta creada con éxito. Inicie sesión para comenzar a utilizarla")
        except ValueError as e:
            print(e)

    @staticmethod
    def crear_mail(cuerpo, email_emisor, email_receptor, encabezado, fecha):
        """Crea un nuevo correo electrónico con los datos proporcionados."""
        return Mail(cuerpo, email_emisor, email_receptor, encabezado, fecha)

    def menu_navegacion(self):
        """Muestra el menú de navegación de la aplicación de Mail."""
        os.system('cls')
        salir = False
        print("Bienvenido a la aplicacion de Mail")
        while not salir:
            print("Menú de Mail:")
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
                    criterio = input("Ingrese el criterio de lectura (1: No leídos primeros, 2: Por fecha): ")
                    while criterio not in ["1", "2"]:
                        criterio = input("Criterio no válido. Ingrese el criterio de lectura (1: No leídos primeros, 2: Por fecha): ")
                    self.ver_bandeja_entrada(CriterioLectura(int(criterio)))
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Mail...")
                os.system('cls')
            elif opcion == "2":
                os.system("cls")
                try:
                    self.ver_bandeja_enviados()
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Mail...")
                os.system('cls')
            elif opcion == "3":
                os.system("cls")
                #email_emisor = input("Ingrese el email del emisor: ")
                email_receptor = input("Ingrese el email del receptor: ")
                encabezado = input("Ingrese el encabezado: ")
                cuerpo = input("Ingrese el cuerpo: ")
                try:
                    mensaje = self.crear_mail(cuerpo, self.cuenta_mail, email_receptor, encabezado, datetime.now())
                    self.enviar_mail(mensaje)
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Mail...")
                os.system('cls')
            elif opcion == "4":
                os.system("cls")
                mail = input("Ingrese la direccion de mail: ")
                contrasenia = input("Ingrese la contraseña: ")
                try:
                    self.iniciar_sesion(mail, contrasenia)
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Mail...")
                os.system('cls')
            elif opcion == "5":
                os.system("cls")
                try:
                    self.cerrar_sesion()
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Mail...")
                os.system('cls')
            elif opcion == "6":
                os.system("cls")
                mail = input("Ingrese el mail: ")
                contrasenia = input("Ingrese la contraseña: ")
                try:
                    self.crear_cuenta(mail, contrasenia)
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Mail...")
                os.system('cls')
            elif opcion == "7":
                os.system('cls')
                print("Saliendo del Mail..")
                salir = True
            else:
                os.system('cls')
                print("Opción inválida, intente nuevamente")
                input("Presione cualquier tecla para volver al menu del mail...")
                os.system('cls')

class CuentaMail:
    """
    Clase para gestionar cuentas de correo electrónico. Representa una cuenta de correo electrónico 
    con un mail y una contraseña.
    
    Atributos:
    ----------
    cuentas (dict):
        Diccionario que almacena todas las cuentas de correo creadas.
        
    Métodos:
    --------
    __init__(self, mail, contrasenia):
        Inicializa una nueva cuenta de correo electrónico.
    validar_mail(cls, mail):
        Valida si un correo electrónico es válido y único.
    validar_contrasenia(contrasenia):
        Valida si una contraseña cumple con los requisitos de seguridad.
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
        """Valida si un correo electrónico es válido y único."""
        # Expresión regular para validar un correo electrónico
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return (re.match(regex, mail) is not None) and (mail not in cls.cuentas) #Si la expresión regular coincide con el email, retorna True

    @staticmethod
    def validar_contrasenia(contrasenia):
        """Valida si una contraseña cumple con los requisitos de seguridad."""
        # Expresión regular para validar una contraseña
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.match(regex, contrasenia) is not None

    def __str__(self):
        return f"La cuenta es: {self.mail} y la contrasenia es: {self.contrasenia}"
