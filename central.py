"""
Módulo que contiene la clase Central, que simula una central telefónica.
"""

from datetime import datetime, timedelta
from collections import deque
from comunicacion import Llamada, Mensaje
from Apps.configuracion import ModoRed
#from manejadorCSV import ManejadorSMS
#La primera vez que se activa el servicio del celular se da de alta en la central
#Luego la central chequea que tenga servicio o LTE segun corresponda para realizar la comunicacion

class Central:
    """
    La clase Central representa una central de comunicaciones que maneja 
    dispositivos, llamadas y mensajes. Contiene todos los celulares registrados.
    
    Atributos:
    ----------
    registro_llamadas (deque):
        Pila de llamadas registradas en la central.
    registro_dispositivos (dict):
        Diccionario que contiene el número de teléfono como clave y el objeto celular como valor.
    registro_mensajes (dict):
        Diccionario que contiene colas de mensajes.

    Métodos:
    --------
    __init__():
        Inicializa una instancia de la clase Central.
    registrar_dispositivo(numero, celular):
        Registra un dispositivo en la central.
    consultar_LTE(numero):
        Consulta si un dispositivo está en modo LTE.
    esta_registrado(numero: str) -> bool:
        Verifica si un número está registrado en la central.
    esta_activo(numero: str) -> bool:
        Verifica si un número está activo en la central.
    registrar_llamada(llamada):
        Registra una llamada en la central.
    registrar_mensaje_nuevo(mensaje: Mensaje):
        Registra un nuevo mensaje en la central.
    registrar_mensajes(numero_cel):
        Registra los mensajes no sincronizados de un dispositivo.
    esta_ocupado(numero, fecha_inicio_llamada_nueva: datetime):
        Verifica si un número está ocupado en una llamada.
    terminar_llamada(numero):
        Termina una llamada en curso.
    manejar_llamada(emisor, receptor, fecha_inicio: datetime, duracion: timedelta):
        Maneja una llamada entre dos dispositivos.
    manejar_mensaje(emisor, receptor):
        Maneja el envío de un mensaje entre dos dispositivos.
    eliminar_mensaje(mensaje, numero):
        Elimina un mensaje de la central.
    mostrar_dispositivos():
        Muestra todos los dispositivos registrados en la central.
    cargar_mensajes():
        Carga los mensajes desde un archivo.
    exportar_mensajes():
        Exporta los mensajes a un archivo.
    """

    def __init__(self):
        self.registro_llamadas = deque()
        self.registro_dispositivos = {} #diccionario que contiene el numero en la key y el objeto celular en el valor
        self.registro_mensajes =  {} #Diccionario que contiene el numero en la key y una pila de mensajes en el valor

    def registrar_dispositivo(self, numero, celular):
        """
        Registra un dispositivo en la central.
        
        Args:
            numero (str): Número de teléfono del dispositivo.
            celular (Celular): Objeto celular a registrar en la central
            
        Returns:
            None
        """
        self.registro_dispositivos[numero]=celular
        print(f"Dispositivo {numero} registrado correctamente en la central")

    def consultar_LTE(self, numero):
        """Devuelve True si un dispositivo está en modo LTE."""
        return self.registro_dispositivos[numero].aplicaciones["Configuracion"].configuracion.modo_red == ModoRed.LTE

    def esta_registrado(self, numero: str):
        """Verifica si un número está registrado en la central."""
        return numero in self.registro_dispositivos

    def esta_activo(self, numero:str):
        """Verifica si un número está activo en la central."""
        return self.registro_dispositivos[numero].aplicaciones["Configuracion"].configuracion.modo_red != ModoRed.SIN_RED

    def registrar_llamada(self, llamada):
        """
        Registra una llamada en la central y en los dispositivos correspondientes.
        
        Args:
            llamada (Llamada): Llamada a registrar en la central y en los dispositivos.
        """
        self.registro_llamadas.appendleft(llamada)
        emisor = llamada.get_emisor()
        receptor = llamada.get_receptor()
        
        self.registro_dispositivos[emisor].aplicaciones["Telefono"].aniadir_llamada(llamada, iniciada=True)
        self.registro_dispositivos[receptor].aplicaciones["Telefono"].aniadir_llamada(llamada, iniciada=False)
        print("")
        print(f"Se a registrado la llamada {'perdida' if llamada.get_perdida() else 'recibida'} por el numero - {receptor} - enviada por - {emisor} - en la central")

    def registrar_mensaje_nuevo(self, mensaje: Mensaje):
        """
        Registra un nuevo mensaje en el sistema y lo envía al receptor si está registrado y activo.
        
        Args:
            mensaje (Mensaje): El mensaje a registrar.
            
        Returns:
            None
        """

        receptor = mensaje.get_receptor()

        if receptor not in self.registro_mensajes:
            self.registro_mensajes[receptor] = deque()  # Crear una pila para el receptor

        self.registro_mensajes[receptor].appendleft(mensaje)

        if  self.esta_registrado(receptor) and self.esta_activo(receptor):
            self.registro_dispositivos[receptor].aplicaciones["Mensajes"].recibir_sms(mensaje)

    def registrar_mensajes(self, numero_cel):
        """
        Registra y sincroniza los mensajes no sincronizados para un número de celular específico.
        Este método se utiliza para recibir los mensajes que no fueron sincronizados al momento 
        de encender nuevamente el servicio del dispositivo. Los mensajes se sincronizan en orden 
        cronológico, del más antiguo al más reciente.
        
        Args:
            numero_cel (str): El número de celular para el cual se desean registrar los mensajes.
            
        Returns:
            None

        Raises:
            ValueError: Si el número de celular no está registrado.
            ValueError: Si no hay mensajes nuevos para el número de celular.
        """

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

        if not mensajes_no_sinc:
            raise ValueError(f"No hay Mensajes nuevos para el numero {numero_cel}")

        while mensajes_no_sinc:
            mensaje = mensajes_no_sinc.popleft()
            self.registro_dispositivos[numero_cel].aplicaciones["Mensajes"].recibir_sms(mensaje)
            # se envian los mensajes en orden cornologico
            #primero los mas viejos, es decir los primeros de la lista, por eso popleft
            # Tambien fueron los ultimos en enntrar por eso pila

    def esta_ocupado(self, numero):
        """Verifica si el número de celular se encuentra ocupado en una llamada en curso.
        
        Args:
            numero (str): Número de teléfono a verificar.
        
        Returns:
            bool: True si el número de teléfono se encuentra en una llamada en curso, False en caso contrario.
        """
        fecha_actual = datetime.now()
        llamada = self.registro_dispositivos[numero].aplicaciones["Telefono"].get_ultima_llamada()
        if llamada:
            return fecha_actual < llamada.get_fecha() + llamada.get_duracion() 
        return False  

    def terminar_llamada(self, numero):

        """
        Termina la llamada en curso de un número de celular.
        
        Args:
            numero (str): Número de teléfono para el cual se desea terminar la llamada en curso.
        
        Raises:
            ValueError: Si el número de celular no está registrado.
            ValueError: Si el número de celular no se encuentra activo en la Central.
            ValueError: Si no hay llamada en curso.
        """

        if not self.esta_ocupado(numero):
            raise ValueError ("No hay llamada en curso")
        if not self.esta_registrado(numero):    
            raise ValueError (f"El celular {numero} no se encuentra registrado en la Central")
        if not self.esta_activo(numero):
            raise ValueError (f"El celular {numero} no se encuentra activo en la Central")

        llamada = self.registro_dispositivos[numero].aplicaciones["Telefono"].get_ultima_llamada()
        fecha_inicio = llamada.get_fecha()
        fecha_fin = datetime.now()

        duracion_nueva = fecha_fin - fecha_inicio        
        llamada.set_duracion(duracion_nueva)

        print(f"Se termino la llamada en curso entre {llamada.emisor} y {llamada.receptor}")

    def manejar_llamada(self, emisor, receptor, fecha_inicio:datetime, duracion:timedelta):
        """
        Maneja una llamada que se produce en la central, la registra y la almacena en el 
        registro de llamadas.
        
        Args:
            emisor (str): Número de teléfono del emisor de la llamada.
            receptor (str): Número de teléfono del receptor de la llamada.
            fecha_inicio (datetime): Fecha y hora en que se inicio la llamada.
            duracion (timedelta): Duración de la llamada.
        
        Raises:
            ValueError: Si el emisor o receptor no se encuentra registrado en la central.
            ValueError: Si el emisor o receptor no se encuentra activo en la central.
            ValueError: Si el emisor o receptor se encuentra ocupado.
        """
        if not self.esta_registrado(emisor):
            raise ValueError(f"No se puede realizar la llamada por el celular {emisor} al no estar registrado en la central")
        if not self.esta_registrado(receptor):
            raise ValueError(f"No se puede realizar la llamada al celular {receptor} al no estar registrado en la central")
        if not self.esta_activo(emisor):
            raise ValueError(f"No se puede realizar la llamada por el celular {emisor} al no estar activo el servicio")
        #if not self.esta_activo(receptor):
        #    raise ValueError(f"No se puede realizar la llamada al celular {receptor} al no estar activo el servicio")

        print(f"{emisor} llamando a {receptor}...")
        if self.esta_ocupado(emisor):
            raise ValueError("Usted ya se encuentra ocupado")
        llamada= Llamada(emisor, receptor, duracion, fecha_inicio)
        if self.esta_ocupado(receptor):
            print(f"El dispositivo de numero {receptor} esta ocupado")
            llamada.set_perdida(True)
            llamada.set_duracion(timedelta(0))
        if not self.esta_activo(receptor):
            print(f"No se puede realizar la llamada al celular {receptor} al no estar activo el servicio")
            llamada.set_perdida(True)
            llamada.set_duracion(timedelta(0))
        self.registrar_llamada(llamada)

    def manejar_mensaje(self, emisor, receptor):
        """
        Maneja el envío de un mensaje de un emisor a un receptor.
        
        Args:
            emisor (str): El número de celular del emisor del mensaje.
            receptor (str): El número de celular del receptor del mensaje.
            
        Returns:
            bool: True si el mensaje se envía correctamente.
            
        Raises:
            ValueError: Si el emisor no está registrado en la central.
            ValueError: Si el emisor está sin servicio y no puede mandar mensajes.
            ValueError: Si el receptor no está registrado en la central.
        """

        if not self.esta_registrado(emisor):
            raise ValueError(f"El celular {emisor} no se encuentra registrado en la Central")
        if not self.esta_activo(emisor):
            raise ValueError(f"El celular {emisor} se encuentra sin servicio e incapaz de mandar mensajes")
        if not self.esta_registrado(receptor):
            raise ValueError(f"El celular {receptor} no esta registrado en la Central")
        print(f"Enviando mensaje de {emisor} a {receptor}...\n")

    def eliminar_mensaje(self, mensaje, numero):
        """
        Elimina un mensaje específico de un registro de mensajes.
        
        Args:
            mensaje (str): El mensaje a eliminar.
            numero (int): El índice del registro de mensajes del cual se eliminará el mensaje.
            
        Returns:
            None
        """
        self.registro_mensajes[numero].remove(mensaje)
        print("Mensaje eliminado correctamente")

    def mostrar_dispositivos(self):
        """
        Muestra todos los dispositivos registrados.
        Itera sobre la lista de dispositivos registrados y los imprime en la consola.
        """
        for dispositivo in self.registro_dispositivos:
            print(dispositivo)

    def __str__(self):
        return f"Registro de llamadas: {self.registro_llamadas}\n Registro de dispositivos: {self.registro_dispositivos}\n Registro de mensajes: {self.registro_mensajes}"
