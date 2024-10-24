from aplicacion import Aplicacion
from collections import deque

class MailApp(Aplicacion):
    def __init__(self):
        super().__init__("Mail", 100, True)
        self.bandeja_de_entrada = deque()

    def importar_mail(self, mail): #hay que ver como guardar los mails de cada celular en un archivo
        self.bandeja_de_entrada.append(mail)

    def ver_mails(self, criterio):
        if (criterio == "no leídos primeros"):
            no_leidos = deque(mail for mail in self.bandeja_de_entrada if not mail.leido)
            while no_leidos:
                print(no_leidos.popleft())
        elif (criterio == "por fecha"):
            pila = self.bandeja_de_entrada.copy()
            while pila:
                print(pila.pop())
        else:
            raise ValueError("Criterio no válido")

class Mail:
    def __init__(self, cuerpo, email_emisor, encabezado, leido=False):
        self.cuerpo = cuerpo
        self.email_emisor = email_emisor
        self.encabezado = encabezado
        self.leido = leido

    def __str__(self):
        return f"Encabezado: {self.encabezado}, Emisor: {self.email_emisor}, Leído: {self.leido}, Cuerpo: {self.cuerpo}"
    