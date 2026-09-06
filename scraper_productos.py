import requests
from bs4 import BeautifulSoup
import pandas as pd

# Página principal del sitio
url = "https://webscraper.io/test-sites/e-commerce/allinone"

datos = []

# Recorrer las páginas del catálogo
for pagina in range(1, 21):

    # Construir la URL de cada página
    if pagina == 1:
        url_pagina = url
    else:
        url_pagina = f"{url}?page={pagina}"

    print("Procesando:", url_pagina)

    # Solicitud a la página
    response = requests.get(url_pagina)
    response.encoding = "utf-8"

    # Analizar HTML
    texto = BeautifulSoup(response.text, "html.parser")

    # Buscar productos
    productos = texto.find_all("div", class_="thumbnail")

    print("Productos encontrados:", len(productos))

    # Extraer información
    for producto in productos:

        nombre_tag = producto.find("a", class_="title")
        precio_tag = producto.find("span", itemprop="price")
        descripcion_tag = producto.find("p", class_="description")
        reviews_tag = producto.find("span", itemprop="reviewCount")
        rating_tag = producto.find("p", attrs={"data-rating": True})

        if nombre_tag and precio_tag and descripcion_tag and reviews_tag and rating_tag:

            nombre = nombre_tag.get("title")
            precio = precio_tag.text.strip()
            descripcion = descripcion_tag.text.strip()
            reviews = reviews_tag.text.strip()
            calificacion = rating_tag.get("data-rating")

            datos.append({
                "nombre": nombre,
                "precio": precio,
                "descripcion": descripcion,
                "reviews": reviews,
                "calificacion": calificacion
            })


# Crear DataFrame
df = pd.DataFrame(datos)

# Limpiar precio
df["precio"] = (
    df["precio"]
    .str.replace("$", "", regex=False)
    .astype(float)
)

# Convertir a números
df["reviews"] = pd.to_numeric(df["reviews"])
df["calificacion"] = pd.to_numeric(df["calificacion"])

# Eliminar duplicados
df = df.drop_duplicates()

# Guardar CSV
df.to_csv(
    "catalogo_productos.csv",
    index=False,
    encoding="utf-8-sig"
)

print()
print("===================================")
print("SCRAPING TERMINADO")
print("===================================")
print("Total de productos:", len(df))
print("Archivo creado: catalogo_productos.csv")
