"""
Archivo principal del proyecto, donde se prueban las clases y métodos implementados.
"""








#from Apps.mail import MailApp, CuentaMail
from manejadorCSV import *

if "__main__" == __name__:
    from celular import Celular
    manejador_celulares = ManejadorDispositivos("celulares.csv", Celular.central)
    manejador_sms = ManejadorSMS("archivo_sms.csv", Celular.central)
    manejador_llamadas = ManejadorLlamadas("archivo_llamadas.csv", Celular.central)
    manejador_cuentas_mail = ManejadorCuentasMail("cuentas_mail.csv")
    #manejador_mails = ManejadorMails("mails.csv", Celular.central)
    
    #Cargamos los datos de los archivos csv
    # manejador_celulares.cargar_dispositivos()
    # for celular in Celular.central.registro_dispositivos.values():
    #     print(celular)
    # input("")
    manejador_sms.cargar_mensajes()
    manejador_llamadas.cargar_llamadas()
    manejador_cuentas_mail.cargar_cuentas()
    
    #Instanciamos algunos celulares
    celular1 = Celular("iPhone de Franco", "iPhone 13", "123456789", "iOS", "4GB", "64GB")
    celular2 = Celular("Samsung de Juan", "Samsung Galaxy S21", "987654321", "Android", "6GB", "128GB")
    celular3 = Celular("Motorola de Pedro", "Motorola G9", "456789123", "Android", "4GB", "32GB")
    celular4 = Celular("Huawei de Ana", "Huawei P40", "654321987", "Android", "8GB", "256GB")
    
    #Encendemos el 1,2,3
    celular1.encender_dispositivo()
    celular2.encender_dispositivo()
    celular3.encender_dispositivo()
    
    #Agregamos algunos contactos
    celular1.lanzar_app("Contactos").agregar_contacto("987654321", "Juan")
    celular1.lanzar_app("Contactos").agregar_contacto("456789123", "Pedro")

    #Enviamos algunos mails
    # try:
    #     #celular3.lanzar_app("Telefono").iniciar_llamada("987654321", 5)
    #     #celular1.lanzar_app("Telefono").iniciar_llamada("987654321", 5)
    # except ValueError as e:
    #     print(e)
    #input(" ")
    #celular1.lanzar_app("Telefono").terminar_llamada_en_curso()
    #celular2.lanzar_app("Telefono").iniciar_llamada("123456789", 5)
    celular1.lanzar_app("Contactos").agregar_contacto("987654321", "Alec")
    celular1.lanzar_app("Configuracion").configurar_nombre("Lionelanderere")
    print(celular1.aplicaciones["Configuracion"].configuracion.nombre)
    #celular2.encencer_dispositivo()
    try:
        celular1.menu_navegacion()
    except ValueError as e:
        print(e)
    except:
        print("Error")
    print(celular1.lanzar_app("Configuracion").configuracion)

    #Guardamos los datos en los archivos csv
    manejador_celulares.exportar_dispositivos()
    manejador_sms.exportar_mensajes()
    manejador_llamadas.exportar_llamadas()
    manejador_cuentas_mail.exportar_cuentas()
    