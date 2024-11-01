from comunicacion import Llamada, Mensaje
from datetime import datetime, timedelta
#from celular import Celular
from Apps.configuracion import ModoRed
from collections import deque 
from manejadorCSV import ManejadorSMS
#La primera vez que se activa el servicio del celular se da de alta en la central
#Luego la central chequea que tenga servicio o LTE segun corresponda para realizar la comunicacion
#

class Central:
    
    def __init__(self):
        self.registro_llamadas = {} #registro de llamadas_perdidas_o_realizadas
        self.registro_dispositivos = {} #diccionario que contiene el numero en la key y el objeto celular en el valor
        self.registro_mensajes =  {} #Colas de mensajes
        self.ultima_llamada_por_persona = {}  #guarda al numero como clave y como valor a la llamada
        self.manejador_sms = ManejadorSMS("archivo_sms.csv")
        
    def registrar_dispositivo(self, numero, celular):
        self.registro_dispositivos[numero]=celular
        print(f"Dispositivo {numero} registrado correctamente en la central")

        #creo una ultima llamada de la persona, vacia, pero para agregar al numero al diccionario
        llamada = Llamada(numero, numero, datetime.now(), timedelta(minutes=0))
        self.ultima_llamada_por_persona[numero] = llamada
    
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
        
        if receptor not in self.registro_mensajes:
            self.registro_mensajes[receptor] = deque()  # Crear una pila para el receptor
            
        self.registro_mensajes[receptor].appendleft(mensaje)
        
        if  self.esta_registrado(receptor) and self.esta_activo(receptor):
            self.registro_dispositivos[receptor].aplicaciones["Mensajes"].recibir_sms(mensaje)
    
    def registrar_mensajes(self, numero_cel):
        # el metodo sirve para recibir los mensajes aun no sincronizados al momento de encender de vuelta el servicio del dispositivo         
        if not self.esta_registrado(numero_cel):
            raise ValueError 
        if numero_cel not in self.registro_mensajes:
            raise ValueError(f"No hay Mensajes nuevos para el numero {numero_cel}")
        
        # el diccionario registro_mensajes tiene por nro celular una lista de los mensajes recibidos
        # necesito generar una lista en este caso pila que almacene los mensajes no sincronizados, es decir los primeros de la lista hasta el primer sincronizado
        # esta pila se recorre y se reciben los sms del mas antiguo al mas reciente en la bandeja de entrada del numero, el cual encendio el servico
        # sincronizando los mensajes  
        
        mensajes = self.registro_mensajes[numero_cel].copy()
        mensajes_no_sinc = deque() #pila de mensajes no sincronizados que va del mas viejo al mas reciente
        
        while mensajes:
            mensaje = mensajes.popleft()
            if mensaje.get_sincronizado():
                break
            else:
                mensajes_no_sinc.appendleft(mensaje)
                
        if not(len(mensajes_no_sinc)):
            raise ValueError(f"No hay Mensajes nuevos para el numero {numero_cel}")  
        
        while mensajes_no_sinc:
            mensaje = mensajes_no_sinc.popleft()
            self.registro_dispositivos[numero_cel].aplicaciones["Mensajes"].recibir_sms(mensaje)
            # se envian los mensajes en orden cornologico
            #primero los mas viejos, es decir los primeros de la lista, por eso popleft
            # Tambien fueron los ultimos en enntrar por eso pila

    def esta_ocupado(self, numero, fecha_inicio_llamada_nueva:datetime):
        llamada = self.ultima_llamada_por_persona[numero]
        fecha_inicio_anterior = llamada.fecha
        duracion = llamada.duracion
        fecha_fin_llamada_anterior = fecha_inicio_anterior + duracion
        return fecha_fin_llamada_anterior > fecha_inicio_llamada_nueva
    
    def terminar_llamada(self, numero):
        if not self.esta_ocupado(numero, datetime.now()):
            raise ValueError ("No hay llamada en curso")
        else:
            llamada = self.ultima_llamada_por_persona[numero]
            fecha_inicio = llamada.fecha
            fecha_fin = datetime.now()

            duracion_nueva = fecha_fin - fecha_inicio               #cambio la duracion a el tiempo entre el inicio y fin.
            llamada.set_duracion(duracion_nueva)
            print(f"Se termino la llamada en curso entre {llamada.emisor} y {llamada.receptor}")
    
        
    def manejar_llamada(self, emisor, receptor, fecha_inicio:datetime, duracion:timedelta):
        if not self.esta_registrado(emisor):
            raise ValueError(f"No se puede realizar la llamada por el celular {emisor} al no estar registrado en la central")
        if not self.esta_registrado(receptor):
            raise ValueError(f"No se puede realizar la llamada al celular {receptor} al no estar registrado en la central")
        if not self.esta_activo(emisor):
            raise ValueError(f"No se puede realizar la llamada por el celular {emisor} al no estar activo el servicio")
        if not self.esta_activo(receptor):
            raise ValueError(f"No se puede realizar la llamada al celular {receptor} al no estar activo el servicio")
        if self.esta_ocupado(receptor, fecha_inicio):
            raise ValueError(f"El celular {emisor} se encuentra ocupado")
        
        llamada= Llamada(emisor, receptor, duracion, fecha_inicio)
        print(f"{emisor} llamando a {receptor}")
        if not self.esta_ocupado(receptor, fecha_inicio):
            self.registrar_llamada(llamada)

            self.ultima_llamada_por_persona[emisor] = llamada
            self.ultima_llamada_por_persona[receptor] = llamada
        else:
            print(f'El dispositivo de numero {receptor} esta ocupado')
            llamada.set_perdida(True)
            llamada.set_duracion(0)
            self.registrar_llamada(llamada)
        return True
           
    def manejar_mensaje(self, emisor, receptor):
        if not self.esta_registrado(emisor):
            raise ValueError(f"El celular {emisor} no se encuentra registrado en la Central")
        if not self.esta_activo(emisor):
            raise ValueError(f"El celular {emisor} se encuentra sin servicio e incapaz de mandar mensajes")
        if not self.esta_registrado(receptor):
            raise ValueError(f"El celular {receptor} no esta registrado en la Central")
        print(f"Enviando mensaje de {emisor} a {receptor}\n")
        return True

    def eliminar_mensaje(self, mensaje, numero):
        self.registro_mensajes[numero].remove(mensaje)
        print("Mensaje eliminado correctamente")
            
    
    def mostrar_dispositivos(self):
        for dispositivo in self.registro_dispositivos:
            print(dispositivo)
    
    def cargar_mensajes(self):
        self.manejador_sms.cargar_mensajes(self)
    
    def exportar_mensajes(self):
        self.manejador_sms.exportar_mensajes(self.registro_mensajes)
            
    def __str__(self) -> str:
        return f"Registro de llamdas: {self.registrar_llamada}\nRegistro de dispositivos: {self.registro_dispositivos}\n Registro de mensajes: {self.registro_mensajes}"
    




    
    