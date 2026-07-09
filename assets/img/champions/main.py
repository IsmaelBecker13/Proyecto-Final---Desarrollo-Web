import requests
import json
import os

# Última versión de League of Legends
version = requests.get(
    "https://ddragon.leagueoflegends.com/api/versions.json"
).json()[0]

print(f"Versión detectada: {version}")

# Obtener todos los campeones
url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
champions = requests.get(url).json()["data"]

# Carpeta de salida
output_folder = "champions"
os.makedirs(output_folder, exist_ok=True)

champions_info = []

print(f"Descargando {len(champions)} campeones...\n")

for champ_key, champ in champions.items():

    name = champ["name"]
    title = champ["title"]
    tags = champ["tags"]

    # Imagen vertical tipo carta
    image_url = (
        f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champ_key}_0.jpg"
    )

    response = requests.get(image_url)

    if response.status_code == 200:

        filename = os.path.join(output_folder, f"{name}.jpg")

        with open(filename, "wb") as f:
            f.write(response.content)

        champions_info.append({
            "id": champ_key,
            "name": name,
            "title": title,
            "roles": tags,
            "image": f"{name}.jpg"
        })

        print(f"✔ {name}")

    else:
        print(f"✘ No se pudo descargar {name}")

# Guardar JSON
with open("champions.json", "w", encoding="utf-8") as f:
    json.dump(champions_info, f, ensure_ascii=False, indent=4)

print("\nDescarga finalizada.")