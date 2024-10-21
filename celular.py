from configuracion import Configuracion
from configuracion import ConfigApp
from appstore import AppStore
from telefono import TelefonoApp
import uuid

class Celular:
    
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
        self.descargar_apps_basicas(nombre, almacenamiento_gb)
    
    def descargar_apps_basicas(self, nombre, almacenamiento_gb):
        #self.aplicaciones['Configuracion'] = ConfigApp(self.configuracion)
        self.aplicaciones["Configuracion"] = ConfigApp(Configuracion(nombre, almacenamiento_gb))
        self.aplicaciones["Telefono"] = None
        self.aplicaciones["Mensajes"] = None
        self.aplicaciones["Mail"] = None
        self.aplicaciones["AppStore"] = AppStore(self.aplicaciones, self.aplicaciones["Configuracion"])
        
    def encencer_dispositivo(self):
        if self.encendido:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra encendido ")
        else:
            self.encendido = True
            self.servicio = True
            print(f"Se ha encencido el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
            
    def apagar_dispositivo(self):
        if self.encendido:
            self.encendido = False
            print(f"Se ha apagado el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
        else:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra apagado ")
    
    def bloquear_dispositivo(self):
        if self.bloqueado:
            raise ValueError(f" El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra bloqueado ")
        else:
            self.bloqueado = True
            print(f"Se ha bloqueado el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
    
    def desbloquear_dispositivo(self, contrasenia = None):
        if self.bloqueado and (contrasenia == self.aplicaciones['Configuracion'].get_contrasenia() or contrasenia == None):
            self.bloqueado = False
            print(f"Se ha desbloqueado el dispositivo - {self.aplicaciones['Configuracion'].get_nombre()} -")
        elif not(self.bloqueado):
            raise ValueError(f"El dispositivo {self.aplicaciones['Configuracion'].get_nombre()} ya se encuentra desbloqueado")
        else:
            raise ValueError("La contraseña ingresada es incorrecta")
        
    
    def get_numero(self) -> str:
        return self.numero
    
    def __str__(self) -> str:
        return f"ID: {self.id}\nNombre: {self.aplicaciones['Configuracion'].get_nombre()}\nModelo: {self.modelo}\nSistema operativo: {self.sistema_operativo}\nMemoria RAM: {self.memoria_ram}\nAlmacenamiento: {self.almacenamiento}"



if __name__== "__main__":
    celular1 = Celular("Samsung", "Galaxy", "123456789", "Android", "2GB", "16")
    celular2 = Celular("iPhone", "11", "987654321", "iOS", "4GB", "64")
    celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()
    print("\n") 
    print(celular1.aplicaciones["Configuracion"].get_almacenamiento_disponible())
    celular1.aplicaciones["AppStore"].descargar_app("WhatsApp")
    print(celular1.aplicaciones["Configuracion"].get_almacenamiento_disponible())
    celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()
    print(celular1.aplicaciones) #Las apps nuevas del appstore no van a tener ningun objeto asociado pq "no existen" como objetos
    celular1.aplicaciones["AppStore"].descargar_app("Zoom") #No hay espacio suficiente
    celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()

    # celular1.aplicaciones["AppStore"].mostar_apps()
    