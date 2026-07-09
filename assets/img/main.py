import requests

# Obtener la última versión del juego
version = requests.get(
    "https://ddragon.leagueoflegends.com/api/versions.json"
).json()[0]

# Datos de campeones en español
url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/es_MX/championFull.json"

champions = requests.get(url).json()["data"]

# Traducción de roles e íconos
roles = {
    "Assassin": ("Asesino", "assasin.png"),
    "Fighter": ("Luchador", "fighter.png"),
    "Mage": ("Mago", "mage.png"),
    "Marksman": ("Tirador", "marksman.png"),
    "Support": ("Soporte", "support.png"),
    "Tank": ("Tanque", "tank.png")
}

MAX_CHARS = 100

html = ""

for champ in champions.values():

    name = champ["name"]
    title = champ["title"]

    # Descripción
    description = champ["blurb"].replace("\n", " ").strip()

    if len(description) > MAX_CHARS:
        description = description[:MAX_CHARS]

        # No cortar palabras
        last_space = description.rfind(" ")
        if last_space != -1:
            description = description[:last_space]

        description += "..."

    # Rol
    role_en = champ["tags"][0]
    role, role_icon = roles.get(role_en, ("Desconocido", "fighter.png"))

    # Dificultad
    difficulty_value = champ["info"]["difficulty"]

    if difficulty_value <= 3:
        difficulty = "Fácil"
        difficulty_icon = "easy.png"
    elif difficulty_value <= 7:
        difficulty = "Media"
        difficulty_icon = "medium.png"
    else:
        difficulty = "Difícil"
        difficulty_icon = "hard.png"

    html += f"""
<article class="show-champs-box" data-aos="flip-left" data-aos-delay="200">

    <div class="show-champs-image">
        <img src="../assets/img/champions/{name}.jpg" alt="{name}">
    </div>

    <div class="show-champs-description">

        <h2>{name}</h2>

        <h3>{title}</h3>

        <p>{description}</p>

        <p>Rol: {role} | Dificultad: {difficulty}</p>

        <div class="show-champs-graphs">

            <div>
                <img src="../assets/img/icons/{role_icon}" alt="{role}">
            </div>

            <div>
                <img src="../assets/img/icons/{difficulty_icon}" alt="{difficulty}">
            </div>

        </div>

    </div>

</article>

"""

with open("cards.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Se generaron {len(champions)} tarjetas correctamente.")