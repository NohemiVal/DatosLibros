
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Página objetivo
url = "https://webscraper.io/test-sites/e-commerce/allinone"

# Solicitud al servidor
response = requests.get(url)
response.encoding = "utf-8"

# Analizar HTML
texto = BeautifulSoup(response.text, "html.parser")

# Buscar productos
productos = texto.find_all("div", class_="thumbnail")

# Extraer información
datos = []

for producto in productos:
    nombre = producto.find("a", class_="title").get("title")
    precio = producto.find("span", itemprop="price").text.strip()
    descripcion = producto.find("p", class_="description").text.strip()
    reviews = producto.find("span", itemprop="reviewCount").text.strip()
    calificacion = producto.find("p", attrs={"data-rating": True}).get("data-rating")

    datos.append({
        "nombre": nombre,
        "precio": precio,
        "descripcion": descripcion,
        "reviews": reviews,
        "calificacion": calificacion
    })

# Crear DataFrame
df = pd.DataFrame(datos)

# Limpiar datos
df["precio"] = df["precio"].str.replace("$", "", regex=False).astype(float)
df["reviews"] = pd.to_numeric(df["reviews"])
df["calificacion"] = pd.to_numeric(df["calificacion"])

# Guardar CSV
df.to_csv("catalogo_productos.csv", index=False, encoding="utf-8-sig")

print("Scraping completado correctamente.")
