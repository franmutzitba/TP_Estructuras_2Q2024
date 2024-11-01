from Apps.aplicacion import Aplicacion
from comunicacion import Mensaje
from datetime import datetime
from central import Central
from collections import deque
from Apps.contactos import ContactosApp
import os

class MensajesApp(Aplicacion):
    def __init__(self, numero ,contactos: ContactosApp, central: Central):
        super().__init__(nombre = "MensajeriaSMS", tamanio = "100 MB", esencial = True,)
        self.numero_cel = numero
        self.contactos = contactos.agenda
        self.central = central
        self.mensajes = deque() 
    
    def crear_mensaje(self, receptor: str, mensaje: str):
        return Mensaje(self.numero_cel, receptor, mensaje,datetime.now())

    def numero_en_contactos(self, numero):
        return numero in self.contactos
 
    def nombre_en_contactos(self, nombre):
        return nombre in self.contactos.values()
    
    def nombre_contacto(self, numero):
        return self.contactos[numero]

    def numeros_de_nombre(self, nombre):
        lista=deque()
        i=1
        for numero, nombre in self.contactos.items():
            if nombre == nombre:
                lista.append(numero)
                i+=1
        return lista

    def enviar_sms(self, receptor, texto):
        if self.central.manejar_mensaje(self.numero_cel, receptor):
            mensaje = self.crear_mensaje(receptor, texto)
            self.central.registrar_mensaje_nuevo(mensaje)
            print(f"Mensaje enviado correctamente al numero {receptor}") 

    def recibir_sms(self, mensaje: Mensaje):
        if not(mensaje.get_sincronizado()):
            mensaje.set_sincronizado()
            self.mensajes.appendleft(mensaje)
        else:
            print("El mensaje ya ha sido recibido")
    
    def ver_bandeja_de_entrada(self):
        bandeja_de_entrada = self.mensajes.copy()
        i=1
        if not(bandeja_de_entrada):
            raise ValueError(f"El numero -{self.numero_cel}- no tiene mensajes en la bandeja de entrada")
        print(f"Bandeja de Entrada del numero: {self.numero_cel}")
        
        while bandeja_de_entrada:
            print(f"- {i} - ", end="")
            mensaje = bandeja_de_entrada.popleft()
            if self.numero_en_contactos(mensaje.get_emisor()) :
                fecha_min = mensaje.fecha.strftime("%Y-%m-%d %H:%M")
                print(f"Emisor: {self.nombre_contacto(mensaje.get_emisor())}, Texto: {mensaje.mensaje}, Fecha: {fecha_min}")
            else:
                print(f"Emisor: {mensaje.get_emisor()}, Texto: {mensaje.mensaje}, Fecha: {fecha_min}")
            i += 1
        
    def ver_mensajes_de(self, numero, contacto):
        mensajes = self.mensajes.copy()
        i=1
        print(f"Mensajes de: {contacto if contacto else numero}")
        while mensajes:
            mensaje = mensajes.popleft()
            if mensaje.get_emisor() == numero:
                print(f"- {i} - ", end="")
                fecha_min = mensaje.fecha.strftime("%Y-%m-%d %H:%M")
                print(f"Texto: {mensaje.mensaje}, Fecha: {fecha_min}")
                i += 1
    
    def ver_chats_recientes(self):
        if not self.mensajes:
            raise ValueError(f"EL numero: {self.numero_cel} no tiene mensajes") 
        recientes = deque() #cola de numeros/contactos recientes
        mensajes = self.mensajes.copy()
        i=1
        while mensajes:
            mensaje = mensajes.popleft()
            if mensaje.get_emisor() not in recientes:
                recientes.append(mensaje.get_emisor())
                print(f"{i} - {self.nombre_contacto(mensaje.get_emisor()) if self.numero_en_contactos(mensaje.get_emisor()) else mensaje.get_emisor()}")
                i +=1
        return recientes 
    
    def eliminar_mensaje(self, indice):
        mensaje = self.mensajes[indice-1]
        self.mensajes.remove(mensaje)
        self.central.eliminar_mensaje(mensaje, self.numero_cel)

    @staticmethod
    def validar_indice(indice, len):
        return  indice.isdigit() and (not int(indice) < 1) and (not int(indice) > len)

    def __str__(self):
        return f"Aplicacion Mensajeria del numero: {self.numero_cel}"
    
    def menu_navegacion(self):
        os.system('cls')
        print(f"\nBienvenido a la aplicacion de Mensajes SMS del numero {self.numero_cel}")
        salir = False
        while not salir:
            print(f"\nAplicacion de Mensajes SMS del numero {self.numero_cel}:")
            print("1. Enviar mensaje")
            print("2. Ver bandeja de entrada")
            print("3. Ver bandeja de entrada por numero/contacto")
            print("4. Eliminar Mensaje")
            print("5. Salir")
            opcion = input("Ingrese el número de la opción deseada: ")
            if opcion == "1":
                print("1. Enviar mensaje a contaco")
                print("2. Enviar mensaje a numero ")
                opcion2 = input("Ingrese el número de la opción deseada: ")
                try:
                    if opcion2 == "1":
                        os.system('cls')
                        receptor = input("Ingrese el nombre del contacto receptor: ")
                        if not self.nombre_en_contactos(receptor):
                            raise ValueError(f"El nombre: {receptor} no se encuentra en la lista de contactos")
                        lista = self.numeros_de_nombre(receptor)
                        if len(lista) > 1:
                            print(f"Numeros del contacto: {receptor}")
                            lista2 = lista.copy()
                            while lista2:
                                print(lista2)
                            indice = (input("Ingrese el indice del contacto deseado: "))
                            while not MensajesApp.validar_indice(indice,len(lista)): #Puedo hacer un metodo de validacion
                                indice = input("Entrada incorrecta. Ingrese el indice del contacto deseado: ")
                        else:
                            indice = 1
                        numero = lista[indice-1]
                        texto = input("Ingrese el mensaje a enviar: ")
                        if not texto:
                            raise ValueError("No se pueden enviar mensajes vacios")
                        self.enviar_sms(numero, texto)                 

                    elif opcion2 == "2":
                        os.system('cls')
                        receptor = input("Ingrese el número de teléfono del receptor: ")
                        texto = input("Ingrese el mensaje a enviar: ")
                        if not texto:
                            raise ValueError("No se pueden enviar mensajes vacios")
                        self.enviar_sms(receptor, texto)
                    else:
                        os.system('cls')
                        print("Opción inválida, intente nuevamente")
                except ValueError as e:
                    os.system('cls')
                    print(e)
                input("Presione cualquier tecla para volver al menu de la Mensajeria... ")
                os.system('cls')
            elif opcion == "2":
                os.system("cls")
                try:
                    self.ver_bandeja_de_entrada()
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de la Mensajeria... ")
                os.system('cls')
            elif opcion == "3":
                os.system('cls')
                try:
                    recientes = self.ver_chats_recientes()
                    indice = input("Ingrese el número del chat deseado: ")
                    while not MensajesApp.validar_indice(indice, len(recientes)):
                        indice = input("Entrada incorrecta. Ingrese el número del chat deseado: ")
                    emisor = recientes[int(indice)-1]
                    contacto = self.nombre_contacto(emisor) if self.numero_en_contactos(emisor) else None
                    self.ver_mensajes_de(emisor,contacto)    
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de la Mensajeria... ")
                os.system('cls')
            elif opcion == "4":
                os.system('cls')
                try:
                    self.ver_bandeja_de_entrada()
                    indice = input("Ingrese el número del mensaje a eliminar: ")
                    while not MensajesApp.validar_indice(indice, len(self.mensajes)):
                        indice = input("Entrada incorrecta. Ingrese el número del mensaje a eliminar: ")
                    self.eliminar_mensaje(int(indice))
                except ValueError as e:
                    print(e)
                except IndexError:
                    print("Error al eliminar mensaje intente nuevamente")
                input("Presione cualquier tecla para volver al menu de la Mensajeria...")
                os.system('cls')
            elif opcion == "5":
                os.system('cls')
                print("Saliendo de la aplicacion de Mensajes...")
                salir = True
                input("Presione cualquier tecla para volver al menu del celular...")
                os.system('cls')
            else:
                os.system('cls')
                print("Opción inválida, intente nuevamente")
                input("Presione cualquier tecla para volver al menu de Mensajes...")
                os.system('cls')
    
