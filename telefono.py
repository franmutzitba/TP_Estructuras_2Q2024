from aplicacion import Aplicacion
from central import Central
from comunicacion import Llamada

class TelefonoApp(Aplicacion):
    def __init__(self, numero, central:Central):
        super().__init__("Telefono", 200, True)
        self.numero = numero
        self.contactos = {}                 #ver como poner los contactos en un diccionario aca. la calve debe ser el numero telefonico y el valor el nombre del contacto.
        self.central = central
        ocupado = False
        
    def agregar_contacto(self, numero, nombre):
        self.contactos[numero] = nombre

    def numero_en_contactos(self, numero):
        return numero in self.contactos.keys() 
    
    def nombre_contacto(self, numero):
        return self.contactos.get(numero)

    def iniciar_llamada_contacto(self, nombre_receptor):
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
                self.iniciar_llamada(contactos_con_ese_nombre[j-1])
            else:
                self.iniciar_llamada(contactos_con_ese_nombre[1])


    def iniciar_llamada(self, numero_receptor):
            self.central.manejar_llamada(self.numero, numero_receptor)
    
'''
    def actualizar_historial_aceptada(self, llamada:Llamada):
        if llamada.emisor == self.numero:
            emisor = "su celular"
            if self.numero_en_contactos(llamada.receptor):
                receptor = self.nombre_contacto(llamada.receptor)
            else:
                receptor = llamada.receptor

        else:
            receptor = "su celular"
            if self.numero_en_contactos(llamada.emisor):
                emisor = self.nombre_contacto(llamada.emisor)
            else:
                emisor = llamada.emisor

        self.historial_llamadas.append(f"Llamada realizada, emisor: {emisor}, receptor: {receptor}, duracion: {llamada.duracion}")

    def actualizar_historial_perdida(self, llamada:Llamada_perdida):
         
        if llamada.emisor == self.numero:
            emisor = "su celular"
            if self.numero_en_contactos(llamada.receptor):
                receptor = self.nombre_contacto(llamada.receptor)
            else:
                receptor = llamada.receptor

        else:
            receptor = "su celular"
            if self.numero_en_contactos(llamada.emisor):
                emisor = self.nombre_contacto(llamada.emisor)
            else:
                emisor = llamada.emisor

        self.historial_llamadas.append(f"Llamada no realizada, emisor: {emisor}, receptor: {receptor}, tipo: {llamada.tipo}")
'''

#def mostrar_historial_llamadas(self):
#    historial = []
#    for clave, valor in self.central.registro_llamadas.values():


              
