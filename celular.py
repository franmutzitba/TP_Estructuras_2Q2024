from configuracion import *
import uuid

class Celular:
    id = 0
    def __init__(self, nombre, modelo, numero, sistema, memoria_ram, almacenamiento):
        #Almaceno los parámetros no modificables por Configuración
        self.id = uuid.uuid4() #Genera un UUID (Universal Unique Identifier) para el dispositivo
        self.nombre = nombre
        self.modelo = modelo
        self.numero = numero
        self.sistema_operativo = sistema
        self.memoria_ram = memoria_ram
        self.almacenamiento = almacenamiento
        
        self.encendido = False
        self.bloqueado = False #hay que configurar una contraseña en Configuracion
        
        self.aplicaciones = {}  
        #self.configuracion = Configuracion()
        self.descargar_apps_basicas()
                
        # self.servicio = False #se administran desde la Configuracion
        # self.wifi = False #se administran desde la Configuracion
        # self.contrasenia = None
    
    def descargar_apps_basicas(self):
        #self.aplicaciones['Configuracion'] = ConfigApp(self.configuracion)
        self.aplicaciones['Configuracion'] = ConfigApp(Configuracion())
        self.aplicaciones['Llamadas'] = None
        self.aplicaciones['Mensajes'] = None
        self.aplicaciones['Mail'] = None
        
    def encencer_dispositivo(self):
        if self.encendido:
            print(f" El dispositivo {self.nombre} ya se encuentra encendido ")
        else:
            self.encendido = True
            print(f"Se ha encencido el dispositivo - {self.nombre} -")
    
    def get_numero(self):
        return self.numero
    
    def get_servicio(self):
        return self.servicio
    
    def get_contrasenia(self):
        return self.contrasenia 
    
    def __str__(self) -> str:
        return f"ID: {self.id}\nNombre: {self.nombre}\nModelo: {self.modelo}\nSistema operativo: {self.sistema_operativo}\nMemoria RAM: {self.memoria_ram}\nAlmacenamiento: {self.almacenamiento}"



if __name__== "__main__":
    celular1 = Celular("Samsung", "Galaxy", "123456789", "Android", "2GB", "16GB")
    print(celular1.aplicaciones["Configuracion"])
    celular1.aplicaciones["Configuracion"].set_servicio(True)
    print(celular1.aplicaciones["Configuracion"])
    