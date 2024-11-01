"""
Módulo que contiene la aplicación AppStore
"""

import os
from Apps.aplicacion import Aplicacion
from Apps.configuracion import ConfigApp, ModoRed
from manejadorCSV import ManejadorCSV
from funciones_utiles import tamanio_a_bytes

class AppStore(Aplicacion):
    """
    Clase que representa la tienda de aplicaciones de un celular
    
    Atributos:
    ----------
    exportador (ManejadorCSV):
        Manejador para exportar datos a un archivo CSV.
    aplicaciones_celular (dict):
        Diccionario que contiene las aplicaciones instaladas en el celular.
    configuracion (Configuracion):
        Configuración del dispositivo, incluyendo almacenamiento disponible.
        
    Métodos:
    --------
    __init__(self, aplicaciones_celular, configuracion: Configuracion):
        Inicializa una instancia de AppStore para cada celular, con las aplicaciones instaladas 
        en el celular y la configuración del dispositivo.
    mostrar_apps_disponibles(self):
        Muestra las aplicaciones disponibles en la tienda, indicando si ya están instaladas 
        en el celular.
    descargar_app(self, nombre):
        Descarga una aplicación de la tienda al celular, si hay suficiente espacio y no está 
        ya instalada. Para descargarla se agrega a las aplicaciones del celular y se resta el 
        espacio de almacenamiento disponible.
    desinstalar_app(self, nombre):
        Desinstala una aplicación del celular, si no es esencial y está instalada.
    agregar_descarga(self, nombre):
        Incrementa el contador de descargas de una aplicación y actualiza el archivo CSV.
    consultar_tamanio(self, nombre):
        Consulta el tamaño de una aplicación disponible en la tienda.
    aplicaciones_disponibles(self):
        Devuelve una lista de las aplicaciones disponibles en la tienda.
    __str__(self):
        Devuelve una representación en cadena de la instancia de AppStore.
    """
    exportador = ManejadorCSV("appstore.csv")

    def __init__(self, aplicaciones_celular, configuracion: ConfigApp):
        """
        Args:
            aplicaciones_celular (list): Lista de aplicaciones instaladas en el celular.
            configuracion (Configuracion): Objeto de configuración que contiene las 
            configuraciones del celular
        """
        super().__init__(nombre = "AppStore", tamanio = "200 MB", esencial = True)
        self.aplicaciones_celular = aplicaciones_celular
        self.configuracion = configuracion

    def mostrar_apps_disponibles(self):
        """Muestra las aplicaciones disponibles en la tienda, indicando si ya están 
        instaladas en el celular.
        
        Returns:
            None
        """
        if self.configuracion.get_modo_red() != ModoRed.LTE:
            raise ValueError("No es posible mostrar las aplicaciones disponibles en este momento. Consulte su conexión a internet")

        aplicaciones_disponibles = self.aplicaciones_disponibles()
        for app in aplicaciones_disponibles:
            if app[0] not in self.aplicaciones_celular:
                print(f"Nombre: {app[0]} - Tamaño: {app[1]}")
            else:
                print(f"Nombre: {app[0]} - Tamaño: {app[1]} - INSTALADA")

    def descargar_app(self, nombre):
        """Descarga una aplicación de la tienda al celular, si hay suficiente espacio
        y no está ya instalada. Para descargarla se agrega al diccionario de las aplicaciones 
        del celular y se resta el espacio de almacenamiento disponible.
        
        Args:
            nombre (str): Nombre de la aplicación a descargar.
        
        Returns:
            None
            
        Raises:
            ValueError: Si la aplicación ya está instalada, no hay suficiente espacio o 
            no se encuentra en la tienda.
        """
        if nombre in self.aplicaciones_celular:
            raise ValueError(f"La aplicación {nombre} ya se encuentra instalada")
        if self.configuracion.get_modo_red() != ModoRed.LTE:
            raise ValueError("No es posible descargar aplicaciones en este momento. Consulte su conexión a internet")

        encontrada = False
        aplicaciones_disponibles = self.aplicaciones_disponibles()
        for app in aplicaciones_disponibles:
            if app[0] == nombre and encontrada is False:
                if tamanio_a_bytes(app[1]) <= self.configuracion.get_almacenamiento_disponible():
                    self.aplicaciones_celular[nombre] = Aplicacion(nombre=nombre, tamanio=app[1], esencial=False) # Instancia de la clase Aplicacion. Se asume que las apps descargadas del appstore no son esenciales.
                    nuevo_almacenamiento = self.configuracion.get_almacenamiento_disponible() - tamanio_a_bytes(app[1])
                    self.configuracion.set_almacenamiento_disponible(nuevo_almacenamiento)
                    self.agregar_descarga(nombre)
                    print(f"La aplicación {nombre} se ha descargado correctamente")
                else:
                    raise ValueError(f"No hay suficiente espacio para instalar la aplicación {nombre}")
                encontrada = True
        if encontrada is False:
            raise ValueError(f"La aplicación {nombre} no se encuentra en la AppStore")

    def desinstalar_app(self, nombre):
        """Desinstala una aplicación del celular, si no es esencial y está instalada. 
        Para desinstalarla la elimina del diccionario de aplicaciones del celular y 
        suma el espacio de almacenamiento disponible.
    
        Args:
            nombre (str): Nombre de la aplicación a desinstalar.
        
        Returns:
            None
            
        Raises:
            ValueError: Si la aplicación no está instalada o si es una aplicación esencial.
        """
        if nombre not in self.aplicaciones_celular:
            raise ValueError(f"La aplicación {nombre} no se encuentra instalada")
        if self.aplicaciones_celular[nombre].es_esencial():
            raise ValueError(f"La aplicación {nombre} es esencial y no se puede desinstalar")

        self.aplicaciones_celular.pop(nombre)
        nuevo_almacenamiento = self.configuracion.get_almacenamiento_disponible() + self.consultar_tamanio(nombre)
        self.configuracion.set_almacenamiento_disponible(nuevo_almacenamiento)
        print(f"La aplicación {nombre} se ha desinstalado correctamente")

    def agregar_descarga(self, nombre):
        """Incrementa el contador de descargas de una aplicación específica y actualiza el CSV.

        Args:
            nombre (str): El nombre de la aplicación cuya descarga se va a incrementar.

        Returns:
            None
        """
        aplicaciones_disponibles = self.aplicaciones_disponibles()
        for app in aplicaciones_disponibles:
            if app[0] == nombre:
                app[2] = int(app[2]) + 1
        aplicaciones_disponibles.insert(0, ["Nombre", "Tamaño", "Descargas"])
        AppStore.exportador.exportar(aplicaciones_disponibles)

    def consultar_tamanio(self, nombre):
        """Consulta el tamaño de una aplicación específica de la tienda por su nombre.

        Args:
            nombre (str): El nombre de la aplicación cuyo tamaño se desea consultar.

        Returns:
            int: El tamaño de la aplicación en MB si se encuentra, de lo contrario None.
        """
        aplicaciones_disponibles = self.aplicaciones_disponibles()
        for app in aplicaciones_disponibles:
            if app[0] == nombre:
                return tamanio_a_bytes(app[1])

    def aplicaciones_disponibles(self):
        """Obtiene la lista de aplicaciones disponibles en la appstore desde el archivo CSV.
        
        Returns:
            list: Una lista de aplicaciones disponibles. Si el archivo no se encuentra, 
            retorna una lista vacía.
        """
        try:
            return AppStore.exportador.leer_archivo(True)
        except FileNotFoundError:
            return []

    def listar_apps_instaladas(self):
        """Imprime las aplicaciones instaladas en el celular.
        
        Returns:
            None
        """
        for app in self.aplicaciones_celular:
            print(app)

    def buscar_app(self, nombre):
        """Lista todas las aplicaciones disponibles en la tienda que contienen el nombre ingresado.
        
        Args:
            nombre (str): Nombre de la aplicación a buscar.
               
        Returns:
            None
        """
        if self.configuracion.get_modo_red() != ModoRed.LTE:
            raise ValueError("No es posible buscar aplicaciones en este momento. Consulte su conexión a internet")
        encontrado = False
        aplicaciones_disponibles = self.aplicaciones_disponibles()
        for app in aplicaciones_disponibles:
            if nombre.lower() in app[0].lower():
                print(f"Nombre: {app[0]} - Tamaño: {app[1]}")
                encontrado = True
        if encontrado is False:
            raise ValueError(f"No se encontraron aplicaciones con el nombre {nombre}")

    def menu_navegacion(self):
        """Menú de navegación de la AppStore.
        
        Returns:
            None
        """
        os.system('cls')
        print("\nBienvenido a la AppStore")
        salir = False
        while not salir:
            print("\nMenu de AppStore")
            print("1. Listar todas las aplicaciones disponibles en la AppStore")
            print("2. Descargar aplicación")
            print("3. Desinstalar aplicación")
            print("4. Buscar aplicación por nombre")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                os.system('cls')
                self.mostrar_apps_disponibles()
                input("Presione cualquier tecla para volver al menu de AppStore...")
                os.system('cls')
            elif opcion == "2":
                os.system('cls')
                nombre = input("Ingrese el nombre de la aplicación a descargar: ")
                try:
                    self.descargar_app(nombre)
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de AppStore...")
                os.system('cls')
            elif opcion == "3":
                os.system('cls')
                nombre = input("Ingrese el nombre de la aplicación a desinstalar: ")
                try:
                    self.desinstalar_app(nombre)
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de AppStore...")
                os.system('cls')
            elif opcion == "4":
                os.system('cls')
                nombre = input("Ingrese el nombre de la aplicación a buscar: ")
                try:
                    self.buscar_app(nombre)
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de AppStore...")
                os.system('cls')
            elif opcion == "5":
                os.system('cls')
                print("Saliendo de la AppStore")
                salir = True
                input("Presione cualquier tecla para volver al menu del celular...")
                os.system('cls')
            else:
                os.system('cls')
                print("Opción inválida, intente nuevamente")
                input("Presione cualquier tecla para volver al menu de AppStore...")
                os.system('cls')
