from aplicacion import Aplicacion
from celular import Celular

class Telefono(Aplicacion):
    def __init__(self, celular: Celular):
        super().__init__("Telefono", 200, True)

