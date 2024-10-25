from Apps.configuracion import Configuracion
from central import Central
from Apps.configuracion import ConfigApp
from Apps.appstore import AppStore
from Apps.telefono import TelefonoApp
from Apps.mensajeriaSMS import MensajesApp
from Apps.mail import MailApp
from Apps.contactos import ContactosApp
import csv
import uuid

class Celular:
    central = Central()
    
    def __init__(self, nombre, modelo, numero, sistema_operativo, memoria_ram, almacenamiento_gb):
        #Almaceno los parámetros no modificables por Configuración
        self.id = uuid.uuid4() #Genera un UUID (Universal Unique Identifier) para el dispositivo
        self.modelo = modelo
        self.numero = numero
        self.sistema_operativo = sistema_operativo
        self.memoria_ram = memoria_ram
        self.almacenamiento_gb = int(almacenamiento_gb)
        
        self.encendido = False
        self.bloqueado = False
        
        self.aplicaciones = {}
        self.descargar_apps_basicas(nombre, almacenamiento_gb, numero, self.aplicaciones)
 
    def descargar_apps_basicas(self, nombre, almacenamiento_gb, numero, aplicaciones):
        self.aplicaciones["Configuracion"] = ConfigApp(Configuracion(nombre, almacenamiento_gb, Celular.central, numero, aplicaciones))
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
        return f"ID: {self.id}\nNombre: {self.aplicaciones['Configuracion'].get_nombre()}\nModelo: {self.modelo}\nSistema operativo: {self.sistema_operativo}\nMemoria RAM: {self.memoria_ram}\nAlmacenamiento: {self.almacenamiento_gb}"

    def guardar_datos(self, filename): #ESTE METODO Y EL DE ABAJO HAY Q PASARLO AL EXPORTADOR Y HAY Q AGREGAR UNA VARIABLE CON TODOS LOS CELULARES
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'nombre', 'modelo', 'numero', 'sistema_operativo', 'memoria_ram', 'almacenamiento_gb', 'aplicaciones'])
            aplicaciones = ','.join(self.aplicaciones.keys())
            writer.writerow([self.id, self.nombre, self.modelo, self.numero, self.sistema_operativo, self.memoria_ram, self.almacenamiento_gb, aplicaciones])

    @staticmethod
    def cargar_datos(filename):
        celulares = []
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                celular = Celular(row['nombre'], row['modelo'], row['numero'], row['sistema_operativo'], row['memoria_ram'], row['almacenamiento_gb'])
                aplicaciones = row['aplicaciones'].split(',')
                for app in aplicaciones:
                    if app == "Configuracion":
                        celular.aplicaciones[app] = ConfigApp(Configuracion(celular.nombre, celular.almacenamiento_gb, Celular.central, celular.numero))
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
    from Apps.mail import *
    from Apps.mail import CriterioLectura
    celular1 = Celular("iPhone de Franco", "iPhone 13", "123456789", "iOS", "4GB", "64")
    celular2 = Celular("Samsung de Juan", "Samsung Galaxy S21", "987654321", "Android", "6GB", "128")
    celular2.encencer_dispositivo()
    #celular2.desbloquear_dispositivo()
    celular1.encencer_dispositivo()
    #celular1.desbloquear_dispositivo()
    celular1.lanzar_app("Configuracion").set_datos(True)
    celular2.lanzar_app("Configuracion").set_datos(True)
    print(Celular.central.registro_dispositivos["987654321"])
    print(Celular.central.registro_dispositivos["123456789"])
    
    celular1.lanzar_app("Mail").crear_cuenta("franco.mutz@gmail.com", "Franco123!")
    celular2.lanzar_app("Mail").crear_cuenta("franco.mutz2@gmail.com", "Franco123!")
    celular1.lanzar_app("Mail").iniciar_sesion("franco.mutz@gmail.com", "Franco123!")
    celular2.lanzar_app("Mail").iniciar_sesion("franco.mutz2@gmail.com", "Franco123!")
    
    celular1.lanzar_app("Mail").enviar_mail(Mail("Hola", "franco.mutz@gmail.com", "franco.mutz2@gmail.com", "Saludo"))
    celular2.lanzar_app("Mail").ver_bandeja_entrada(CriterioLectura.NO_LEIDOS_PRIMEROS)
    
    celular2.apagar_dispositivo()
    celular1.lanzar_app("Mensajes").enviar_sms("987654321", "MEssi")
    # print(celular1.central.registro_mensajes["987654321"].popleft())
    celular2.encencer_dispositivo()
    

    
    # celular1.encencer_dispositivo()
    # celular1.central.mostrar_dispositivos()
    # celular1.aplicaciones["Configuracion"].set_servicio(True)
    # celular2.aplicaciones["Configuracion"].set_servicio(True)
    # celular1.central.mostrar_dispositivos()
    # celular1.apagar_dispositivo()
    # celular1.central.mostrar_dispositivos()

    # celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()
    # print("\n") 
    # print(celular1.aplicaciones["Configuracion"].get_almacenamiento_disponible())
    # celular1.aplicaciones["AppStore"].descargar_app("WhatsApp")
    # print(celular1.aplicaciones["Configuracion"].get_almacenamiento_disponible())
    # celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()
    # print(celular1.aplicaciones) #Las apps nuevas del appstore no van a tener ningun objeto asociado pq "no existen" como objetos
    # celular1.aplicaciones["AppStore"].descargar_app("Zoom") #No hay espacio suficiente
    # celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()
    # celular1.aplicaciones["AppStore"].mostar_apps()
    