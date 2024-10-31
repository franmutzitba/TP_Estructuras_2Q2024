from Apps.aplicacion import Aplicacion
from central import Central
from comunicacion import Llamada
from Apps.contactos import ContactosApp
import datetime
import os

class TelefonoApp(Aplicacion):
    """
    Clase que representa la aplicación de Teléfono.
    Hereda de la clase Aplicacion.
    """

    def __init__(self, numero, central, contactos):
        """
        Inicializa la clase TelefonoApp con un número, una central y una instancia de ContactosApp.

        Args:
            numero (str): El número de teléfono del dispositivo.
            central (Central): La instancia de la central telefónica.
            contactos (ContactosApp): La instancia de la aplicación de contactos.
        """
        super().__init__(nombre="Telefono", tamanio="200 MB", esencial=True)
        self.numero = numero
        self.contactos = contactos  # pedir la instancia de contactos creada en ese celular
        self.central = central

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
        Obtiene el nombre del contacto asociado a un número de teléfono.

        Args:
            numero (str): El número de teléfono del contacto.

        Returns:
            str: El nombre del contacto, o None si el número no está en la lista de contactos.
        """
        return self.contactos.get(numero)

    def iniciar_llamada_contacto(self, item, duracion):
        """
        Inicia una llamada a un contacto por su índice en la lista de contactos.

        Args:
            item (int): El índice del contacto en la lista de contactos.
            duracion (int): La duración de la llamada en minutos.
            hora_inicio (datetime): La hora de inicio de la llamada.

        Raises:
            ValueError: Si el índice del contacto es inválido.
        """
        indice = int(item) - 1
        if indice < 0 or indice >= len(self.contactos.agenda):
            raise ValueError("El contacto seleccionado no existe")
        numero_receptor = list(self.contactos.agenda.keys())[indice]
        self.iniciar_llamada(numero_receptor, duracion)

    def iniciar_llamada(self, numero_receptor, duracion=5):
        """
        Inicia una llamada a un número de receptor con una duración específica.

        Args:
            numero_receptor (str): El número del receptor.
            duracion (int): La duración de la llamada en minutos. Por defecto es 5 minutos.

        Raises:
            ValueError: Si la duración de la llamada es mayor a 1440 minutos (24 horas).
        """
        if duracion > 1440:
            raise ValueError("La duracion no puede ser mayor a 24hs (1440 minutos)")

        hora_inicio = datetime.datetime.now()
        duracion = datetime.timedelta(minutes=duracion)
        self.central.manejar_llamada(self.numero, numero_receptor, hora_inicio, duracion)

    def mostrar_historial_llamadas(self):
        """
        Muestra el historial de llamadas.
        """
        #cuando se termine lo comentamos bien
        historial_personal = []
        for receptor, historial_receptor in self.central.registro_llamadas.values():                 #guarda todas las llamadas en la lista
            for emisor, historial_emisor_receptor in self.central.registro_llamadas[receptor].values():
                for llamada in historial_emisor_receptor:
                    if llamada.emisor == self.numero or llamada.receptor == self.numero:
                        historial_personal.append(llamada)  # falta terminar pero no lo entiendo
        
        
        historial_organizado = []                                   #cambia los numeros por contactos cuando corresponde
        for llamada in historial_personal:
            if llamada.perdida:
                tipo = "Llamada perdida"
            else:
                tipo = "Llamada realizada"
            
            if llamada.emisor == self.numero:
                emisor = "Usted"
                if llamada.receptor in self.contactos:
                    receptor = self.contactos[llamada.receptor]     #busca el nombre del contacto
                else:
                    receptor = llamada.receptor
            elif llamada.receptor == self.numero:
                receptor = "Usted"
                if llamada.emisor in self.contactos:
                    emisor = self.contactos[llamada.emisor]
                else:
                    emisor = llamada.emisor

                datos_llamada = (llamada.fecha, emisor, receptor, tipo, llamada.duracion)
                historial_organizado.append(datos_llamada)
        
        historial_en_orden = sorted(historial_organizado, key=self.fecha_en_tupla)
        print("Historial de llamadas:")
        for llamada in historial_en_orden:
            print(f"Fecha: {llamada[0]}, emisor: {llamada[1]}, receptor: {llamada[2]}, tipo de llamada: {llamada[3]}, duracion: {llamada[4]} minutos")


    @staticmethod
    def fecha_en_tupla(tupla):
        return tupla[0]

    def menu_navegacion(self):
        """
        Muestra el menú de navegación de la aplicación de teléfono.
        Permite al usuario iniciar llamadas, ver contactos y salir de la aplicación.
        """
        salir = False
        while not salir:
            print("Menu de navegacion de la aplicacion Telefono")
            print("1. Iniciar llamada")
            print("2. Iniciar llamada a contacto")
            print("3. Mostrar historial de llamadas")
            print("4. Salir de la aplicacion")
            opcion = int(input("Ingrese el numero de la opcion deseada: "))
            if opcion == "1":
                os.system("cls")
                receptor = input("Ingrese el numero del receptor: ")
                duracion = int(input("Ingrese la duracion de la llamada en minutos: "))
                self.iniciar_llamada(receptor, duracion)
            elif opcion == "2":
                os.system("cls")
                print(self.contactos)
                item_receptor = input("Ingrese el indice del contacto al que desea llamar: ")
                duracion = int(input("Ingrese la duracion de la llamada en minutos: "))
                # hora_inicio = datetime.datetime.now()    no se quien lo puso pero ya se hace en iniciar_llamada
                self.iniciar_llamada_contacto(item_receptor, duracion)
            elif opcion == "3":
                os.system("cls")
                self.mostrar_historial_llamadas()
            elif opcion == "4":
                os.system("cls")
                print("Saliendo de la aplicacion Telefono...")
                salir = True
                input("Presione cualquier tecla para volver al menú del celular...")
                os.system('cls')
            else:
                print("Opción inválida")
            input("Presione cualquier tecla para volver al menú del celular...")
