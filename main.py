from celular import Celular

if "__main__" == __name__:
    from Apps.mail import *
    from Apps.mail import CriterioLectura
    celular1 = Celular("iPhone de Franco", "iPhone 13", "123456789", "iOS", "4GB", "64GB")
    celular2 = Celular("Samsung de Juan", "Samsung Galaxy S21", "987654321", "Android", "6GB", "128GB")
    celular2.encencer_dispositivo()
    #celular2.desbloquear_dispositivo()
    celular1.encencer_dispositivo()
    #celular1.desbloquear_dispositivo()
    # celular1.lanzar_app("Configuracion").set_datos(True)
    # celular2.lanzar_app("Configuracion").set_datos(F)
    
    # salir = input("Presione 's' para salir: ")
    # while salir != "s":
    #     try:
    #         datos = input("Ingrese 1 para activar datos, 0 para desactivar: ")
    #         celular1.lanzar_app("Configuracion").set_datos(bool(int(datos)))
    #     except ValueError as e:
    #         print(e)
    
    print(celular1.get_nombre())
    celular1.lanzar_app("Configuracion").configurar_nombre("Franco")
    print(celular1.get_nombre())
    
    print(celular1.aplicaciones)
    print(celular1.get_almacenamiento_disponible())
    celular1.aplicaciones["AppStore"].descargar_app("WhatsApp")
    print(celular1.get_almacenamiento_disponible())
    print(celular1.aplicaciones)
    #celular1.aplicaciones["AppStore"].descargar_app("Zoom") #No hay espacio suficiente
    celular1.lanzar_app("AppStore").buscar_app("oK")
    #celular1.lanzar_app("AppStore").desinstalar_app("WhatsApp")
    celular1.lanzar_app("AppStore").listar_apps_instaladas()
    
    # print(Celular.central.registro_dispositivos["987654321"])
    # print(Celular.central.registro_dispositivos["123456789"])
    
    # celular1.lanzar_app("Mail").crear_cuenta("franco.mutz@gmail.com", "Franco123!")
    # celular2.lanzar_app("Mail").crear_cuenta("franco.mutz2@gmail.com", "Franco123!")
    # celular1.lanzar_app("Mail").iniciar_sesion("franco.mutz@gmail.com", "Franco123!")
    # celular2.lanzar_app("Mail").iniciar_sesion("franco.mutz2@gmail.com", "Franco123!")
    
    # celular1.lanzar_app("Mail").enviar_mail(Mail("Hola", "franco.mutz@gmail.com", "franco.mutz2@gmail.com", "Saludo"))
    # celular2.lanzar_app("Mail").ver_bandeja_entrada(CriterioLectura.NO_LEIDOS_PRIMEROS)
    
    # celular2.apagar_dispositivo()
    # celular1.lanzar_app("Mensajes").enviar_sms("987654321", "MEssi")
    # # print(celular1.central.registro_mensajes["987654321"].popleft())
    # celular2.encencer_dispositivo()
    

    
    # celular1.encencer_dispositivo()
    # celular1.central.mostrar_dispositivos()
    # celular1.aplicaciones["Configuracion"].set_servicio(True)
    # celular2.aplicaciones["Configuracion"].set_servicio(True)
    # celular1.central.mostrar_dispositivos()
    # celular1.apagar_dispositivo()
    # celular1.central.mostrar_dispositivos()

    # celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()
    # print("\n") 
    # print(celular1.aplicaciones["Configuracion"].get_almacenamiento_disponible())
    # celular1.aplicaciones["AppStore"].descargar_app("WhatsApp")
    # print(celular1.aplicaciones["Configuracion"].get_almacenamiento_disponible())
    # celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()
    # print(celular1.aplicaciones) #Las apps nuevas del appstore no van a tener ningun objeto asociado pq "no existen" como objetos
    # celular1.aplicaciones["AppStore"].descargar_app("Zoom") #No hay espacio suficiente
    # celular1.aplicaciones["AppStore"].mostrar_apps_disponibles()
    # celular1.aplicaciones["AppStore"].mostar_apps()