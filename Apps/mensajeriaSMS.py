"""
Módulo que contiene la clase MensajesApp que representa una aplicación de mensajería SMS.
"""

import os
from datetime import datetime
from collections import deque
from Apps.aplicacion import Aplicacion
from Apps.contactos import ContactosApp
from comunicacion import Mensaje
from central import Central

class MensajesApp(Aplicacion):
    """
    Clase MensajesApp que representa una aplicación de mensajería SMS.
    
    Atributos:
    ----------
    numero_cel (str):
        Número de teléfono del usuario.
    contactos (dict):
        Diccionario de contactos de la aplicación.
    central (Central):
        Objeto central que maneja la comunicación de mensajes.
    mensajes (deque):
        Cola de mensajes recibidos.
        
    Métodos:
    --------
    __init__(self, numero, contactos: ContactosApp, central: Central):
        Inicializa la aplicación de mensajería con el número de teléfono, contactos y central.
    crear_mensaje(self, receptor: str, mensaje: str):
        Crea un nuevo mensaje con el receptor y el texto del mensaje.
    numero_en_contactos(self, numero):
        Verifica si un número está en la lista de contactos.
    nombre_en_contactos(self, nombre):
        Verifica si un nombre está en la lista de contactos.
    nombre_contacto(self, numero):
        Obtiene el nombre del contacto dado un número de teléfono.
    numeros_de_nombre(self, nombre):
        Obtiene una lista de números asociados a un nombre de contacto.
    enviar_sms(self, receptor, texto):
        Envía un mensaje SMS al receptor con el texto proporcionado.
    recibir_sms(self, mensaje: Mensaje):
        Recibe un mensaje y lo agrega a la bandeja de entrada si no está sincronizado.
    ver_bandeja_de_entrada(self):
        Muestra la bandeja de entrada de mensajes recibidos.
    ver_mensajes_de(self, numero, contacto):
        Muestra los mensajes recibidos de un número o contacto específico.
    ver_chats_recientes(self):
        Muestra los chats recientes y devuelve una cola de números/contactos recientes.
    eliminar_mensaje(self, indice):
        Elimina un mensaje de la bandeja de entrada dado su índice.
    validar_indice(indice, len):
        Valida si un índice es un número entero dentro del rango permitido.
    menu_navegacion(self):
        Muestra el menú de navegación de la aplicación de mensajería.
    """
    def __init__(self, numero ,contactos: ContactosApp, central: Central):
        super().__init__(nombre = "MensajeriaSMS", tamanio = "100 MB", esencial = True,)
        self.numero_cel = numero
        self.contactos = contactos.agenda
        self.central = central
        self.mensajes = deque()

    def crear_mensaje(self, receptor: str, mensaje: str):
        """
        Crea un nuevo mensaje a partir de la clase Mensaje.
        
        Args:
            receptor (str): Número de teléfono del receptor.
            mensaje (str): Texto del mensaje.
        
        Returns:
            Mensaje: Objeto de la clase Mensaje.
        """
        return Mensaje(self.numero_cel, receptor, mensaje,datetime.now())

    def numero_en_contactos(self, numero):
        """
        Verifica si un número está en la lista de contactos.
        
        Args:
            numero (str): Número de teléfono a verificar.
            
        Returns:
            bool: True si el número está en la lista de contactos, False en caso contrario.
        """
        return numero in self.contactos

    def nombre_en_contactos(self, nombre):
        """
        Verifica si un nombre está en la lista de contactos.
        
        Args:
            nombre (str): Nombre a verificar.
            
        Returns:
            bool: True si el nombre está en la lista de contactos, False en caso contrario.
        """
        return nombre in self.contactos.values()

    def nombre_contacto(self, numero):
        """
        Obtiene el nombre del contacto dado un número de tel
        
        Args:
            numero (str): Número de teléfono del contacto.
            
        Returns:
            str: Nombre del contacto.
        """
        return self.contactos[numero]

    def numeros_de_nombre(self, nombre):
        """
        Obtiene una lista de números asociados a un nombre de contacto.
        
        Args:
            nombre (str): Nombre del contacto.
            
        Returns:
            deque: Cola de números asociados al nombre del contacto.
        """

        lista=deque()
        i=1
        for numero, nombre in self.contactos.items():
            if nombre == nombre:
                lista.append(numero)
                i+=1
        return lista

    def enviar_sms(self, receptor, texto):
        """
        Envía un mensaje SMS al receptor con el texto proporcionado.
        
        Args:
            receptor (str): Número de teléfono del receptor.
            texto (str): Texto del mensaje.
            
        Returns:
            None
        """
        if self.central.manejar_mensaje(self.numero_cel, receptor):
            mensaje = self.crear_mensaje(receptor, texto)
            self.central.registrar_mensaje_nuevo(mensaje)
            print(f"Mensaje enviado correctamente al numero {receptor}")

    def recibir_sms(self, mensaje: Mensaje):
        """
        Recibe un mensaje y lo agrega a la bandeja de entrada si no está sincronizado.
        
        Args:
            mensaje (Mensaje): Objeto de la clase Mensaje.
            
        Returns:
            None
        """
        if not mensaje.get_sincronizado():
            mensaje.set_sincronizado()
            self.mensajes.append(mensaje)
        else:
            print("El mensaje ya ha sido recibido")

    def ver_bandeja_de_entrada(self):
        """
        Muestra los mensajes en la bandeja de entrada del número de celular asociado.
        Si la bandeja de entrada está vacía, lanza una excepción ValueError.
        Recorre los mensajes en la bandeja de entrada y los imprime en la consola. 
        Si el emisor del mensaje está en la lista de contactos, muestra el nombre del contacto; 
        de lo contrario, muestra el número del emisor.
        
        Raises:
            ValueError: Si la bandeja de entrada está vacía.
            
        Prints:
            Información de cada mensaje en la bandeja de entrada, incluyendo el emisor, 
            el texto del mensaje y la fecha de recepción.
        """

        bandeja_de_entrada = self.mensajes.copy()
        i=1
        if not bandeja_de_entrada:
            raise ValueError(f"El numero: {self.numero_cel} no tiene mensajes en la bandeja de entrada")
        print(f"Bandeja de Entrada del numero: {self.numero_cel}")

        while bandeja_de_entrada:
            print(f"- {i} - ", end="")
            mensaje = bandeja_de_entrada.popleft()
            fecha_min = mensaje.fecha.strftime("%Y-%m-%d %H:%M")
            if self.numero_en_contactos(mensaje.get_emisor()) :
                print(f"Emisor: {self.nombre_contacto(mensaje.get_emisor())}, Fecha: {fecha_min}")
                print(f"      {mensaje.mensaje}")
            else:
                print(f"Emisor: {mensaje.get_emisor()}, Fecha: {fecha_min}")
                print(f"      Texto: {mensaje.mensaje}")
            print("")
            i += 1

    def ver_mensajes_de(self, numero, contacto):
        """
        Muestra los mensajes recibidos de un número o contacto específico.
        
        Args:
            numero (str): Número de teléfono del emisor.
            contacto (str): Nombre del contacto.
        
        Returns:
            None
        """
        mensajes = self.mensajes.copy()
        i=1
        print(f"Mensajes recibidos de: {contacto if contacto else numero}")
        while mensajes:
            mensaje = mensajes.popleft()
            if mensaje.get_emisor() == numero:
                print(f"- {i} - ", end="")
                fecha_min = mensaje.fecha.strftime("%Y-%m-%d %H:%M")
                print(f"{fecha_min}")
                print(f"      {mensaje.mensaje}")
                i += 1

    def ver_chats_recientes(self):
        """
        Muestra los chats recientes y devuelve una cola de números/contactos recientes.
        Si no hay mensajes en la bandeja de entrada, lanza una excepción ValueError.
        
        Returns:
            deque: Cola de números/contactos recientes.
            
        Raises:
            ValueError: Si no hay mensajes en la bandeja de entrada.
        """
        if not self.mensajes:
            raise ValueError(f"EL numero: {self.numero_cel} no tiene mensajes")
        recientes = deque() #cola de numeros/contactos recientes
        mensajes = self.mensajes.copy()
        i=1
        while mensajes:
            mensaje = mensajes.popleft()
            if mensaje.get_emisor() not in recientes:
                recientes.append(mensaje.get_emisor())
                print(f"{i} - {self.nombre_contacto(mensaje.get_emisor()) if self.numero_en_contactos(mensaje.get_emisor()) else mensaje.get_emisor()}")
                i +=1
        return recientes

    def eliminar_mensaje(self, indice):
        """
        Elimina un mensaje de la bandeja de entrada dado su índice.
        
        Args:
            indice (int): Índice del mensaje a eliminar.
            
        Raises:
            ValueError: Si el índice no es un número entero o está fuera de rango.
            IndexError: Si el índice está fuera de rango.
        """
        mensaje = self.mensajes[indice-1]
        self.mensajes.remove(mensaje)
        self.central.eliminar_mensaje(mensaje, self.numero_cel)

    @staticmethod
    def validar_indice(indice, largo):
        """Valida si un índice es un número entero dentro del rango permitido."""
        return  indice.isdigit() and int(indice) >= 1 and (not int(indice) > largo)

    def menu_navegacion(self):
        os.system('cls')
        print(f"\nBienvenido a la aplicacion de Mensajes SMS del numero {self.numero_cel}")
        salir = False
        while not salir:
            print(f"\nAplicacion de Mensajes SMS del numero {self.numero_cel}:")
            print("1. Enviar mensaje")
            print("2. Ver bandeja de entrada")
            print("3. Ver bandeja de entrada por numero/contacto")
            print("4. Eliminar Mensaje")
            print("5. Salir")
            opcion = input("Ingrese el número de la opción deseada: ")
            if opcion == "1":
                os.system('cls')
                print("1. Enviar mensaje a contacto")
                print("2. Enviar mensaje a numero ")
                opcion2 = input("Ingrese el número de la opción deseada: ")
                try:
                    if opcion2 == "1":
                        os.system('cls')
                        receptor = input("Ingrese el nombre del contacto receptor: ")
                        if not self.nombre_en_contactos(receptor):
                            raise ValueError(f"El nombre: {receptor} no se encuentra en la lista de contactos")
                        lista = self.numeros_de_nombre(receptor)
                        if len(lista) > 1:
                            print(f"Numeros del contacto: {receptor}")
                            lista2 = lista.copy()
                            while lista2:
                                print(lista2)
                            indice = input("Ingrese el indice del contacto deseado: ")
                            while not MensajesApp.validar_indice(indice,len(lista)): #Puedo hacer un metodo de validacion
                                indice = input("Entrada incorrecta. Ingrese el indice del contacto deseado: ")
                        else:
                            indice = 1
                        numero = lista[indice-1]
                        texto = input("Ingrese el mensaje a enviar: ")
                        if not texto:
                            raise ValueError("No se pueden enviar mensajes vacios")
                        self.enviar_sms(numero, texto)

                    elif opcion2 == "2":
                        os.system('cls')
                        receptor = input("Ingrese el número de teléfono del receptor: ")
                        texto = input("Ingrese el mensaje a enviar: ")
                        if not texto:
                            raise ValueError("No se pueden enviar mensajes vacios")
                        self.enviar_sms(receptor, texto)
                    else:
                        os.system('cls')
                        print("Opción inválida, intente nuevamente")
                except ValueError as e:
                    os.system('cls')
                    print(e)
                input("Presione cualquier tecla para volver al menu de la Mensajeria... ")
                os.system('cls')
            elif opcion == "2":
                os.system("cls")
                try:
                    self.ver_bandeja_de_entrada()
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de la Mensajeria... ")
                os.system('cls')
            elif opcion == "3":
                os.system('cls')
                try:
                    recientes = self.ver_chats_recientes()
                    indice = input("Ingrese el número del chat deseado: ")
                    while not MensajesApp.validar_indice(indice, len(recientes)):
                        indice = input("Entrada incorrecta. Ingrese el número del chat deseado: ")
                    emisor = recientes[int(indice)-1]
                    contacto = self.nombre_contacto(emisor) if self.numero_en_contactos(emisor) else None
                    self.ver_mensajes_de(emisor,contacto)
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de la Mensajeria... ")
                os.system('cls')
            elif opcion == "4":
                os.system('cls')
                try:
                    self.ver_bandeja_de_entrada()
                    indice = input("Ingrese el número del mensaje a eliminar: ")
                    while not MensajesApp.validar_indice(indice, len(self.mensajes)):
                        indice = input("Entrada incorrecta. Ingrese el número del mensaje a eliminar: ")
                    self.eliminar_mensaje(int(indice))
                except ValueError as e:
                    print(e)
                except IndexError:
                    print("Error al eliminar mensaje intente nuevamente")
                input("Presione cualquier tecla para volver al menu de la Mensajeria...")
                os.system('cls')
            elif opcion == "5":
                os.system('cls')
                print("Saliendo de la aplicacion de Mensajes...")
                salir = True
            else:
                os.system('cls')
                print("Opción inválida, intente nuevamente")
                input("Presione cualquier tecla para volver al menu de Mensajes...")
                os.system('cls')

    def __str__(self):
        return f"Aplicacion Mensajeria del numero: {self.numero_cel}"
