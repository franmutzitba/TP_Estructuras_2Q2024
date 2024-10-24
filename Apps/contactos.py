from aplicacion import Aplicacion

class ContactosApp(Aplicacion):
    def __init__(self):
        super().__init__("Contacto", 800, True)
        self.agenda = {}

    def get_contactos(self):
        return self.agenda

    def agregar_contacto(self, numero, nombre):
        self.agenda[numero] = nombre
    
    def __str__(self):
        return f"Agenda de contactos: {self.agenda}"