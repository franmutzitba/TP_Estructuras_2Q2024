from Apps.aplicacion import Aplicacion
from central import Central
from comunicacion import Llamada
from Apps.contactos import ContactosApp
import datetime

class TelefonoApp(Aplicacion):
    def __init__(self, numero, central, contactos):
        super().__init__("Telefono", 200, True)
        self.numero = numero
        self.contactos = contactos.agenda                 #ver como poner los contactos en un diccionario aca. la calve debe ser el numero telefonico y el valor el nombre del contacto.
        self.central = central
        

    def numero_en_contactos(self, numero):
        return numero in self.contactos.keys() 
    
    def nombre_contacto(self, numero):
        return self.contactos.get(numero)

    def iniciar_llamada_contacto(self, nombre_receptor, duracion, hora_inicio):
        
        if not nombre_receptor in self.contactos.values():
            raise ValueError("No tiene ningun contacto con ese nombre")
        else: 
            for clave, valor in self.contactos.items():
                #puede haber dos contactos con el mismo nombre? si los hay a quien llamo?
                contactos_con_ese_nombre = []           # guarda los numeros telefonicos de los contactos con ese nombre
                if valor == nombre_receptor:
                    contactos_con_ese_nombre.append(clave)

            if len(contactos_con_ese_nombre)>1:
                print("Tiene mas de un contacto con ese nombre, a cual desea llamar?")
                i = 0
                while contactos_con_ese_nombre[i]:
                    i+=1
                    print(f"Contacto {i}: Numero: {contactos_con_ese_nombre[i-1]}")
                j = 1                                       # aca hay que hacer un input creo para decidir a que contacto llamar
                self.iniciar_llamada(self.numero, contactos_con_ese_nombre[j-1], hora_inicio, duracion,)
            else:
                self.iniciar_llamada(self.numero, contactos_con_ese_nombre[1], hora_inicio, duracion)


    def iniciar_llamada(self, numero_receptor, duracion=5): #duracion en minutos
        if duracion > 60:
            raise ValueError("La duracion no puede ser mayor a una hora")
        hora_inicio = datetime.now()
        duracion = datetime.timedelta(0, 0, 0, 0, duracion)
        self.central.manejar_llamada(self.numero, numero_receptor, hora_inicio, duracion)
    
    def mostrar_historial_llamadas(self):
        historial = []
        for receptor, historial_receptor in self.central.registro_llamadas.values():
            for emisor, historial_emisor_receptor in self.central.registro_llamadas[receptor].values():          #historial_emisor_receptor es una lista
                for llamada in historial_emisor_receptor:
                    historial.append(llamada)
                    
            
        
    
