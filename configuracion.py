from aplicacion import Aplicacion

class Configuracion():
    def __init__(self, nombre, almacenamiento_gb, central, numero, modo_avion=False, servicio=False, contrasenia = None, wifi=False):
        self.nombre = nombre
        self.almacenamiento_disponible = int(almacenamiento_gb)*1024 #Trabajo en megas que es más sencillo pero dejo que se ingrese en gb que es mas común
        self.central = central
        self.numero = numero
        self.modo_avion = modo_avion
        self.servicio = servicio
        self.wifi = wifi
        self.contrasenia = contrasenia
        
        
    def __str__(self):
        return f"Modo avion: {self.modo_avion}\nServicio: {self.servicio}\nWifi: {self.wifi}\nContraseña: {self.contrasenia}"
        
class ConfigApp(Aplicacion):
    def __init__(self, configuracion: Configuracion):
        super().__init__(nombre = "Configuración", tamanio_mb = 100, esencial = True)
        self.configuracion = configuracion
        
    def configurar_contrasenia(self, contrasenia_nueva, contrasenia_vieja = None):
        if contrasenia_vieja == self.configuracion.contrasenia or self.configuracion.contrasenia == None:
            if self.validar_contrasenia(contrasenia_nueva): 
                self.set_contrasenia(contrasenia_nueva)
            else: 
                raise ValueError("La nueva contraseña no cumple con los requisitos")
        else:
            raise ValueError("Contraseña actual incorrecta")
        
    def configurar_nombre(self, nombre):
        if self.validar_nombre(nombre):
            self.configuracion.nombre = nombre
            print("Nombre actualizado correctamente")
        else:
            raise ValueError("El nombre ingresado no cumple con los requisitos")
    
    ##setters          
    def set_servicio(self,valor:bool):
        if self.configuracion.servicio == valor:
            raise ValueError(f"El servicio ya se encuentra {'encendido' if valor==True else 'apagado'}")
        else:
            self.configuracion.servicio = valor
            if valor:
                self.configuracion.modo_avion = False
                self.configuracion.central.registrar_dispositivo(self.configuracion.numero)
            else:
                self.configuracion.central.eliminar_dispositivo(self.configuracion.numero)
        print(f"El servicio se ha {'encendido' if valor==True else 'apagado'}")
             
    def set_wifi(self,valor:bool):
        if self.configuracion.wifi == valor:
            raise ValueError(f"El wifi ya se encuentra {'encendido' if valor==True else 'apagado'}")
        else:
            self.configuracion.wifi=valor
            print(f"El wifi se ha {'encendido' if valor==True else 'apagado'}")
    
    def set_modo_avion(self,valor:bool):
        if self.configuracion.modo_avion == valor:
            raise ValueError(f"El modo avion ya se encuentra {'encendido' if valor==True else 'apagado'}")
        else:
            if valor:
                self.set_servicio(False)
            self.configuracion.modo_avion=valor
            print(f"El modo avion se ha {'encendido' if valor==True else 'apagado'}")
            
    def set_contrasenia(self, contrasenia):
        self.configuracion.contrasenia = contrasenia
        print("Contraseña actualizada correctamente")
        
    def set_almacenamiento_disponible(self, almacenamiento):
        self.configuracion.almacenamiento_disponible = almacenamiento
    
    ##getters  
    def get_contrasenia(self):
        return self.configuracion.contrasenia
    
    def get_nombre(self):
        return self.configuracion.nombre
    
    def get_almacenamiento_disponible(self):
        return int(self.configuracion.almacenamiento_disponible)
        
    @staticmethod
    def validar_contrasenia(contrasenia:str): #la contraseña debe ser un número de 4 a 6 dígitos
        if len(contrasenia) <= 4 and len(contrasenia) <= 6 and contrasenia.isnumeric():
            return True
        else:
            return False
    
    @staticmethod
    def validar_nombre(nombre:str): #el nombre debe contener al menos 6 caracteres y no puede contener caracteres especiales. Ademas debe comenzar con una letra
        if len(nombre) >= 6 and nombre.isalnum() and nombre[0].isalpha():
            return True
        else:
            return False
        
    def __str__(self):
        return f"Configuración: {self.configuracion}"
    