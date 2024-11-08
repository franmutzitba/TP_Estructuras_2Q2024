"""
Módulo para manejar la importación y exportación de la data a 
archivos CSV
"""

import csv
from collections import deque
from datetime import datetime, timedelta 
import numpy as np
from Apps.mail import CuentaMail, Mail
from comunicacion import Mensaje, Llamada
from celular import Celular

class ManejadorCSV:
    """
    Clase base para manejar archivos CSV.
    """

    def __init__(self, nombre_archivo):
        """
        Inicializa la clase ManejadorCSV con el nombre del archivo.

        Args:
            nombre_archivo (str): El nombre del archivo CSV.
        """
        self.nombre_archivo = nombre_archivo

    def exportar(self, lista: list, modo = "w"): #Por default escribe un archivo nuevo. Se puede cambiar a "a" para agregar al final
        """
        Exporta una lista a un archivo CSV.
        
        Args:
            lista (list): La lista a exportar.
            modo (str): El modo de escritura del archivo. Por defecto es "w".
        """
        try:
            with open(self.nombre_archivo, mode=modo, newline="", encoding='utf-8') as archivo_csv:
                escritor = csv.writer(archivo_csv)
                escritor.writerows(lista)
        except FileNotFoundError:
            print("Archivo no encontrado")
        except IOError:
            print("Error al exportar archivo")

    def leer_archivo(self, skip_first = False):
        """
        Lee el archivo CSV y devuelve su contenido.
        
        Args:
            skip_first (bool): Indica si se debe omitir la primera fila del archivo. 
            Por defecto es False.
        """
        try:
            with open(self.nombre_archivo, "r", encoding='utf-8') as archivo_csv:
                lector = csv.reader(archivo_csv)
                if skip_first:
                    next(lector)
                return list(lector)
        except FileNotFoundError:
            print("Archivo no encontrado")
        except IOError:
            print("Error al leer archivo")
    # def leer_archivo(self, skip_header=False):
    #     """
    #     Lee el archivo CSV y devuelve su contenido.

    #     Args:
    #         skip_header (bool): Indica si se debe omitir la primera fila del archivo. 
    #         Por defecto es False.

    #     Returns:
    #         list: Una lista con el contenido del archivo CSV.
    #     """
    #     try:
    #         if skip_header:
    #             data = np.genfromtxt(self.nombre_archivo, delimiter=',', dtype=str, skip_header=1)
    #         else:
    #             data = np.genfromtxt(self.nombre_archivo, delimiter=',', dtype=str)
    #         return data.tolist()
    #     except FileNotFoundError:
    #         print("Archivo no encontrado")
    #     except IOError:
    #         print("Error al leer archivo")

    def leer_matriz(self):
        """
        Lee el archivo CSV y devuelve su contenido como una matriz.

        Returns:
            numpy.ndarray: Una matriz con el contenido del archivo CSV.
        """
        try:
            matriz = np.genfromtxt(self.nombre_archivo, delimiter=',', dtype=str, skip_header=1)
            return matriz
        except FileNotFoundError:
            print("Archivo no encontrado")
        except IOError:
            print("Error al leer archivo")

class ManejadorSMS(ManejadorCSV):
    """
    Clase para manejar archivos CSV específicos de mensajes SMS.
    Hereda de ManejadorCSV.
    Atributos:
    nombre_archivo (str): Nombre del archivo CSV.
    central (Central): Central telefónica a la que se le cargarán los mensajes
    """
    def __init__(self, nombre_archivo, central):
        """
        Inicializa la clase ManejadorSMS con el nombre del archivo y la central.
        
        """
        super().__init__(nombre_archivo)
        self.central = central

    def exportar_mensajes(self):
        """
        Exporta los mensajes a un archivo CSV.
        """
        colas = self.central.registro_mensajes.values()
        lista_a_exportar = []
        titulo = ["Emisor", "Receptor", "Texto", "Fecha", "Sincronizado"]
        lista_a_exportar.append(titulo)
        for cola in colas:
            cola_2 = cola.copy()
            while cola_2:
                mensaje = cola_2.popleft()
                lista_a_exportar.append([mensaje.get_emisor(), mensaje.get_receptor(), mensaje.get_mensaje(), mensaje.get_fecha(), mensaje.get_sincronizado()])
        self.exportar(lista_a_exportar)

    def cargar_mensajes(self):
        """"
        Carga los mensajes desde un archivo CSV y los registra en la central.
        """
        lista_mensajes = deque(self.leer_archivo(True))  # cola
        if not lista_mensajes:
            return None
        while lista_mensajes:
            lista = lista_mensajes.popleft()
            mensaje = Mensaje(lista[0], lista[1], lista[2], datetime.fromisoformat(lista[3]))
            self.central.registrar_mensaje_nuevo(mensaje)

