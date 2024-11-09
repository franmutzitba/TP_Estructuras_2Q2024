"""
Módulo para cargar datos al programa, los cuales serán 
luego utilizados para ejecutar el main
"""
import os
from datetime import datetime
from manejadorCSV import ManejadorDispositivos, ManejadorSMS, ManejadorLlamadas
from manejadorCSV import ManejadorCuentasMail, ManejadorContactos, ManejadorMails
from celular import Celular
from Apps.mail import CuentaMail
from comunicacion import Mail



###########################
####### Manejadores #######
###########################
manejador_celulares = ManejadorDispositivos("z_celulares.csv", Celular.central)
manejador_sms = ManejadorSMS("z_archivo_sms.csv", Celular.central)
manejador_llamadas = ManejadorLlamadas("z_archivo_llamadas.csv", Celular.central)
manejador_cuentas_mail = ManejadorCuentasMail("z_cuentas_mail.csv")
manejador_contactos = ManejadorContactos("z_contactos.csv", Celular.central)
manejador_mails = ManejadorMails("z_mails.csv")



###########################
# Instancia de celulares ##
###########################
os.system("cls")
input("Presione para instanciar 4 celulares:")
celular1 = Celular("iPhone de Franco", "iPhone 13", "46579361", "iOS", "4GB", "64GB")
celular2 = Celular("Samsung de Eze", "Samsung Galaxy S21", "48321234", "Android", "6GB", "128GB")
celular3 = Celular("Oneplus de Manuel", "Oneplus 9T", "22349876", "Android", "4GB", "32GB")
celular4 = Celular("Huawei de Alec", "Huawei P40", "45671230", "Android", "8GB", "256GB")

#Enciendo los 4 celulares
input("Presione para encender los celulares:")
celular1.encender_dispositivo()
celular2.encender_dispositivo()
celular3.encender_dispositivo()
celular4.encender_dispositivo()



###########################
# Instancia de contactos ##
###########################
input("Presione para agregar contactos a los celulares:")
#Celu 1 (Franco)
celular1.lanzar_app("Contactos").agregar_contacto("48321234", "Eze")
celular1.lanzar_app("Contactos").agregar_contacto("22349876", "Manuel")
celular1.lanzar_app("Contactos").agregar_contacto("45671230", "Alec")

#Celu 2 (Eze)
celular2.lanzar_app("Contactos").agregar_contacto("46579361", "Franco")
celular2.lanzar_app("Contactos").agregar_contacto("22349876", "Manuel")

#Celu 3 (Manuel)
celular3.lanzar_app("Contactos").agregar_contacto("46579361", "Franco")
celular3.lanzar_app("Contactos").agregar_contacto("48321234", "Eze")

#Celu 4 (Alec)
celular4.lanzar_app("Contactos").agregar_contacto("46579361", "Franco")



###########################
# Instancia de SMS #######
###########################
input("Presione para apagar el celular de Alec:")
if celular4.encendido:
    celular4.apagar_dispositivo()
input("Presione para enviar mensajes:")
mensajes_del_celular1 =[["22349876","Hola"],["22349876","Como andas?"],["48321234","Hola Eze"],
                        ["48321234","Como andas?"],["45671230","Hola Alec"],["45671230","Como andas?"],["12341890","Mensaje Error"]]

#Envio de mensajes
for mensaje in mensajes_del_celular1:
    try:
        celular1.lanzar_app("Mensajes").enviar_sms(mensaje[0],mensaje[1])
        print("")
    except ValueError as e:
        print(e)

# Recibir mensajes no sincronizados al momento de encender el dispostitivo
input("Presione para mostrar la bandeja de entrada de Alec antes de encender el dispositivo:")
print("")
os.system("cls")
try:
    celular4.aplicaciones["Mensajes"].ver_bandeja_de_entrada()
except ValueError as e:
    print(e)

input("Presione para encender el celu de Alec y recibir los mensajes no sincronizados:")
os.system("cls")
celular4.encender_dispositivo()
print("")
input("Presione para ver la bandeja de entrada de Alec con los mensajes recibidos despues de encenderse el celualr:")
os.system("cls")
celular4.lanzar_app("Mensajes").ver_bandeja_de_entrada()
print("")



###########################
# Instancia de llamadas ###
###########################
input("Presione para realizar llamadas:")
celular1.lanzar_app("Telefono").iniciar_llamada("48321234")
celular3.lanzar_app("Telefono").iniciar_llamada("48321234") #El 3 llama al 2 que está ocupado
celular1.lanzar_app("Telefono").terminar_llamada_en_curso()



###############################
# Instacia de cuentas de mail #
###############################
input("Presione para agregar cuentas de mail:")
CuentaMail("fmutz@itba.edu.ar", "Datos2024*")
CuentaMail("ahoffmann@itba.edu.ar", "Datos2024*")
CuentaMail("ellabra@gmail.com", "Datos2024*")

input("Presione para intentar crear una cuenta con un mail ya existente:")
try:
    CuentaMail("ahoffmann@itba.edu.ar", "Hola123!")
except ValueError as e:
    print(e)



###########################
# Instancia de mails #####
###########################
input("Presione para enviar mails:")
celular1.lanzar_app("Configuracion").set_datos(True)
celular1.lanzar_app("Mail").iniciar_sesion("fmutz@itba.edu.ar", "Datos2024*")
celular1.lanzar_app("Mail").enviar_mail(Mail("Cuerpo de prueba 1", "fmutz@itba.edu.ar", "ahoffmann@itba.edu.ar", "Prueba 1", datetime.strptime("2022-07-01 12:00:00.000001", '%Y-%m-%d %H:%M:%S.%f')))
celular1.lanzar_app("Mail").enviar_mail(Mail("Cuerpo de prueba 2", "fmutz@itba.edu.ar", "ahoffmann@itba.edu.ar", "Prueba 2",datetime.strptime("2022-12-01 12:00:00.000001", '%Y-%m-%d %H:%M:%S.%f')))
celular1.lanzar_app("Mail").enviar_mail(Mail("Cuerpo de prueba 3", "fmutz@itba.edu.ar", "ellabra@itba.edu.ar", "Prueba 3", datetime.strptime("2022-01-01 12:00:00.000001", '%Y-%m-%d %H:%M:%S.%f')))

celular1.lanzar_app("Mail").cerrar_sesion()

#Inicio sesion con la cuenta de Alec en el celular de franco
celular1.lanzar_app("Mail").iniciar_sesion("ahoffmann@itba.edu.ar", "Datos2024*")
celular1.lanzar_app("Mail").enviar_mail(Mail("Cuerpo de prueba 4", "ahoffmann@itba.edu.ar", "fmutz@itba.edu.ar", "Prueba 4", datetime.strptime("2023-06-01 12:00:00.000001", '%Y-%m-%d %H:%M:%S.%f')))
celular1.lanzar_app("Mail").enviar_mail(Mail("Cuerpo de prueba 5", "ahoffmann@itba.edu.ar", "fmutz@itba.edu.ar", "Prueba 5", datetime.strptime("2020-06-01 12:00:00.000001", '%Y-%m-%d %H:%M:%S.%f')))
celular1.lanzar_app("Mail").cerrar_sesion()



#############################
# Carga de datos a archivos #
#############################
input("Presione para cargar los datos a los archivos csv:")
#Cargamos los datos a los archivos csv
manejador_celulares.exportar_dispositivos()
manejador_contactos.exportar_contactos()
manejador_sms.exportar_mensajes()
manejador_llamadas.exportar_llamadas()
manejador_cuentas_mail.exportar_cuentas()
manejador_mails.exportar_mails()
