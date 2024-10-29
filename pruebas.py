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

pila2 = pila
while pila2:
    print(pila2.popleft())

print(pila)

from comunicacion import Mensaje 
mensaje = Mensaje("1","2","hola",datetime.now())
print(mensaje)

cadena = "Hola"
print("ol" in cadena)