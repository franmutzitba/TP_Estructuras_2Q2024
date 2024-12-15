"""
Archivo principal del proyecto, donde se prueban las clases y métodos implementados.
"""

#from Apps.mail import MailApp, CuentaMail
import os
from manejadorCSV import ManejadorDispositivos, ManejadorSMS, ManejadorLlamadas
from manejadorCSV import ManejadorCuentasMail, ManejadorContactos, ManejadorMails, ManejadorCentrales
from analisis_de_datos import AnalisisDatos

if "__main__" == __name__:
    from celular import Celular
    from central import Central

    manejador_celulares = ManejadorDispositivos("z_celulares.csv")
    manejador_sms = ManejadorSMS("z_archivo_sms.csv")
    manejador_llamadas = ManejadorLlamadas("z_archivo_llamadas.csv")
    manejador_contactos = ManejadorContactos("z_contactos.csv")
    manejador_cuentas_mail = ManejadorCuentasMail("z_cuentas_mail.csv")
    manejador_mails = ManejadorMails("z_mails.csv")
    manejador_centrales = ManejadorCentrales("z_centrales.csv")

    #Cargamos los datos de los archivos csv

    centrales = manejador_centrales.cargar_centrales()
    celulares = manejador_celulares.cargar_dispositivos()
    manejador_sms.cargar_mensajes()
    manejador_llamadas.cargar_llamadas()
    manejador_cuentas_mail.cargar_cuentas()
    manejador_mails.cargar_mails()
    manejador_contactos.cargar_contactos()
    # except ValueError as e :
    #     print("Peron")
    #     print(e)
    #     print(Central.centrales.values())
    #     input("Ingrese hola:")

    os.system("cls")
    salir = False
    while not salir:
        print("Bienvenido al menu de navegacion de celulares")
        print(" 1. Manejo de centrales")
        print(" 2. Manejar un celular existente")
        print(" 3. Agregar un nuevo celular")
        print(" 4. Menu de analisis de datos")
        print(" 5. Salir")
        opcion = input("Ingrese la opcion deseada: ")
        
        if opcion == "1":
            os.system("cls")
            try:
                centrales = Central.menu_navegacion()
            except ValueError as e:
                print(e)
            except Exception as e:
                print(f"Error al manejar las centrales: {e}")

            input("Presione para volver al menu de navegacion... ")
            os.system("cls")
    

        elif opcion == "2":
            os.system("cls")
            try:
                if not celulares:
                    raise ValueError("No hay celulares registrados")
                for celular in celulares:
                    print(f"{celulares.index(celular)+1}. {celular.aplicaciones['Configuracion'].configuracion.nombre}: {celular.aplicaciones['Configuracion'].configuracion.numero}")
                indice = input("Ingrese el indice del celular a navegar: ")
                while not indice.isdigit() or int(indice) > len(celulares) or int(indice) < 1:
                    indice = input("Ingrese el indice del celular a navegar: ")
                os.system("cls")
                celulares[int(indice)-1].menu_navegacion()
            except ValueError as e:
                print(e)
            except Exception as e:
                print(f"Error: {e}")

            input("Presione para volver al menu de navegacion... ")
            os.system("cls")

        elif opcion == "3":
            os.system("cls")
            try:
                nombre = input("Ingrese el nombre del celular: ")
                modelo = input("Ingrese el modelo del celular: ")
                numero = input("Ingrese el numero del celular: ")
                sistema_operativo = input("Ingrese el sistema operativo del celular: ")
                ram = input("Ingrese la cantidad de RAM del celular: ")
                almacenamiento = input("Ingrese la cantidad de almacenamiento del celular: ")
                celulares.append(Celular(nombre, modelo, numero, sistema_operativo, ram, almacenamiento))
                print("Celular agregado con exito!")
            except ValueError as e:
                print(e)
            except Exception as e:
                print(f"Error al agregar un nuevo: {e}")

            input("Presione para volver al menu de navegacion... ")
            os.system("cls")

        elif opcion == "4":
            os.system("cls")
            try:
                analisis_de_datos = AnalisisDatos('Play Store Data.csv')
                analisis_de_datos.menu_navegacion()
            except Exception as e:
                print(f"Error al analizar los datos: {e}")
            os.system("cls")

        elif opcion == "5":
            os.system("cls")
            try:
                salir = True
                manejador_celulares.exportar_dispositivos()
                manejador_sms.exportar_mensajes()
                manejador_llamadas.exportar_llamadas()
                manejador_cuentas_mail.exportar_cuentas()
                manejador_mails.exportar_mails()
                manejador_contactos.exportar_contactos()
                manejador_centrales.exportar_centrales()
                print("Saliendo del programa...")
                print("")
                print("Gracias por utilizar este programa!")
            except Exception as e:
                print(f"Error al cerrar el programa: {e}")
        else:
            os.system("cls")
            print("Opción no válida, intente nuevamente")
            input("Presione cualquier tecla para volver al menú del celular...")
            os.system('cls')
