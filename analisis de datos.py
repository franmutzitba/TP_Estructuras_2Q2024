"""
    This script contains various functions to generate different types of plots for analyzing application data from a CSV file. The plots include bar charts, pie charts, scatter plots, histograms, line charts, stacked bar charts, box plots, area charts, violin plots, and bubble charts. Each function reads data from a CSV file using the ManejadorCSV class and generates a specific type of plot using matplotlib.
Functions:
- grafico_barras_categorias(nombre_archivo): Generates a bar chart of the most common application categories.
- grafico_pastel_tipos(nombre_archivo): Generates a pie chart of the distribution of application types (Free vs. Paid).
- grafico_dispersion_calificaciones_resenas(nombre_archivo): Generates a scatter plot of the relationship between ratings and the number of reviews.
- histograma_calificaciones(nombre_archivo): Generates a histogram of application ratings.
- grafico_dispersion_installs_calificaciones(nombre_archivo): Generates a scatter plot of the relationship between the number of installations and ratings.
- grafico_lineas_tamano_promedio_categoria(nombre_archivo): Generates a line chart of the average size of applications by category.
- grafico_barras_apiladas_categoria_tipo(nombre_archivo): Generates a stacked bar chart of the distribution of applications by category and type (Free vs. Paid).
- grafico_boxplot_calificaciones_categoria(nombre_archivo): Generates a box plot of ratings by category.
- grafico_area_evolucion_aplicaciones(nombre_archivo): Generates an area chart of the evolution of the number of applications by year.
- grafico_violin_calificaciones_tipo(nombre_archivo): Generates a violin plot of ratings by application type (Free vs. Paid).
- grafico_burbujas_calificaciones_resenas_tamano(nombre_archivo): Generates a bubble chart of the relationship between ratings, the number of reviews, and the size of the application.
Usage:
- Ensure the CSV file is available and the ManejadorCSV class is implemented.
- Call the desired function with the path to the CSV file to generate the corresponding plot.
    """
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from manejadorCSV import ManejadorCSV

def grafico_barras_categorias(nombre_archivo):
    """
    Genera un gráfico de barras de las categorías de aplicaciones más comunes.
    """
    manejador = ManejadorCSV(nombre_archivo)
    data = manejador.leer_archivo()
    categorias = defaultdict(int)
    for row in data:
        categorias[row[1]] += 1
    categorias = dict(sorted(categorias.items(), key=lambda item: item[1], reverse=True))
    
    plt.figure(figsize=(10, 6))
    plt.bar(categorias.keys(), categorias.values(), color='skyblue')
    plt.title('Categorías de Aplicaciones Más Comunes')
    plt.xlabel('Categoría')
    plt.ylabel('Número de Aplicaciones')
    plt.xticks(rotation=90)
    plt.show()

def grafico_pastel_tipos(nombre_archivo):
    """
    Genera un gráfico de pastel de la distribución de tipos de aplicaciones (Gratis vs. Pagadas).
    """
    manejador = ManejadorCSV(nombre_archivo)
    data = manejador.leer_archivo()
    tipos = defaultdict(int)
    for row in data:
        tipos[row[6]] += 1
    
    plt.figure(figsize=(8, 8))
    plt.pie(tipos.values(), labels=tipos.keys(), autopct='%1.1f%%', startangle=140, colors=['lightgreen', 'lightcoral'])
    plt.title('Distribución de Tipos de Aplicaciones (Gratis vs. Pagadas)')
    plt.show()

def grafico_dispersion_calificaciones_resenas(nombre_archivo):
    """
    Genera un gráfico de dispersión de la relación entre calificaciones y número de reseñas.
    """
    manejador = ManejadorCSV(nombre_archivo)
    data = manejador.leer_archivo()
    calificaciones = []
    resenas = []
    for row in data:
        if row[2] != 'NaN' and row[3].isdigit():
            calificaciones.append(float(row[2]))
            resenas.append(int(row[3]))
    
    plt.figure(figsize=(10, 6))
    plt.scatter(resenas, calificaciones, alpha=0.5, c='blue')
    plt.title('Relación entre Calificaciones y Número de Reseñas')
    plt.xlabel('Número de Reseñas')
    plt.ylabel('Calificación')
    plt.xscale('log')
    plt.show()

def histograma_calificaciones(nombre_archivo):
    """
    Genera un histograma de las calificaciones de las aplicaciones.
    """
    manejador = ManejadorCSV(nombre_archivo)
    data = manejador.leer_archivo(True)
    calificaciones = [float(row[2]) for row in data if row[2] != 'NaN']
    
    plt.figure(figsize=(10, 6))
    plt.hist(calificaciones, bins=np.arange(0, 5.5, 0.5), color='purple', edgecolor='black')
    plt.title('Distribución de Calificaciones de las Aplicaciones')
    plt.xlabel('Calificación')
    plt.ylabel('Frecuencia')
    plt.show()

def grafico_dispersion_installs_calificaciones(nombre_archivo):
    """
    Genera un gráfico de dispersión de la relación entre cantidad de instalaciones y calificaciones.
    """
    manejador = ManejadorCSV(nombre_archivo)
    data = manejador.leer_archivo()
    installs = []
    calificaciones = []
    for row in data:
        if row[2] != 'NaN' and row[5] != 'NaN':
            try:
                installs.append(int(row[5].replace(',', '').replace('+', '')))
                calificaciones.append(float(row[2]))
            except ValueError:
                continue
    
    plt.figure(figsize=(10, 6))
    plt.scatter(installs, calificaciones, alpha=0.5, c='green')
    plt.title('Relación entre Cantidad de Instalaciones y Calificaciones')
    plt.xlabel('Cantidad de Instalaciones')
    plt.ylabel('Calificación')
    plt.xscale('log')
    plt.show()

