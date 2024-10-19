from aplicacion import Aplicacion
from configuracion import Configuracion
import csv

class AppStore(Aplicacion):
    def __init__(self, aplicaciones_celular, configuracion: Configuracion):
        super().__init__("AppStore", 200, True)
        self.aplicaciones_celular = aplicaciones_celular
        self.configuracion = configuracion
    
    def mostrar_apps(self):
        aplicaciones_disponibles = self.aplicaciones_disponibles()
        for app in aplicaciones_disponibles:
            if app[0] not in self.aplicaciones_celular:
                print(f"Nombre: {app[0]} - Tamaño: {app[1]}mb")
            else:
                print(f"Nombre: {app[0]} - Tamaño: {app[1]}mb - INSTALADA")
        
    def descargar_app(self, nombre):
        encontrada = False
        if nombre in self.aplicaciones_celular:
            raise ValueError(f"La aplicación {nombre} ya se encuentra instalada")
        else:
            aplicaciones_disponibles = self.aplicaciones_disponibles()
            for app in aplicaciones_disponibles:
                if app[0] == nombre and encontrada == False:
                    if int(app[1]) <= self.configuracion.get_almacenamiento_disponible():
                        self.aplicaciones_celular[nombre] = None
                        nuevo_almacenamiento = self.configuracion.get_almacenamiento_disponible() - int(app[1])
                        self.configuracion.set_almacenamiento_disponible(nuevo_almacenamiento)
                        self.agregar_descarga(nombre)
                        print(f"La aplicación {nombre} se ha descargado correctamente")
                    else:
                        raise ValueError(f"No hay suficiente espacio para instalar la aplicación {nombre}")
                    encontrada = True
            if encontrada == False:
                raise ValueError(f"La aplicación {nombre} no se encuentra en la AppStore")
    
    def desinstalar_app(self, nombre):
        if nombre not in self.aplicaciones_celular:
            raise ValueError(f"La aplicación {nombre} no se encuentra instalada")
        else:
            self.aplicaciones_celular.pop(nombre)
            nuevo_almacenamiento = self.configuracion.almacenamiento_disponible + self.consultar_tamanio(nombre)
            self.configuracion.set_almacenamiento_disponible(nuevo_almacenamiento)
            print(f"La aplicación {nombre} se ha desinstalado correctamente")
    
    def agregar_descarga(self, nombre):
        aplicaciones_disponibles = self.aplicaciones_disponibles()
        with open("appstore.csv", "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Nombre", "Tamaño", "Descargas"])
            for app in aplicaciones_disponibles:
                if app[0] == nombre:
                    app[2] = int(app[2]) + 1
                    escritor.writerow(app)
                else:
                    escritor.writerow(app)
    
    def consultar_tamanio(self, nombre):
        aplicaciones_disponibles = self.aplicaciones_disponibles()
        for app in aplicaciones_disponibles:
            if app[0] == nombre:
                return int(app[1])
     
    def aplicaciones_disponibles(self):
        apps = []
        with open("appstore.csv", "r", encoding="utf-8") as archivo:
            archivo.__next__() #Omito la primer linea
            lector = csv.reader(archivo)
            for fila in lector:
                apps.append(fila)
        return apps
    
    def __str__(self):
        return super().__str__()
