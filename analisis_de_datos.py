"""
En este módulo se realizan los análisis de datos de las aplicaciones de la Play Store 
y se generan diferentes tipos de gráficos.
"""

import os
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from manejadorCSV import ManejadorCSV

class AnalisisDatos:

    """
    Clase para realizar análisis de datos de aplicaciones y generar diferentes tipos de gráficos.

    Atributos:
    ----------
    manejador : ManejadorCSV
        Instancia de la clase ManejadorCSV para manejar la lectura del archivo CSV.
    data : list
        Lista de datos leídos del archivo CSV.
    """
    def __init__(self, nombre_archivo):
        self.manejador = ManejadorCSV(nombre_archivo)
        self.data = self.manejador.leer_archivo()

    def menu_navegacion(self):
        """Menu Navegacion"""
        salir = False
        while not salir:
            os.system('cls')
            print("1. Gráfico de Barras de Descargas por Categoría")
            print("2. Apps Gratis vs Pagas")
            print("3. Histograma de Calificaciones")
            print("4. Gráfico de Líneas de Tamaño Promedio por Categoría")
            print("5. Gráfico de Barras Apiladas de Categorías y Tipos")
            print("6. Gráfico de Barars de Calificaciones promedio por Categoría")
            print("7. Top 5 Apps Gratis con más Descargas")
            print("0. Salir")
            #Hacer uno que sea top 10 apps gratis con más descargas
            opcion = input("Seleccione una opción: ")
            os.system('cls')
            if opcion == '1':
                self.grafico_barras_categorias()
            elif opcion == '2':
                self.grafico_pastel_tipos()
            elif opcion == '3':
                self.histograma_calificaciones()
            elif opcion == '4':
                self.grafico_lineas_tamano_promedio_categoria()
            elif opcion == '5':
                self.grafico_barras_apiladas_categoria_tipo()
            elif opcion == '6':
                self.calificacion_promedio_top_categorias()
            elif opcion == '7':
                self.top_5_apps()
            elif opcion == '0':
                print("Saliendo de analisis de datos...")
                input("Presione para volver al menu de navegacion... ")
                os.system('cls')
                salir = True
            else:
                print("Opción inválida. Inténtelo de nuevo.")
                opcion = input("Seleccione una opción correcta: ")
                os.system('cls')

    def grafico_barras_categorias(self):
        """
        Genera un gráfico de barras de las categorías de aplicaciones más comunes.
        """
        categorias = defaultdict(int)
        for row in self.data:
            categorias[row[1]] += 1
        categorias = dict(sorted(categorias.items(), key=lambda item: item[1], reverse=True)[:10]) #me quedo con las 10 categorias mas comunes

        plt.figure(figsize=(10, 6))
        plt.barh(categorias.keys(), categorias.values(), color='skyblue')
        plt.title('Categorías de Aplicaciones Más Comunes')
        plt.xlabel('Número de Descargas')
        plt.ylabel('Categoría')
        plt.show()

    def grafico_pastel_tipos(self):
        """
        Genera un gráfico de pastel de la distribución de tipos de aplicaciones (Gratis vs. Pagadas).
        """
        tipos = defaultdict(int)
        self.data.pop(0)
        for row in self.data:
            if row[6] != 'NaN':
                tipos[row[6]] += 1

        plt.figure(figsize=(8, 8))
        plt.pie(tipos.values(), labels=tipos.keys(), autopct='%1.1f%%', startangle=140, colors=['lightgreen', 'lightcoral'])
        plt.title('Distribución de Tipos de Aplicaciones (Gratis vs. Pagadas)')
        plt.show()

    def histograma_calificaciones(self):
        """
        Genera un histograma de las calificaciones de las aplicaciones.
        """
        data= self.data[1:]
        calificaciones = [float(row[2]) for row in data if row[2] != 'NaN']

        plt.figure(figsize=(10, 6))
        plt.hist(calificaciones, bins=np.arange(0, 5.5, 0.5), color='purple', edgecolor='black')
        plt.title('Distribución de Calificaciones de las Aplicaciones')
        plt.xlabel('Calificación')
        plt.ylabel('Cantidad')
        plt.show()

    def grafico_lineas_tamano_promedio_categoria(self):
        """
        Genera un gráfico de líneas del tamaño promedio de las aplicaciones por categoría.
        """
        tamanos = defaultdict(list)
        for row in self.data:
            if 'M' in row[4]:
                tamanos[row[1]].append(float(row[4].replace('M', '')))
            elif 'k' in row[4]:
                tamanos[row[1]].append(float(row[4].replace('k', '')) / 1000)

        tamanos_promedio = {categoria: np.mean(tamanos[categoria]) for categoria in tamanos}
        tamanos_promedio = dict(sorted(tamanos_promedio.items(), key=lambda item: item[1]))

        plt.figure(figsize=(10, 6))
        plt.plot(list(tamanos_promedio.keys()), list(tamanos_promedio.values()), marker='o', color='orange')
        plt.title('Tamaño Promedio de las Aplicaciones por Categoría')
        plt.xlabel('Categoría')
        plt.ylabel('Tamaño Promedio (MB)')
        plt.xticks(rotation=90)
        plt.show()

    def grafico_barras_apiladas_categoria_tipo(self):
        """
        Genera un gráfico de barras apiladas de la distribución de aplicaciones por categoría y tipo (Gratis vs. Pagadas).
        """
        data= self.data[1:]
        categorias = defaultdict(lambda: {'Free': 0, 'Paid': 1})
        for row in data:
            if len(row) > 6 and row[6] in ['Free', 'Paid']:
                categorias[row[1]][row[6]] += 1

        categorias_ordenadas = sorted(categorias.items(), key=lambda item: sum(item[1].values()), reverse=True)
        categorias, valores = zip(*categorias_ordenadas)
        free = [v['Free'] for v in valores]
        paid = [v['Paid'] for v in valores]

        plt.figure(figsize=(10, 6))
        plt.bar(categorias, free, label='Free', color='lightgreen')
        plt.bar(categorias, paid, bottom=free, label='Paid', color='lightcoral')
        plt.title('Distribución de Aplicaciones por Categoría y Tipo')
        plt.xlabel('Categoría')
        plt.ylabel('Número de Aplicaciones')
        plt.xticks(rotation=90)
        plt.legend()
        plt.show()

    def top_5_apps(self):
        """
        Genera un gráfico de barras con las 5 aplicaciones más descargadas.
        """
        # Top 5 aplicaciones gratis con más descargas
        apps_gratis = [app for app in self.data if app[6] == 'Free']
        apps_gratis_sorted = sorted(apps_gratis, key=lambda x: int(x[5].replace(',', '').replace('+', '')), reverse=True)[:5]

        top_5_apps_gratis_nombres = [app[0] for app in apps_gratis_sorted]
        top_5_apps_gratis_installs = [int(app[5].replace(',', '').replace('+', '')) / 1000000 for app in apps_gratis_sorted]

        plt.figure(figsize=(14, 6))
        plt.barh(top_5_apps_gratis_nombres, top_5_apps_gratis_installs, color='lightgreen')
        plt.title('Top 5 Apps Gratis con más descargas')
        plt.xlabel('Número de Descargas (en millones)')
        plt.ylabel('App')
        plt.gca().invert_yaxis()  # Invertir el eje y para que el top esté arriba
        plt.grid(True)
        plt.show()

    def calificacion_promedio_top_categorias(self):
        """
        Genera un gráfico de barras con la calificación promedio de las aplicaciones según las 10 categorías con más descargas.
        """
        categorias_descargas = defaultdict(int)
        categorias_calificaciones = defaultdict(list)

        for row in self.data:
            if row[2] != 'NaN' and row[5] != 'NaN':
                try:
                    descargas = int(row[5].replace(',', '').replace('+', ''))
                    calificacion = float(row[2])
                    categoria = row[1]
                    categorias_descargas[categoria] += descargas
                    categorias_calificaciones[categoria].append(calificacion)
                except ValueError:
                    continue

        top_10_categorias = sorted(categorias_descargas.items(), key=lambda item: item[1], reverse=True)[:10]
        categorias = [item[0] for item in top_10_categorias]
        calificaciones_promedio = [np.mean(categorias_calificaciones[categoria]) for categoria in categorias]
        categorias, calificaciones_promedio = zip(*sorted(zip(categorias, calificaciones_promedio), key=lambda x: x[1], reverse=False))

        plt.figure(figsize=(14, 6))
        plt.bar_label(plt.barh(categorias, calificaciones_promedio, color='skyblue'), color='red')
        plt.title('Calificación Promedio de las Aplicaciones según las 10 Categorías con Más Descargas')
        plt.xlabel('Calificación Promedio')
        plt.ylabel('Categoría')
        plt.show()

# Llamar a las funciones para generar los gráficos
if __name__ == '__main__':
    analisis = AnalisisDatos('Play Store Data.csv')
    analisis.menu_navegacion()
