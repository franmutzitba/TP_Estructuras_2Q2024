from datetime import datetime
from collections import deque
fecha = datetime.now()

print(fecha.strftime("%Y-%m-%d %H:%M"))

dic={
    "1":2
}



pila = deque()
pila.appendleft("1")
pila.appendleft("2")
pila.appendleft("3")

print("1" in pila)
print(pila[2])
pila2 = pila
while pila2:
    print(pila2.popleft())

print(pila)


from comunicacion import Mensaje 
mensaje = Mensaje("1","2","hola",datetime.now())
print(mensaje)

cadena = "Hola"
print("ol" in cadena)

contacto = 1 if 1==1 else 0
print(contacto)

class Messi:
    def __init__(self, hola):
        self.hola = hola
        
    def validar(numero):
        return numero is 0
    
    def hola(self, numero):
        return Messi.validar(numero)
    
messi = Messi("lol")

if False and True:
    print("messi")

