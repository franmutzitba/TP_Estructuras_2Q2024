# Demostraciones de las distintas areas del proyecto

import os
from manejadorCSV import *
if "__main__" == __name__:
    from celular import Celular
    
    input("Presione para instanciar 4 celulares:")
    celular1 = Celular("iPhone de Franco", "iPhone 13", "46579361", "iOS", "4GB", "64GB")
    celular2 = Celular("Samsung de Eze", "Samsung Galaxy S21", "48321234", "Android", "6GB", "128GB")
    celular3 = Celular("Motorola de Manuel", "Motorola G9", "22349876", "Android", "4GB", "32GB")
    celular4 = Celular("Huawei de Alec", "Huawei P40", "45671230", "Android", "8GB", "256GB")
    lista_cel = [celular1,celular2,celular3,celular4]
    
    input("Presione para encender los celulares:")
    for cel in lista_cel:
        os.system("cls")
        cel.encender_dispositivo()
        input("Presione para encender el siguiente...")
    
    os.system("cls")
    input("Presione para apagr el celular 3 y 4:")
    celular3.apagar_dispositivo()
    celular4.apagar_dispositivo()
    input("Presione para continuar:")
    
    # Aca deberiamos de seguir probando cosas del celu o la configuracion
    # Prueba de las demas areas...
    # El area de contactos es clave para mostrar el resto, asi que hay que hacerla de las primeras
    #...
    try:
        celular4.aplicaciones["Contactos"].agregar_contacto("46579361", "Franquito")
    except ValueError as e:
        print(e)
    
    
    ################################
    #Pruba del area de la Mensajeria
    ################################
    def prueba_mensajeria(celular1,celular4):
        """
        Funcion que prueba el funcionamiento de la mensajeria, 
        en donde se envian mensajes desde el celular 1 a los demas celulares,
        y se recibe un mensaje no sincronizado en el celular 4,
        y se elimina el primer mensaje de la bandeja de entrada.
        
        Parameters:
        celular4 (Celular): El celular 4 de Alec.
        
        Returns:
        None
        """
        if celular4.encendido:
            celular4.apagar_dispositivo()
            
        input("Presione para enviar mensajes:")
        mensajes_del_celular1 =[["22349876","Hola"],["22349876","Como andas?"],["48321234","Hola Eze"],["48321234","Como andas?"],
                                ["45671230","Hola Alec"],["45671230","Como andas?"],["1234189","Mensaje Error"]]
        
        #Envio de mensajes
        for mensaje in mensajes_del_celular1:
            try:
                os.system("cls")
                celular1.lanzar_app("Mensajes").enviar_sms(mensaje[0],mensaje[1])
                print("")
                input("Presione para enviar el siguiente...")
            except ValueError as e:
                print(e)
                input("Presione para enviar el siguiente...")
        try:
            celular2.lanzar_app("Mensajes").enviar_sms("45671230","Como estas querido?")
            os.system("cls")
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
        
        # Eliminacion de mensajes
        input("Presione para eliminar el primer mensaje de la bandeja de entrada de Alec:")
        os.system("cls")
        # Aclaracion: Por como estaban pensados los menus, el valor del indice se valida en el menu
        try:
            celular4.lanzar_app("Mensajes").eliminar_mensaje(1)
        except ValueError as e:
            print(e)
        print("")
        input("Presione para visualizar nuevamente la bandeja de entrada de Alec con el primer mensaje eliminado:")
        os.system("cls")
        try:
            celular4.lanzar_app("Mensajes").ver_bandeja_de_entrada()
        except ValueError as e:
            print(e)
    
    os.system("cls")
    input("Presione para empezar las pruebas del funcionamiento de la Mensajeria:")
    os.system("cls")
    prueba_mensajeria(celular1,celular4)
   
    # Finalmente pasamos todos los datos a archivos csv:
    # manejador_celulares = ManejadorDispositivos("celulares_DEMO.csv", Celular.central)
    # manejador_sms = ManejadorSMS("archivo_sms_DEMO.csv", Celular.central)
    # manejador_llamadas = ManejadorLlamadas("archivo_llamadas_DEMO.csv", Celular.central)
    # manejador_cuentas_mail = ManejadorCuentasMail("cuentas_mail_DEMO.csv")
    # manejador_contactos = ManejadorContactos("contactos_DEMO.csv", Celular.central)
    # manejador_mails = ManejadorMails("mails_DEMO.csv")

    
    
    