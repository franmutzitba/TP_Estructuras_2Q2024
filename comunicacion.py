"""
Módulo que contiene las clases Comunicacion, Llamada y Mensaje.
"""

from datetime import datetime

class Comunicacion:
    """
    Clase que representa una comunicación entre dos dispositivos.
    
    Atributos:
    ----------
    emisor (str):
        Identificador del emisor de la comunicación.
    receptor (str):
        Identificador del receptor de la comunicación.
    tipo (str):
        Tipo de comunicación (Llamada, Mensaje).
    
    Métodos:
    --------
    __init__(self, emisor, receptor, tipo):
        Inicializa una instancia de la clase Comunicacion.
    get_emisor(self):
        Devuelve el identificador del emisor.
    get_receptor(self):
        Devuelve el identificador del receptor.
    """
    def __init__(self, emisor, receptor, tipo):
        self.emisor = emisor
        self.receptor = receptor
        self.tipo = tipo

    def get_emisor(self):
        """Devuelve el identificador del emisor"""
        return self.emisor

    def get_receptor(self):
        """Devuelve el identificador del receptor"""
        return self.receptor

class Llamada(Comunicacion):
    """
    Clase que representa una llamada telefónica, heredando de la clase Comunicación.
    
    Atributos:
    ----------
    emisor(str):
        El número o identificador del emisor de la llamada.
    receptor(str):
        El número o identificador del receptor de la llamada.
    duracion (int):
        La duración de la llamada en segundos.
    fecha (datetime):
        La fecha y hora en que se realizó la llamada.
    perdida (bool):
        Indica si la llamada fue perdida (True) o no (False).
        
    Métodos:
    --------
    __init__(self, emisor, receptor, duracion, fecha):
        Inicializa una nueva instancia de la clase Llamada.
    set_duracion(self, tiempo):
        Establece la duración de la llamada.
    get_duracion(self):
        Retorna la duración de la llamada.
    get_fecha(self):
        Retorna la fecha y hora en que se realizó la llamada.
    get_perdida(self):
        Retorna si la llamada fue perdida o no.
    set_perdida(self, perdida):
        Establece si la llamada fue perdida o no.
    """

    def __init__(self, emisor, receptor, duracion, fecha, perdida=False):
        super().__init__(emisor, receptor, 'Llamada realizada')
        self.duracion = duracion
        self.fecha = fecha
        self.perdida = perdida

    def set_duracion(self, tiempo):
        """Establece la duración de la llamada"""
        self.duracion = tiempo

    def get_duracion(self):
        """Retorna la duración de la llamada"""
        return self.duracion

    
    def get_fecha_inicio(self):
        """Retorna la fecha y hora en que se realizó la llamada"""
        return self.fecha

    def get_perdida(self):
        """Retorna si la llamada fue perdida o no"""
        return self.perdida

    def set_perdida(self, perdida):
        """Establece si la llamada fue perdida o no"""
        self.perdida = perdida

    def __str__(self):
        return f"Emisor: {self.emisor}, Receptor: {self.receptor}, Duracion: {self.duracion}"

class Mensaje(Comunicacion):
    """
    Clase que representa un mensaje de comunicación entre un emisor y un receptor.
    
    Atributos:
    ----------
    emisor (str):
        Identificador del emisor del mensaje.
    receptor (str):
        Identificador del receptor del mensaje.
    mensaje (str):
        Contenido del mensaje.
    fecha (datetime):
        Fecha y hora en que se envió el mensaje.
    sincronizado (bool):
        Indica si el mensaje ha sido sincronizado (recibido por el receptor).
        
    Métodos:
    --------
    __init__(self, emisor, receptor, mensaje, fecha: datetime):
        Inicializa una instancia de la clase Mensaje.
    get_sincronizado(self):
        Devuelve si el mensaje está sincronizado.
    set_sincronizado(self):
        Marca el mensaje como sincronizado.
    get_mensaje(self):
        Devuelve el contenido del mensaje.
    get_fecha(self):
        Devuelve la fecha en formato datetime.
    """

    def __init__(self, emisor, receptor, mensaje, fecha: datetime):
        if not isinstance(fecha,datetime):
            raise ValueError("La fecha debe de estar en formato datetime")
        super().__init__(emisor, receptor, 'Mensaje')
        self.mensaje = mensaje
        self.fecha = fecha
        self.sincronizado = False #El mensaje se sincroniza cuando el receptor es capaz de recibirlo en su bandeja de entrada

    def get_sincronizado(self):
        """Devuelve si el mensaje está sincronizado"""
        return self.sincronizado

    def set_sincronizado(self):
        """Marca el mensaje como sincronizado"""
        self.sincronizado = True

    def get_mensaje(self):
        """Devuelve el mensaje"""
        return self.mensaje

    def get_fecha(self):
        """Devuelve la fecha en formato datetime"""
        return self.fecha

    def __str__(self):
        fecha_min = self.fecha.strftime("%Y-%m-%d %H:%M")
        return f"Emisor: {self.emisor}, Receptor: {self.receptor}, Texto: {self.mensaje}, Fecha: {fecha_min}"
