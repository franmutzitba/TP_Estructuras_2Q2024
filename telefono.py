from aplicacion import Aplicacion
from celular import Celular
from central import Central
from comunicacion import Llamada, Llamada_perdida

class Telefono(Aplicacion):
    
    todos_los_telefonos = {}
    def __init__(self, celular:Celular, contactos:dict):
        super().__init__("Telefono", 200, True)
        self.numero = celular.get_numero()
        self.historial_llamadas = []
        self.contactos = contactos                            #ver como poner los contactos en un diccionario aca. la calve debe ser el numero telefonico y el valor el nombre del contacto.
        Telefono.todos_los_telefonos[self.numero] = self

    def numero_en_contactos(self, numero):
        return numero in self.contactos.keys() 
    
    def nombre_contacto(self, numero):
        return self.contactos.get(numero)

    def iniciar_llamada_contacto(self, contacto_receptor):
        if not contacto_receptor in self.contactos.values():
            raise ValueError("No tiene ningun contacto con ese nombre")
        else: 
            for clave, valor in self.contactos.items():
                #puede haber dos contactos con el mismo nombre? si los hay a quien llamo?
                1 = 2

    def iniciar_llamada_numero(self, numero_receptor):
            Central.manejar_llamada(self.numero, numero_receptor)
    

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

         
    def ver_historial_llamadas(self):
         for llamada in self.historial_llamadas:
              print(llamada)
              
