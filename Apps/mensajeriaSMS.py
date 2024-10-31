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
        self.contactos = contactos
        self.central = central
        self.mensajes = deque() 
    
    def crear_mensaje(self, receptor: str, mensaje: str):
        return Mensaje(self.numero_cel, receptor, mensaje,datetime.now())
    
    def enviar_sms(self, receptor, texto):
        try:
            if self.central.manejar_mensaje(self.numero_cel, receptor):
                mensaje = self.crear_mensaje(receptor, texto)
                self.central.registrar_mensaje_nuevo(mensaje)
                print(f"Mensaje enviado correctamente al numero {receptor}") 
        except ValueError as e: 
            print(e)

    def recibir_sms(self, mensaje: Mensaje):
        if not(mensaje.get_sincronizado()):
            mensaje.set_sincronizado()
            self.mensajes.appendleft(mensaje)
        else:
            print("El mensaje ya ha sido recibido")
    
    def numero_en_contactos(self, numero):
        return numero in self.contactos.get_contactos()
    
    def nombre_contacto(self, numero):
        return self.contactos.get_contactos()[numero]

    def ver_bandeja_de_entrada(self):
        bandeja_de_entrada = self.mensajes
        i=1
        if not(bandeja_de_entrada):
            raise ValueError(f"El numero -{self.numero_cel}- no tiene mensajes en la bandeja de entrada")
        print(f"Bandeja de Entrada del numero: {self.numero_cel}")
        # ??? Hago un raise o un print??
        for mensaje in bandeja_de_entrada:
            print(f"- {i} - ", end="")
            if self.numero_en_contactos(mensaje.get_emisor()) :
                # Invente roman invente
                # Polemico
                # aux = mensaje.get_emisor()
                # mensaje.emisor = self.nombre_contacto(aux)
                # print(mensaje)
                # mensaje.emisor = aux
                fecha_min = mensaje.fecha.strftime("%Y-%m-%d %H:%M")
                print(f"Emisor: {self.nombre_contacto(mensaje.get_emisor())}, Receptor: {mensaje.receptor}, Texto: {mensaje.mensaje}, Fecha: {fecha_min}")
            else:
                print(mensaje)
            i+=1
        
    def ver_bandeja_de_entrada_x_numero(self, numero, contacto):
        #Ya deberia de estar validado que este numero tenga mensajes
        mensajes = self.mensajes.copy()
        
        while mensajes:
            mensaje = mensajes.popleft()
            if mensaje.get_emisor() == numero:
                if contacto:
                    fecha_min = mensaje.fecha.strftime("%Y-%m-%d %H:%M")
                    print(f"Emisor: {contacto}, Receptor: {mensaje.receptor}, Texto: {mensaje.mensaje}, Fecha: {fecha_min}")
                else:
                    print(mensaje)   
    
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
    
    def __str__(self):
        return f"Aplicacion Mensajeria del numero: {self.numero_cel}"
    
    def menu_navegacion(self):
        salir = False
        while not salir:
            print(f"\nBienvenido a la aplicacion de Mensajes SMS del numero {self.numero_cel}")
            print("1. Enviar mensaje")
            print("2. Ver bandeja de entrada")
            print("3. Ver bandeja de entrada por numero/contacto")
            print("4. Salir")
            opcion = input("Ingrese el número de la opción deseada: ")
            if opcion == "1":
                os.system("cls")
                receptor = input("Ingrese el número de teléfono del receptor: ")
                texto = input("Ingrese el mensaje a enviar: ")
                self.enviar_sms(receptor, texto)
            elif opcion == "2":
                os.system("cls")
                try:
                    self.ver_bandeja_de_entrada()
                except ValueError as e:
                    print(e)
            elif opcion == "3":
                os.system('cls')
                try:
                    recientes = self.ver_chats_recientes()
                    indice = int(input("Ingrese el número del chat deseado: "))
                    #Verificar que sea posible
                    emisor = recientes[indice-1]
                    contacto = self.nombre_contacto(emisor) if self.numero_en_contactos(emisor) else None
                    self.ver_bandeja_de_entrada_x_numero(emisor,contacto)
                except ValueError as e:
                    print(e)        
            elif opcion == "4":
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
    
#creo q faltan validar muchas cosas