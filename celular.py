from Apps.configuracion import Configuracion
from central import Central
from Apps.configuracion import ConfigApp
from Apps.appstore import AppStore
from Apps.telefono import TelefonoApp
from Apps.mensajeriaSMS import MensajesApp
from Apps.mail import MailApp
from Apps.contactos import ContactosApp
from funciones_utiles import tamanio_a_bytes
import csv
import uuid

class Celular:
    central = Central()
    
    def __init__(self, nombre, modelo, numero, sistema_operativo, memoria_ram, almacenamiento):
        #Almaceno los parámetros no modificables por Configuración
        self.id = uuid.uuid4() #Genera un UUID (Universal Unique Identifier) para el dispositivo
        self.modelo = modelo
        self.numero = numero
        self.sistema_operativo = sistema_operativo
        self.memoria_ram = memoria_ram
        self.almacenamiento = tamanio_a_bytes(almacenamiento)
        self.nombre = nombre
        
        self.encendido = False
        self.bloqueado = False
        
        self.aplicaciones = {}
        self.descargar_apps_basicas(self.nombre, self.almacenamiento, self.numero, self.aplicaciones)
 
    def descargar_apps_basicas(self, nombre, almacenamiento, numero, aplicaciones):
        self.aplicaciones["Configuracion"] = ConfigApp(Configuracion(nombre, almacenamiento, Celular.central, numero, aplicaciones))
        self.aplicaciones["Contactos"] = ContactosApp()
        self.aplicaciones["Mensajes"] = MensajesApp(numero, Celular.central)
        self.aplicaciones["Mail"] = MailApp(numero, Celular.central)
        self.aplicaciones["AppStore"] = AppStore(self.aplicaciones, self.aplicaciones["Configuracion"])
        self.aplicaciones["Telefono"] = TelefonoApp(numero, Celular.central, self.aplicaciones["Contactos"])
        
    def encencer_dispositivo(self):
        if self.encendido:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra encendido ")
    
        self.encendido = True
        self.aplicaciones["Configuracion"].set_servicio(True)
        self.central.registrar_dispositivo(self.numero, self)
        print(f"Se ha encencido el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
        try :
            self.aplicaciones["Mensajes"].registrar_mensajes()    
        except ValueError as e:
            print(e)
            
    def apagar_dispositivo(self):
        if not self.encendido:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra apagado ")
        
        self.encendido = False
        self.aplicaciones["Configuracion"].set_servicio(False)
        print(f"Se ha apagado el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
            
    
    def bloquear_dispositivo(self):
        if self.bloqueado:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra bloqueado ")
        if not(self.encendido):
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} se encuentra apagado")
        
        self.bloqueado = True
        print(f"Se ha bloqueado el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
    
    def desbloquear_dispositivo(self, contrasenia = None):
        if self.bloqueado and (contrasenia == self.aplicaciones['Configuracion'].get_contrasenia() or contrasenia is None) and self.encendido:
            self.bloqueado = False
            print(f"Se ha desbloqueado el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
        elif not(self.bloqueado):
            raise ValueError(f"El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra desbloqueado")
        elif not(self.encendido):
            raise ValueError(f"El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} se encuentra apagado")
        else:
            raise ValueError("La contraseña ingresada es incorrecta")
    
    def get_numero(self) -> str:
        return self.numero
    
    def __str__(self) -> str:
        return f"ID: {self.id}\nNombre: {self.aplicaciones['Configuracion'].get_nombre()}\nModelo: {self.modelo}\nSistema operativo: {self.sistema_operativo}\nMemoria RAM: {self.memoria_ram}\nAlmacenamiento: {self.almacenamiento}"

    def guardar_datos(self, filename): #ESTE METODO Y EL DE ABAJO HAY Q PASARLO AL EXPORTADOR Y HAY Q AGREGAR UNA VARIABLE CON TODOS LOS CELULARES
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'nombre', 'modelo', 'numero', 'sistema_operativo', 'memoria_ram', 'almacenamiento', 'aplicaciones'])
            aplicaciones = ','.join(self.aplicaciones.keys())
            writer.writerow([self.id, self.nombre, self.modelo, self.numero, self.sistema_operativo, self.memoria_ram, self.almacenamiento, aplicaciones])

    @staticmethod
    def cargar_datos(filename):
        celulares = []
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                celular = Celular(row['nombre'], row['modelo'], row['numero'], row['sistema_operativo'], row['memoria_ram'], row['almacenamiento'])
                aplicaciones = row['aplicaciones'].split(',')
                for app in aplicaciones:
                    if app == "Configuracion":
                        celular.aplicaciones[app] = ConfigApp(Configuracion(celular.nombre, celular.almacenamiento, Celular.central, celular.numero))
                    elif app == "Telefono":
                        celular.aplicaciones[app] = TelefonoApp(celular.numero, Celular.central)
                    elif app == "Mensajes":
                        celular.aplicaciones[app] = MensajesApp(celular.numero, Celular.central)
                    elif app == "AppStore":
                        celular.aplicaciones[app] = AppStore(celular.aplicaciones, celular.aplicaciones["Configuracion"])
                    else:
                        celular.aplicaciones[app] = None
                celulares.append(celular)
        return celulares

    def lanzar_app(self,nombre_app):
        if nombre_app not in self.aplicaciones:
            raise ValueError(f"La aplicación {nombre_app} no se encuentra instalada")
        elif self.bloqueado:
            raise ValueError("El dispositivo se encuentra bloqueado")
        elif self.encendido:
            return self.aplicaciones[nombre_app]
        else:
            raise ValueError("El dispositivo se encuentra apagado")
        
if __name__ =="__main__":
    pass