"""
Módulo que contiene la clase Calculadora.
"""

import os
from Apps.aplicacion import Aplicacion

class CalculadoraApp(Aplicacion):
    """Clase que representa la aplicación de calculadora."""
    def __init__(self, nombre = "Calculadora", tamanio = "1.1 GB" , esencial = False):
        """
        Args:
            nombre (str): El nombre de la aplicación.
            tamanio (str): El tamaño de la aplicación.
            esencial (bool): Indica si la aplicación es esencial o no. Por defecto es False.
        """
        super().__init__(nombre, tamanio, esencial)

    def suma(self, num1, num2):
        """
        Realiza una suma de dos números.

        Args:
            num1 (int): El primer número.
            num2 (int): El segundo número.

        Returns:
            int: El resultado de la suma.
        """
        return num1 + num2

    def resta(self, num1, num2):
        """
        Realiza una resta de dos números.

        Args:
            num1 (int): El primer número.
            num2 (int): El segundo número.

        Returns:
            int: El resultado de la resta.
        """
        return num1 - num2

    def multiplicacion(self, num1, num2):
        """
        Realiza una multiplicación de dos números.

        Args:
            num1 (int): El primer número.
            num2 (int): El segundo número.

        Returns:
            int: El resultado de la multiplicación.
        """
        return num1 * num2

    def division(self, num1, num2):
        """
        Realiza una division de dos números.

        Args:
            num1 (int): El primer número.
            num2 (int): El segundo número.

        Returns:
            int: El resultado de la division.
        """
        return num1 / num2

    def validar_numero(self, numero):
        """
        Valida si un string es un número.

        Args:
            numero (str): El string a validar.

        Returns:
            bool: True si el string es un número, False en caso contrario.
        """
        try:
            float(numero)
            return True
        except ValueError:
            return False

    def menu_navegacion(self):
        """
        Muestra el menú de navegación de la aplicación de calculadora.
        Permite al usuario realizar operaciones aritmeticas y salir de la aplicación.
        """
        os.system('cls')
        print("Bienvenido a la aplicación de Calculadora")
        salir = False
        while not salir:
            print("Menu de navegacion de la aplicacion Calculadora:")
            print("1. Sumar")
            print("2. Restar")
            print("3. Multiplicar")
            print("4. Dividir")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                os.system('cls')
                print("Sumar")

                num1 = (input("Ingrese el primer número: "))
                while not self.validar_numero(num1):
                    print("El primer número debe ser un número")
                    num1 = (input("Ingrese el primer número: "))

                num2 = (input("Ingrese el segundo número: "))
                while not self.validar_numero(num2):
                    print("El segundo número debe ser un número")
                    num2 = (input("Ingrese el segundo número: "))

                print(f"El resultado de la suma es: {self.suma(float(num1), float(num2))}")
                input("Presione cualquier tecla para volver al menu de navegación de la aplicacion Calculadora...")
                os.system('cls')
            elif opcion == "2":
                os.system('cls')
                print("Restar")
                num1 = (input("Ingrese el primer número: "))
                while not self.validar_numero(num1):
                    print("El primer número debe ser un número")
                    num1 = (input("Ingrese el primer número: "))

                num2 = (input("Ingrese el segundo número: "))    
                while not self.validar_numero(num2):
                    print("El segundo número debe ser un número")
                    num2 = (input("Ingrese el segundo número: "))
                print(f"El resultado de la resta es: {self.resta(float(num1), float(num2))}")
                input("Presione cualquier tecla para volver al menu de navegación de la aplicacion Calculadora...")
                os.system('cls')
            elif opcion == "3":
                os.system('cls')
                print("Multiplicar")
                num1 = (input("Ingrese el primer número: "))
                while not self.validar_numero(num1):
                    print("El primer número debe ser un número")
                    num1 = (input("Ingrese el primer número: "))

                num2 = (input("Ingrese el segundo número: "))
                while not self.validar_numero(num2):
                    print("El segundo número debe ser un número")
                    num2 = (input("Ingrese el segundo número: "))
                print(f"El resultado de la multiplicación es: {self.multiplicacion(float(num1), float(num2))}")
                input("Presione cualquier tecla para volver al menu de navegación de la aplicacion Calculadora...")
                os.system('cls')
            elif opcion == "4":
                os.system('cls')
                print("Dividir")
                num1 = (input("Ingrese el primer número: "))
                while not self.validar_numero(num1):
                    print("El primer número debe ser un número")
                    num1 = (input("Ingrese el primer número: "))

                num2 = (input("Ingrese el segundo número: "))
                while not self.validar_numero(num2) or float(num2) == 0:
                    print("El segundo número debe ser un número distinto de cero")
                    num2 = (input("Ingrese el segundo número: "))
                print(f"El resultado de la division es: {self.division(float(num1), float(num2))}")
                input("Presione cualquier tecla para volver al menu de navegación de la aplicacion Calculadora...")
                os.system('cls')
            elif opcion == "5":
                os.system('cls')
                salir = True
                print("Saliendo de la calculadora...")
            else:
                os.system('cls')
                print("Opción no válida, intente nuevamente")
                input("Presione cualquier tecla para volver al menú de la aplicación de Calculadora...")
