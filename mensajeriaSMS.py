from aplicacion import Aplicacion
from comunicacion import Mensaje
import datetime
from central import Central

class MensajesApp(Aplicacion):
    def __init__(self, numero, central: Central):
        super().__init__(nombre = "MensajeriaSMS", tamanio_mb = 100, esencial = True,)
        self.numero_cel = numero
        self.central = central 
    
    def crear_mensaje(self, receptor: str, mensaje: str):
        return Mensaje(self.numero_cel, receptor, mensaje, datetime.now)
    
    def enviar_sms(self, receptor, texto):
        if self.central.manejar_mensaje(self.numero_cel, receptor, texto):
            mensaje = self.crear_mensaje(self.numero_cel, receptor, texto)
            self.central.registrar_mensaje(self, mensaje)
            print(f"Mensaje enviado correctamente al numero {receptor}") 

    def ver_bandeja_de_entrada():
        pass