class ManejadorLlamadas(ManejadorCSV):
    """
    Clase para manejar archivos CSV específicos de llamadas.
    Hereda de ManejadorCSV.
    """

    def __init__(self, nombre_archivo, central):
        """
        Inicializa la clase ManejadorLlamadas con el nombre del archivo y la central.

        Args:
            nombre_archivo (str): El nombre del archivo CSV.
            central (Central): La instancia de la central telefónica.
        """
        super().__init__(nombre_archivo)
        self.central = central

    def exportar_llamadas(self):
        """
        Exporta las llamadas a un archivo CSV.
        """
        self.exportar([['Emisor', 'Receptor', 'Duracion', 'Fecha Inicio', 'Perdida']])
        while self.central.registro_llamadas:
            llamada = self.central.registro_llamadas.popleft()
            duracion = str(llamada.get_duracion())[:-7:] if len(str(llamada.get_duracion())[:-7:]) > 6 else str(llamada.get_duracion())
            self.exportar([[llamada.get_emisor(), llamada.get_receptor(), duracion, llamada.get_fecha(), llamada.get_perdida()]], "a")

    def cargar_llamadas(self):
        """
        Carga las llamadas desde un archivo CSV y las registra en la central.
        """
        lista_llamadas = self.leer_archivo(True)
        if not lista_llamadas:
            return None
        for llamada in lista_llamadas:
            duracion = datetime.strptime(llamada[2],'%H:%M:%S').time()
            duracion_en_formato = timedelta(hours=duracion.hour, minutes=duracion.minute, seconds=duracion.second)
            self.central.registrar_llamada(Llamada(llamada[0], llamada[1], duracion_en_formato , datetime.fromisoformat(llamada[3]), llamada[4] == "True"))

class ManejadorContactos(ManejadorCSV):
    """
    Clase para manejar archivos CSV específicos de contactos.
    Hereda de ManejadorCSV.
    """

    def __init__(self, nombre_archivo, central):
        """
        Inicializa la clase ManejadorContactos con el nombre del archivo y la aplicación 
        de contactos.

        Args:
            nombre_archivo (str): El nombre del archivo CSV.
            contactos_app (ContactosApp): La instancia de la aplicación de contactos.
        """
        super().__init__(nombre_archivo)
        self.central = central

    def exportar_contactos(self):
        """
        Exporta los contactos a un archivo CSV.
        """
        self.exportar([['Numero Celuar','Nombre', 'Numero Contacto']])
        for celular in self.central.registro_dispositivos.values():
            for numero, contacto in celular.aplicaciones["Contactos"].agenda.items():
                self.exportar([[celular.aplicaciones['Configuracion'].configuracion.numero, contacto, numero]], "a")

    def cargar_contactos(self):
        """
        Carga los contactos desde un archivo CSV y los registra en la aplicación de contactos.
        """
        lista_contactos = self.leer_archivo(True)
        if not lista_contactos:
            return None
        for linea in lista_contactos:
            celular = self.central.registro_dispositivos[linea[0]]
            celular.aplicaciones["Contactos"].agregar_contacto(linea[2], linea[1])

