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
        if not numero.isdigit():
            raise ValueError("El número de teléfono debe contener solo dígitos")
        if not nombre:
            raise ValueError("El nombre del contacto no puede estar vacío")
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
        if numero not in self.agenda:
            raise ValueError("Número no encontrado en la agenda")
        del self.agenda[numero]
        print(f"Contacto con número {numero} eliminado con éxito")
 
    
    def menu_navegacion(self):
        """
        Muestra el menú de navegación de la aplicación de Contactos.
        Permite al usuario agregar, ver y eliminar contactos, o salir de la aplicación.
        """
        
        os.system('cls')
        print("Bienvenido a tus Contactos")
        salir = False
        while not salir:
            os.system('cls')
            print("Menu de Contactos:")
            print("1. Agendar contacto")
            print("2. Ver contactos")
            print("3. Eliminar contacto")
            print("4. Actualizar contacto")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                os.system("cls")
                print("Agendar contacto")
                nombre = input("Ingrese el nombre del contacto: ")
                numero = input("Ingrese el número de teléfono: ")
                try:
                    self.agregar_contacto(numero, nombre)
                    print(f"Contacto de {nombre} agregado con éxito")
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Contactos...")
                os.system('cls')
            elif opcion == "2":
                os.system("cls")
                print("Contactos:")
                if not self.agenda:
                    print("No hay contactos en la agenda")
                else:
                    for numero, nombre in self.agenda.items():
                        print(f"Nombre: {nombre}       Número: {numero}")
                input("Presione cualquier tecla para volver al menu de Contactos...")
                os.system('cls')
            elif opcion == "3":
                os.system("cls")
                print("Eliminar contacto:")
                contacto = input("Ingrese el número de teléfono del contacto a eliminar: ")
                try:
                    self.eliminar_contacto(contacto)
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Contactos...")
                os.system('cls')
            elif opcion == "4":
                os.system('cls')
                print("Actualizar contacto:")
                contacto = input("Ingrese el nombre del contacto que desea actualizar: ")
                try:
                    for numero, nombre in self.agenda.items():
                        if nombre == contacto:
                            nuevo_nombre = input("Ingrese el nuevo nombre del contacto: ")
                            nuevo_numero = input("Ingrese el nuevo número de teléfono: ")
                            self.agregar_contacto(nuevo_numero, nuevo_nombre)
                            self.eliminar_contacto(numero)
                            print("Contacto actualizado con éxito")
                            break
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menú del celular...")
                os.system('cls')
            elif opcion == "5":
                os.system('cls')
                print("Saliendo de la aplicación de Contactos...")
                salir = True
                input("Presione cualquier tecla para volver al menú del celular...")
                os.system('cls')
            else:
                os.system('cls')
                print("Opción inválida")
                input("Presione cualquier tecla para volver al menú del celular...")
                os.system('cls')