def grafico_lineas_tamano_promedio_categoria(nombre_archivo):
    """
    Genera un gráfico de líneas del tamaño promedio de las aplicaciones por categoría.
    """
    manejador = ManejadorCSV(nombre_archivo)
    data = manejador.leer_archivo()
    tamanos = defaultdict(list)
    for row in data:
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

def grafico_barras_apiladas_categoria_tipo(nombre_archivo):
    """
    Genera un gráfico de barras apiladas de la distribución de aplicaciones por categoría y tipo (Gratis vs. Pagadas).
    """
    manejador = ManejadorCSV(nombre_archivo)
    data = manejador.leer_archivo(True)
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

def grafico_boxplot_calificaciones_categoria(nombre_archivo):
    """
    Genera un gráfico de caja y bigotes (boxplot) de las calificaciones por categoría.
    """
    manejador = ManejadorCSV(nombre_archivo)
    data = manejador.leer_archivo(True)
    calificaciones = defaultdict(list)
    for row in data:
        if row[2] != 'NaN':
            calificaciones[row[1]].append(float(row[2]))
    
    categorias, valores = zip(*calificaciones.items())
    
    plt.figure(figsize=(10, 6))
    plt.boxplot(valores, labels=categorias, vert=False)
    plt.title('Distribución de Calificaciones por Categoría')
    plt.xlabel('Calificación')
    plt.ylabel('Categoría')
    plt.show()

def grafico_area_evolucion_aplicaciones(nombre_archivo):
    """
    Genera un gráfico de área de la evolución del número de aplicaciones por año.
    """
    manejador = ManejadorCSV(nombre_archivo)
    data = manejador.leer_archivo(True)
    aplicaciones_por_ano = defaultdict(int)
    for row in data:
        fecha = datetime.strptime(row[10], "%B %d, %Y")
        aplicaciones_por_ano[fecha.year] += 1
    
    anos, valores = zip(*sorted(aplicaciones_por_ano.items()))
    
    plt.figure(figsize=(10, 6))
    plt.fill_between(anos, valores, color='skyblue', alpha=0.5)
    plt.plot(anos, valores, color='Slateblue', alpha=0.6, linewidth=2)
    plt.title('Evolución del Número de Aplicaciones por Año')
    plt.xlabel('Año')
    plt.ylabel('Número de Aplicaciones')
    plt.show()

def grafico_violin_calificaciones_tipo(nombre_archivo):
    """
    Genera un gráfico de violín de las calificaciones por tipo de aplicación (Gratis vs. Pagadas).
    """
    manejador = ManejadorCSV(nombre_archivo)
    data = manejador.leer_archivo(True)
    calificaciones = defaultdict(list)
    for row in data:
        if row[2] != 'NaN':
            calificaciones[row[6]].append(float(row[2]))
    
    tipos, valores = zip(*calificaciones.items())
    
    plt.figure(figsize=(10, 6))
    plt.violinplot(valores, showmeans=True)
    plt.title('Distribución de Calificaciones por Tipo de Aplicación')
    plt.xlabel('Tipo de Aplicación')
    plt.ylabel('Calificación')
    plt.xticks([1, 2], tipos)
    plt.show()

def grafico_burbujas_calificaciones_resenas_tamano(nombre_archivo):
    """
    Genera un gráfico de burbujas de la relación entre calificaciones, número de reseñas y tamaño de la aplicación.
    """
    manejador = ManejadorCSV(nombre_archivo)
    data = manejador.leer_archivo()
    calificaciones = []
    resenas = []
    tamanos = []
    for row in data:
        if row[2] != 'NaN' and row[3].isdigit() and ('M' in row[4] or 'k' in row[4]):
            calificaciones.append(float(row[2]))
            resenas.append(int(row[3]))
            if 'M' in row[4]:
                tamanos.append(float(row[4].replace('M', '')))
            elif 'k' in row[4]:
                tamanos.append(float(row[4].replace('k', '')) / 1000)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(resenas, calificaciones, s=np.array(tamanos) * 10, alpha=0.5, c='purple')
    plt.title('Relación entre Calificaciones, Número de Reseñas y Tamaño de la Aplicación')
    plt.xlabel('Número de Reseñas')
    plt.ylabel('Calificación')
    plt.xscale('log')
    plt.show()

# Llamar a las funciones para generar los gráficos
file = 'Play Store Data.csv'
grafico_barras_categorias(file)
grafico_pastel_tipos(file)
grafico_dispersion_calificaciones_resenas(file)
histograma_calificaciones(file)
grafico_dispersion_installs_calificaciones(file)
grafico_lineas_tamano_promedio_categoria(file)
grafico_barras_apiladas_categoria_tipo(file)
grafico_boxplot_calificaciones_categoria(file)
grafico_area_evolucion_aplicaciones(file)
grafico_violin_calificaciones_tipo(file)
grafico_burbujas_calificaciones_resenas_tamano(file)