class ManejadorDispositivos(ManejadorCSV):
    """
    Clase para manejar archivos CSV específicos de dispositivos.
    Hereda de ManejadorCSV.
    """

    def __init__(self, nombre_archivo, central):
        """
        Inicializa la clase ManejadorDispositivos con el nombre del archivo y la central.

        Args:
            nombre_archivo (str): El nombre del archivo CSV.
            central (Central): La instancia de la central telefónica.
        """
        super().__init__(nombre_archivo)
        self.central = central

    def exportar_dispositivos(self):
        """
        Exporta los dispositivos a un archivo CSV.
        """
        self.exportar([['Nombre', 'Modelo', 'Numero', 'Sistema Operativo', 'Memoria RAM', 'Almacenamiento', 'ID', 'Encendido', 'Bloqueado','Contraseña', 'Aplicaciones']])
        for celular in self.central.registro_dispositivos.values():
            if celular.aplicaciones["Configuracion"].configuracion.contrasenia is None:
                contrasenia = "None"
            else:
                contrasenia = celular.aplicaciones["Configuracion"].configuracion.contrasenia
            lista = [
                celular.aplicaciones["Configuracion"].configuracion.nombre,
                celular.modelo,
                celular.aplicaciones["Configuracion"].configuracion.numero,
                celular.sistema_operativo,
                celular.memoria_ram,
                celular.almacenamiento_original,
                celular.id_celular,
                celular.encendido,
                celular.bloqueado,
                contrasenia
            ]
            #Instala las aplicaciones que no se instalan solas
            lista.extend(nombre for nombre, app in celular.aplicaciones.items() if app.es_esencial() is False)
            self.exportar([lista], "a")

    def cargar_dispositivos(self):
        """
        Carga los dispositivos desde un archivo CSV y los registra en la central.
        
        Return:
            lista_celulares (list): Lista de objetos Celular.
        """
        lista_celulares = []
        lista_dispositivos = self.leer_archivo(True)
        if not lista_dispositivos:
            return None
        for dispositivo in lista_dispositivos:
            celular = Celular(
                nombre = dispositivo[0],
                modelo = dispositivo[1],
                numero = dispositivo[2],
                sistema_operativo = dispositivo[3],
                memoria_ram = dispositivo[4],
                almacenamiento = dispositivo[5],
                id_celular = dispositivo[6]
            )

            if dispositivo[7] == "True":
                celular.encender_dispositivo()

            if dispositivo[9] != "None":
                celular.aplicaciones["Configuracion"].configurar_contrasenia(contrasenia_nueva = dispositivo[9])

            if dispositivo[8] == "True":
                celular.bloquear_dispositivo()

            for aplicacion in dispositivo[10:]:
                celular.aplicaciones["AppStore"].descargar_app(aplicacion, carga_datos = True)
            self.central.registrar_dispositivo(dispositivo[2], celular)
            lista_celulares.append(celular)

        return lista_celulares

class ManejadorMails(ManejadorCSV):
    """
    Clase para manejar archivos CSV específicos de mails.
    Hereda de ManejadorCSV.
    """

    def exportar_mails(self):
        """
        Exporta los mails a un archivo CSV. Exporta solo los de la bandeja de entrada,
        de forma de que no haya mails duplicados.
        """
        self.exportar([['Cuerpo', 'Emisor', 'Receptor', 'Asunto', 'Fecha', 'Leido']])
        for cuenta in CuentaMail.cuentas.values():
            for mail in cuenta.bandeja_entrada:
                self.exportar([[mail.cuerpo, mail.emisor, mail.receptor, mail.asunto, mail.fecha, mail.leido]], "a")

    def cargar_mails(self):
        """
        Carga los mails desde un archivo CSV y los registra en la bandeja de entrada
        o enviados de cada cuenta, segun si es el receptor o emisor, respectivamente.
        """
        formato_fecha = "%Y-%m-%d %H:%M:%S.%f"
        lista_mails = self.leer_archivo(True)
        for mail in lista_mails:
            mail = Mail(cuerpo = mail[0], emisor = mail[1], receptor = mail[2], asunto = mail[3], fecha = datetime.strptime(mail[4], formato_fecha), leido = mail[5]=="True")
            CuentaMail.cuentas[mail.receptor].bandeja_entrada.append(mail)
            CuentaMail.cuentas[mail.emisor].bandeja_enviados.append(mail)

class ManejadorCuentasMail(ManejadorCSV):
    """
    Clase para manejar archivos CSV específicos de cuentas de mail.
    Hereda de ManejadorCSV.
    """

    def exportar_cuentas(self):
        """
        Exporta las cuentas de mail a un archivo CSV.
        """
        self.exportar([['Usuario', 'Contraseña']])
        for cuenta in CuentaMail.cuentas.values():
            self.exportar([[cuenta.mail, cuenta.contrasenia]], "a")

    def cargar_cuentas(self):
        """
        Carga las cuentas de mail desde un archivo CSV y las registra en la aplicación de mail.
        """
        lista_cuentas = self.leer_archivo(True)
        if not lista_cuentas:
            return None
        for cuenta in lista_cuentas:
            CuentaMail(cuenta[0], cuenta[1])
