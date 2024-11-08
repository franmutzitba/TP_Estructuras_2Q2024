import csv
import numpy as np
import matplotlib.pyplot as plt

# Leer el archivo CSV
filename = 'Play Store Data.csv'
apps = []

with open(filename, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Leer la cabecera
    for row in reader:
        apps.append(row)

# Convertir los datos relevantes a numpy arrays
ratings = []
reviews = []
installs = []
categories = []

for app in apps:
    try:
        rating = float(app[2])
        review = int(app[3])
        install = int(app[5].replace(',', '').replace('+', ''))
        category = app[1]
        ratings.append(rating)
        reviews.append(review)
        installs.append(install)
        categories.append(category)
    except ValueError:
        continue  # Ignorar filas con datos no válidos

ratings = np.array(ratings)
reviews = np.array(reviews)
installs = np.array(installs)

# Análisis básico
mean_rating = np.mean(ratings)
median_rating = np.median(ratings)
std_rating = np.std(ratings)

print(f'Mean Rating: {mean_rating}')
print(f'Median Rating: {median_rating}')
print(f'Standard Deviation of Rating: {std_rating}')

# Visualización
# Histograma de las calificaciones
plt.figure(figsize=(10, 6))
plt.hist(ratings, bins=np.arange(0, 5.5, 0.5), edgecolor='black')
plt.title('Distribution of App Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Gráfico de dispersión de calificaciones vs. número de reseñas
plt.figure(figsize=(10, 6))
plt.scatter(reviews, ratings, alpha=0.5)
plt.title('App Ratings vs. Number of Reviews')
plt.xlabel('Number of Reviews')
plt.ylabel('Rating')
plt.grid(True)
plt.show()

# Gráfico de dispersión de calificaciones vs. número de instalaciones
plt.figure(figsize=(10, 6))
plt.scatter(installs, ratings, alpha=0.5)
plt.title('App Ratings vs. Number of Installs')
plt.xlabel('Number of Installs')
plt.ylabel('Rating')
plt.grid(True)
plt.show()

# Gráfico de barras de la cantidad de aplicaciones por categoría
unique_categories, counts_categories = np.unique(categories, return_counts=True)
plt.figure(figsize=(12, 8))
plt.barh(unique_categories, counts_categories, color='skyblue')
plt.title('Number of Apps per Category')
plt.xlabel('Number of Apps')
plt.ylabel('Category')
plt.grid(True)
plt.show()

# Top 10 aplicaciones gratis con más descargas
free_apps = [app for app in apps if app[6] == 'Free']
free_apps_sorted = sorted(free_apps, key=lambda x: int(x[5].replace(',', '').replace('+', '')), reverse=True)[:10]

top_10_free_apps_names = [app[0] for app in free_apps_sorted]
top_10_free_apps_installs = [int(app[5].replace(',', '').replace('+', '')) for app in free_apps_sorted]

plt.figure(figsize=(12, 8))
plt.barh(top_10_free_apps_names, top_10_free_apps_installs, color='lightgreen')
plt.title('Top 10 Free Apps by Number of Installs')
plt.xlabel('Number of Installs')
plt.ylabel('App Name')
plt.gca().invert_yaxis()  # Invertir el eje y para que el top esté arriba
plt.grid(True)
plt.show()

# Evolución de la cantidad de nuevas apps por año
years = []

for app in apps:
    try:
        year = int(app[10].split('-')[-1])  # Asumiendo que la fecha está en el formato 'dd-mm-yyyy'
        years.append(year)
    except (ValueError, IndexError):
        continue  # Ignorar filas con datos no válidos

years = np.array(years)
unique_years, counts_years = np.unique(years, return_counts=True)

plt.figure(figsize=(12, 8))
plt.plot(unique_years, counts_years, marker='o', linestyle='-', color='b')
plt.title('Evolution of the Number of New Apps per Year')
plt.xlabel('Year')
plt.ylabel('Number of New Apps')
plt.grid(True)
plt.show()