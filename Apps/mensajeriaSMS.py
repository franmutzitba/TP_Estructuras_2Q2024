from Apps.aplicacion import Aplicacion
from comunicacion import Mensaje
from datetime import datetime
from central import Central
from collections import deque

class MensajesApp(Aplicacion):
    def __init__(self, numero, central: Central):
        super().__init__(nombre = "MensajeriaSMS", tamanio = "100 MB", esencial = True,)
        self.numero_cel = numero
        self.central = central
        self.mensajes = deque() 
    
    def crear_mensaje(self, receptor: str, mensaje: str):
        return Mensaje(self.numero_cel, receptor, mensaje,datetime.now())
    
    def enviar_sms(self, receptor, texto):
        try:
            if self.central.manejar_mensaje(self.numero_cel, receptor):
                mensaje = self.crear_mensaje(receptor, texto)
                self.central.registrar_mensaje_nuevo(mensaje)
                print(f"Mensaje enviado correctamente al numero {receptor}") 
        except ValueError as e: 
            print(e)

    def recibir_sms(self, mensaje: Mensaje):
        if not(mensaje.get_sincronizado()):
            mensaje.set_sincronizado()
            self.mensajes.appendleft(mensaje)
        else:
            print("El mensaje ya ha sido recibido")

    def ver_bandeja_de_entrada(self):
        bandeja_de_entrada = self.mensajes
        i=1
        if not(bandeja_de_entrada):
            raise ValueError(f"El numero -{self.numero_cel}- no tiene mensajes en la bandeja de entrada")
        print(f"Bandeja de Entrada del numero: {self.numero_cel}")
        # ??? Hago un raise o un print??
        for mensaje in bandeja_de_entrada:
            print(f"- {i} - ", end="")
            print(mensaje)
            i+=1
