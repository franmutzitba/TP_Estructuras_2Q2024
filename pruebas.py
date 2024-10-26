from datetime import datetime
fecha = datetime.now()

print(fecha.strftime("%Y-%m-%d %H:%M"))

dic={
    "1":2
}

if dic["3"]:
    print("Hola")