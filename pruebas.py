import datetime
from collections import deque

fecha_hoy = datetime.datetime.now()
fecha_random1 = datetime.datetime(2021, 12, 31, 23, 59, 59)
fecha_random2 = datetime.datetime(2023, 12, 31, 23, 55, 59)
fecha_random3 = datetime.datetime(2022, 1, 1, 0, 0, 0)
fecha_random4 = datetime.datetime(2019, 3, 27, 20, 0, 0)
fecha_random5 = datetime.datetime(2016, 3, 27, 20, 0, 0)
delta = datetime.timedelta(minutes=1)

print(isinstance(fecha_hoy - fecha_random1, datetime.timedelta))

print(fecha_random1)
l = {"1":2, "2":3}
print(l.get("1"))
print(len(l))
for i, contacto in enumerate(l):
    print(f"{i+1}. {contacto}")
z = list(l.values())
for valor in z:
    print(z.index(valor)+1)
a = deque()
b = deque()

a.appendleft(fecha_random1)
a.appendleft(fecha_random2)
a.appendleft(fecha_random3)

b.appendleft(fecha_hoy)
b.appendleft(fecha_random4)
b.appendleft(fecha_random5)
print("WWWWWWWWWWWWWWWWWWWWWWWWw")
x = deque()
print(min(a +x))
print(a[0])

print(sorted(list(a + b), reverse=True))
llamadas = a + b
while llamadas:
    print(llamadas.popleft())
    
print(datetime.datetime.strptime(str(delta),'%H:%M:%S').time() == delta)

c = datetime.datetime.strptime(str(delta),'%H:%M:%S').time()
print( fecha_hoy > fecha_random1 + c)

