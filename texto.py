import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://books.toscrape.com/"
response = requests.get(url)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, "html.parser")
libros = soup.find_all("article", class_="product_pod")

datos = []
for libro in libros:
    titulo = libro.h3.a["title"]
    precio_texto = libro.find("p", class_="price_color").text
    precio = float(precio_texto.replace("£", "").replace("Â", ""))
    disponibilidad = libro.find("p", class_="instock availability").text.strip()

    datos.append({
        "titulo": titulo,
        "precio_gbp": precio,
        "disponibilidad": disponibilidad
    })

df = pd.DataFrame(datos)
df.to_csv("catalogo_libros.csv", index=False)
print("Scraping exitoso y archivo catalogo_libros.csv creado.")
