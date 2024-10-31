# from manejadorCSV import ManejadorCSV
# import csv
# from comunicacion import Llamada
# from datetime import datetime
# from central import Central

# class ManejadorLlamadas(ManejadorCSV):
#     def __init__(self,nombre_archivo):
#         super().__init__(nombre_archivo)
    
#     def grabarCSV(self, nombre):
#         with open(nombre, 'w', newline='') as file:
#             writer = csv.writer(file)
#             for llamada in self.__llamadas:
#                 writer.writerow(llamada.getRow())

#     def leerCSV(self, nombre):
#         with open(nombre, newline='') as csvfile:
#             reader = csv.reader(csvfile)
#             for row in reader:
#                 llamada = Llamada(row[0], row[1], row[2], row[3])
                
    def exportar_registro_llamadas(self):
        with open(self.nombre_archivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Receptor', 'Emisor', 'Duracion','Fecha Inicio'])

            for receptor, emisores in self.registro_llamadas.items():
                for emisor, llamadas in emisores.items():
                    for llamada in llamadas:
                        writer.writerow([receptor, emisor, llamada.get_duracion(),llamada.get_fecha_inicio()])
                        
    def cargar_llamadas_desde_csv(self, filename):
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    emisor = row['emisor']
                    receptor = row['receptor']
                    duracion = int(row['duracion'])
                    fecha_inicio = datetime.strptime(row['fecha_inicio'], '%Y-%m-%d %H:%M:%S')
                    self.registrar_llamada(emisor, receptor, duracion, fecha_inicio)