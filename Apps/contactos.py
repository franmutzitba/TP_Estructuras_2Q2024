from Apps.aplicacion import Aplicacion

class ContactosApp(Aplicacion):
    def __init__(self):
        super().__init__(nombre = "Contacto", tamanio = "800 MB", esencial = True)
        self.agenda = {}

    def get_contactos(self):
        return self.agenda

    def agregar_contacto(self, numero, nombre):
        self.agenda[numero] = nombre
    
    def __str__(self):
        return f"Agenda de contactos: {self.agenda}"