"""
Archivo principal del proyecto, donde se prueban las clases y métodos implementados.
"""

#from Apps.mail import MailApp, CuentaMail
from manejadorCSV import ManejadorCSV

if "__main__" == __name__:
    from celular import Celular
    exportadorCelulares = ManejadorCSV("celulares.csv")
    celular1 = Celular("iPhone de Franco", "iPhone 13", "123456789", "iOS", "4GB", "64GB")
    celular2 = Celular("Samsung de Juan", "Samsung Galaxy S21", "987654321", "Android", "6GB", "128GB")
    celular3 = Celular("Motorola de Pedro", "Motorola G9", "456789123", "Android", "4GB", "32GB")
    celular4 = Celular("Huawei de Ana", "Huawei P40", "654321987", "Android", "8GB", "256GB")
    celular1.encender_dispositivo()
    celular1.lanzar_app("Configuracion").configurar_contrasenia("1234")
    celular2.encender_dispositivo()
    # celular2.encencer_dispositivo()
    try:
        celular1.menu_navegacion()
    except ValueError as e:
        print(e)

    telefono1 = celular1.aplicaciones["Telefono"]
    telefono2 = celular2.aplicaciones["Telefono"]
    telefono1.iniciar_llamada("987654321", 5)
    #telefono1.mostrar_historial_llamadas()
    #telefono2.mostrar_historial_llamadas()
    input("")
    telefono2.terminar_llamada_en_curso()
    celular3.encender_dispositivo()
    telefono2.iniciar_llamada(456789123, 10)
    telefono2.mostrar_historial_llamadas()
