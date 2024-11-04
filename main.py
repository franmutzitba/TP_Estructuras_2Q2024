"""
Archivo principal del proyecto, donde se prueban las clases y métodos implementados.
"""

#from Apps.mail import MailApp, CuentaMail
import os
from manejadorCSV import *

if "__main__" == __name__:
    from celular import Celular
    manejador_celulares = ManejadorDispositivos("celulares.csv", Celular.central)
    manejador_sms = ManejadorSMS("archivo_sms.csv", Celular.central)
    manejador_llamadas = ManejadorLlamadas("archivo_llamadas.csv", Celular.central)
    manejador_cuentas_mail = ManejadorCuentasMail("cuentas_mail.csv")
    manejador_contactos = ManejadorContactos("contactos.csv", Celular.central)
    #manejador_mails = ManejadorMails("mails.csv", Celular.central)

    #Cargamos los datos de los archivos csv
    celulares = manejador_celulares.cargar_dispositivos()
    os.system("cls")
    for celular in celulares:
        print(f"{celulares.index(celular)+1}. {celular.aplicaciones['Configuracion'].configuracion.nombre}: {celular.aplicaciones['Configuracion'].configuracion.numero}")
    indice = input("Ingrese el indice del celular a navegar: ")
    while not indice.isdigit() or int(indice) > len(celulares):
        indice = input("Ingrese el indice del celular a navegar: ")

    manejador_sms.cargar_mensajes()
    manejador_llamadas.cargar_llamadas()
    manejador_cuentas_mail.cargar_cuentas()
    manejador_contactos.cargar_contactos()

    #Instanciamos algunos celulares
    # celular1 = Celular("iPhone de Franco", "iPhone 13", "234567890", "iOS", "4GB", "64GB")
    # celular2 = Celular("Samsung de Juan", "Samsung Galaxy S21", "345678901", "Android", "6GB", "128GB")
    # celular3 = Celular("Motorola de Pedro", "Motorola G9", "000000000", "Android", "4GB", "32GB")
    # celular4 = Celular("Huawei de Ana", "Huawei P40", "012347618", "Android", "8GB", "256GB")

    #Encendemos el 1,2,3
    # celular1.encender_dispositivo()
    # celular2.encender_dispositivo()
    # celular3.encender_dispositivo()
    
    #Agregamos algunos contactos
    # celular1.lanzar_app("Contactos").agregar_contacto("987654321", "Juan")
    # celular1.lanzar_app("Contactos").agregar_contacto("456789123", "Pedro")

    #Enviamos algunos mails
    # try:
    #     #celular3.lanzar_app("Telefono").iniciar_llamada("987654321", 5)
    #     #celular1.lanzar_app("Telefono").iniciar_llamada("987654321", 5)
    # except ValueError as e:
    #     print(e)
    #input(" ")
    #celular1.lanzar_app("Telefono").terminar_llamada_en_curso()
    #celular2.lanzar_app("Telefono").iniciar_llamada("123456789", 5)
    # celular1.lanzar_app("Contactos").agregar_contacto("987654321", "Alec")
    # celular1.lanzar_app("Contactos").agregar_contacto("456789123", "Pedro")
    # celular2.lanzar_app("Contactos").agregar_contacto("654321987", "Ana")
    # celular1.lanzar_app("Configuracion").configurar_nombre("Lionelanderere")
    # print(celular1.aplicaciones["Configuracion"].configuracion.nombre)
    #celular2.encencer_dispositivo()
    os.system("cls")
    
    try:
        celulares[int(indice)-1].menu_navegacion()
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")

    #Guardamos los datos en los archivos csv
    manejador_celulares.exportar_dispositivos()
    manejador_sms.exportar_mensajes()
    manejador_llamadas.exportar_llamadas()
    manejador_cuentas_mail.exportar_cuentas()
    manejador_contactos.exportar_contactos()
