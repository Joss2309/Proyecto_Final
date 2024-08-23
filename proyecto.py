
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import Flask, jsonify, request



# 1. Web Scraping 
PAGINA_PRINCIPAL = "https://www.scrapethissite.com/pages/forms/"


navegador = webdriver.Chrome()

navegador.get(PAGINA_PRINCIPAL)  

navegador.implicitly_wait(10)

datos = []

equipos = navegador.find_elements(By.CLASS_NAME, 'team')

for equipo in equipos:
    nombre = equipo.find_element(By.CLASS_NAME, 'name')
    year = equipo.find_element(By.CLASS_NAME, 'year')
    wins = equipo.find_element(By.CLASS_NAME, 'wins')
    losses = equipo.find_element(By.CLASS_NAME, 'losses')
    datos.append({
        'Nombre': nombre.text,
        'Año': year.text,
        'Victorias': wins.text,
        'Derrotas': losses.text
    })

navegador.quit()

df = pd.DataFrame(datos)
print(df)


ruta = "C:/Users/Usuario/Downloads/PROYECTO_FINAL/proyecto_final_nayib.csv"
df.to_csv(ruta, index=False)


# 2. Desarrollo de una API con Flask (Un lugar para compartir los datos en internet)
# Crear un Flask 
app = Flask(__name__)

# Definir una ruta 
@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    filtro = request.args.get('filtro', default=None, type=str)
    
    if filtro:
        datos_filtrados = df[df['Nombre'].str.contains(filtro, case=False, na=False)]
    else:
        datos_filtrados = df
    
    return jsonify(datos_filtrados.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)


# 3. Análisis y Visualización de Datos 
import seaborn as sns
import matplotlib.pyplot as plt

import requests
response = requests.get("http://127.0.0.1:5000/api/datos?filtro=team_name")
data = response.json()

df_consumido = pd.DataFrame(data)

# Gráfico categórico - Conteo de victorias por equipo
plt.figure(figsize=(10, 6))
sns.countplot(data=df_consumido, x='Victorias')
plt.title('Conteo de Victorias por Equipo')
plt.savefig('grafico_categorico.png')
plt.show()

# Gráfico relacional - Relación entre victorias y derrotas
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_consumido, x='Victorias', y='Derrotas', hue='Nombre')
plt.title('Relación entre Victorias y Derrotas por Equipo')
plt.savefig('grafico_relacional.png')
plt.show()

# Gráfico de distribución - Distribución de los años de los equipos
plt.figure(figsize=(10, 6))
sns.histplot(data=df_consumido, x='Año', kde=True)
plt.title('Distribución de los Años de los Equipos')
plt.savefig('grafico_distribucion.png')
plt.show()