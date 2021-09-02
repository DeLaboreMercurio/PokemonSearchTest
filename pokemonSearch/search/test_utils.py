from urllib import request

import requests
from django.conf import settings
from django.test import TestCase

from search.models import Pokemon
from search.utils.pokemon_fetch import *


class UtilsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Pokemon.objects.create(name="Pokemon 1", url="https://pokeapi.co/api/v2/pokemon/1")
        Pokemon.objects.create(name="Pokemon 2", url="https://pokeapi.co/api/v2/pokemon/2")
        Pokemon.objects.create(name="Pokemon 3", url="https://pokeapi.co/api/v2/pokemon/3")
        Pokemon.objects.create(name="Pokemon 4", url="https://pokeapi.co/api/v2/pokemon/4")
        Pokemon.objects.create(name="Pokemon 5", url="https://pokeapi.co/api/v2/pokemon/5")
        Pokemon.objects.create(name="Pokemon 6", url="https://pokeapi.co/api/v2/pokemon/6")
        Pokemon.objects.create(name="Pokemon 7", url="https://pokeapi.co/api/v2/pokemon/7")
        Pokemon.objects.create(name="Pokemon 8", url="https://pokeapi.co/api/v2/pokemon/8")

    def test_connection_with_external_api(self):
        external_api_base_url = settings.POKEMON_API_ROOT_URL + "pokemon/"
        r = requests.get(external_api_base_url)

        self.assertEqual(r.status_code, 200)

    def test_count_check_against_db_correct(self):
        up_to_date = database_up_to_date(8)
        self.assertEqual(up_to_date, True)

    def test_count_check_against_db_incorrect(self):
        up_to_date = database_up_to_date(100)
        self.assertEqual(up_to_date, False)

    def test_updating_db_with_6_extra_pokemon(self):
        complete = update_database(
            5
        )  # Even though we specify 5, in reality it fetches one more just in case, so we check against 14.
        self.assertTrue(complete)
        total_pokemon = len(Pokemon.objects.all())
        self.assertEqual(total_pokemon, 14)

    def test_eng_to_spa_type_supported_type(self):
        supported_eng_type = "Fairy"
        supported_spa_type = translate_type_eng_to_spa(supported_eng_type)
        self.assertEqual("Hada", supported_spa_type)

    def test_eng_to_spa_type_unsopported_type(self):
        unsupported_eng_type = "Random type"
        self.assertEqual(unsupported_eng_type, translate_type_eng_to_spa(unsupported_eng_type))
