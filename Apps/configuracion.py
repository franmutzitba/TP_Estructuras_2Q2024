from Apps.aplicacion import Aplicacion
from enum import Enum
from funciones_utiles import tamanio_a_bytes
import os

class ModoRed(Enum):
    SIN_RED = 0
    SOLO_VOZ_Y_SMS = 1
    LTE = 2
    
class Configuracion:
    """Clase que contiene todos los atributos de la configuración del celular. Son modificables a través de la clase ConfigApp."""
    def __init__(self, nombre, almacenamiento, central, numero, aplicaciones_instaladas, modo_red = ModoRed.LTE, modo_avion=False, contrasenia = None):
        self.nombre = nombre
        self.almacenamiento_disponible = almacenamiento
        self.central = central
        self.numero = numero
        self.aplicaciones_instaladas = aplicaciones_instaladas 
        
        self.modo_avion = modo_avion
        self.modo_red = modo_red
        self.contrasenia = contrasenia
        
    def __str__(self):
        return f"Nombre: {self.nombre}, Almacenamiento disponible: {self.almacenamiento_disponible} MB, Número: {self.numero}, Modo avión: {self.modo_avion}, Modo red: {self.modo_red}"
        
class ConfigApp(Aplicacion):
    """Esta clase representa la aplicación de configuración de cada celular que permite gestionar diversas configuraciones del dispositivo.
    
    Atributos:
    ----------
    configuracion (Configuracion): 
        Objeto que contiene la configuración actual del dispositivo.
        
    Métodos:
    --------
    __init__(configuracion: Configuracion):
        Inicializa una instancia de ConfigApp con la configuración proporcionada.
    configurar_contrasenia(contrasenia_nueva, contrasenia_vieja=None):
        Configura una nueva contraseña si la contraseña vieja es correcta o si no hay contraseña establecida.
    configurar_nombre(nombre):
        Configura un nuevo nombre para el dispositivo si cumple con los requisitos.
    listar_aplicaciones():
        Lista todas las aplicaciones instaladas en el dispositivo.
    set_servicio(valor: bool):
        Activa o desactiva el servicio de red de voz y SMS.
    set_datos(valor: bool):
        Activa o desactiva los datos móviles(LTE).
    set_modo_avion(valor: bool):
        Activa o desactiva el modo avión.
    set_contrasenia(contrasenia):
        Establece una nueva contraseña para el dispositivo.
    set_almacenamiento_disponible(almacenamiento):
        Establece el almacenamiento disponible en el dispositivo.
    get_contrasenia():
        Retorna la contraseña actual del dispositivo.
    get_nombre():
        Retorna el nombre actual del dispositivo.
    get_numero():
        Retorna el número de teléfono del dispositivo.
    get_almacenamiento_disponible():
        Retorna el almacenamiento disponible en el dispositivo.
    validar_contrasenia(contrasenia: str):
        Valida si la contraseña del celular cumple con los requisitos de seguridad.
    validar_nombre(nombre: str):
        Valida si el nombre del celular cumple con los requisitos.
    __str__():
        Retorna una representación en cadena de la configuración actual del dispositivo.
    """
    
    def __init__(self, configuracion: Configuracion):
        super().__init__(nombre = "Configuración", tamanio = "100 MB", esencial = True)
        self.configuracion = configuracion
        
    def configurar_contrasenia(self, contrasenia_nueva, contrasenia_vieja = None):
        """Configura una nueva contraseña si la contraseña vieja es correcta o si no hay contraseña establecida.
         Este método permite configurar una nueva contraseña para el usuario. Si se proporciona una contraseña actual,
         se verifica que sea correcta antes de establecer la nueva contraseña. La nueva contraseña debe cumplir con ciertos requisitos de validación.
         
        Args:
            contrasenia_nueva (str): La nueva contraseña que se desea configurar.
            contrasenia_vieja (str, opcional): La contraseña actual del usuario. Si no se proporciona, se asume que no hay una contraseña previa configurada.

        Returns:
            None
            
        Raises:
            ValueError: Si la contraseña actual es incorrecta o si la nueva contraseña no cumple con los requisitos.
        """
        
        if contrasenia_vieja == self.configuracion.contrasenia or self.configuracion.contrasenia is None:
            if self.validar_contrasenia(contrasenia_nueva): 
                self.set_contrasenia(contrasenia_nueva)
            else: 
                raise ValueError("La nueva contraseña no cumple con los requisitos")
        else:
            raise ValueError("Contraseña actual incorrecta")
        
    def configurar_nombre(self, nombre):
        """Configura el nombre en la configuración si cumple con los requisitos.
        
        Args:
            nombre (str): El nombre a configurar.
        
        Returns:
            None
            
        Raises:
            ValueError: Si el nombre no cumple con los requisitos de validación.
        """
        
        if not(self.validar_nombre(nombre)):
            raise ValueError("El nombre ingresado no cumple con los requisitos")
        
        self.configuracion.nombre = nombre
        print("Nombre actualizado correctamente")
            
    def listar_aplicaciones(self):
        """Lista todas las aplicaciones instaladas en el dispositivo."""
        
        for app in self.configuracion.aplicaciones_instaladas.keys():
            print(app)
    
    ##setters
    #############################     
    def set_servicio(self,valor:bool):
        """Configura el estado del servicio de red del dispositivo.
        Este método ajusta el modo de red del dispositivo entre SOLO_VOZ_Y_SMS y SIN_RED
        basado en el valor proporcionado. Si el servicio ya está en el estado deseado,
        se lanzará una excepción.
        
        Args:
            valor (bool): True para encender el servicio, False para apagarlo.
            
        Returns: 
            None

        Raises:
            ValueError: Si se intenta encender el servicio cuando ya está encendido
                        o apagarlo cuando ya está apagado.
        """
        
        if self.configuracion.modo_red == ModoRed.SOLO_VOZ_Y_SMS and valor:
            raise ValueError("El servicio ya se encuentra encendido")
        if self.configuracion.modo_red == ModoRed.SIN_RED and not valor:
            raise ValueError("El servicio ya se encuentra apagado")
        
        self.configuracion.modo_red = ModoRed.SOLO_VOZ_Y_SMS if valor else ModoRed.SIN_RED
        if valor: #HAY Q VER ESTO
            self.configuracion.modo_avion = False
            try:
                self.configuracion.central.registrar_mensajes(self.configuracion.numero)  
            except ValueError as e:
                print(e)
        print(f"El servicio se ha {'encendido' if valor==True else 'apagado'}")
             
    def set_datos(self,valor:bool):
        """
        Configura el estado de los datos móviles según el valor proporcionado.
        
        Args:
            valor (bool): Si es True, se encienden los datos móviles. Si es False, se apagan los datos móviles.
            
        Returns:
            None
            
        Raises:
            ValueError: Si se intenta encender los datos móviles cuando ya están encendidos.
            ValueError: Si se intenta apagar los datos móviles cuando ya están apagados.
        """
        
        if self.configuracion.modo_red == ModoRed.LTE and valor:
            raise ValueError("Los datos ya se encuentran encendidos")
        if self.configuracion.modo_red != ModoRed.LTE and not valor:
            raise ValueError("Los datos ya se encuentran apagados")
        
        self.configuracion.modo_red = ModoRed.LTE if valor else ModoRed.SOLO_VOZ_Y_SMS
        print(f"Los datos se han {'encendido' if valor==True else 'apagado'}")
    
    def set_modo_avion(self, valor:bool):
        """Activa o desactiva el modo avión en la configuración.
        
        Args:
            valor (bool): True para activar el modo avión, False para desactivarlo.
        
        Returns: 
            None
            
        Raises:
            ValueError: Si el modo avión ya se encuentra en el estado deseado.
            
        Efectos:
            - Si se activa el modo avión, se establece el modo de red a SIN_RED.
            - Si se desactiva el modo avión, se establece el modo de red a SOLO_VOZ_Y_SMS.
            - Se actualiza el estado del modo avión en la configuración.
            - Se imprime un mensaje indicando el nuevo estado del modo avión.
        """
        
        if self.configuracion.modo_avion == valor:
            raise ValueError(f"El modo avion ya se encuentra {'encendido' if valor==True else 'apagado'}")

        if valor:
            self.configuracion.modo_red = ModoRed.SIN_RED
        else:
            self.configuracion.modo_red = ModoRed.SOLO_VOZ_Y_SMS
        self.configuracion.modo_avion = valor
        print(f"El modo avion se ha {'encendido' if valor==True else 'apagado'}")
            
    def set_contrasenia(self, contrasenia):
        self.configuracion.contrasenia = contrasenia
        print("Contraseña actualizada correctamente")
        
    def set_almacenamiento_disponible(self, almacenamiento):
        self.configuracion.almacenamiento_disponible = almacenamiento
    #############################
    
    ##getters  
    #############################
    def get_contrasenia(self):
        return self.configuracion.contrasenia
    
    def get_nombre(self):
        return self.configuracion.nombre
    
    def get_numero(self):
        return self.configuracion.numero
    
    def get_almacenamiento_disponible(self):
        return self.configuracion.almacenamiento_disponible
    
    def get_modo_red(self):
        return self.configuracion.modo_red
    #############################
        
    @staticmethod
    def validar_contrasenia(contrasenia:str): #la contraseña debe ser un número de 4 a 6 dígitos
        """Valida si la contraseña del celular cumple con los requisitos de seguridad."""
        return len(contrasenia) <= 4 and len(contrasenia) <= 6 and contrasenia.isnumeric()
    
    @staticmethod
    def validar_nombre(nombre:str): #el nombre debe contener al menos 6 caracteres y no puede contener caracteres especiales. Ademas debe comenzar con una letra
        """Valida si el nombre del celular cumple con los requisitos."""
        return len(nombre) >= 6 and nombre.isalnum() and nombre[0].isalpha()
    
    def menu_navegacion(self):
        """Muestra un menú de navegación para la aplicación de configuración."""
        os.system('cls')
        print("Bienvenido a la aplicación de Configuración")
        salir = False
        while not salir:
            print("Menú de Configuración:")
            print("1. Configurar nombre")
            print("2. Configurar contraseña")
            print("3. Listar aplicaciones descargadas")
            print("4. Activar/desactivar servicio de red")
            print("5. Activar/desactivar datos móviles")
            print("6. Activar/desactivar modo avión")
            print("7. Ver configuración actual del dispositivo")
            print("8. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                os.system('cls')
                print("Configuración de nombre")
                print("El nombre debe contener al menos 6 caracteres y no puede contener caracteres especiales. Ademas debe comenzar con una letra")
                nombre = input("Ingrese el nuevo nombre que desea ponerle al dispositivo: ")
                try:
                    self.configurar_nombre(nombre)
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Configuración...")
                os.system('cls')
            elif opcion == "2":
                os.system('cls')
                print("Configuración de contraseña")
                print("La contraseña debe ser un número de 4 a 6 dígitos")
                contrasenia = input("Ingrese la nueva contraseña: ")
                contrasenia_vieja = input("Ingrese la contraseña actual: ")
                try:
                    self.configurar_contrasenia(contrasenia, contrasenia_vieja)
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Configuración...")
                os.system('cls')
            elif opcion == "3":
                os.system('cls')
                try:
                    self.listar_aplicaciones()
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Configuración...")
                os.system('cls')
            elif opcion == "4":
                os.system('cls')
                valor = input("Desea encender el servicio? (s/n): ")
                while valor.lower() != "s" and valor.lower() != "n":
                    valor = input("Opción inválida, intente nuevamente: ")
                    
                try:    
                    self.set_servicio(valor.lower() == "s")
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Configuración...")
                os.system('cls')
            elif opcion == "5":
                os.system('cls')
                valor = input("Desea encender los datos móviles? (s/n): ")
                while valor.lower() != "s" and valor.lower() != "n":
                    valor = input("Opción inválida, intente nuevamente: ")
                try:
                    self.set_datos(valor.lower() == "s")
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Configuración...")
                os.system('cls')
            elif opcion == "6":
                os.system('cls')
                valor = input("Desea activar el modo avión? (s/n): ")
                while valor.lower() != "s" and valor.lower() != "n":
                    valor = input("Opción inválida, intente nuevamente: ")
                try:
                    self.set_modo_avion(valor.lower() == "s")
                except ValueError as e:
                    print(e)
                input("Presione cualquier tecla para volver al menu de Configuración...")
                os.system('cls')
            elif opcion == "7":
                os.system('cls')
                print(self)
                input("Presione cualquier tecla para volver al menu de Configuración...")
                os.system('cls')
            elif opcion == "8":
                os.system('cls')
                print("Saliendo de la aplicación de Configuración...")
                salir = True
                input("Presione cualquier tecla para volver al menu del celular...")
                os.system('cls')
            else:
                print("Opción inválida, intente nuevamente")
                input("Presione cualquier tecla para volver al menu de Configuración...")
                os.system('cls')

    def __str__(self):
        return f"Configuración: {self.configuracion}"
    