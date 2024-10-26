from Apps.aplicacion import Aplicacion
from comunicacion import Mensaje
from datetime import datetime
from central import Central
from collections import deque
from Apps.contactos import ContactosApp

class MensajesApp(Aplicacion):
    def __init__(self, numero ,contactos: ContactosApp, central: Central):
        super().__init__(nombre = "MensajeriaSMS", tamanio = "100 MB", esencial = True,)
        self.numero_cel = numero
        self.contactos = contactos
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
    
    def numero_en_contactos(self, numero):
        return numero in self.contactos.get_contactos()
    
    def nombre_contacto(self, numero):
        return self.contactos.get_contactos()[numero]

    def ver_bandeja_de_entrada(self):
        bandeja_de_entrada = self.mensajes
        i=1
        if not(bandeja_de_entrada):
            raise ValueError(f"El numero -{self.numero_cel}- no tiene mensajes en la bandeja de entrada")
        print(f"Bandeja de Entrada del numero: {self.numero_cel}")
        # ??? Hago un raise o un print??
        for mensaje in bandeja_de_entrada:
            print(f"- {i} - ", end="")
            if self.numero_en_contactos(mensaje.get_emisor()) :
                # Invente roman invente
                # Polemico
                aux = mensaje.get_emisor()
                mensaje.emisor = self.nombre_contacto(aux)
                print(mensaje)
                mensaje.emisor = aux
            else:
                print(mensaje)
            i+=1
    
    def __str__(self):
        return f"Aplicacion Mensajeria del numero: {self.numero_cel}"
