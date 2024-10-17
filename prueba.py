class Celular:
    def __init__(self,contrasenia,sistema):
        self.contrasenia=contrasenia
        self.sistema=sistema
        self.configuracion=Configuracion([contrasenia,sistema])
        
class Configuracion:
    def __init__(self,datos):
        self.datos=datos
        
    def actualizar_contrasenia(self,contra_nueva):
        self.datos[0]=contra_nueva
        
if __name__ =="main.py":
    celular=Celular("hola",10)
    print(celular.contrasenia)
    celular.configuracion.actualizar_contrasenia("chau")
    print(celular.contrasenia)
    
    
