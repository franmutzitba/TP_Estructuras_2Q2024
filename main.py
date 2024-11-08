"""
Archivo principal del proyecto, donde se prueban las clases y métodos implementados.
"""

#from Apps.mail import MailApp, CuentaMail
import os
from manejadorCSV import *
from analisis_de_datos import AnalisisDatos

if "__main__" == __name__:
    from celular import Celular
    manejador_celulares = ManejadorDispositivos("celulares.csv", Celular.central)
    manejador_sms = ManejadorSMS("archivo_sms.csv", Celular.central)
    manejador_llamadas = ManejadorLlamadas("archivo_llamadas.csv", Celular.central)
    manejador_cuentas_mail = ManejadorCuentasMail("cuentas_mail.csv")
    manejador_contactos = ManejadorContactos("contactos.csv", Celular.central)
    manejador_mails = ManejadorMails("mails.csv")

    #Cargamos los datos de los archivos csv

    celulares = manejador_celulares.cargar_dispositivos()
    manejador_sms.cargar_mensajes()
    manejador_llamadas.cargar_llamadas()
    manejador_cuentas_mail.cargar_cuentas()
    manejador_mails.cargar_mails()
    manejador_contactos.cargar_contactos()

    os.system("cls")
    salir = False
    while not salir:
        print("Bienvenido al menu de navegacion de celulares")
        print(" 1. Manejar un celular existente")
        print(" 2. Agregar un nuevo celular")
        print(" 3. Menu de analisis de datos")
        print(" 4. Salir")
        opcion = input("Ingrese la opcion deseada: ")
        if opcion == "1":
            os.system("cls")
            try:
                if not celulares:
                    raise ValueError("No hay celulares registrados")
                for celular in celulares:
                    print(f"{celulares.index(celular)+1}. {celular.aplicaciones['Configuracion'].configuracion.nombre}: {celular.aplicaciones['Configuracion'].configuracion.numero}")
                indice = input("Ingrese el indice del celular a navegar: ")
                while not indice.isdigit() or int(indice) > len(celulares):
                    indice = input("Ingrese el indice del celular a navegar: ")
                os.system("cls")
                celulares[int(indice)-1].menu_navegacion()
            except ValueError as e:
                print(e)
            except Exception as e:
                print(f"Error: {e}")

            input("Presione para volver al menu de navegacion... ")
            #print(celulares[int(indice)-1].central.)
            os.system("cls")

        elif opcion == "2":
            os.system("cls")
            try:
                nombre = input("Ingrese el nombre del celular: ")
                modelo = input("Ingrese el modelo del celular: ")
                numero = input("Ingrese el numero del celular: ")
                sistema_operativo = input("Ingrese el sistema operativo del celular: ")
                ram = input("Ingrese la cantidad de RAM del celular: ")
                almacenamiento = input("Ingrese la cantidad de almacenamiento del celular: ")
                celulares.append(Celular(nombre, modelo, numero, sistema_operativo, ram, almacenamiento))
                print("Celular agregado con exito!!")
            except ValueError as e:
                print(e)
            except Exception as e:
                print(f"Error: {e}")

            input("Presione para volver al menu de navegacion... ")
            os.system("cls")
        elif opcion == "3":
            os.system("cls")
            analisis_de_datos = AnalisisDatos('Play Store Data.csv')
            analisis_de_datos.menu_navegacion()
            os.system("cls")
        elif opcion == "4":
            os.system("cls")
            salir = True
            manejador_celulares.exportar_dispositivos()
            manejador_sms.exportar_mensajes()
            manejador_llamadas.exportar_llamadas()
            manejador_cuentas_mail.exportar_cuentas()
            manejador_mails.exportar_mails()
            manejador_contactos.exportar_contactos()
            print("Saliendo del programa...")
            print("")
            print("Gracias por utilizar este programa!")
        else:
            os.system("cls")
            print("Opción no válida, intente nuevamente")
            input("Presione cualquier tecla para volver al menú del celular...")
            os.system('cls')
