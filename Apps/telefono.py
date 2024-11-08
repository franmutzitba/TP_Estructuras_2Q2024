"""
Módulo que contiene la clase TelefonoApp. Esta clase representa la aplicación de Teléfono.
"""

import datetime
import os
from Apps.aplicacion import Aplicacion
from collections import deque

class TelefonoApp(Aplicacion):
    def __init__(self, numero, central, contactos):
        super().__init__(nombre="Telefono", tamanio="200 MB", esencial=True)
        self.numero = numero
        self.contactos = contactos.agenda  # pedir la instancia de contactos creada en ese celular
        self.central = central
        self.llamadas_iniciadas = deque()
        self.llamadas_recibidas = deque()
        
    def numero_en_contactos(self, numero):
        """
        Verifica si un número está en la lista de contactos.
        
        Args:
            numero (str): El número de teléfono a verificar.
        
        Returns:
            bool: True si el número está en la lista de contactos, False en caso contrario.
        """
        return numero in self.contactos.keys()

    def nombre_contacto(self, numero):
        
        """
        Obtiene el nombre del contacto dado un número de teléfono.
        
        Args:
            numero (str): El número de teléfono del contacto.
        
        Returns:
            str: El nombre del contacto o None si no existe.
        """
        return self.contactos.get(numero)

    def iniciar_llamada_contacto(self, item, duracion):
        """
        Inicia una llamada a un contacto por su índice en la lista de contactos.

        Args:
            item (int): El índice del contacto en la lista de contactos.
            duracion (int): La duración de la llamada en minutos.
            hora_inicio (datetime): La hora de inicio de la llamada.

        Returns:
            None
            
        Raises:
            ValueError: Si el índice del contacto es inválido.
            ValueError: Si la duración de la llamada es mayor a 1440 minutos (24 horas).
        """
        if not item.isdigit():
            raise ValueError("El índice del contacto debe ser un número entero")
        if not duracion.isdigit():
            raise ValueError("La duración de la llamada debe ser un número entero")
        indice = int(item) - 1
        if indice < 0 or indice >= len(self.contactos):
            raise ValueError("El contacto seleccionado no existe")
        numero_receptor = list(self.contactos.keys())[indice]
        self.iniciar_llamada(numero_receptor, int(duracion))

    def iniciar_llamada(self, numero_receptor, duracion=5):
    
        """
        Inicia una llamada a un número receptor con una duración especificada.

        Args:
            numero_receptor (str): Número de teléfono del receptor que debe tener 8 dígitos.
            duracion (int, optional): Duración de la llamada en minutos. El valor por defecto es 5.

        Raises:
            ValueError: Si el número de receptor no tiene 8 dígitos.
            ValueError: Si la duración es mayor a 1440 minutos (24 horas).
            ValueError: Si se intenta llamar al mismo número del emisor.

        Returns:
            None
        """
        if len(numero_receptor) != 8 or not numero_receptor.isdigit():
            raise ValueError("Numero incorrecto")
        if duracion > 1440:
            raise ValueError("La duracion no puede ser mayor a 24hs (1440 minutos)")
        if numero_receptor == self.numero:
            raise ValueError("No es posible llamarse a si mismo")

        fecha_inicio = datetime.datetime.now()
        duracion = datetime.timedelta(minutes=duracion)
        self.central.manejar_llamada(self.numero, numero_receptor, fecha_inicio, duracion)
    
    def añadir_llamada(self, llamada, iniciada = False):
        
        """
        Agrega una llamada a la lista de llamadas.
        
        Args:
            llamada (Llamada): La llamada a agregar.
            iniciada (bool, optional): True si la llamada fue iniciada por el usuario. False si la llamada fue recibida. El valor por defecto es False.
        """
        if iniciada:
            self.llamadas_iniciadas.appendleft(llamada)
        else:
            self.llamadas_recibidas.appendleft(llamada)
        
    def mostrar_historial_llamadas(self):

        """
        Muestra el historial de llamadas del teléfono.
        
        Muestra una lista con las llamadas realizadas y recibidas del teléfono,
        ordenadas de manera cronológica inversa. Si una llamada fue realizada
        o recibida por un contacto, se muestra el nombre del contacto en lugar
        del número de teléfono.
        
        Raises:
            ValueError: Si no hay llamadas registradas.
        """
        if not self.llamadas_iniciadas and not self.llamadas_recibidas:
            raise ValueError("No hay llamadas registradas.")
        llamadas = sorted(list(self.llamadas_iniciadas + self.llamadas_recibidas), key = lambda x: x.fecha, reverse=True)
        print(f"Historial de llamadas del telefono {self.numero}:")
        
        for llamada in llamadas:
            if self.numero_en_contactos(llamada.emisor):
                emisor = self.nombre_contacto(llamada.emisor)
            else:
                emisor = llamada.emisor
            if self.numero_en_contactos(llamada.receptor):
                receptor = self.nombre_contacto(llamada.receptor)
            else:
                receptor = llamada.receptor
            if llamada.emisor == self.numero:
                emisor = 'Usted'
            else:
                receptor = 'Usted'
            print(f"Emisor: {emisor}, Receptor: {receptor}, Duracion: {llamada.duracion}, Fecha: {llamada.fecha} {',(Perdida)' if llamada.perdida else ''}")

    def terminar_llamada_en_curso(self):

        """
        Termina la llamada en curso del teléfono.
        
        Raises:
            ValueError: Si no hay llamada en curso.
        """
        self.central.terminar_llamada(self.numero)
    
    def get_ultima_llamada(self):
        """
        Devuelve la última llamada realizada o recibida por el teléfono.
        
        Si no hay llamadas, devuelve None.
        
        Returns:
            Llamada: La última llamada o None si no hay llamadas.
        """
        if self.llamadas_iniciadas and self.llamadas_recibidas:
            return max(self.llamadas_iniciadas[0], self.llamadas_recibidas[0], key=lambda x: x.fecha)
        elif self.llamadas_iniciadas:
            return self.llamadas_iniciadas[0]
        elif self.llamadas_recibidas:
            return self.llamadas_recibidas[0]
        return None   
    def mostrar_contactos(self):

        """
        Muestra la lista de contactos registrados en el teléfono.

        Si no hay contactos registrados, lanza una excepción ValueError.

        Raises:
            ValueError: Si no hay contactos registrados.

        Prints:
            La lista de contactos numerados.
        """
        if not self.contactos.values():
            raise ValueError("No hay contactos registrados.")
        for i, contacto in enumerate(self.contactos.values()):
            print(f"{i+1}. {contacto}")
    
    def menu_navegacion(self):
        """
        Muestra el menú de navegación de la aplicación de teléfono.
        Permite al usuario iniciar llamadas, ver contactos y salir de la aplicación.
        """
        os.system('cls')
        print(f"Bienvenido a la aplicación de Teléfono del número {self.numero}")
        salir = False
        while not salir:
            
            print("Menu de navegacion de la aplicacion Telefono:")
            print("1. Marcar número y llamar")
            print("2. Iniciar llamada a contacto")
            print("3. Mostrar historial de llamadas")
            print("4. Finalizar llamada en curso")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                os.system("cls")
                print("Marcar número y llamar")
                receptor = input("Ingrese el número al que desea llamar: ")
                duracion = input("Ingrese la duracion de la llamada en minutos: ")
                while not duracion.isdigit():
                    print("La duración debe ser un número entero")
                    duracion = input("Ingrese la duracion de la llamada en minutos: ")  
                try:
                    self.iniciar_llamada(receptor, int(duracion))
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menú de Teléfono...")
                os.system('cls')
            elif opcion == "2":
                os.system("cls")
                print("Iniciar llamada a contacto:")
                print("Contactos:")
                try:
                    self.mostrar_contactos()
                    item_receptor = input("Ingrese el indice del contacto al que desea llamar: ")
                    duracion = input("Ingrese la duracion de la llamada en minutos: ")
                    print("")
                    self.iniciar_llamada_contacto(item_receptor, duracion)
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menú de Teléfono...")
                os.system('cls')
            elif opcion == "3":
                os.system("cls")
                print("Mostrar historial de llamadas")
                try:
                    self.mostrar_historial_llamadas()
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menú de Teléfono...")
                os.system('cls')
            elif opcion == "4":
                os.system("cls")
                print("Finalizar llamada en curso")
                try:
                    self.terminar_llamada_en_curso()
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menú de Teléfono...")
                os.system('cls')
            elif opcion == "5":
                os.system("cls")
                print("Saliendo de la aplicacion Telefono...")
                salir = True
            else:
                print("Opción inválida")
                input("Presione cualquier tecla para volver al menú de Teléfono...")
                os.system("cls")
    def __str__ (self):
        """
        Retorna una representación en cadena de la aplicación Telefono.

        Returns:
            str: La representación en cadena de la aplicación Telefono.
        """
        return f"Aplicacion Telefono del numero: {self.numero}"