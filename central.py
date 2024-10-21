from comunicacion import Llamada, Mensaje
import datetime
#from telefono import TelefonoApp
from exportador import Exportador


class Central:
    exportador_dispositivos = Exportador("dispositivos.csv")
    exportador_llamadas = Exportador("llamadas.csv")
    exportador_mensajes = Exportador("mensajes.csv")
    
    def __init__(self):
        self.registro_llamadas = {} #registro de llamadas_perdidas_o_realizadas
        self.registro_dispositivos = []
        self.registro_mensajes =  {} #registro de mensajes (es un diccionario de diccionarios, cada numero es una key 
        #y tiene un diccionario con todos los numeros emisores que guardan el valor de una lista con todos los mensajes enviados)
        
    def registrar_dispositivo(self, numero):
        self.registro_dispositivos.append([numero])
        Central.exportador_dispositivos.exportar(self.registro_dispositivos)
        print(f"Dispositivo {numero} registrado correctamente")
    
    def eliminar_dispositivo(self, numero):
        self.registro_dispositivos.pop(self.registro_dispositivos.index([numero]))
        Central.exportador_dispositivos.exportar(self.registro_dispositivos)
        print(f"Dispositivo {numero} deregistrado correctamente")
        
    def esta_registrado(self, numero: str) -> bool:
        return numero in self.registro_dispositivos
    
    # def esta_activo(self, numero: str) -> bool: #esta activo en la central (encendido y con servicio activo)
    #     return  self.registro_dispositivos[numero].encendido and self.registro_dispositivos[numero].servicio 
    
    def registrar_llamada(self, llamada):
        emisor = llamada.get_emisor()
        receptor = llamada.get_receptor()
        if llamada.get_receptor() not in self.registro_mensajes:
            self.registro_llamadas[receptor] = {}  # Crear un diccionario para el receptor

        if emisor not in self.registro_llamadas[receptor]:
            self.registro_llamadas[receptor][emisor] = []  # Crear una lista para el emisor
            self.registro_llamadas[receptor][emisor].append(llamada)  # Agregar el llamada a la lista
        print(f"Se a registrado la llamada recibida por el numero - {receptor} - enviada por - {emisor} - en la central")
        
        
    def registrar_mensaje(self, mensaje: Mensaje):
        emisor = mensaje.get_emisor()
        receptor = mensaje.get_receptor()
        if receptor not in self.registro_mensajes:
            self.registro_mensajes[receptor] = {}  # Crear un diccionario para el receptor

        if emisor not in self.registro_mensajes[receptor]:
            self.registro_mensajes[receptor][emisor] = []  # Crear una lista para el emisor
            self.registro_mensajes[receptor][emisor].append(mensaje)  # Agregar el mensaje a la lista
        print(f"Se a registrado el mensaje recibido por el numero - {receptor} - enviado por - {emisor} - en la central")
        
    def manejar_llamada(self, emisor, receptor, fecha):
        duracion = 1 #ver como se crea la duracion
        llamada= Llamada(emisor, receptor, duracion, fecha)
        if emisor in self.registro_dispositivos and receptor in self.registro_dispositivos:
            print(f"Conectando llamada de {emisor} a {receptor}")
            self.registrar_llamada(llamada)
            return True
        elif receptor not in self.registro_dispositivos:
            llamada.set_perdida(True)
            llamada.set_duracion(0)
            self.registrar_llamada(llamada)
            print(f"El numero {emisor} no esta registrado en la central")
            return False
        else:
            print("Alguno de los dispositivos no esta activo")
            return False
    
    def manejar_mensaje(self, emisor, receptor, texto):
        if self.esta_activo(emisor) and self.esta_activo(receptor):
            print(f"Enviando mensaje de {emisor} a {receptor}\n Contenido: {texto}")
            return True
        else:
            print("Alguno de los dispositivos no esta activo")
            return False
    
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
    

    
    