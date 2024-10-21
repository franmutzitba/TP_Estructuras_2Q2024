from celular import Celular
from comunicacion import Llamada, Mensaje
import datetime
from telefono import Telefono

class Central:

    def __init__(self):
        self.registro_comunicaciones = []
        self.registro_dispositivos = {}
        
    def registrar_dispositivo(self, dispositivo: Celular):
        self.registro_dispositivos[dispositivo.numero] = dispositivo
        print(f"Dispositivo {dispositivo.numero} registrado correctamente")
    
    def eliminar_dispositivo(self, dispositivo: Celular):
        del self.registro_dispositivos[dispositivo.numero]
        print(f"Dispositivo {dispositivo.numero} deregistrado correctamente")
        
    def esta_registrado(self, numero: str) -> bool:
        return numero in self.registro_dispositivos
    
    def esta_activo(self, numero: str) -> bool: #esta activo en la central (encendido y con servicio activo)
        return  self.registro_dispositivos[numero].encendido and self.registro_dispositivos[numero].servicio 
    
    def registrar_llamada(self, emisor, receptor, duracion):
        self.registro_comunicaciones[datetime.now()] = Llamada(emisor, receptor ,duracion)
    
    def registrar_mensaje(self, emisor, receptor, mensaje):
        self.registro_comunicaciones[datetime.now()] = Mensaje(emisor, receptor, mensaje)
        
    def manejar_llamada(self, emisor, receptor, duracion):
        if self.esta_activo(emisor) and self.esta_activo(receptor):
            print(f"Conectando llamada de {emisor} a {receptor}")
            self.registrar_llamada(emisor, receptor, duracion) #falta registrar_llamada
            return True
        else:
            print("Alguno de los dispositivos no esta activo")
            return False
    
    def manejar_mensaje(self, emisor, receptor, mensaje):
        if self.esta_activo(emisor) and self.esta_activo(receptor):
            print(f"Enviando mensaje de {emisor} a {receptor}\n Contenido: {mensaje}")
            self.registrar_mensaje(emisor, receptor, mensaje) #falta registrar_mensaje
            return True
        else:
            print("Alguno de los dispositivos no esta activo")
            return False
    
    def __str__(self) -> str:
        return f"Registro de comunicaciones: {self.registro_comunicaciones}\nRegistro de dispositivos: {self.registro_dispositivos}"
    
