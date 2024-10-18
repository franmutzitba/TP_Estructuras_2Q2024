from configuracion import *
import uuid

class Celular:
    
    def __init__(self, nombre, modelo, numero, sistema, memoria_ram, almacenamiento_gb):
        #Almaceno los parámetros no modificables por Configuración
        self.id = uuid.uuid4() #Genera un UUID (Universal Unique Identifier) para el dispositivo
        self.nombre = nombre
        self.modelo = modelo
        self.numero = numero
        self.sistema_operativo = sistema
        self.memoria_ram = memoria_ram
        self.almacenamiento = almacenamiento_gb
        
        self.encendido = False
        self.bloqueado = False
        
        self.aplicaciones = {}  
        self.descargar_apps_basicas()
    
    def descargar_apps_basicas(self):
        #self.aplicaciones['Configuracion'] = ConfigApp(self.configuracion)
        self.aplicaciones['Configuracion'] = ConfigApp(Configuracion())
        self.aplicaciones['Llamadas'] = None
        self.aplicaciones['Mensajes'] = None
        self.aplicaciones['Mail'] = None
        
    def encencer_dispositivo(self):
        if self.encendido:
            raise ValueError(f" El dispositivo {self.nombre} ya se encuentra encendido ")
        else:
            self.encendido = True
            print(f"Se ha encencido el dispositivo - {self.nombre} -")
            
    def apagar_dispositivo(self):
        if self.encendido:
            self.encendido = False
            print(f"Se ha apagado el dispositivo - {self.nombre} -")
        else:
            raise ValueError(f" El dispositivo {self.nombre} ya se encuentra apagado ")
    
    def bloquear_dispositivo(self):
        if self.bloqueado:
            raise ValueError(f" El dispositivo {self.nombre} ya se encuentra bloqueado ")
        else:
            self.bloqueado = True
            print(f"Se ha bloqueado el dispositivo - {self.nombre} -")
    
    def desbloquear_dispositivo(self, contrasenia):
        if self.bloqueado and contrasenia == self.aplicaciones["Configuracion"].get_contrasenia():
            self.bloqueado = False
            print(f"Se ha desbloqueado el dispositivo - {self.nombre} -")
        elif not(self.bloqueado):
            raise ValueError(f"El dispositivo {self.nombre} ya se encuentra desbloqueado")
        else:
            raise ValueError("La contraseña ingresada es incorrecta")
        
    
    def get_numero(self):
        return self.numero
    
    def __str__(self) -> str:
        return f"ID: {self.id}\nNombre: {self.nombre}\nModelo: {self.modelo}\nSistema operativo: {self.sistema_operativo}\nMemoria RAM: {self.memoria_ram}\nAlmacenamiento: {self.almacenamiento}"



if __name__== "__main__":
    celular1 = Celular("Samsung", "Galaxy", "123456789", "Android", "2GB", "16GB")
    print(celular1.aplicaciones["Configuracion"])
    celular1.aplicaciones["Configuracion"].set_servicio(True)
    print(celular1.aplicaciones["Configuracion"])
    