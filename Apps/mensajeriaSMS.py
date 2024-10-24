from Apps.aplicacion import Aplicacion
from comunicacion import Mensaje
import datetime
from central import Central
from collections import deque

class MensajesApp(Aplicacion):
    def __init__(self, numero, central: Central):
        super().__init__(nombre = "MensajeriaSMS", tamanio_mb = 100, esencial = True,)
        self.numero_cel = numero
        self.central = central
        self.mensajes = deque() 
    
    def crear_mensaje(self, receptor: str, mensaje: str):
        return Mensaje(self.numero_cel, receptor, mensaje, datetime.datetime.now())
    
    def enviar_sms(self, receptor, texto):
        try:
            self.central.manejar_mensaje(self.numero_cel, receptor)
            mensaje = self.crear_mensaje(receptor, texto)
            self.central.registrar_mensaje_nuevo( mensaje)
            print(f"Mensaje enviado correctamente al numero {receptor}") 
        except ValueError as e: 
            print(e)

    def recibir_sms(self, mensaje: Mensaje):
        if not(mensaje.get_sincronizado):
            mensaje.set_sincronizado
            self.mensajes.appendleft(mensaje)
        else:
            print("El mensaje ya ha sido recibido")
    
    def registrar_mensajes(self):
        self.central.registrar_mensajes(self.numero_cel)
        
    def ver_bandeja_de_entrada():
        pass
