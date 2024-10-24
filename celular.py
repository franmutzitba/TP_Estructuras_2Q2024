from configuracion import Configuracion
from configuracion import ConfigApp
from appstore import AppStore
from telefono import TelefonoApp
from central import Central
from mensajeriaSMS import MensajesApp
import csv
import uuid

class Celular:
    central = Central()
    
    def __init__(self, nombre, modelo, numero, sistema, memoria_ram, almacenamiento_gb):
        #Almaceno los parámetros no modificables por Configuración
        self.id = uuid.uuid4() #Genera un UUID (Universal Unique Identifier) para el dispositivo
        self.modelo = modelo
        self.numero = numero
        self.sistema_operativo = sistema
        self.memoria_ram = memoria_ram
        self.almacenamiento_gb = int(almacenamiento_gb)
        
        self.encendido = False
        self.bloqueado = False
        
        self.aplicaciones = {}
        self.descargar_apps_basicas(nombre, almacenamiento_gb, numero, self.aplicaciones)
 
    def descargar_apps_basicas(self, nombre, almacenamiento_gb, numero, aplicaciones):
        self.aplicaciones["Configuracion"] = ConfigApp(Configuracion(nombre, almacenamiento_gb, Celular.central, numero, aplicaciones))
        self.aplicaciones["Telefono"] = TelefonoApp(numero, Celular.central)
        self.aplicaciones["Mensajes"] = MensajesApp(numero, Celular.central)
        self.aplicaciones["Mail"] = None
        self.aplicaciones["AppStore"] = AppStore(self.aplicaciones, self.aplicaciones["Configuracion"])
        
    def encencer_dispositivo(self):
        if self.encendido:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra encendido ")
        else:
            self.encendido = True
            self.aplicaciones["Configuracion"].set_servicio(True)
            print(f"Se ha encencido el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
            
    def apagar_dispositivo(self):
        if self.encendido:
            self.encendido = False
            self.aplicaciones["Configuracion"].set_servicio(False)
            print(f"Se ha apagado el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
        else:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra apagado ")
    
    def bloquear_dispositivo(self):
        if self.bloqueado:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra bloqueado ")
        elif not(self.encendido):
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} se encuentra apagado")
        else:
            self.bloqueado = True
            print(f"Se ha bloqueado el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
    
    def desbloquear_dispositivo(self, contrasenia = None):
        if self.bloqueado and (contrasenia == self.aplicaciones['Configuracion'].get_contrasenia() or contrasenia == None) and self.encendido:
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
        
if __name__== "__main__":
    celular1 = Celular("Samsung", "Galaxy", "123456789", "Android", "2GB", "16")
    celular2 = Celular("iPhone", "11", "987654321", "iOS", "4GB", "64")
    #celular1.aplicaciones["AppStore"].desinstalar_app("Wasap")
    celular1.aplicaciones["Configuracion"].listar_aplicaciones()
    
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
    