from configuracion import Configuracion

class Celular:
    id = 0
    def __init__(self, nombre, modelo, numero, sistema, memoria_ram, almacenamiento):
        self.id = Celular.agregar_id()
        self.nombre = nombre
        self.modelo = modelo
        self.numero = numero
        self.sistema_operativo = sistema
        self.memoria_ram = memoria_ram
        self.almacenamiento = almacenamiento
        self.encendido = False
        self.bloqueado = False #hay que configurar una contraseña en Configuracion
        self.servicio = False #se administran desde la Configuracion
        self.wifi = False #se administran desde la Configuracion
        self.contrasenia = None
        self.aplicaciones = [Configuracion()]
        self.configuracion=Configuracion(self)
        
    
    def encencer_dispositivo(self):
        if self.encendido:
            print(f" El dispositivo {self.nombre} ya se encuentra encendido ")
        else:
            self.encendido = True
            print(f"Se ha encencido el dispositivo - {self.nombre} -")
        
    def contrasenia(self,contrasenia_nueva):
        self.configuracion.metodo(valores)
        
    @classmethod
    def agregar_id(cls):
        cls.id += 1
        return cls.id
    
    def __str__(self) -> str:
        return f"ID: {self.id}\nNombre: {self.nombre}\nModelo: {self.modelo}\nSistema operativo: {self.sistema_operativo}\nMemoria RAM: {self.memoria_ram}\nAlmacenamiento: {self.almacenamiento}"

    def get_numero(self):
        return self.numero
    
    def get_servicio(self):
        return self.servicio
    
    def get_contrasenia(self):
        return self.contrasenia 
    
    def set_wifi(self,valor:bool):
        if self.wifi == valor:
            print(f"El wifi ya se encuentra {'encendido' if valor==True else 'apagado'}")
        else:
            self.wifi=valor
            print(f"El wifi se ha {'encendido' if valor==True else 'apagado'}")
            
    def set_servicio(self,valor:bool):
        if self.servicio == valor:
            print(f"El servicio ya se encuentra {'encendido' if valor==True else 'apagado'}")
        else:
            self.servicio=valor
            print(f"El servicio se ha {'encendido' if valor==True else 'apagado'}")
            
    def set_contrasenia(self,contrasenia:str):
        self.contrasenia=contrasenia
        print("Contraseña cambiada correctamente")
        
    @staticmethod
    def validar_contrasenia(contrasenia:str):
        if len(contrasenia) <= 4 and len(contrasenia) <= 6 and contrasenia.isnumeric():
            return True
        else:
            return False

    
    

if __name__== "__main__":
    calular1 = Celular('nombre', 'modelo',0, 'sistema', 'memoria', 'almacenamiento')
    calular2 = Celular('nombre', 'modelo',1, 'sistema', 'memoria', 'almacenamiento')
    