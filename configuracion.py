from aplicacion import *
from celular import *

class Configuracion():
    def __init__(self, modo_avion=False, servicio=False, contrasenia = None, wifi=False):
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
        
    def configurar_contrasenia(self, configuracion, contrasenia_vieja, contrasenia_nueva):
        if contrasenia_vieja == configuracion.contrasenia:
            if self.validar_contrasenia(contrasenia_nueva): 
                self.set_contrasenia(contrasenia_nueva)
            else: 
                raise ValueError("La nueva contraseña no cumple con los requisitos")
        else:
            raise ValueError("Contraseña actual incorrecta")
                
    def set_servicio(self,valor:bool):
        if self.configuracion.servicio == valor:
            raise ValueError(f"El servicio ya se encuentra {'encendido' if valor==True else 'apagado'}")
        else:
            self.configuracion.servicio=valor
            print(f"El servicio se ha {'encendido' if valor==True else 'apagado'}")
             
    def set_wifi(self,valor:bool):
        if self.configuracion.wifi == valor:
            raise ValueError(f"El wifi ya se encuentra {'encendido' if valor==True else 'apagado'}")
        else:
            self.configuracion.wifi=valor
            print(f"El wifi se ha {'encendido' if valor==True else 'apagado'}")
        
    def set_contrasenia(self, contrasenia):
        self.configuracion.contrasenia = contrasenia
        print("Contraseña actualizada correctamente")
        
    def get_contrasenia(self):
        return self.configuracion.contrasenia
        
    @staticmethod
    def validar_contrasenia(contrasenia:str):
        if len(contrasenia) <= 4 and len(contrasenia) <= 6 and contrasenia.isnumeric():
            return True
        else:
            return False
        
    def __str__(self):
        return f"Configuración: {self.configuracion}"
    