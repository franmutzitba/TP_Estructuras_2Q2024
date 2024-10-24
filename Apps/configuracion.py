from aplicacion import Aplicacion
from enum import Enum

class ModoRed(Enum):
    SIN_RED = 0
    SOLO_VOZ_Y_SMS = 1
    LTE = 2
    
class Configuracion():
    def __init__(self, nombre, almacenamiento_gb, central, numero, aplicaciones_instaladas, modo_red = ModoRed.LTE, modo_avion=False, contrasenia = None):
        self.nombre = nombre
        self.almacenamiento_disponible = int(almacenamiento_gb)*1024 #Trabajo en megas que es más sencillo pero dejo que se ingrese en gb que es mas común
        self.central = central
        self.numero = numero
        self.aplicaciones_instaladas = aplicaciones_instaladas 
        
        self.modo_avion = modo_avion
        self.modo_red = modo_red
        self.contrasenia = contrasenia
        
    def __str__(self):
        return f"Nombre: {self.nombre}, Almacenamiento disponible: {self.almacenamiento_disponible} MB, Número: {self.numero}, Modo avión: {self.modo_avion}, Modo red: {self.modo_red}"
        
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
        
    def listar_aplicaciones(self):
        for app in self.configuracion.aplicaciones_instaladas.keys():
            print(app)
    
    ##setters          
    def set_servicio(self,valor:bool):
        if self.configuracion.modo_red == ModoRed.SOLO_VOZ_Y_SMS and valor:
            raise ValueError("El servicio ya se encuentra encendido")
        elif self.configuracion.modo_red == ModoRed.SIN_RED and not valor:
            raise ValueError("El servicio ya se encuentra apagado")
        else:
            self.configuracion.modo_red = ModoRed.SOLO_VOZ_Y_SMS if valor else ModoRed.SIN_RED
            if valor: #HAY Q VER ESTO
                self.configuracion.modo_avion = False
                #self.configuracion.central.registrar_dispositivo(self.configuracion.numero)
            else: pass
                #self.configuracion.central.eliminar_dispositivo(self.configuracion.numero)
        print(f"El servicio se ha {'encendido' if valor==True else 'apagado'}")
             
    def set_datos(self,valor:bool):
        if self.configuracion.modo_red == ModoRed.LTE and valor:
            raise ValueError("Los datos ya se encuentran encendidos")
        elif self.configuracion.modo_red != ModoRed.LTE and not valor:
            raise ValueError("Los datos ya se encuentran apagados")
        else:
            self.configuracion.modo_red = ModoRed.LTE if valor else ModoRed.SOLO_VOZ_Y_SMS
            print(f"Los datos se han {'encendido' if valor==True else 'apagado'}")
    
    def set_modo_avion(self, valor:bool):
        if self.configuracion.modo_avion == valor:
            raise ValueError(f"El modo avion ya se encuentra {'encendido' if valor==True else 'apagado'}")
        else:
            if valor:
                self.modo_red = ModoRed.SIN_RED
            else:
                self.modo_red = ModoRed.SOLO_VOZ_Y_SMS
            self.configuracion.modo_avion = valor
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
    