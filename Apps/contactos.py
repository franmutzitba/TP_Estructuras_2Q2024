from Apps.aplicacion import Aplicacion
import os

class ContactosApp(Aplicacion):
    """
    Clase que representa la aplicación de Contactos.
    Hereda de la clase Aplicacion.
    """

    def __init__(self):
        """
        Inicializa la aplicación de Contactos con un nombre, tamaño y esencialidad.
        También inicializa una agenda vacía.
        """
        super().__init__(nombre="Contactos", tamanio="800 MB", esencial=True)
        self.agenda = {}

    def get_contactos(self):
        """
        Devuelve la agenda de contactos.

        Returns:
            dict: La agenda de contactos.
        """
        return self.agenda

    def agregar_contacto(self, numero, nombre):
        """
        Agrega un contacto a la agenda.

        Args:
            numero (str): El número de teléfono del contacto.
            nombre (str): El nombre del contacto.
        """
        self.agenda[numero] = nombre
    
    def __str__(self):
        """
        Devuelve una representación en cadena de la agenda de contactos.

        Returns:
            str: La representación en cadena de la agenda de contactos.
        """
        if not self.agenda:
            return "Agenda de contactos vacía"
        agenda = ""
        item = 1
        for numero, nombre in self.agenda.items():
            agenda += f"\n {item} Nombre: {nombre}       Número: {numero}"
            item += 1
        return f"Agenda de contactos:{agenda}"
    
    def eliminar_contacto(self, numero):
        """
        Elimina un contacto de la agenda.

        Args:
            numero (str): El número de teléfono del contacto a eliminar.
        """
        if numero in self.agenda:
            del self.agenda[numero]
            print(f"Contacto con número {numero} eliminado con éxito")
        else:
            print("Número no encontrado en la agenda")
    
    def menu_navegacion(self):
        """
        Muestra el menú de navegación de la aplicación de Contactos.
        Permite al usuario agregar, ver y eliminar contactos, o salir de la aplicación.
        """
        salir = False
        while not salir:
            os.system('cls')
            print("Bienvenido a tus Contactos")
            print("1. Agregar contacto")
            print("2. Ver contactos")
            print("3. Eliminar contacto")
            print("4. Salir")
            opcion = input("Ingrese una opción: ")
            os.system('cls')
            if opcion == "1":
                os.system("cls")
                numero = input("Ingrese el número de teléfono: ")
                nombre = input("Ingrese el nombre del contacto: ")
                self.agregar_contacto(numero, nombre)
                print(f"Contacto de {nombre} agregado con éxito")
            elif opcion == "2":
                os.system("cls")
                print(self)
            elif opcion == "3":
                os.system("cls")
                contacto = input("Ingrese el número de teléfono del contacto a eliminar: ")
                self.eliminar_contacto(contacto)
            elif opcion == "4":
                os.system('cls')
                print("Saliendo de Contactos...")
                salir = True
                input("Presione cualquier tecla para volver al menú del celular...")
                os.system('cls')
            else:
                print("Opción inválida")
            input("Presione cualquier tecla para volver al menú del celular...")