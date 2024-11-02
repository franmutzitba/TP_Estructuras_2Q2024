"""
Modulo de celular
"""

import os
import uuid
import re
from Apps.configuracion import Configuracion, ConfigApp
from Apps.appstore import AppStore
from Apps.telefono import TelefonoApp
from Apps.mensajeriaSMS import MensajesApp
from Apps.mail import MailApp
from Apps.contactos import ContactosApp
from funciones_utiles import tamanio_a_bytes
from central import Central

class Celular:
    """
    Clase que representa un celular con sus respectivas características 
    y aplicaciones. Contiene los métodos necesarios para encender, apagar,
    bloquear y desbloquear el dispositivo, así como para lanzar aplicaciones.
    El resto de las funcionalidades se encuentran en las aplicaciones.
    
    Atributos:
    ----------
    id_celular (uuid):
        Identificador único del celular.
    modelo (str):
        Modelo del celular.
    sistema_operativo (str):
        Sistema operativo del celular.
    memoria_ram (str):
        Memoria RAM del celular.
    almacenamiento (str):
        Almacenamiento del celular.
    encendido (bool):
        Indica si el dispositivo está encendido.
    bloqueado (bool):
        Indica si el dispositivo está bloqueado.
    aplicaciones (dict):
        Diccionario que contiene las aplicaciones instaladas en el celular.
        
    Métodos:
    --------
    encender_dispositivo():
        Enciende el dispositivo.
    apagar_dispositivo():
        Apaga el dispositivo.
    bloquear_dispositivo():
        Bloquea el dispositivo.
    desbloquear_dispositivo(contrasenia: str):
        Desbloquea el dispositivo.
    get_nombre():
        Retorna el nombre del dispositivo.
    get_almacenamiento_disponible():
        Retorna el almacenamiento disponible del dispositivo.
    lanzar_app(nombre_app: str):
        Lanza una aplicación del dispositivo, validando si el dispositivo está bloqueado o apagado.
    menu_navegacion():
        Menú de navegación del dispositivo
    """
    central = Central()

    def __init__(self, nombre, modelo, numero, sistema_operativo, memoria_ram, almacenamiento, id_celular = uuid.uuid4()):
        if not nombre or not modelo or not numero or not sistema_operativo or not memoria_ram or not almacenamiento:
            raise ValueError("Los campos no pueden estar vacíos")
        if not bool(re.match(r"^\d+(\.\d+)?\s*[KMGTP]?B?$", almacenamiento)):
            raise ValueError("El campo almacenamiento debe ser un número seguido de un espacio y una unidad de medida válida")
        #Se fija que haya espacio suficiente para las aplicaciones básicas
        if tamanio_a_bytes(almacenamiento) < tamanio_a_bytes("1.5 GB"):
            raise ValueError("El almacenamiento no es suficiente para las aplicaciones básicas")
        
        #Almaceno los parámetros no modificables por Configuración
        self.id_celular = id_celular #Genera un UUID (Universal Unique Identifier) para el celular
        self.modelo = modelo
        self.sistema_operativo = sistema_operativo
        self.memoria_ram = memoria_ram

        self.encendido = False
        self.bloqueado = False

        self.aplicaciones = {}
        self.descargar_apps_basicas(nombre, tamanio_a_bytes(almacenamiento), numero, self.aplicaciones)

    def descargar_apps_basicas(self, nombre, almacenamiento, numero, aplicaciones):
        """Descarga las aplicaciones básicas del celular
        Recibe los parámetros necesarios para la creación de las aplicaciones básicas
        """
        self.aplicaciones["Configuracion"] = ConfigApp(Configuracion(nombre, almacenamiento, Celular.central, numero, aplicaciones))
        self.aplicaciones["Contactos"] = ContactosApp()
        self.aplicaciones["Mensajes"] = MensajesApp(numero, self.aplicaciones["Contactos"], Celular.central)
        self.aplicaciones["Mail"] = MailApp(numero, Celular.central)
        self.aplicaciones["AppStore"] = AppStore(self.aplicaciones, self.aplicaciones["Configuracion"])
        self.aplicaciones["Telefono"] = TelefonoApp(numero, Celular.central, self.aplicaciones["Contactos"])

    def encender_dispositivo(self):
        """
        Método que enciende el dispositivo
        
        Returns:
            None
            
        Raises:
            ValueError: Si el dispositivo ya se encuentra encendido
        """
        if self.encendido:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra encendido ")

        self.encendido = True
        if not self.central.esta_registrado(self.aplicaciones["Configuracion"].get_numero()):
            self.central.registrar_dispositivo(self.aplicaciones["Configuracion"].get_numero(), self)
        self.aplicaciones["Configuracion"].set_servicio(True)

        print(f"Se ha encencido el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")

    def apagar_dispositivo(self):
        """
        Método que apaga el dispositivo
        
        Returns:
            None
            
        Raises:
            ValueError: Si el dispositivo ya se encuentra apagado
        """
        if not self.encendido:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra apagado ")

        self.encendido = False
        self.aplicaciones["Configuracion"].set_servicio(False)
        print(f"Se ha apagado el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")

    def bloquear_dispositivo(self):
        """
        Método que bloquea el dispositivo
        
        Returns:
            None
        
        Raises:
            ValueError: Si el dispositivo ya se encuentra bloqueado
            ValueError: Si el dispositivo se encuentra apagado
        """
        if self.bloqueado:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra bloqueado ")
        if not self.encendido:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} se encuentra apagado")

        self.bloqueado = True
        print(f"Se ha bloqueado el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")

    def desbloquear_dispositivo(self, contrasenia = None):
        """
        Método que desbloquea el dispositivo
        
        Args:
            contrasenia (str): Contraseña para desbloquear el dispositivo
        
        Returns:
            None
        
        Raises:
            ValueError: Si el dispositivo ya se encuentra desbloqueado
            ValueError: Si el dispositivo se encuentra apagado
            ValueError: Si la contraseña ingresada es incorrecta
        """
        if self.bloqueado and contrasenia == self.aplicaciones['Configuracion'].get_contrasenia() and self.encendido:
            self.bloqueado = False
            print(f"Se ha desbloqueado el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
        elif not self.encendido:
            raise ValueError(f"El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} se encuentra apagado")
        elif not self.bloqueado:
            raise ValueError(f"El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra desbloqueado")
        else:
            raise ValueError("La contraseña ingresada es incorrecta")

    def get_nombre(self):
        """Método que retorna el nombre del dispositivo"""
        return self.aplicaciones['Configuracion'].get_nombre()

    def get_almacenamiento_disponible(self):
        """Método que retorna el almacenamiento disponible del dispositivo"""
        return self.aplicaciones['Configuracion'].get_almacenamiento_disponible()

    def __str__(self):
        return f"ID: {self.id_celular}\nNombre: {self.aplicaciones['Configuracion'].get_nombre()}\nModelo: {self.modelo}\nSistema operativo: {self.sistema_operativo}\nMemoria RAM: {self.memoria_ram}\nAlmacenamiento: {self.aplicaciones['Configuracion'].get_almacenamiento_disponible()}\n"

    # Esta por verse si lo hacemos o no... Por ahora ignorar
    # def guardar_datos(self, filename): #ESTE METODO Y EL DE ABAJO HAY Q PASARLO AL EXPORTADOR Y HAY Q AGREGAR UNA VARIABLE CON TODOS LOS CELULARES
    #     with open(filename, mode='w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(['id', 'nombre', 'modelo', 'numero', 'sistema_operativo', 'memoria_ram', 'almacenamiento', 'aplicaciones'])
    #         aplicaciones = ','.join(self.aplicaciones.keys())
    #         writer.writerow([self.id, self.aplicaciones['Configuracion'].get_nombre(), self.modelo, self.numero, self.sistema_operativo, self.memoria_ram, self.almacenamiento, aplicaciones])

    # @staticmethod
    # def cargar_datos(filename):
    #     celulares = []
    #     with open(filename, mode='r') as file:
    #         reader = csv.DictReader(file)
    #         for row in reader:
    #             celular = Celular(row['nombre'], row['modelo'], row['numero'], row['sistema_operativo'], row['memoria_ram'], row['almacenamiento'])
    #             aplicaciones = row['aplicaciones'].split(',')
    #             for app in aplicaciones:
    #                 if app == "Configuracion":
    #                     celular.aplicaciones[app] = ConfigApp(Configuracion(aplicaciones['Configuracion'].get_nombre(), celular.almacenamiento, Celular.central, celular.numero))
    #                 elif app == "Telefono":
    #                     celular.aplicaciones[app] = TelefonoApp(celular.numero, Celular.central)
    #                 elif app == "Mensajes":
    #                     celular.aplicaciones[app] = MensajesApp(celular.numero, Celular.central)
    #                 elif app == "AppStore":
    #                     celular.aplicaciones[app] = AppStore(celular.aplicaciones, celular.aplicaciones["Configuracion"])
    #                 else:
    #                     celular.aplicaciones[app] = None
    #             celulares.append(celular)
    #     return celulares

    def lanzar_app(self,nombre_app):
        """
        Método que lanza una aplicación del dispositivo.
        Verifica si el dispositivo está bloqueado, apagado o si la aplicación no se 
        encuentra instalada.
        
        Args:
            nombre_app (str): Nombre de la aplicación a lanzar
            
        Returns:
            Aplicacion: Aplicación lanzada
        
        Raises:
            ValueError: Si la aplicación no se encuentra instalada
            ValueError: Si el dispositivo se encuentra bloqueado
            ValueError: Si el dispositivo se encuentra apagado
        """
        if nombre_app not in self.aplicaciones:
            raise ValueError(f"La aplicación {nombre_app} no se encuentra instalada")
        elif self.bloqueado:
            raise ValueError("El dispositivo se encuentra bloqueado")
        elif self.encendido:
            return self.aplicaciones[nombre_app]
        else:
            raise ValueError("El dispositivo se encuentra apagado")

    def menu_navegacion(self):
        """Menú de navegación del dispositivo"""
        print("Bienvenido al celular")
        salir = False
        while not salir:
            print("Menu del celular:")
            print("1. Encender/Apagar dispositivo")
            print("2. Desbloquear/Bloquear dispositivo")
            print("3. Ver/Lanzar aplicaciones")
            print("4. Mostrar datos del dispositivo")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                os.system('cls')
                print("Encender/Apagar dispositivo")
                valor = input("Encender (1) / Apagar (0): ")
                try:
                    if valor == "1":
                        self.encender_dispositivo()
                    elif valor == "0":
                        self.apagar_dispositivo()
                    else:
                        raise ValueError("Opción no válida, intente nuevamente")
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menú del celular...")
                os.system('cls')
            elif opcion == "2":
                os.system('cls')
                print("Desbloquear/Bloquear dispositivo")
                valor = input("Desbloquear (1) / Bloquear (0): ")
                try:
                    if valor == "1":
                        contrasenia = input("Ingrese la contraseña (o presione Enter si no tiene): ")
                        self.desbloquear_dispositivo(contrasenia if contrasenia else None)
                    elif valor == "0":
                        self.bloquear_dispositivo()
                    else:
                        raise ValueError("Opción no válida, intente nuevamente")
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menú del celular...")
                os.system('cls')
            elif opcion == "3":
                os.system('cls')
                print("Ver/Lanzar aplicaciones")
                print("Aplicaciones instaladas:")
                for app in self.aplicaciones:
                    print(f"- {app}")
                nombre_app = input("Ingrese el nombre de la aplicación que desea lanzar: ")
                try:
                    print(f"Lanzando {nombre_app}...")
                    self.lanzar_app(nombre_app).menu_navegacion()
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menú del celular...")
                os.system('cls')
            elif opcion == "4":
                os.system('cls')
                print("Mostrar datos del dispositivo")
                print(self)
                input("Presione cualquier tecla para volver al menú del celular...")
                os.system('cls')
            elif opcion == "5":
                salir = True
            else:
                print("Opción no válida, intente nuevamente")
                input("Presione cualquier tecla para volver al menú del celular...")
                os.system('cls')

# if __name__ =="__main__":
#     from Apps.mail import *
#     from Apps.mail import CriterioLectura
#     celular1 = Celular("iPhone de Franco", "iPhone 13", "123456789", "iOS", "4GB", "64")
#     celular2 = Celular("Samsung de Juan", "Samsung Galaxy S21", "987654321", "Android", "6GB", "128")
#     #celular2.encencer_dispositivo()
#     #celular2.desbloquear_dispositivo()
#     #celular1.encencer_dispositivo()
#     #celular1.desbloquear_dispositivo()
#     celular1.lanzar_app("Configuracion").set_datos(True)
#     celular2.lanzar_app("Configuracion").set_datos(True)
#     print(Celular.central.registro_dispositivos["987654321"])
#     print(Celular.central.registro_dispositivos["123456789"])
#     celular1.lanzar_app("Mail").crear_cuenta("franco.mutz@gmail.com", "Franco123!")
#     celular2.lanzar_app("Mail").crear_cuenta("franco.mutz2@gmail.com", "Franco123!")
#     celular1.lanzar_app("Mail").iniciar_sesion("franco.mutz@gmail.com", "Franco123!")
#     celular2.lanzar_app("Mail").iniciar_sesion("franco.mutz2@gmail.com", "Franco123!")
#     celular1.lanzar_app("Mail").enviar_mail(Mail("Hola", "franco.mutz@gmail.com", "franco.mutz2@gmail.com", "Saludo", fecha=datetime.now()))
#     celular2.lanzar_app("Mail").ver_bandeja_entrada(CriterioLectura.NO_LEIDOS_PRIMEROS)
#     celular1.lanzar_app("Mensajes").enviar_sms("987654321", "mensaje 0")
#     celular2.apagar_dispositivo()
#     celular1.lanzar_app("Mensajes").enviar_sms("987654321", "MEssi")
#     celular1.lanzar_app("Mensajes").enviar_sms("987654321", "mensaje 2")
#     celular1.lanzar_app("Mensajes").enviar_sms("987654321", "mensaje 3")
#     # print(celular1.central.registro_mensajes["987654321"].popleft())
#     print(celular2.central.registro_mensajes["987654321"][0].get_sincronizado())
#     # #print(celular2.aplicaciones["Mensajes"].mensajes[0].get_sincronizado())
#     #celular2.encencer_dispositivo()
#     celular1.lanzar_app("Mensajes").enviar_sms("987654321", "mensaje 4")
#     print(celular2.aplicaciones["Configuracion"].configuracion.modo_red)
#     print(celular2.central.registro_mensajes["987654321"][0].get_sincronizado())
#     print(celular2.aplicaciones["Mensajes"].mensajes[0].get_sincronizado())
#     celular2.lanzar_app("Contactos").agregar_contacto("123456789","Juan")
#     celular2.lanzar_app("Mensajes").ver_bandeja_de_entrada()
#     print()
#     celular2.lanzar_app("Mensajes").ver_bandeja_de_entrada()
#     celular2.lanzar_app("Mensajes").ver_chats_recientes()
#     #celular2.lanzar_app("Mensajes").menu_navegacion()
#     #celular2.menu_navegacion()
#     Celular.central.exportar_mensajes()

#     central2 = Central()
#     central2.cargar_mensajes()
#     for cola in (central2.registro_mensajes.values()):
#         for mensaje in cola:
#             print(mensaje)
#     # celular1.encencer_dispositivo()
#     # celular1.central.mostrar_dispositivos()
#     # celular1.aplicaciones["Configuracion"].set_servicio(True)
#     # celular2.aplicaciones["Configuracion"].set_servicio(True)
#     # celular1.central.mostrar_dispositivos()
#     # celular1.apagar_dispositivo()
#     # celular1.central.mostrar_dispositivos()

#     # celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()
#     # print("\n")
#     # print(celular1.aplicaciones["Configuracion"].get_almacenamiento_disponible())
#     # celular1.aplicaciones["AppStore"].descargar_app("WhatsApp")
#     # print(celular1.aplicaciones["Configuracion"].get_almacenamiento_disponible())
#     # celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()
#     # print(celular1.aplicaciones) #Las apps nuevas del appstore no van a tener ningun objeto asociado pq "no existen" como objetos
#     # celular1.aplicaciones["AppStore"].descargar_app("Zoom") #No hay espacio suficiente
#     # celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()
#     # celular1.aplicaciones["AppStore"].mostar_apps()
