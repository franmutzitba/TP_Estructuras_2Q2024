from aplicacion import *
from celular import *

class Configuracion(Aplicacion):
    def __init__(self, celular:Celular):
        super().__init__("Configuracion", 100, True)
        self.contrasenia=None
        
        
    def configurar_contrasenia(self, celular: Celular, contrasenia_vieja, contrasenia_nueva):
        if contrasenia_vieja == celular.contrasenia:
            if celular.validar_contrasenia(contrasenia_nueva): 
                celular.set_contrasenia(contrasenia_nueva)
            else: 
                raise ValueError("La nueva contraseña no cumple con los requisitos")
        else:
            raise ValueError("Contraseña actual incorrecta")
        
    def activar_datos_moviles(self, celular: Celular):
        celular.datos_moviles = True
    
    def activar_wifi(self):
        self.wifi = True
        
    def __str__(self) -> str:
        return f"Nombre: {self.nombre}\nEsencial: {self.esencial}\nTamaño: {self.tamanio}\nContraseña: {self.contrasenia}\nDatos móviles: {self.datos_moviles}\nWifi: {self.wifi}"
    