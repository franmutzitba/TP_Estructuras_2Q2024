from comunicacion import Llamada, Mensaje
from datetime import datetime, timedelta
#from celular import Celular
from configuracion import ModoRed
from collections import deque 
#La primera vez que se activa el servicio del celular se da de alta en la central
#Luego la central chequea que tenga servicio o LTE segun corresponda para realizar la comunicacion
#

class Central:
    
    def __init__(self):
        self.registro_llamadas = {} #registro de llamadas_perdidas_o_realizadas
        self.registro_dispositivos = {} #diccionario que contiene el numero en la key y el objeto celular en el valor
        self.telefonos_ocupados = {} #guarda la fecha en el que el telefono se libera.
        self.registro_mensajes =  {} #registro de mensajes (es un diccionario de diccionarios, cada numero es una key 
        #y tiene un diccionario con todos los numeros emisores que guardan el valor de una lista con todos los mensajes enviados)
        
    def registrar_dispositivo(self, numero, celular):
        self.registro_dispositivos[numero]=celular
        print(f"Dispositivo {numero} registrado correctamente")
    
    def consultar_LTE(self, numero):
        return self.registro_dispositivos[numero].aplicaciones["Configuracion"].configuracion.modo_red == ModoRed.LTE
    
    def esta_registrado(self, numero: str) -> bool:
        return numero in self.registro_dispositivos
    
    def esta_activo(self, numero:str) -> bool:
        return self.registro_dispositivos[numero].aplicaciones["Configuracion"].configuracion.modo_red != ModoRed.SIN_RED
    
    def registrar_llamada(self, llamada):
        emisor = llamada.get_emisor()
        receptor = llamada.get_receptor()
        if llamada.get_receptor() not in self.registro_mensajes:
            self.registro_llamadas[receptor] = {}  # Crear un diccionario para el receptor

        if emisor not in self.registro_llamadas[receptor]:
            self.registro_llamadas[receptor][emisor] = []  # Crear una lista para el emisor
            self.registro_llamadas[receptor][emisor].append(llamada)  # Agregar el llamada a la lista
        print(f"Se a registrado la llamada recibida por el numero - {receptor} - enviada por - {emisor} - en la central")
        
        
    def registrar_mensaje_nuevo(self, mensaje: Mensaje):
        receptor = mensaje.get_receptor()
        emisor = mensaje.get_emisor()
        if receptor not in self.registro_mensajes:
            self.registro_mensajes[receptor] = deque()  # Crear una pila para el receptor
        self.registro_mensajes[receptor].appendleft(mensaje)
        print(f"Se a registrado el mensaje recibido por el numero - {receptor} - enviado por - {emisor} - en la central")
        if self.esta_activo(receptor):
            self.registro_dispositivos[receptor].aplicaciones["Mensajes"].recibir_sms(mensaje)
    
    def registrar_mensajes(self, numero_cel):
        try:
            mensajes = self.registro_mensajes[numero_cel]
        except KeyError:
            raise ValueError
        
        # if mensajes:
        #     mensaje = mensajes.popleft()
        #     while not(mensaje.get_sincronizado()):
        #         self.registro_dispositivos[numero_cel].aplicaciones["Mensajes"].recibir_sms(mensaje)
        #         try:
        #             mensaje = mensajes.popleft()
        #         except IndexError:
        #             print("Error aca cabron")
        else:
            raise ValueError(f"No hay Mensajes nuevos para el numero {numero_cel}")
            

    def esta_ocupado(self, numero, fecha_inicio_llamada_nueva:datetime):
        fecha_fin_llamada_anterior = self.telefonos_ocupados[numero]
        return fecha_fin_llamada_anterior > fecha_inicio_llamada_nueva
    
        
    def manejar_llamada(self, emisor, receptor, fecha_inicio:datetime, duracion:timedelta):
        llamada= Llamada(emisor, receptor, duracion, fecha_inicio)
        if self.esta_registrado(emisor) and self.esta_registrado(receptor) and not self.esta_ocupado(emisor, fecha_inicio) and self.esta_activo(emisor) and self.esta_activo(receptor):
            print(f"{emisor} llamando a {receptor}")
            if not self.esta_ocupado(receptor, fecha_inicio):
                self.registrar_llamada(llamada)
                self.telefonos_ocupados[emisor] = fecha_inicio + duracion
                self.telefonos_ocupados[receptor] = fecha_inicio + duracion
            else:
                print(f'El dispositivo de numero {receptor} esta ocupado')
                llamada.set_perdida(True)
                llamada.set_duracion(0)
                self.registrar_llamada
            return True
        elif not self.esta_registrado(emisor):
            raise ValueError(f"No se puede realizar la llamada por el celular {emisor} al no estar registrado en la central")
        elif not self.esta_registrado(receptor):
            raise ValueError(f"No se puede realizar la llamada al celular {receptor} al no estar registrado en la central")
        elif not self.esta_activo(emisor):
            raise ValueError(f"No se puede realizar la llamada por el celular {emisor} al no estar activo el servicio")
        elif not self.esta_activo(receptor):
            raise ValueError(f"No se puede realizar la llamada al celular {receptor} al no estar activo el servicio")

            
    
    def manejar_mensaje(self, emisor, receptor):
        if self.esta_registrado(emisor):
            if self.esta_activo(emisor):
                if self.esta_registrado(receptor):
                    print(f"Enviando mensaje de {emisor} a {receptor}\n")
                else:
                    raise ValueError(f"El celular {receptor} no esta registrado en la Central")
            else:
                raise ValueError(f"El celular {emisor} se encuentra sin servicio e incapaz de mandar mensajes")
        else:
            raise ValueError(f"El celular {emisor} no se encuentra registrado en la Central")
            
    
    def mostrar_dispositivos(self):
        for dispositivo in self.registro_dispositivos:
            print(dispositivo)
            
    def __str__(self) -> str:
        return f"Registro de comunicaciones: {self.registro_comunicaciones}\nRegistro de dispositivos: {self.registro_dispositivos}"
    


if __name__ == "__main__":
    central1 = Central()
    central1.registrar_dispositivo("123456789")
    central1.registrar_dispositivo("987654321")
    print(central1)
    central1.manejar_llamada("123456789", "987654321", 10)
    

    
    