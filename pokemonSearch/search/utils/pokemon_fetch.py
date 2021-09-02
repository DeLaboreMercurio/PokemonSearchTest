import os
import pathlib
import shutil
from io import FileIO
from urllib.request import ProxyDigestAuthHandler, urlretrieve

import django
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from tqdm import tqdm

from ..models import Pokemon

eng_to_spa_types = {
    "Grass": "Planta",
    "Poison": "Veneno",
    "Fire": "Fuego",
    "Water": "Agua",
    "Fairy": "Hada",
    "Dark": "Oscuro",
    "Fighting": "Lucha",
    "Electric": "Electrico",
    "Ghost": "Fantasma",
    "Ice": "Hielo",
    "Flying": "Volador",
    "Bug": "Insecto",
}


def translate_type_eng_to_spa(eng_type: str) -> str:
    """[Translates the pokemon type to its spanish equivalent. If its not present in the dictionary, it returns itself.]

    Args:
        eng_type (str): [Pokemon type in english.]

    Returns:
        str: [Pokemon type in spanish.]
    """
    if eng_type in eng_to_spa_types:
        return eng_to_spa_types[eng_type]

    else:
        return eng_type


def fetch_pokemon_count() -> int:
    """[Fetches the total pokemon count from External API.]

    Returns:
        [int]: [Total External API Pokemon count.]
    """

    url = settings.POKEMON_API_ROOT_URL + "pokemon/?limit=1"

    r = requests.get(url=url).json()

    return r["count"]


def database_up_to_date(api_count: int) -> bool:
    """[Compare database row count with API count to check whether DB needs updating.]

    Args:
        api_count (int): [Number of pokemons in external API]

    Returns:
        [bool]: [True or False bool]
    """

    database_count = len(Pokemon.objects.all())

    return database_count >= api_count


def update_database(api_count: int):
    """[Iterate over External API Pokemons and save necessary information in DB.]

    Args:
        api_count (int): [Limit number to fetch in GET request to external API.]
    """

    url = settings.POKEMON_API_ROOT_URL + "pokemon/?limit=" + str(api_count + 1)

    r = requests.get(url=url).json()

    for pokemon in tqdm(r["results"]):
        try:
            create_if_not_exist(pokemon)

        except requests.exceptions.MissingSchema:  # Broken connection when contacting server
            continue

    return True


def create_if_not_exist(pokemon_result: dict):
    """[Creates new Pokemon entry in DB.]

    Args:
        pokemon_result (dict): [Dictionary of pokemon information.]
    """

    obj, created = Pokemon.objects.get_or_create(
        name=pokemon_result["name"].title(),
        url=pokemon_result["url"],
    )

    if created:
        path = fetch_pokemon_image(obj.url, obj.name)

        data = ContentFile(path, name=obj.name + ".png")

        obj.image = data
        obj.save()


def fetch_pokemon_image(pokemon_url: str, name: str) -> django.core.files.base.ContentFile:
    """[Fetches the Pokemon Artwork image.]

    Args:
        pokemon_url (str): [URL of detailed pokemon information.]
        name (str): [Name of POkemon]

    Returns:
        django.core.files.base.ContentFile: [ContentFile object containing Image.]
    """

    r = requests.get(pokemon_url).json()

    image_url = r["sprites"]["other"]["official-artwork"]["front_default"]

    save_path = settings.POKEMON_IMAGES_PATH
    file_name = name + ".png"

    pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

    file_path = os.path.join(save_path, file_name)

    file = requests.get(image_url)  # , stream=True)

    return file.content


def gather_detailed_information(pokemon_url: str) -> dict:
    """[Gather detail information about pokemon and translates to Spanish]

    Args:
        pokemon_url (str): [URL of detailed Pokemon information.]

    Returns:
        dict: [Dictionary containing height, weight and types of the Pokemon.]
    """

    r = requests.get(pokemon_url).json()

    detailed_info = {
        "Altura": r["height"],
        "Peso": r["weight"],
        "Tipos": "".join(
            "%s, " % translate_type_eng_to_spa(element["type"]["name"].title())
            for element in r["types"]
        )[:-2],
    }

    return detailed_info
